# Production Readiness Report: Notes API (ch05)

## Security
- Status: red
- Biggest risk: no authentication; anyone who can reach the port can
  read, change or delete every note.
- Smallest next step: require an API key header on every route, read
  from an environment variable.

## Observability
- Status: yellow
- Biggest risk: no health endpoint, so a monitor can't tell a hung API
  from a working one.
- Smallest next step: add GET /health that checks the database.

## Deployment
- Status: red
- Biggest risk: dependencies aren't pinned, and the only documented run
  command is the development server with --reload.
- Smallest next step: add requirements.txt with exact versions and a
  production run command without --reload.

## Runbooks
- Status: red
- Biggest risk: when it fails out of hours, nobody knows the first
  action to take.
- Smallest next step: write RUNBOOK.md with five failures and the first
  command for each.

## Rollback
- Status: yellow
- Biggest risk: code can be reverted, but there is no release tag and no
  database backup to restore.
- Smallest next step: tag each release and back up notes.db before
  every deploy.

## Verdict
Go / No-Go: No-Go. Rationale: No authentication or input limits, no
reproducible deployment and no runbook. Fine on a trusted laptop; not
for other people's data.
