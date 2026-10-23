#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İnsanlık öldü mü? · installer

Installs the skill into the agents on this computer and prepares the bridge between the
review page and the agent.

What it does:
  1. Checks the Python version and the skill files.
  2. Finds Claude Code, Codex, Gemini CLI and Antigravity and checks which bridge engines they support.
  3. Asks which of them to install into (the ones found are preselected). "Ortak klasör" installs
     through npx skills into ~/.agents/skills with the skills lock file, like other shared skills.
  4. Links the skill into Claude Code (~/.claude/skills), Codex (~/.codex/skills) and Antigravity
     (~/.gemini/config/skills, which npx skills leaves out), and writes the /insanlik-oldu-mu command for Gemini.
  5. Writes the bridge config to ~/.config/insanlik-oldu-mu/config.json.
  6. If asked (--permissions), lets Claude Code use the skill and run its scripts without asking every time.
     If asked (--codex-routing), adds a routing note to Codex's global instructions.
  7. Runs a short check.

Run from the copy that npx skills put into ~/.agents/skills, it installs nothing again: the skill is
already in place, so it only does the settings (Claude Code and Antigravity links, permissions, Codex routing,
Gemini command).

Usage:
  python3 ~/.agents/skills/insanlik-oldu-mu/scripts/install.py   # after npx skills add: settings only
  python3 scripts/install.py                  # asks which agents to install into, then before each step
  python3 scripts/install.py --targets claude,codex
  python3 scripts/install.py --yes            # installs without asking (leaves permissions alone)
  python3 scripts/install.py --yes --permissions
  python3 scripts/install.py --dry-run        # shows what it would do without changing anything
  python3 scripts/install.py --try-engine     # tries the suggestion engine with a real call (uses some quota)

Uses only the Python 3 standard library.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

NAME = "insanlik-oldu-mu"
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
HOME = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME, ".config", NAME)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SCRIPTS = ("audit.py", "review.py", "bridge.py")
OLD_SCRIPTS = ("denetim.py", "inceleme.py", "kopru.py", "preview_prompt.py")  # scripts that no longer exist, cleaned out of permissions

ARGS = None


def say(mark, text):
    print(f"{mark} {text}")


def ask(question, default=True):
    if ARGS.yes:
        return default
    if ARGS.dry_run or not sys.stdin.isatty():
        return False
    answer = input(f"? {question} [{'E/h' if default else 'e/H'}] ").strip().lower()
    if not answer:
        return default
    return answer in ("e", "evet", "y", "yes")


def run(cmd, timeout=20):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return 1, str(e)


# ---------------------------------------------------------------- 1. preflight

def preflight():
    if sys.version_info < (3, 8):
        sys.exit("Python 3.8 ya da daha yenisi gerekiyor.")
    say("✓", f"Python {sys.version.split()[0]}")
    missing = [p for p in ["SKILL.md", "notebook.json", "notebook/template.html", "notebook/page.py", "notebook/bridge.py"] + [f"scripts/{s}" for s in SCRIPTS]
               if not os.path.exists(os.path.join(SKILL_ROOT, p))]
    if missing:
        sys.exit("Skill dosyaları eksik: " + ", ".join(missing))
    say("✓", f"Skill dosyaları tamam ({SKILL_ROOT})")


# ---------------------------------------------------------------- 2. find agents

def find_agents():
    agents = {}
    path = shutil.which("claude")
    if path:
        _, version = run([path, "--version"])
        _, help_text = run([path, "--help"])
        agents["claude"] = {"path": path, "version": version.strip().splitlines()[0] if version.strip() else "?",
                            "fork": "--fork-session" in help_text, "stateless": "--print" in help_text}
    path = shutil.which("codex")
    if path:
        _, version = run([path, "--version"])
        code_fork, _ = run([path, "exec", "fork", "--help"])
        code_exec, _ = run([path, "exec", "--help"])
        agents["codex"] = {"path": path, "version": version.strip().splitlines()[0] if version.strip() else "?",
                           "fork": code_fork == 0, "stateless": code_exec == 0}
    path = shutil.which("gemini")
    if path:
        _, version = run([path, "--version"])
        _, help_text = run([path, "--help"])
        agents["gemini"] = {"path": path, "version": version.strip().splitlines()[0] if version.strip() else "?",
                            "fork": False, "stateless": "--prompt" in help_text}
    if not agents:
        say("!", "Claude Code, Codex ya da Gemini CLI bulunamadı. Skill yine kurulur, köprünün öneri motorları çalışmaz.")
    for name, a in agents.items():
        engines = ["bağlamsız" if a["stateless"] else None, "oturum çatalı" if a["fork"] else None]
        say("✓", f"{name} {a['version']} · köprü yolları: {', '.join(e for e in engines if e) or 'yok'}")
    return agents


