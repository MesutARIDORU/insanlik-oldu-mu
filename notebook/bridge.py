# -*- coding: utf-8 -*-
"""Notebook review · the live bridge

Runs a local bridge between the review page and the agent (Claude Code, Codex or Gemini CLI).
The page sends its suggestion requests and the user's decisions here. A suggestion request is
answered through one of three engines:

  agent      the listening agent: if the agent in the chat is waiting with `bridge.py wait`,
             it answers the request itself
  fork       a fork of the chat session (claude --resume --fork-session, codex exec fork):
             keeps the whole context, the main chat stays free
  stateless  a call without chat history: claude -p / codex exec / gemini -p

A skill's scripts/bridge.py calls configure() with its product and its own path, then main().
Commands (run by the agent):
  python3 bridge.py start --page review.html [--agent claude|codex|gemini] [--open]
  python3 bridge.py wait [--timeout 540]
  python3 bridge.py reply --request N --suggestion "..." [--suggestion "..."]
  python3 bridge.py status
  python3 bridge.py close

Security: the server binds to 127.0.0.1 only, requires a per-session token on every request
and checks the Host header. Forked and stateless calls cannot use tools (--tools "" for Claude,
read-only sandbox for Codex, plan mode for Gemini).

Uses only the Python 3 standard library.
"""

import argparse
import hmac
import http.server
import json
import os
import re
import secrets
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
import webbrowser

VALID_PREFERENCES = {"paper": {"lined", "grid", "plain"}, "font": {"airy", "soft", "book", "hand"},
                     "theme": {"", "light", "dark"}, "engine": {"auto", "agent", "fork", "stateless"}}
ENGINES = ("agent", "fork", "stateless")
IDLE_SHUTDOWN = 3 * 60 * 60  # seconds
LISTENING_GRACE = 25         # the agent counts as listening for this many seconds after its last wait call
ENGINE_TIMEOUT = 240

# set by configure()
PRODUCT = None
SCRIPT = None
CONFIG_FILE = None
PREFERENCES_FILE = None


def configure(product, script):
    """Binds the bridge to a product. script is the skill's bridge.py: the background server runs it."""
    global PRODUCT, SCRIPT, CONFIG_FILE, PREFERENCES_FILE
    PRODUCT = product
    SCRIPT = os.path.abspath(script)
    CONFIG_FILE = os.path.join(product.config_dir, "config.json")
    PREFERENCES_FILE = os.path.join(product.config_dir, "preferences.json")


def t(key, **values):
    return PRODUCT.t(key, **values)


def root_dir():
    root = PRODUCT.temp_dir
    os.makedirs(root, exist_ok=True)
    return root


