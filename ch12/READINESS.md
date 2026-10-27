# Production Readiness Report: Bookmarks API (ch12)

Target: a public deployment, reachable from the internet.

## Security
- Status: red
- Biggest risk: no authentication; anyone who can reach the port can
  read and delete every bookmark.
- Smallest next step: require an API key header on every route, read
  from an environment variable.

## Observability
- Status: red
- Biggest risk: no logging and no health endpoint, so failures are
  invisible until a user reports them.
- Smallest next step: add GET /health that runs SELECT 1, and log one
  line per request with its status.

## Deployment
- Status: yellow
- Biggest risk: no pinned dependencies; the run command is documented
  but a fresh install may get different versions.
- Smallest next step: add service/requirements.txt, frozen from a clean
  virtual environment, as in Exercise 11.6.

## Runbooks
- Status: red
- Biggest risk: no runbook, so nobody knows the first action when it
  fails out of hours.
- Smallest next step: write RUNBOOK.md with the five failures from
  Exercise 11.4 and the first command for each.

## Rollback
- Status: yellow
- Biggest risk: code can be reverted, but there is no release tag and no
  backup of bookmarks.db.
- Smallest next step: tag the release and back up bookmarks.db before
  every deploy.

## Verdict
Go / No-Go: No-Go. Rationale: Anyone on the internet could read or
delete every bookmark, and nobody would know. Fine for one trusted user
on localhost.

## Evidence
| Axis | Check | Result |
|---|---|---|
| Security | `grep -n -i -E "auth\|api_key\|Depends" ch12/service/bookmarks_api.py` | No matches: no authentication |
| Security | `grep -n "execute(" ch12/service/bookmarks_api.py` | Every query uses ? placeholders |
| Security | POST a 201-character title, a 2,049-character URL, `javascript:alert(1)` | 422 for each: input limits hold |
| Security | GET /docs | 200: API documentation is public |
| Observability | `grep -n "logging" ch12/service/bookmarks_api.py`; GET /health | No matches; 404 |
| Deployment | `ls ch12/service` | No requirements.txt, container or service file |
| Runbooks | `ls ch12/RUNBOOK.md` | No such file or directory |
| Rollback | `ls ch12/service` | No backup of bookmarks.db |
