# Stack (ch12 only)
- In this folder, FastAPI, Pydantic v2 and uvicorn are allowed runtime
  dependencies, with the standard sqlite3 module. Nothing else.
- pytest and FastAPI's TestClient for tests. No mocks of the service.

# Layout
- The service is one file: service/bookmarks_api.py. Tests live in
  service/tests/. The contract is smoke.sh; don't change it to make
  code pass.

# Commands
- Run (from service/): uvicorn bookmarks_api:app --port 8000
- Test (from the workspace root): python3 -m pytest -q ch12/service/tests
- Smoke (server running, fresh database): ch12/smoke.sh 8000

# Rules
- PROMPT.md is the spec. If code and PROMPT.md disagree, ask me.
- 404 bodies are exactly {"error": "not found"}.
- Don't touch other chapters' folders.
