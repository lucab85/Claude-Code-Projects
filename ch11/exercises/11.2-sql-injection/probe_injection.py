"""Exercise 11.2: show whether GET /notes?q= is open to SQL injection."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "ch05"))
import notes_api  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

notes_api.DB_PATH = Path(tempfile.mkdtemp()) / "notes.db"
notes_api.init_db()
client = TestClient(notes_api.app)

client.post("/notes", json={"title": "public", "body": "for everyone"})
client.post("/notes", json={"title": "private", "body": "for me only"})
attack = "zzz' OR 1=1 --"
found = client.get("/notes", params={"q": attack}).json()
print(f"GET /notes?q={attack}:", [n["title"] for n in found])
print("INJECTION" if found else "SAFE: no note contains zzz")
