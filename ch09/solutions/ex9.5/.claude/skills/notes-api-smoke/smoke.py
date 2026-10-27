#!/usr/bin/env python3
"""Smoke-test a single-file Notes API: smoke.py MODULE.py [PORT]."""
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


def call(method, url, body=None):
    """Send one request; return (status code, parsed JSON or None)."""
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        url, data=data, method=method,
        headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            status, raw = response.status, response.read()
    except urllib.error.HTTPError as error:
        status, raw = error.code, error.read()
    try:
        return status, json.loads(raw) if raw else None
    except ValueError:
        return status, None


def port_in_use(port):
    """Return True if something already listens on the port."""
    with socket.socket() as sock:
        return sock.connect_ex(("127.0.0.1", port)) == 0


def wait_until_up(base, server, seconds=15):
    """Poll the API until it answers, the server dies or time runs out."""
    deadline = time.time() + seconds
    while time.time() < deadline and server.poll() is None:
        try:
            call("GET", f"{base}/notes")
            return True
        except OSError:
            time.sleep(0.3)
    return False


def run_checks(base):
    """Run every check in order; return the number of failures."""
    failures = 0

    def check(label, ok, got):
        nonlocal failures
        print(f"{'PASS' if ok else 'FAIL'}  {label} ({got})")
        failures += not ok

    status, note = call("POST", f"{base}/notes",
                        {"title": "smoke", "body": "test"})
    note_id = note.get("id") if isinstance(note, dict) else None
    check("create note", status == 201 and note_id is not None, status)
    status, _ = call("POST", f"{base}/notes", {"title": "  ", "body": "x"})
    check("blank title rejected", status == 422, status)
    status, notes = call("GET", f"{base}/notes")
    ids = [n.get("id") for n in notes or [] if isinstance(n, dict)]
    check("list notes", status == 200 and note_id in ids, status)
    status, found = call("GET", f"{base}/notes?q=smoke")
    ids = [n.get("id") for n in found or [] if isinstance(n, dict)]
    check("search notes", status == 200 and note_id in ids, status)
    status, found = call("GET", f"{base}/notes?q=%25")
    ids = [n.get("id") for n in found or [] if isinstance(n, dict)]
    check("search treats % literally", status == 200 and note_id not in ids,
          status)
    status, _ = call("GET", f"{base}/notes/{note_id}")
    check("get note", status == 200, status)
    status, note = call("PATCH", f"{base}/notes/{note_id}",
                        {"body": "updated"})
    updated = isinstance(note, dict) and note.get("body") == "updated"
    check("update note", status == 200 and updated, status)
    status, _ = call("DELETE", f"{base}/notes/{note_id}")
    check("delete note", status == 204, status)
    status, body = call("GET", f"{base}/notes/{note_id}")
    check("deleted note is 404",
          status == 404 and body == {"error": "not found"},
          f"{status} {json.dumps(body)}")
    return failures


def main():
    """Start a temporary copy of the API, check it and stop it."""
    if len(sys.argv) not in (2, 3):
        print("usage: smoke.py MODULE.py [PORT]", file=sys.stderr)
        return 1
    module = Path(sys.argv[1]).resolve()
    port = int(sys.argv[2]) if len(sys.argv) == 3 else 8099
    if not module.is_file():
        print(f"FAIL  no such file: {module}")
        return 1
    if port_in_use(port):
        print(f"FAIL  port {port} is already in use; pick another")
        return 1
    workdir = Path(tempfile.mkdtemp(prefix="notes-smoke-"))
    shutil.copy(module, workdir / module.name)
    log = open(workdir / "server.log", "w")
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", f"{module.stem}:app",
         "--port", str(port)], cwd=workdir, stdout=log, stderr=log)
    base = f"http://127.0.0.1:{port}"
    try:
        if not wait_until_up(base, server):
            print("FAIL  server did not start. Last lines of its log:")
            log.flush()
            print((workdir / "server.log").read_text()[-800:])
            return 1
        failures = run_checks(base)
    finally:
        server.terminate()
        server.wait(timeout=10)
        log.close()
        shutil.rmtree(workdir, ignore_errors=True)
    print(f"RESULT: {'PASS' if failures == 0 else 'FAIL'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