# ---------------------------------------------------------------- 3. choose the agents

TARGETS = [("claude", "Claude Code"), ("codex", "Codex"), ("gemini", "Gemini CLI"), ("antigravity", "Antigravity"),
           ("shared", "Ortak klasör")]
SHARED_DIR = os.path.join(HOME, ".agents", "skills")
SKILL_LOCK = os.path.join(HOME, ".agents", ".skill-lock.json")
DEFAULT_SOURCE = "MesutARIDORU/insanlik-oldu-mu"
CLI_AGENT_IDS = {"claude": "claude-code", "codex": "codex", "gemini": "gemini-cli"}
# running from the copy npx skills installed: the skill is already in place, only the settings are left
IN_SHARED = os.path.realpath(SKILL_ROOT) == os.path.realpath(os.path.join(SHARED_DIR, NAME))
# Antigravity has no command line to look for, only its app and its folder in ~/.gemini
ANTIGRAVITY_APPS = ("/Applications/Antigravity.app", "/Applications/Antigravity IDE.app")


def antigravity_found():
    return any(os.path.isdir(p) for p in ANTIGRAVITY_APPS) or os.path.isdir(os.path.join(HOME, ".gemini", "antigravity"))


def antigravity_skills_dir():
    """Where Antigravity reads global skills: ~/.gemini/config/skills; earlier versions read ~/.gemini/antigravity/skills.
    npx skills counts Antigravity among the agents that read ~/.agents/skills and links nothing there."""
    old = os.path.join(HOME, ".gemini", "antigravity", "skills")
    if os.path.isdir(old) and not os.path.isdir(os.path.join(HOME, ".gemini", "config")):
        return old
    return os.path.join(HOME, ".gemini", "config", "skills")


def present(key, agents):
    return key in agents or (key == "antigravity" and antigravity_found())


def shared_available():
    return bool(shutil.which("npx"))


def target_state(key, agents):
    if key == "shared":
        if not shared_available():
            return "npx bulunamadı (Node.js gerekir)"
        used = " · bu bilgisayarda zaten kullanılıyor" if os.path.exists(SKILL_LOCK) else ""
        return f"~/.agents/skills, npx skills ile kilit dosyasına yazılır, diğer ajanlar da seçilebilir{used}"
    if key == "antigravity":
        if not antigravity_found():
            return "bu bilgisayarda bulunamadı"
        return "bulundu · " + antigravity_skills_dir().replace(HOME, "~", 1) + (f" · {SETUP_STEPS[key]}" if IN_SHARED else "")
    if key not in agents:
        return "bu bilgisayarda bulunamadı"
    return f"bulundu · {agents[key]['version']}" + (f" · {SETUP_STEPS[key]}" if IN_SHARED else "")


SETUP_STEPS = {"claude": "bağlantı ve betik izinleri", "codex": "yönlendirme notu", "gemini": f"/{NAME} komutu",
               "antigravity": "skill bağlantısı"}