def read_preferences():
    try:
        with open(PREFERENCES_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


PREFERENCES_LOCK = threading.Lock()


def write_preferences(data):
    """Writes the preferences. Looks at the timestamp so an older request never overwrites a newer one."""
    clean = {k: data[k] for k, allowed in VALID_PREFERENCES.items() if data.get(k) in allowed}
    clean["time"] = data["time"] if isinstance(data.get("time"), (int, float)) else time.time() * 1000
    with PREFERENCES_LOCK:
        current = read_preferences() or {}
        if (current.get("time") or 0) > clean["time"]:
            return current
        os.makedirs(os.path.dirname(PREFERENCES_FILE), exist_ok=True)
        tmp = PREFERENCES_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(clean, f, ensure_ascii=False)
        os.replace(tmp, PREFERENCES_FILE)
    return clean


def read_config():
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ---------------------------------------------------------------- agent and session detection

def guess_agent():
    if os.environ.get("CLAUDE_CODE_SESSION_ID") or os.environ.get("CLAUDECODE"):
        return "claude"
    if any(k.startswith("CODEX_") for k in os.environ):
        return "codex"
    if any(k.startswith("GEMINI_CLI") for k in os.environ):
        return "gemini"
    return read_config().get("default_agent") or next((a for a in ("claude", "codex", "gemini") if shutil.which(a)), None)


def latest_codex_session(cwd):
    """Finds the id of the most recent Codex session opened in this folder, from Codex's session files."""
    root = os.path.join(os.path.expanduser("~"), ".codex", "sessions")
    candidates = []
    for folder, _, files in os.walk(root):
        for name in files:
            if name.endswith(".jsonl"):
                path = os.path.join(folder, name)
                try:
                    candidates.append((os.path.getmtime(path), path))
                except OSError:
                    pass
    for _, path in sorted(candidates, reverse=True)[:60]:
        try:
            with open(path, encoding="utf-8") as f:
                first = json.loads(f.readline())
            p = first.get("payload", {})
            if os.path.realpath(p.get("cwd", "")) == os.path.realpath(cwd):
                return p.get("id") or p.get("session_id")
        except Exception:
            continue
    return None


def session_id(agent, cwd):
    if agent == "claude":
        return os.environ.get("CLAUDE_CODE_SESSION_ID")
    if agent == "codex":
        for k in ("CODEX_SESSION_ID", "CODEX_THREAD_ID", "CODEX_CONVERSATION_ID"):
            if os.environ.get(k):
                return os.environ[k]
        return latest_codex_session(cwd)
    return None


def cli_path(agent):
    path = ((read_config().get("agents") or {}).get(agent) or {}).get("path")
    return path if path and os.path.exists(path) else shutil.which(agent or "")


# ---------------------------------------------------------------- suggestion engines

def suggestion_prompt(req):
    def quote(x):
        return (x or "").strip().replace("\n", " ") or t("bridge.none")
    return t("bridge.prompt", before=quote(req.get("before")), after=quote(req.get("after")),
             context_before=quote(req.get("context_before")), context_after=quote(req.get("context_after")),
             reason=quote(req.get("reason")),
             request=quote(req.get("request")) if req.get("request") else t("bridge.default_request"))


def parse_suggestions(text):
    text = (text or "").strip()
    candidates = [text]
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        candidates.append(text[start:end + 1])
    for c in candidates:
        try:
            d = json.loads(c)
            if isinstance(d, dict) and isinstance(d.get("suggestions"), list):
                return [str(x).strip() for x in d["suggestions"] if str(x).strip()][:5]
        except Exception:
            pass
    lines = [re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", s).strip().strip('"«»“”') for s in text.splitlines()]
    return [s for s in lines if s][:5]


def run_engine(engine, agent, session, cwd, req):
    """Runs the CLI through the chosen engine and returns a list of suggestions. Raises RuntimeError on failure."""
    path = cli_path(agent)
    if not path:
        raise RuntimeError(t("bridge.command_missing", agent=agent))
    prompt = suggestion_prompt(req)
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)  # avoid the nested-call warning
    if agent == "claude":
        cmd = [path, "-p", "--output-format", "json", "--no-session-persistence"]
        if engine == "fork":
            cmd += ["--resume", session, "--fork-session"]
        cmd += ["--tools", ""]
        result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=ENGINE_TIMEOUT, cwd=cwd, env=env)
        if result.returncode != 0:
            raise RuntimeError((result.stderr or result.stdout or t("bridge.agent_error", agent=agent)).strip()[-400:])
        try:
            text = json.loads(result.stdout).get("result", "")
        except Exception:
            text = result.stdout
    elif agent == "codex":
        out_file = tempfile.NamedTemporaryFile(prefix=f"{PRODUCT.slug}-codex-", suffix=".txt", delete=False).name
        if engine == "fork":
            cmd = [path, "exec", "fork", session, "--ephemeral", "--skip-git-repo-check",
                   "-c", 'sandbox_mode="read-only"', "-c", 'approval_policy="never"', "-o", out_file, "-"]
        else:
            cmd = [path, "exec", "--ephemeral", "--skip-git-repo-check", "-s", "read-only",
                   "-c", 'approval_policy="never"', "-o", out_file, "-"]
        result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=ENGINE_TIMEOUT, cwd=cwd, env=env)
        try:
            with open(out_file, encoding="utf-8") as f:
                text = f.read()
        finally:
            try:
                os.remove(out_file)
            except OSError:
                pass
        if not text.strip():
            raise RuntimeError((result.stderr or result.stdout or t("bridge.no_answer", agent=agent)).strip()[-400:])
    elif agent == "gemini":
        # plan mode is read-only; without --skip-trust Gemini refuses to run headless in an untrusted folder
        cmd = [path, "-p", prompt, "--approval-mode", "plan", "--skip-trust", "-o", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=ENGINE_TIMEOUT, cwd=cwd, env=env)
        if result.returncode != 0:
            raise RuntimeError((result.stderr or result.stdout or t("bridge.agent_error", agent=agent)).strip()[-400:])
        try:
            text = json.loads(result.stdout).get("response", "")
        except Exception:
            text = result.stdout
    else:
        raise RuntimeError(t("bridge.unknown_agent", agent=agent))
    suggestions = parse_suggestions(text)
    if not suggestions:
        raise RuntimeError(t("bridge.no_suggestions"))
    return suggestions


# ---------------------------------------------------------------- server state

