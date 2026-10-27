# Code review: ch12/service against ch12/PROMPT.md

Reviewed with the code-review skill, as a stranger's pull request,
on the winning candidate before any fix. Ranked by severity.

- [High] The URL check is a prefix test, so `http://`, `https:///path`
  and `http:// example.com` are saved with 201, although PROMPT.md asks
  for an absolute URL with a host and no whitespace. It also rejects
  `HTTPS://Example.com`, although URL schemes are case-insensitive.
  Smallest patch: parse with `urllib.parse.urlsplit`; require
  `scheme.lower()` in http/https and a `hostname`; reject whitespace.
- [Medium] `if tag:` treats `GET /bookmarks?tag=` as "no filter" and
  returns every bookmark; PROMPT.md says an empty tag matches nothing.
  Smallest patch: `if tag is not None:`.
- [Medium] `GET /bookmarks` has no paging, so the response grows with
  the table.
  Smallest patch: `limit` (default 50, max 200) and `offset` query
  parameters.
- [Low] FastAPI's `/docs` and `/openapi.json` are open to anyone who can
  reach the port.
  Smallest patch: `FastAPI(docs_url=None, redoc_url=None,
  openapi_url=None)` outside development.
- [Low] Unknown fields in a POST body (for example `"tags": [...]`) are
  silently ignored, so a client that sends several tags gets no error.
  Smallest patch: `model_config = ConfigDict(extra="forbid")` on
  `BookmarkIn`.

## Triage

| # | Decision | Why |
|---|---|---|
| 1 | Fixed | Breaks the spec, and a hostless link is useless to a reader. |
| 2 | Fixed | Breaks the spec; one-line change. |
| 3 | Deferred | Fine for a small internal tool; a next step in READINESS.md. |
| 4 | Deferred | Only matters for a public deployment; in READINESS.md. |
| 5 | Deferred | Product decision; noted for Exercise 12.1. |

## Fixes applied

Each fix came with a test that failed before the change and passes after
it. Against the code before the fixes, the suite reports
`2 failed, 6 passed`; after them, `8 passed`. smoke.sh passed both
before and after, because it checks only status codes on valid input
and `ftp://x`.

| Finding | Test | Commit |
|---|---|---|
| 1 | `test_url_must_have_a_host` (new) | `fix(ch12): require a host in bookmark URLs` |
| 2 | `test_tag_filter_is_exact_and_case_sensitive` (added `?tag=` -> `[]`) | `fix(ch12): make an empty tag filter match nothing` |

The diff for finding 1:

```diff
     def url_is_web_address(cls, v: str) -> str:
-        if not v.startswith(("http://", "https://")):
-            raise ValueError("url must start with http:// or https://")
+        if any(c.isspace() for c in v):
+            raise ValueError("url must not contain whitespace")
+        parts = urlsplit(v)
+        if parts.scheme.lower() not in ALLOWED_SCHEMES or not parts.hostname:
+            raise ValueError("url must be an absolute http or https URL")
         return v
```

The diff for finding 2:

```diff
-        if tag:
+        if tag is not None:
```
