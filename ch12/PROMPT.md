GOAL
Build a small Bookmarks API persisting to SQLite: save a URL with a
title and a tag, list bookmarks, filter them by tag, fetch one and
delete one.

CONSTRAINTS
- Python 3.11+ with FastAPI, Pydantic v2 and the standard sqlite3
  module. One file: ch12/service/bookmarks_api.py. Create the schema at
  startup. Keep the database path in a module-level DB_PATH, next to
  the file, named bookmarks.db.
- Open a connection per request and always close it.
- Fields: url, title and tag are all required.
  - url: absolute http or https URL with a host, at most 2,048
    characters, no whitespace. Reject every other scheme, including
    javascript:, data:, mailto: and ftp://. Store it exactly as sent;
    don't normalize it.
  - title: not blank, at most 200 characters.
  - tag: exactly one tag per bookmark, one word with no spaces, at
    most 50 characters.
- GET /bookmarks?tag=<t> returns only bookmarks whose tag equals t
  exactly. Case-sensitive, no partial matches. An empty tag= matches
  nothing.
- Duplicate URLs are allowed. No update route.
- Lists are ordered by id, oldest first. No paging yet.
- HTTP status codes: 201 on create, 200 on read, 204 with an empty body
  on delete, 404 on a missing id, 422 on an invalid body.
- The 404 body is exactly {"error":"not found"}, as in the Notes API.
- Timestamps in ISO 8601 UTC.

OUTPUT FORMAT
- The single source file plus ch12/service/README.md with the run
  command. Don't write tests yet. When you're done, tell me the run
  command.

EXAMPLES
- POST /bookmarks {"url":"https://example.com","title":"ex","tag":"misc"}
  -> 201 {"id":1,"url":"https://example.com","title":"ex","tag":"misc",
  "created_at":"..."}
- POST /bookmarks {"url":"ftp://x","title":"ex","tag":"misc"} -> 422
- GET /bookmarks?tag=misc -> 200 [only bookmarks tagged exactly misc]
- GET /bookmarks?tag=Misc -> 200 []
- DELETE /bookmarks/1 -> 204, then GET /bookmarks/1 -> 404
  {"error":"not found"}