class State:
    def __init__(self, info):
        self.info = info
        self.lock = threading.Condition()
        self.events = []
        self.requests = {}
        self.counter = 0
        self.agent_last_seen = 0.0
        self.agents_waiting = 0
        self.last_activity = time.time()
        self.sent = None

    def agent_listening(self):
        return self.agents_waiting > 0 or time.time() - self.agent_last_seen < LISTENING_GRACE

    def engines(self):
        agent, session = self.info.get("agent"), self.info.get("session")
        cli = bool(cli_path(agent)) if agent else False
        return {
            "agent": self.agent_listening(),
            "fork": cli and bool(session) and agent in ("claude", "codex"),
            "stateless": cli,
        }

    def pick_engine(self, wanted):
        available = self.engines()
        if wanted in ENGINES:
            return wanted if available[wanted] else None
        for candidate in ENGINES:
            if available[candidate]:
                return candidate
        return None


def make_server(info, page_html):
    state = State(info)
    token = info["token"]

    class Handler(http.server.BaseHTTPRequestHandler):
        server_version = PRODUCT.slug

        def log_message(self, *a):
            pass

        def _authorized(self):
            port = self.server.server_address[1]
            if self.headers.get("Host") not in (f"127.0.0.1:{port}", f"localhost:{port}"):
                return False
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            given = self.headers.get("X-Token") or (query.get("t") or [""])[0]
            return hmac.compare_digest(given, token)

        def _json(self, code, data):
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _body(self):
            n = int(self.headers.get("Content-Length") or 0)
            if n > 2_000_000:
                raise ValueError(t("bridge.too_large"))
            raw = self.rfile.read(n) if n else b"{}"
            return json.loads(raw.decode("utf-8") or "{}")

        def do_GET(self):
            if not self._authorized():
                return self._json(403, {"error": t("bridge.unauthorized")})
            state.last_activity = time.time()
            path = urllib.parse.urlparse(self.path).path
            if path == "/":
                live = {"token": token, "agent": info.get("agent"), "has_session": bool(info.get("session")),
                        "preferences": read_preferences()}
                html = page_html.replace("/*__LIVE__*/null", json.dumps(live, ensure_ascii=False))
                body = html.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if path == "/api/status":
                return self._json(200, {"agent": info.get("agent"), "agent_listening": state.agent_listening(),
                                        "engines": state.engines(), "sent": state.sent is not None})
            m = re.fullmatch(r"/api/suggestions/(\d+)", path)
            if m:
                req = state.requests.get(int(m.group(1)))
                return self._json(200 if req else 404, req or {"error": t("bridge.not_found")})
            if path == "/api/agent/wait":
                query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                seconds = min(max(float((query.get("timeout") or ["540"])[0]), 1.0), 3600.0)
                return self._json(200, agent_wait(seconds))
            if path == "/api/agent/status":
                pending = [e for e in state.events if not e["delivered"]]
                return self._json(200, {"pending_events": len(pending), "sent": state.sent,
                                        "requests": state.requests, "info": {k: v for k, v in info.items() if k != "token"}})
            return self._json(404, {"error": t("bridge.not_found")})

        def do_POST(self):
            if not self._authorized():
                return self._json(403, {"error": t("bridge.unauthorized")})
            if "application/json" not in (self.headers.get("Content-Type") or ""):
                return self._json(415, {"error": t("bridge.json_expected")})
            state.last_activity = time.time()
            path = urllib.parse.urlparse(self.path).path
            try:
                data = self._body()
            except Exception as e:
                return self._json(400, {"error": str(e)})
            if path == "/api/suggest":
                engine = state.pick_engine(data.get("engine") or "auto")
                if not engine:
                    return self._json(409, {"error": t("bridge.no_engine")})
                with state.lock:
                    state.counter += 1
                    no = state.counter
                    state.requests[no] = {"id": no, "status": "pending", "engine": engine, "suggestions": [], "error": None,
                                          "part": data.get("part")}
                    if engine == "agent":
                        state.events.append({"type": "suggestion", "request": no, "data": data, "delivered": False})
                        state.lock.notify_all()
                if engine != "agent":
                    threading.Thread(target=engine_job, args=(no, engine, data), daemon=True).start()
                return self._json(200, {"request": no, "engine": engine})
            if path == "/api/send":
                text = str(data.get("text") or "")
                with state.lock:
                    state.sent = text
                    listening = state.agent_listening()
                    state.events.append({"type": "send", "data": {"text": text}, "delivered": False})
                    state.lock.notify_all()
                with open(os.path.join(info["dir"], "feedback.txt"), "w", encoding="utf-8") as f:
                    f.write(text)
                return self._json(200, {"status": "delivered" if listening else "saved"})
            if path == "/api/agent/reply":
                no = int(data.get("request") or 0)
                req = state.requests.get(no)
                if not req:
                    return self._json(404, {"error": t("bridge.no_request")})
                suggestions = [str(x).strip() for x in (data.get("suggestions") or []) if str(x).strip()]
                with state.lock:
                    req.update({"status": "ready" if suggestions else "error", "suggestions": suggestions,
                                "error": None if suggestions else t("bridge.agent_sent_none")})
                return self._json(200, {"status": req["status"]})
            if path == "/api/preferences":
                try:
                    return self._json(200, write_preferences(data))
                except Exception as e:
                    return self._json(500, {"error": str(e)})
            if path == "/api/close":
                self._json(200, {"status": "closing"})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            return self._json(404, {"error": t("bridge.not_found")})

    def agent_wait(seconds):
        deadline = time.time() + seconds
        with state.lock:
            state.agents_waiting += 1
            try:
                while True:
                    state.agent_last_seen = time.time()
                    for e in state.events:
                        if not e["delivered"]:
                            e["delivered"] = True
                            return {"type": e["type"], **({"request": e["request"]} if "request" in e else {}), "data": e["data"]}
                    left = deadline - time.time()
                    if left <= 0:
                        return {"type": "timeout"}
                    state.lock.wait(timeout=min(left, 5))
            finally:
                state.agents_waiting -= 1
                state.agent_last_seen = time.time()

    def engine_job(no, engine, data):
        try:
            suggestions = run_engine(engine, info.get("agent"), info.get("session"), info.get("cwd"), data)
            result = {"status": "ready", "suggestions": suggestions, "error": None}
        except subprocess.TimeoutExpired:
            result = {"status": "error", "suggestions": [], "error": t("bridge.agent_timeout")}
        except Exception as e:
            result = {"status": "error", "suggestions": [], "error": str(e)}
        with state.lock:
            state.requests[no].update(result)

    class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    server = Server(("127.0.0.1", 0), Handler)

    def watchdog():
        while True:
            time.sleep(60)
            if time.time() - state.last_activity > IDLE_SHUTDOWN and state.agents_waiting == 0:
                server.shutdown()
                return
    threading.Thread(target=watchdog, daemon=True).start()
    return server