def choose_targets(agents):
    """Which agents to install into (from the shared copy: which ones to set up). The ones found are preselected."""
    options = [(key, label) for key, label in TARGETS if not (IN_SHARED and key == "shared")]
    names = dict(TARGETS)
    found = [key for key, _ in options if present(key, agents)]
    if not IN_SHARED and shared_available() and os.path.exists(SKILL_LOCK):
        found.append("shared")  # skills on this computer are already installed this way
    if ARGS.targets == "all":
        return found
    if ARGS.targets != "ask":
        picked = [t.strip().lower() for t in ARGS.targets.split(",") if t.strip()]
        unknown = [t for t in picked if t not in names]
        if unknown:
            sys.exit(f"Bilinmeyen hedef: {', '.join(unknown)}. Geçerli hedefler: {', '.join(names)}")
        return [t for t in picked if t in dict(options)]
    if ARGS.yes or ARGS.dry_run or not sys.stdin.isatty():
        return found
    print("Hangi araçlar için ayar yapılsın?" if IN_SHARED else "Hangi yapay zeka araçlarına kurulsun?")
    for i, (key, label) in enumerate(options, 1):
        print(f"  {i}) [{'x' if key in found else ' '}] {label:<12} {target_state(key, agents)}")
    while True:
        answer = input("? Numaraları virgülle yaz (örnek: 1,2). Enter: işaretliler, 0: hiçbiri: ").strip().lower()
        if not answer:
            return found
        if answer == "0":
            return []
        picked, wrong = [], []
        for part in re.split(r"[,\s]+", answer):
            if part.isdigit() and 1 <= int(part) <= len(options):
                key = options[int(part) - 1][0]
            elif part in dict(options):
                key = part
            else:
                wrong.append(part)
                continue
            if key not in picked:
                picked.append(key)
        if not wrong:
            return picked
        print(f"  Anlaşılmadı: {', '.join(wrong)}. 1-{len(options)} arası numaralar yaz.")


# ---------------------------------------------------------------- 4. link the skill

def link(target_dir, label, source=None):
    """Links (or with --copy, copies) the skill into an agent's skills folder: this copy, or source when given."""
    source = source or SKILL_ROOT
    target = os.path.join(target_dir, NAME)
    if os.path.islink(target) and os.path.realpath(target) == os.path.realpath(source):
        say("✓", f"{label}: zaten bağlı ({target})")
        return target
    if os.path.realpath(target) == os.path.realpath(source):
        say("✓", f"{label}: skill zaten burada ({target})")
        return target
    if os.path.islink(target):
        # only a pointer: nothing to keep, and a renamed link would show up as a second skill
        if not ARGS.dry_run:
            os.unlink(target)
        say("·", f"{label}: eski bağlantı ({os.path.realpath(target)}) {'değiştirilecekti' if ARGS.dry_run else 'değiştirildi'}")
    elif os.path.exists(target):
        if not ask(f"{label}: {target} zaten var. Yedekleyip yenisiyle değiştireyim mi?"):
            say("·", f"{label}: dokunulmadı")
            return target
        # the backup goes outside the skills folder, otherwise the agent loads it as a second skill
        backup = os.path.join(CONFIG_DIR, "backups", f"{label.lower().replace(' ', '-')}-{NAME}-{time.strftime('%Y%m%d-%H%M%S')}")
        if not ARGS.dry_run:
            os.makedirs(os.path.dirname(backup), exist_ok=True)
            shutil.move(target, backup)
        say("·", f"{label}: eskisi {backup} olarak {'saklanacaktı (deneme çalışması)' if ARGS.dry_run else 'saklandı'}")
    if ARGS.dry_run:
        say("·", f"{label}: {target} {'kopyalanacaktı' if ARGS.copy else 'bağlanacaktı'} (deneme çalışması)")
        return target
    os.makedirs(target_dir, exist_ok=True)
    if ARGS.copy:
        shutil.copytree(source, target, ignore=shutil.ignore_patterns(".git", ".github", "__pycache__", "evals", "*.pyc", "PROGRESS.md"))
        say("✓", f"{label}: kopyalandı ({target})")
    else:
        os.symlink(source, target)
        say("✓", f"{label}: bağlandı ({target} → {source})")
    return target


def skill_source():
    """owner/repo of this checkout on GitHub, for npx skills; the published repository otherwise."""
    code, out = run(["git", "-C", SKILL_ROOT, "remote", "get-url", "origin"])
    m = re.search(r"github\.com[:/]([^/\s]+/[^/\s]+?)(?:\.git)?\s*$", out) if code == 0 else None
    return m.group(1) if m else DEFAULT_SOURCE


