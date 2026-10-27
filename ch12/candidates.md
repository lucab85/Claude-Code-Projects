# Candidates

Both candidates implement the same PROMPT.md. Each ran on its own port
against a fresh database and was checked with smoke.sh, then with a few
extra curl requests for the step 1 decisions in DECISIONS.md. Only the
winner is kept in this folder.

Candidate: a
Correctness (0-3): 3. Every smoke line passes. Blank titles, ftp:// and
                   javascript: URLs get 422; ?tag=Misc doesn't match misc;
                   the URL comes back exactly as sent.
Simplicity  (0-3): 2. One readable file, but three validators and two
                   helpers make it more than twice as long as B
                   (156 lines against 64).
Fit         (0-3): 3. Follows CLAUDE.md and PROMPT.md: DB_PATH, closed
                   connections, 404 body {"error":"not found"}, id order.
Total: 8 / 9
Notes: the URL check is a prefix test, startswith("http://", "https://").
       Looked fine at scoring time; see REVIEW.md, finding 1.

Candidate: b
Correctness (0-3): 1. Every smoke line passes, but a title of "   " and a
                   tag of " " are accepted with 201, ?tag=misc also
                   returns a bookmark tagged Misc (COLLATE NOCASE), and
                   https://example.com is stored as https://example.com/.
Simplicity  (0-3): 3. 64 lines; very easy to read.
Fit         (0-3): 1. 404 body is {"detail":{"error":"not found"}};
                   the database path is a bare string, so tests can't
                   point it at a scratch file; connections are never
                   closed; uses the deprecated @app.on_event("startup");
                   lists have no ORDER BY.
Total: 5 / 9

| Criterion (0 to 3) | Candidate A | Candidate B |
|---|---|---|
| Correctness | 3: every smoke line and every decision check passes | 1: blank title and tag accepted, case-insensitive tag filter, URL rewritten |
| Simplicity | 2: readable, but longer | 3: short and clear |
| Fit | 3: follows CLAUDE.md and PROMPT.md | 1: wrapped 404, no DB_PATH, unclosed connections, deprecated startup hook |
| Total | 8 / 9 | 5 / 9 |

Winner: Candidate A (8/9 vs 5/9). Both pass smoke.sh, which only checks
status codes, so the decisions from step 1 separated them: B accepts a
blank title, matches tags case-insensitively and changes the URL the user
saved, and its 404 body breaks the shared contract. B is shorter, but
fixing it would mean rewriting most of it.

Lesson: a green smoke test didn't separate the candidates. The extra
checks came straight from DECISIONS.md, which is why the decisions belong
in the prompt before any code exists.