# ---------------------------------------------------------------- session files

def latest_session_dir():
    try:
        with open(os.path.join(root_dir(), "latest"), encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return None


def open_sessions():
    """Folders of sessions whose server is running, newest first."""
    root = root_dir()
    dirs = [os.path.join(root, d) for d in os.listdir(root) if os.path.exists(os.path.join(root, d, "state.json"))]
    return sorted(dirs, key=lambda d: os.path.getmtime(os.path.join(d, "state.json")), reverse=True)


def read_info(session=None):
    if session:
        folder = os.path.join(root_dir(), session)
    else:
        folder = latest_session_dir()
        if not folder or not os.path.exists(os.path.join(folder, "state.json")):
            running = open_sessions()
            folder = running[0] if running else None
    if not folder or not os.path.exists(os.path.join(folder, "state.json")):
        sys.exit(t("bridge.no_session"))
    with open(os.path.join(folder, "state.json"), encoding="utf-8") as f:
        return json.load(f)


def call(info, path, data=None, timeout=30):
    url = f"http://127.0.0.1:{info['port']}{path}"
    headers = {"X-Token": info["token"], "Host": f"127.0.0.1:{info['port']}"}
    body = None
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST" if data is not None else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------------------------------------------------------------- commands

def start(page, agent=None, session=None, open_page=False):
    """Starts the server in the background and returns its address. page.main() calls this too."""
    with open(page, encoding="utf-8") as f:
        f.read(1)
    cwd = os.getcwd()
    agent = agent or guess_agent()
    session = session or session_id(agent, cwd)
    sid = time.strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
    folder = os.path.join(root_dir(), sid)
    os.makedirs(folder, exist_ok=True)
    info = {"id": sid, "dir": folder, "token": secrets.token_urlsafe(18), "agent": agent,
            "session": session, "cwd": cwd, "page": os.path.abspath(page), "started": time.time()}
    with open(os.path.join(folder, "start.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False)
    with open(os.path.join(folder, "server.log"), "w", encoding="utf-8") as log:
        subprocess.Popen([sys.executable, SCRIPT, "_serve", folder],
                         stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True, cwd=cwd)
    state_path = os.path.join(folder, "state.json")
    for _ in range(100):
        if os.path.exists(state_path):
            break
        time.sleep(0.1)
    else:
        with open(os.path.join(folder, "server.log"), encoding="utf-8") as f:
            raise RuntimeError(t("bridge.start_failed", log=f.read()[-500:]))
    with open(state_path, encoding="utf-8") as f:
        info = json.load(f)
    with open(os.path.join(root_dir(), "latest"), "w", encoding="utf-8") as f:
        f.write(folder)
    address = f"http://127.0.0.1:{info['port']}/?t={info['token']}"
    if open_page:
        try:
            webbrowser.open(address)
        except Exception:
            pass
    return info, address


def _serve(folder):
    with open(os.path.join(folder, "start.json"), encoding="utf-8") as f:
        info = json.load(f)
    with open(info["page"], encoding="utf-8") as f:
        html = f.read()
    server = make_server(info, html)
    info["port"] = server.server_address[1]
    info["pid"] = os.getpid()
    tmp = os.path.join(folder, "state.json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False)
    os.replace(tmp, os.path.join(folder, "state.json"))
    try:
        server.serve_forever(poll_interval=0.5)
    finally:
        try:
            os.remove(os.path.join(folder, "state.json"))
        except OSError:
            pass


def print_event(event):
    kind = event.get("type")
    if kind == "suggestion":
        d = event["data"]
        print(t("bridge.event_suggestion", request=event["request"], part=d.get("part")))
        print(t("bridge.event_before", x=repr(d.get("before", ""))))
        print(t("bridge.event_after", x=repr(d.get("after", ""))))
        print(t("bridge.event_context", before=repr(d.get("context_before", "")), after=repr(d.get("context_after", ""))))
        print(t("bridge.event_reason", x=repr(d.get("reason", ""))))
        print(t("bridge.event_request", x=d.get("request") or t("bridge.event_no_request")))
        print(t("bridge.event_answer", script=SCRIPT, request=event["request"]))
    elif kind == "send":
        print(t("bridge.event_send"))
        print(event["data"]["text"])
        print(t("bridge.event_send_next", script=SCRIPT))
    else:
        print(t("bridge.event_timeout"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=f"{PRODUCT.name} · live bridge")
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("start", help="serve the review page through the bridge")
    p.add_argument("--page", required=True)
    p.add_argument("--agent", choices=["claude", "codex", "gemini"])
    p.add_argument("--session-id")
    p.add_argument("--open", action="store_true")
    p = sub.add_parser("wait", help="wait for the next request from the page")
    p.add_argument("--session")
    p.add_argument("--timeout", type=float, default=540)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("reply", help="answer a suggestion request")
    p.add_argument("--session")
    p.add_argument("--request", type=int, required=True)
    p.add_argument("--suggestion", action="append", required=True)
    p = sub.add_parser("status", help="show the bridge status and the decisions the user sent")
    p.add_argument("--session")
    p = sub.add_parser("close", help="close the bridge")
    p.add_argument("--session")
    p = sub.add_parser("_serve")
    p.add_argument("folder")
    a = ap.parse_args(argv)

    if a.command == "_serve":
        return _serve(a.folder)
    if a.command == "start":
        info, address = start(a.page, a.agent, a.session_id, a.open)
        print(t("cli.live", address=address))
        print(t("cli.session", id=info["id"], agent=info.get("agent") or t("cli.none"),
                fork=t("cli.fork_possible") if info.get("session") else t("cli.fork_none")))
        return
    info = read_info(getattr(a, "session", None))
    if a.command == "wait":
        try:
            event = call(info, f"/api/agent/wait?timeout={a.timeout}", timeout=a.timeout + 15)
        except Exception as e:
            sys.exit(t("bridge.unreachable", error=e))
        if a.json:
            print(json.dumps(event, ensure_ascii=False, indent=1))
        else:
            print_event(event)
    elif a.command == "reply":
        print(call(info, "/api/agent/reply", {"request": a.request, "suggestions": a.suggestion}))
    elif a.command == "status":
        s = call(info, "/api/agent/status")
        print(t("bridge.status", id=info["id"], port=info["port"], pending=s["pending_events"]))
        if s.get("sent"):
            print(t("bridge.status_sent"))
            print(s["sent"])
        else:
            print(t("bridge.status_not_sent"))
    elif a.command == "close":
        try:
            call(info, "/api/close", {})
            print(t("bridge.closed"))
        except Exception as e:
            print(t("bridge.already_closed", error=e))