def install_shared(selected):
    """Installs through npx skills: one copy in ~/.agents/skills, recorded in the skills lock file,
    linked into the agents chosen there. This is how other skills on this computer are installed."""
    source = skill_source()
    cmd = ["npx", "-y", "skills", "add", source, "-g"]
    interactive = not ARGS.yes and sys.stdin.isatty()
    if not interactive:
        ids = [CLI_AGENT_IDS[t] for t in selected if t in CLI_AGENT_IDS]
        cmd += ["-y"] + (["-a"] + ids if ids else [])
    else:
        print("  npx skills hangi ajanlara kurulacağını soracak. Codex ve Gemini CLI kendiliğinden seçili gelir.")
        print("  Claude Code seçili gelmez: Search alanına claude yazıp boşluk tuşuyla işaretle, sonra Enter.")
    if ARGS.dry_run:
        say("·", "Ortak klasör: şu komut çalıştırılacaktı (deneme çalışması): " + " ".join(cmd))
        return os.path.join(SHARED_DIR, NAME)
    print("  $ " + " ".join(cmd))
    code = subprocess.run(cmd, cwd=HOME).returncode
    installed = os.path.exists(os.path.join(SHARED_DIR, NAME, "SKILL.md"))
    if code == 0 and installed:
        say("✓", f"Ortak klasör: kuruldu ({os.path.join(SHARED_DIR, NAME)}), kilit dosyasına yazıldı. Güncellemek için: npx skills update {NAME}")
    else:
        say("!", f"Ortak klasör: npx skills kurulumu tamamlanmadı (çıkış kodu {code}). Elle denemek için: npx skills add {source} -g")
    return os.path.join(SHARED_DIR, NAME)


def write_gemini_command(skill_path):
    folder = os.path.join(HOME, ".gemini", "commands")
    target = os.path.join(folder, f"{NAME}.toml")
    content = f'''description = "İnsanlık öldü mü? Türkçe metindeki yapay zeka izlerini temizler"

prompt = """
Önce {skill_path}/SKILL.md dosyasını oku ve oradaki talimata uy. Betikler {skill_path}/scripts altında,
referans dosyaları {skill_path}/references altında. Aşağıdaki isteği o talimata göre ele al.

{{{{args}}}}
"""
'''
    if ARGS.dry_run:
        say("·", f"gemini: {target} yazılacaktı (deneme çalışması)")
        return
    os.makedirs(folder, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    say("✓", f"gemini: /{NAME} komutu yazıldı ({target})")


# ---------------------------------------------------------------- 5. bridge config

LEGACY_PREFERENCE_VALUES = {  # Turkish values used by early development versions
    "kagit": ("paper", {"cizgili": "lined", "kareli": "grid", "duz": "plain"}),
    "yazi": ("font", {"ferah": "airy", "yumusak": "soft", "kitap": "book", "el": "hand"}),
    "tema": ("theme", {"": "", "light": "light", "dark": "dark"}),
    "motor": ("engine", {"otomatik": "auto", "ajan": "agent", "catal": "fork", "tek": "stateless"}),
}


def migrate_legacy_files():
    """Carries the preferences over from the Turkish file names of early development versions and removes the old files."""
    old_prefs = os.path.join(CONFIG_DIR, "tercihler.json")
    new_prefs = os.path.join(CONFIG_DIR, "preferences.json")
    if os.path.exists(old_prefs) and not os.path.exists(new_prefs):
        try:
            with open(old_prefs, encoding="utf-8") as f:
                old = json.load(f)
            new = {"time": old.get("zaman") or time.time() * 1000}
            for key, (new_key, values) in LEGACY_PREFERENCE_VALUES.items():
                if old.get(key) in values:
                    new[new_key] = values[old[key]]
            with open(new_prefs, "w", encoding="utf-8") as f:
                json.dump(new, f, ensure_ascii=False)
            say("✓", "Eski görünüm tercihleri yeni dosyaya taşındı")
        except Exception as e:
            say("!", f"Eski tercihler taşınamadı ({e})")
    for name in ("tercihler.json", "ayar.json"):
        path = os.path.join(CONFIG_DIR, name)
        if os.path.exists(path):
            os.remove(path)


def write_config(agents, installs):
    config = {
        "version": "1.7.0",
        "skill_dir": SKILL_ROOT,
        "installs": installs,
        "agents": agents,
        "default_agent": next((a for a in ("claude", "codex", "gemini") if a in agents), None),
        "default_engine": "auto",
        "engine_order": ["agent", "fork", "stateless"],
        "updated": time.strftime("%Y-%m-%d %H:%M"),
    }
    if ARGS.dry_run:
        say("·", f"köprü ayarı {CONFIG_FILE} dosyasına yazılacaktı (deneme çalışması)")
        return
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=1)
    migrate_legacy_files()
    say("✓", f"Köprü ayarı yazıldı ({CONFIG_FILE})")


