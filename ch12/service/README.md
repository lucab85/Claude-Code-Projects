# Bookmarks API

Save URLs with a title and a tag, list them, filter by tag and delete
them. FastAPI and SQLite, in one file.

## Run

```bash
pip install fastapi uvicorn
cd ch12/service
uvicorn bookmarks_api:app --port 8000
```

The database is `bookmarks.db`, next to `bookmarks_api.py`. Delete it
for a fresh start.

## Endpoints

| Method | Path | Body | Status |
|---|---|---|---|
| POST | `/bookmarks` | `{"url": "...", "title": "...", "tag": "..."}` | 201 / 422 |
| GET | `/bookmarks` | | 200 |
| GET | `/bookmarks?tag=<t>` | | 200 (exact, case-sensitive match) |
| GET | `/bookmarks/{id}` | | 200 / 404 |
| DELETE | `/bookmarks/{id}` | | 204 / 404 |

A 404 body is exactly `{"error": "not found"}`. URLs must be absolute
`http` or `https` URLs with a host. The rules for each field are in
`../PROMPT.md` and `../DECISIONS.md`.

## Test

From the workspace root, with pytest and httpx2 (or httpx) installed:

```bash
python3 -m pytest -q ch12/service/tests
```

With the server running on a fresh database, in a second terminal:

```bash
ch12/smoke.sh 8000
```
