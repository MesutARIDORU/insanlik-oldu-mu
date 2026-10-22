# -*- coding: utf-8 -*-
"""Notebook review · the interactive review page

Compares the original text with the rewrite and builds a single-file HTML page. In the page only
the changed words are marked. For each change the user keeps the new version, goes back to the
old one, picks another option or writes their own, adds notes and sends the decisions back to the
agent (or copies them into the chat).

A skill calls main() from its own scripts/review.py with its product (see product.py) and its
audit module. The audit module is the skill's own: it knows the skill's language. The page needs
four functions from it:
  read(source)          a file, - for standard input, or a text saved earlier
  measure(text)         a dict of measurements with at least "words"
  alarms(measurement)   rows of (label, value, status, note)
  guess_profile(text)   {"genre", "label", "sector", ...}, used when the agent's notes have no profile

Notes format (every field optional):
  {
    "title": "LinkedIn announcement",
    "mode": "Full rewrite",
    "profile": {"label": "Social media", "subtype": "company announcement", "sector": "software",
                "audience": "general readers", "approach": "short note on what was kept and what changed"},
    "changes": [
      {"before": "sentence in the original", "after": "sentence that replaced it",
       "reason": "short reason", "pattern": "R1",
       "alternatives": [{"kind": "Shorter", "text": "..."}, {"kind": "More formal", "text": "..."}]}
    ]
  }

Uses only the Python 3 standard library.
"""

import argparse
import base64
import datetime
import difflib
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile

from . import languages
from .product import HERE, TEMPLATE

TOKEN_RE = re.compile(r"\w+|[^\w\s]|\s+")
LANGUAGE = "en"  # set by build_page from the product


def tokens(s):
    return TOKEN_RE.findall(s)


def word_tokens(s):
    return [languages.lower(t, LANGUAGE) for t in tokens(s) if re.match(r"\w", t)]


def normalize(s):
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = "\n".join(line.rstrip() for line in s.split("\n"))
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip("\n")


def paragraphs(s):
    return [p for p in s.split("\n\n")]


def similarity(x, y):
    a, b = tokens(x), tokens(y)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def align(pa, pb, threshold=0.25):
    """Pairs units with the highest total similarity (order-preserving dynamic programming)."""
    n, m = len(pa), len(pb)
    sim = [[similarity(pa[i], pb[j]) for j in range(m)] for i in range(n)]
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            best = max(dp[i + 1][j], dp[i][j + 1])
            if sim[i][j] >= threshold:
                best = max(best, sim[i][j] + dp[i + 1][j + 1])
            dp[i][j] = best
    pairs, i, j = [], 0, 0
    while i < n and j < m:
        if sim[i][j] >= threshold and abs(dp[i][j] - (sim[i][j] + dp[i + 1][j + 1])) < 1e-9:
            pairs.append((i, j))
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1
        else:
            j += 1
    return pairs, sim


