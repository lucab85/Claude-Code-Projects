"""Collect readiness evidence from the Notes API, on a scratch database."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ch05"))
import notes_api  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

notes_api.DB_PATH = Path(tempfile.mkdtemp()) / "notes.db"
notes_api.init_db()
client = TestClient(notes_api.app)

big = client.post("/notes", json={"title": "x" * 100_000,
                                  "body": "y" * 5_000_000})
print("100,000-char title + 5 MB body:", big.status_code)
size = len(client.get("/notes").content)
print("GET /notes response size:", size, "bytes")
print("GET /health:", client.get("/health").status_code)
print("GET /docs:", client.get("/docs").status_code)