# ---------------------------------------------------------------- 6. permissions

def claude_permissions(skill_path):
    settings = os.path.join(HOME, ".claude", "settings.json")
    # the skill itself also needs a rule: without it Claude Code asks before every use of the skill
    rules = [f"Skill({NAME})"] + [f"Bash(python3 {skill_path}/scripts/{s}:*)" for s in SCRIPTS]
    stale_rules = [f"Bash(python3 {skill_path}/scripts/{s}:*)" for s in OLD_SCRIPTS]
    try:
        with open(settings, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    except Exception as e:
        say("!", f"Claude ayar dosyası okunamadı ({e}), izinlere dokunulmadı.")
        return
    allow = data.setdefault("permissions", {}).setdefault("allow", [])
    added = [r for r in rules if r not in allow]
    removed = [r for r in stale_rules if r in allow]
    if not added and not removed:
        say("✓", "Claude Code: skill ve betik izinleri zaten var")
        return
    print("  Claude Code ayarında yapılacak değişiklik:")
    for r in removed:
        print(f"    - {r}  (artık olmayan betik)")
    for r in added:
        print(f"    + {r}")
    if not ARGS.permissions and not ask("Bu değişikliği ~/.claude/settings.json dosyasına uygulayayım mı?", default=False):
        say("·", "Claude Code: izinlere dokunulmadı. Claude skill'i ve betikleri her seferinde sorarak çalıştıracak.")
        return
    if ARGS.dry_run:
        say("·", "Claude Code: izinler güncellenecekti (deneme çalışması)")
        return
    if os.path.exists(settings):
        shutil.copy2(settings, f"{settings}.yedek-{time.strftime('%Y%m%d-%H%M%S')}")
    allow[:] = [r for r in allow if r not in removed] + added
    os.makedirs(os.path.dirname(settings), exist_ok=True)
    with open(settings, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    say("✓", "Claude Code: skill ve betik izinleri güncellendi (eski ayarın yedeği yanında)")


ROUTING_START = "<!-- insanlik-oldu-mu:start -->"
ROUTING_END = "<!-- insanlik-oldu-mu:end -->"
CODEX_ROUTING = f"""{ROUTING_START}
## İnsanlık öldü mü?

Kullanıcı Türkçe bir metni doğallaştırmak, insanlaştırmak, akıcı yapmak, yapay zeka izlerinden arındırmak ya da "yapay zeka mı yazmış?" diye incelemek istediğinde `{NAME}` skill'ini kullan.
{ROUTING_END}
"""


def codex_routing():
    """Adds a short routing note to Codex's global instructions.

    With many skills installed Codex may not pick this one by itself; tested on codex-cli 0.162.1,
    the note makes it use the skill without the user typing $insanlik-oldu-mu. Codex reads
    AGENTS.override.md instead of AGENTS.md when the override exists, so the note goes there.
    """
    home = os.path.join(HOME, ".codex")
    override = os.path.join(home, "AGENTS.override.md")
    target = override if os.path.exists(override) and os.path.getsize(override) > 0 else os.path.join(home, "AGENTS.md")
    try:
        with open(target, encoding="utf-8") as f:
            current = f.read()
    except FileNotFoundError:
        current = ""
    if ROUTING_START in current:
        say("✓", f"Codex: yönlendirme notu zaten var ({target})")
        return
    print(f"  Codex'te çok sayıda skill yüklüyse Codex bu skill'i kendiliğinden seçmeyebilir.")
    print(f"  {target} dosyasının sonuna üç satırlık bir yönlendirme notu eklenirse Türkçe metin istekleri bu skill'e gider.")
    if not ARGS.codex_routing and not ask("Bu notu ekleyeyim mi?", default=False):
        say("·", "Codex: yönlendirme eklenmedi. Skill'i istediğinde $insanlik-oldu-mu yazarak çağırabilirsin.")
        return
    if ARGS.dry_run:
        say("·", f"Codex: yönlendirme notu {target} dosyasına eklenecekti (deneme çalışması)")
        return
    if current:
        shutil.copy2(target, f"{target}.yedek-{time.strftime('%Y%m%d-%H%M%S')}")
    os.makedirs(home, exist_ok=True)
    with open(target, "a", encoding="utf-8") as f:
        f.write(("\n\n" if current and not current.endswith("\n\n") else "") + CODEX_ROUTING)
    say("✓", f"Codex: yönlendirme notu eklendi ({target}){' · eski dosyanın yedeği yanında' if current else ''}")


def codex_note():
    say("·", "Codex: Canlı köprü yalnız 127.0.0.1'de çalışan yerel bir sunucu açar. Sandbox ayarların sıkıysa")
    print("    Codex komut için onay isteyebilir, o oturum için izin vermen yeterli. Öneri çağrıları salt okunur sandbox'ta çalışır.")


# ---------------------------------------------------------------- 7. check

SAMPLE = """Günümüzde yapay zeka, iş dünyasının vazgeçilmez bir parçası haline gelmiştir. Bu bağlamda şirketimiz kapsamlı bir dönüşüm sürecine girmiştir. Bu sadece bir teknoloji yatırımı değil, aynı zamanda bir kültür değişimidir. Sonuç olarak geleceğe güvenle bakıyoruz."""
SAMPLE_REWRITE = """Şirketimiz yapay zekaya geniş çaplı bir yatırım yapıyor. Bu yatırım iş yapış biçimimizi de değiştirecek."""


def check(agents):
    tmp = tempfile.mkdtemp(prefix="iom-install-")
    old, new = os.path.join(tmp, "old.txt"), os.path.join(tmp, "new.txt")
    with open(old, "w", encoding="utf-8") as f:
        f.write(SAMPLE)
    with open(new, "w", encoding="utf-8") as f:
        f.write(SAMPLE_REWRITE)
    code, out = run([sys.executable, os.path.join(HERE, "audit.py"), old])
    say("✓" if code == 0 and "Alarm:" in out else "!", "Sayısal denetim " + ("çalışıyor" if code == 0 else "hata verdi: " + out[-200:]))
    page = os.path.join(tmp, "review.html")
    code, out = run([sys.executable, os.path.join(HERE, "review.py"), "--before", old, "--after", new, "--output", page])
    say("✓" if code == 0 and os.path.exists(page) else "!", "İnceleme sayfası " + ("üretiliyor" if code == 0 else "hata verdi: " + out[-200:]))
    sys.path.insert(0, HERE)
    try:
        import bridge
        info, _ = bridge.start(page, agent=next(iter(agents), None))
        status = bridge.call(info, "/api/status")
        labels = {"agent": "dinleyen ajan", "fork": "oturum çatalı", "stateless": "bağlamsız çağrı"}
        engines = [labels[e] for e, ok in status["engines"].items() if ok]
        say("✓", f"Canlı köprü açılıp kapanıyor · bu klasörde kullanılabilir yollar: {', '.join(engines) or 'yok (ajan dinlerken açılır)'}")
        if ARGS.try_engine and status["engines"].get("stateless"):
            no = bridge.call(info, "/api/suggest", {"part": 1, "before": "Bu sadece bir teknoloji yatırımı değil, aynı zamanda bir kültür değişimidir.",
                                                    "after": "Bu yatırım iş yapış biçimimizi de değiştirecek.", "request": "", "engine": "stateless"})["request"]
            for _ in range(90):
                r = bridge.call(info, f"/api/suggestions/{no}")
                if r["status"] != "pending":
                    break
                time.sleep(2)
            say("✓" if r["status"] == "ready" else "!", "Bağlamsız öneri motoru: " + ("; ".join(r["suggestions"]) if r["status"] == "ready" else r.get("error") or "cevap gelmedi"))
        bridge.call(info, "/api/close", {})
    except Exception as e:
        say("!", f"Canlı köprü açılamadı ({e}). Sayfa dosya olarak çalışır, geri bildirim kopyala-yapıştırla gelir.")
    shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- main

def main(argv=None):
    global ARGS
    ap = argparse.ArgumentParser(description="İnsanlık öldü mü? · installer")
    ap.add_argument("--targets", default="ask",
                    help="claude,codex,gemini,antigravity,shared, or all for every agent found (default: ask; without a terminal, every agent found). "
                         "shared installs through npx skills into ~/.agents/skills")
    ap.add_argument("--copy", action="store_true", help="copy instead of linking")
    ap.add_argument("--permissions", action="store_true", help="let Claude Code use the skill and its scripts without asking")
    ap.add_argument("--codex-routing", action="store_true", help="add a note to Codex's global instructions so Codex picks this skill by itself")
    ap.add_argument("--yes", action="store_true", help="install with defaults, without asking")
    ap.add_argument("--dry-run", action="store_true", help="show what would be done without changing anything")
    ap.add_argument("--no-check", action="store_true", help="skip the final check")
    ap.add_argument("--try-engine", action="store_true", help="try the stateless suggestion engine with a real call")
    ARGS = ap.parse_args(argv)

    print("İnsanlık öldü mü? · kurulum\n")
    preflight()
    agents = find_agents()
    print()
    if IN_SHARED:
        print(f"· Skill ortak klasörde kurulu, yeniden kurulmayacak. Güncellemek için: npx skills update {NAME}\n")
    targets = choose_targets(agents)
    labels = dict(TARGETS)
    if not targets:
        print("· Hiçbir araç seçilmedi, yalnızca ayar dosyası yazılacak.")
    else:
        print(("· Ayar yapılacak: " if IN_SHARED else "· Kurulacak: ") + ", ".join(labels[t] for t in targets))
        for t in targets:
            if t != "shared" and not present(t, agents):
                print(f"  {labels[t]} bu bilgisayarda bulunamadı. Skill yine kurulur, {labels[t]} kurulunca hazır olur.")
    installs = {}
    if IN_SHARED:
        installs["shared"] = SKILL_ROOT
        if "claude" in targets:
            # npx skills has usually linked it already; if not, the link points at this same copy
            installs["claude"] = link(os.path.join(HOME, ".claude", "skills"), "Claude Code")
        if "codex" in targets:
            installs["codex"] = SKILL_ROOT  # Codex reads ~/.agents/skills itself; a second link would show the skill twice
    elif "shared" in targets:
        # npx skills links the agents itself; linking them here too would give Codex the skill twice
        installs["shared"] = install_shared(targets)
        for key, folder in (("claude", ".claude"), ("codex", ".codex")):
            if key in targets:
                installs[key] = os.path.join(HOME, folder, "skills", NAME)
    else:
        if "claude" in targets:
            installs["claude"] = link(os.path.join(HOME, ".claude", "skills"), "Claude Code")
        if "codex" in targets:
            installs["codex"] = link(os.path.join(HOME, ".codex", "skills"), "Codex")
    if "antigravity" in targets:
        # npx skills leaves Antigravity out, so it is linked here in every case, to the shared copy when there is one
        installs["antigravity"] = link(antigravity_skills_dir(), "Antigravity", installs.get("shared"))
    if "gemini" in targets:
        # with the shared folder, Gemini reads the same copy as the other agents
        write_gemini_command(installs.get("shared") or SKILL_ROOT)
        installs["gemini"] = os.path.join(HOME, ".gemini", "commands", f"{NAME}.toml")
    print()
    write_config(agents, installs)
    if "claude" in installs:
        claude_permissions(installs["claude"])
    if "codex" in installs:
        codex_routing()
        codex_note()
    if not ARGS.no_check and not ARGS.dry_run:
        print()
        check(agents)
    print("\nBitti. Denemek için ajana şunu yaz: \"Şu metni doğallaştır: Günümüzde yapay zeka hayatımızın vazgeçilmez bir parçası haline gelmiştir.\"")


if __name__ == "__main__":
    main()
