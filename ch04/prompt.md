GOAL
Build a small Notes API persisting to SQLite.

CONSTRAINTS
- Python 3.11 with FastAPI, Pydantic v2 and the standard sqlite3 module.
- One process. No migrations framework: create the schema at startup.
- HTTP status codes: 201 on create, 200 on read/update, 204 on delete,
  404 on missing, 422 on invalid body.
- Timestamps in ISO 8601 UTC.

OUTPUT FORMAT
- A runnable project (a single source file is fine) plus a 5-line README
  with the run command.

EXAMPLES
- POST /notes {"title":"a","body":"b"} -> 201 {"id":1,"title":"a",
  "body":"b","created_at":"...","updated_at":"..."}
- GET /notes?q=spec -> 200 [matching notes]
- GET /notes/999 -> 404 {"error":"not found"}
- PATCH /notes/1 {"body":"new"} -> 200, other fields unchanged