def word_diff(a, b, merge=3):
    """Token-level diff between two paragraphs; nearby changes are merged into one piece."""
    ta, tb = tokens(a), tokens(b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    raw = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        d, i = "".join(ta[i1:i2]), "".join(tb[j1:j2])
        if tag == "equal":
            raw.append(["eq", d, d])
        elif not d.strip() and not i.strip():
            raw.append(["eq", i, i])  # whitespace-only difference
        else:
            raw.append(["ch", d, i])
    out = []
    k = 0
    while k < len(raw):
        s = raw[k]
        if (s[0] == "eq" and out and out[-1][0] == "ch" and k + 1 < len(raw)
                and raw[k + 1][0] == "ch" and len(word_tokens(s[1])) < merge):
            out[-1][1] += s[1] + raw[k + 1][1]
            out[-1][2] += s[2] + raw[k + 1][2]
            k += 2
            continue
        if out and out[-1][0] == s[0]:
            out[-1][1] += s[1]
            out[-1][2] += s[2]
        else:
            out.append(list(s))
        k += 1
    return out


def trim_whitespace(seg):
    """Moves whitespace shared by both sides of a change piece into the neighbouring equal pieces."""
    out = []
    for s in seg:
        if s[0] != "ch":
            out.append(s)
            continue
        d, i = s[1], s[2]
        head = os.path.commonprefix([re.match(r"\s*", d).group(), re.match(r"\s*", i).group()])
        d, i = d[len(head):], i[len(head):]
        sd, si = re.search(r"\s*$", d).group(), re.search(r"\s*$", i).group()
        tail = os.path.commonprefix([sd[::-1], si[::-1]])[::-1]
        if tail:
            d, i = d[:-len(tail)], i[:-len(tail)]
        if head:
            out.append(["eq", head, head])
        if d or i:
            out.append(["ch", d, i] + list(s[3:]))
        if tail:
            out.append(["eq", tail, tail])
    return out


def sentences(p):
    """Splits a paragraph into sentences; joining the pieces gives back the paragraph."""
    parts, start = [], 0
    for m in re.finditer(r"[.!?…]+[\"”’»)]*\s+", p):
        following = p[m.end():m.end() + 1]
        if following and following.islower():
            continue  # "e.g. the", "vb. gibi"
        if m.group().startswith(".") and not m.group().startswith(".."):
            previous = re.findall(r"[^\s(]+$", p[start:m.start()])
            if previous and languages.is_abbreviation(previous[0], LANGUAGE):
                continue  # "Dr. Ayşe", "J. Smith"
        parts.append(p[start:m.end()])
        start = m.end()
    if start < len(p):
        parts.append(p[start:])
    return parts


def paragraph_diff(a, b):
    """Pairs sentences; every changed sentence becomes its own piece, similar sentences go down to word level."""
    sa, sb = sentences(a), sentences(b)
    pairs, sim = align(sa, sb, threshold=0.3)
    seg, pi, pj = [], 0, 0
    for (i, j) in pairs + [(len(sa), len(sb))]:
        dl, il = sa[pi:i], sb[pj:j]
        if dl or il:
            seg.append(["ch", "".join(dl), "".join(il)])
        if i < len(sa) and j < len(sb):
            if sa[i] == sb[j]:
                seg.append(["eq", sa[i], sa[i]])
            elif sim[i][j] < 0.5:
                seg.append(["ch", sa[i], sb[j]])
            else:
                seg.extend(word_diff(sa[i], sb[j]))
        pi, pj = i + 1, j + 1
    return seg


def diff_segments(before, after):
    pa, pb = paragraphs(before), paragraphs(after)
    pairs, sim = align(pa, pb)

    # ordered units: a matched paragraph pair or an unmatched block in between
    units = []
    pi, pj = 0, 0
    for (i, j) in pairs + [(len(pa), len(pb))]:
        dels, ins = pa[pi:i], pb[pj:j]
        if dels or ins:
            units.append(("block", dels, ins))
        if i < len(pa) and j < len(pb):
            units.append(("pair", i, j))
        pi, pj = i + 1, j + 1

    seg = []
    skip_separator = False
    for k, u in enumerate(units):
        has_prev, has_next = k > 0, k < len(units) - 1
        pure = u[0] == "block" and (not u[1] or not u[2])
        if pure:
            text = "\n\n".join(u[1] or u[2])
            if has_next:
                if has_prev and not skip_separator:
                    seg.append(["eq", "\n\n", "\n\n"])
                piece = text + "\n\n"
                skip_separator = True
            else:
                piece = ("\n\n" + text) if has_prev and not skip_separator else text
                skip_separator = False
            seg.append(["ch", piece if u[1] else "", piece if u[2] else ""])
            continue
        if has_prev and not skip_separator:
            seg.append(["eq", "\n\n", "\n\n"])
        skip_separator = False
        if u[0] == "block":
            seg.append(["ch", "\n\n".join(u[1]), "\n\n".join(u[2])])
        else:
            i, j = u[1], u[2]
            if sim[i][j] < 0.35:
                seg.append(["ch", pa[i], pb[j]])
            else:
                seg.extend(paragraph_diff(pa[i], pb[j]))

    return seg


def finalize(seg):
    """Turns raw pieces into what the page expects: trims whitespace, merges equal pieces, assigns ids."""
    seg = trim_whitespace(seg)
    merged = []
    for s in seg:
        if merged and merged[-1][0] == s[0] == "eq":
            merged[-1][1] += s[1]
            merged[-1][2] += s[2]
        else:
            merged.append(list(s))
    out, next_id = [], 0
    for s in merged:
        if s[0] == "eq":
            out.append({"t": "eq", "x": s[1]})
        else:
            next_id += 1
            out.append({"t": "ch", "id": next_id, "d": s[1], "i": s[2], "note": s[3] if len(s) > 3 else None})
    return out


def anchored_segments(before, after, notes):
    """Uses the before/after sentences in the agent's notes as anchors.

    In a heavy rewrite sentences stop resembling each other, and similarity matching puts the
    wrong sentences side by side. The notes already name every changed sentence: each note is
    searched for in order, and the ones found become their own pieces. Notes that are not found
    and the gaps between anchors fall back to the similarity diff.
    Returns None when fewer than half of the notes are found.
    """
    def shared_prefix(x, y, start_y):
        k = 0
        while k < len(x) and start_y + k < len(y) and x[k] == y[start_y + k]:
            k += 1
        return k

    anchors, a, b = [], 0, 0
    for k, n in enumerate(notes):
        nb, na = (n.get("before") or "").strip(), (n.get("after") or "").strip()
        if not nb and not na:
            continue
        pa = before.find(nb, a) if nb else -1
        pb = after.find(na, b) if na else -1
        # a deleted sentence has no place of its own in the new text (and an added one none in the old):
        # it sits where the unchanged text in front of it ends, not right after the previous anchor.
        # It also takes the space after it along (at a paragraph end, the space before it), so no double space is left behind
        if not na and pa >= 0:
            end = pa + len(nb)
            space = re.match(r"[ \t]+", before[end:])
            if space:
                end += len(space.group())
            else:
                space = re.search(r"[ \t]+$", before[a:pa])
                if space:
                    pa -= len(space.group())
            nb = before[pa:end]
            pb = b + shared_prefix(before[a:pa], after, b)
        elif not nb and pb >= 0:
            end = pb + len(na)
            space = re.match(r"[ \t]+", after[end:])
            if space:
                end += len(space.group())
            else:
                space = re.search(r"[ \t]+$", after[b:pb])
                if space:
                    pb -= len(space.group())
            na = after[pb:end]
            pa = a + shared_prefix(after[b:pb], before, a)
        if pa < 0 or pb < 0:
            continue
        anchors.append((pa, pa + len(nb), pb, pb + len(na), k))
        a, b = pa + len(nb), pb + len(na)
    found = len(anchors)
    if not found or found * 2 < sum(1 for n in notes if (n.get("before") or n.get("after"))):
        return None

    seg, a, b = [], 0, 0
    pending = None  # whitespace-only difference to prepend to the next anchor
    for (a1, a2, b1, b2, k) in anchors + [(len(before), len(before), len(after), len(after), None)]:
        ga, gb = before[a:a1], after[b:b1]
        if ga == gb:
            if ga:
                seg.append(["eq", ga, ga])
        elif not ga.strip() and not gb.strip():
            prev = seg[-1] if seg and seg[-1][0] == "ch" else None
            if prev is not None and (not prev[1] or not prev[2]):
                prev[1] += ga  # a deleted or inserted sentence takes its own whitespace along
                prev[2] += gb
            elif k is not None:
                pending = (ga, gb)
            elif prev is not None:
                prev[1] += ga
                prev[2] += gb
            else:
                seg.append(["ch", ga, gb])
        else:
            seg.extend(diff_segments(ga, gb) if "\n\n" in ga + gb else word_diff(ga, gb))
        if k is not None:
            d, i = before[a1:a2], after[b1:b2]
            if pending:
                d, i = pending[0] + d, pending[1] + i
                pending = None
            seg.append(["ch", d, i, k] if d != i else ["eq", d, d])
        a, b = a2, b2
    return seg


def overlap(x, y):
    a, b = set(word_tokens(x)), set(word_tokens(y))
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def attach_notes(segments, notes):
    for n in notes:
        n.setdefault("parts", [])
    for s in segments:
        if s["t"] != "ch":
            continue
        if s["note"] is not None:  # already attached by an anchor
            notes[s["note"]]["parts"].append(s["id"])
            continue
        best, best_score = None, 0.0
        for k, n in enumerate(notes):
            score = 0.0
            if s["d"] and n.get("before"):
                score = max(score, overlap(n["before"], s["d"]))
            if s["i"] and n.get("after"):
                score = max(score, overlap(n["after"], s["i"]))
            if score > best_score:
                best, best_score = k, score
        if best is not None and best_score >= 0.5:
            s["note"] = best
            notes[best]["parts"].append(s["id"])


def measurement_summary(audit, before, after):
    m1, m2 = audit.measure(before), audit.measure(after)
    old = {label: (value, status) for label, value, status, _ in audit.alarms(m1)}
    rows = []
    for label, value, status, note in audit.alarms(m2):
        o = old.get(label, ("", "info"))
        rows.append({"label": label, "before": o[0], "after": value, "status_before": o[1], "status_after": status, "note": note})
    return {
        "words": [m1["words"], m2["words"]],
        "alarms": [sum(1 for v in old.values() if v[1] == "alarm"),
                   sum(1 for r in rows if r["status_after"] == "alarm")],
        "rows": rows,
    }


def read_preferences(product):
    """The user's paper, font, theme and suggestion-engine choices (set in the page's settings, valid on every page)."""
    try:
        with open(os.path.join(product.config_dir, "preferences.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def page_profile(audit, meta, before):
    """The text profile shown on the page: the agent's decision, or the audit's guess when there is none."""
    profile = meta.get("profile")
    if isinstance(profile, dict) and profile.get("label"):
        return profile
    guess = audit.guess_profile(before)
    if not guess.get("genre"):
        return None
    return {"label": guess["label"], "sector": guess["sector"], "guessed": True}


def as_script_json(value):
    """JSON that is safe inside a <script> element and holds no /*placeholder*/ the bridge could fill in later."""
    return (json.dumps(value, ensure_ascii=False).replace("</", "<\\/").replace("/*", "/\\u002a")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


FONTS_DIR = os.path.join(HERE, "fonts")
# the handwriting face (Patrick Hand, SIL Open Font License, see fonts/OFL.txt), embedded so the page needs nothing from outside
FONTS = [
    ("patrick-hand-latin.woff2", "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"),
    ("patrick-hand-latin-ext.woff2", "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF"),
]


def font_faces():
    """@font-face rules with the font files inlined; a missing file is skipped and the page falls back to the system's handwriting face."""
    rules = []
    for name, ranges in FONTS:
        try:
            with open(os.path.join(FONTS_DIR, name), "rb") as f:
                data = base64.b64encode(f.read()).decode("ascii")
        except OSError:
            continue
        rules.append('@font-face { font-family: "Patrick Hand"; font-style: normal; font-weight: 400; font-display: swap; '
                     'src: url(data:font/woff2;base64,%s) format("woff2"); unicode-range: %s; }' % (data, ranges))
    return "\n".join(rules)


TEXTURES_DIR = os.path.join(HERE, "textures")
# paper grain, masking tape and a highlighter stroke, from the notebook's texture pack: (file, media type, CSS variable)
TEXTURES = [
    ("grain.png", "image/png", "--grain"),
    ("tape.webp", "image/webp", "--tape-image"),
    ("marker.webp", "image/webp", "--marker-image"),
    ("wood.jpg", "image/jpeg", "--wood-image"),
]


def texture_rules():
    """The textures as CSS variables with the files inlined; a missing file leaves the page's drawn fallback in place."""
    values = []
    for name, media, var in TEXTURES:
        try:
            with open(os.path.join(TEXTURES_DIR, name), "rb") as f:
                data = base64.b64encode(f.read()).decode("ascii")
        except OSError:
            continue
        values.append("%s: url(data:%s;base64,%s);" % (var, media, data))
        if var == "--marker-image":
            values.append("--divider-drawn: hidden;")  # the highlighter image replaces the drawn divider
        if var == "--wood-image":
            values.append("--wood-size: 1000px auto; --wood-seams: none;")  # a real desk has its own grain, no drawn planks
    return ":root { %s }" % " ".join(values) if values else ""


def render(product, data):
    """Fills the template: {{key}} with the product's texts, then the slots with the page data and the product's settings."""
    with open(TEMPLATE, encoding="utf-8") as f:
        page = f.read()

    def text(m):
        key = m.group(1)
        value = product.t(key)
        return value if key.endswith("_html") else html.escape(value)
    page = re.sub(r"\{\{([a-z_]+\.[a-z_]+)\}\}", text, page)
    settings = {"name": product.name, "slug": product.slug, "language": product.language, "patterns": product.patterns}
    slots = {
        "__LANG__": html.escape(product.language),
        "__PRODUCT_TITLE_HTML__": product.title_html,
        "__TITLE__": html.escape(data["title"] + " · " + product.name).replace("/*", "&#47;*"),
        "/*__STRINGS__*/null": as_script_json(product.page_strings()),
        "/*__PRODUCT__*/null": as_script_json(settings),
        "/*__DATA__*/null": as_script_json(data),
        "/*__FONTS__*/": font_faces(),
        "/*__TEXTURES__*/": texture_rules(),
    }
    # one pass, so nothing filled in (a title, the user's text) is read again as a slot
    return re.sub("|".join(re.escape(k) for k in slots), lambda m: slots[m.group()], page)


def build_page(product, audit, before, after, meta):
    global LANGUAGE
    LANGUAGE = product.language
    before, after = normalize(before), normalize(after)
    notes = list(meta.get("changes") or [])
    raw = anchored_segments(before, after, notes) if notes else None
    segments = finalize(raw if raw is not None else diff_segments(before, after))
    attach_notes(segments, notes)
    data = {
        "product": product.name,
        "title": meta.get("title") or product.t("page.untitled"),
        "mode": meta.get("mode") or "",
        "profile": page_profile(audit, meta, before),
        "date": datetime.datetime.now().strftime(product.date_format),
        "id": hashlib.sha1((before + "\u0000" + after).encode("utf-8")).hexdigest()[:16],
        "segments": segments,
        "notes": notes,
        "measurement": measurement_summary(audit, before, after),
        "preferences": read_preferences(product),
    }
    return render(product, data), data


def open_in_browser(path):
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", path])
        elif os.name == "nt":
            os.startfile(path)  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def main(product, audit, bridge=None, bridge_script=None, argv=None):
    """The command line of a skill's scripts/review.py. bridge is the skill's bridge module, for --live."""
    ap = argparse.ArgumentParser(description=f"{product.name} · builds the interactive review page")
    ap.add_argument("--before", required=True, help="original text: a file or a name saved with audit.py --save")
    ap.add_argument("--after", required=True, help="rewritten text: a file or a name saved with audit.py --save")
    ap.add_argument("--notes", help="change reasons (JSON file, or - for standard input)")
    ap.add_argument("--title", help="page title")
    ap.add_argument("--output", help="path of the HTML file (default: temp folder)")
    ap.add_argument("--open", action="store_true", help="open in the browser once built")
    ap.add_argument("--live", action="store_true", help="serve the page through the local bridge that talks to the agent")
    ap.add_argument("--agent", choices=["claude", "codex", "gemini"], help="agent the bridge should use (default: guessed)")
    args = ap.parse_args(argv)

    meta = {}
    if args.notes:
        meta = json.loads(audit.read(args.notes))
        if isinstance(meta, list):
            meta = {"changes": meta}
    if args.title:
        meta["title"] = args.title

    page, data = build_page(product, audit, audit.read(args.before), audit.read(args.after), meta)
    path = args.output
    if not path:
        folder = os.path.join(tempfile.gettempdir(), product.slug)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"review-{data['id'][:8]}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)

    n_changes = sum(1 for s in data["segments"] if s["t"] == "ch")
    n_noted = sum(1 for s in data["segments"] if s["t"] == "ch" and s["note"] is not None)
    print(product.t("cli.changed_parts", n=n_changes, noted=n_noted))
    if args.live and bridge is not None:
        try:
            info, address = bridge.start(path, agent=args.agent, open_page=args.open)
            print(product.t("cli.live", address=address))
            print(product.t("cli.session", id=info["id"], agent=info.get("agent") or product.t("cli.none"),
                            fork=product.t("cli.fork_possible") if info.get("session") else product.t("cli.fork_none")))
            print(product.t("cli.listen", script=bridge_script or "bridge.py"))
            return
        except Exception as e:
            print(product.t("cli.bridge_failed", error=e))
    print(product.t("cli.page", path=os.path.abspath(path)))
    if args.open:
        print(product.t("cli.opened") if open_in_browser(os.path.abspath(path)) else product.t("cli.open_failed"))
