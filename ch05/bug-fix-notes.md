# Bug fix notes: ch05 Notes API

Two bugs were planted on purpose to prove the test suite works. Two more
were real bugs in the Chapter 4 winner, found by the stranger's-PR review.

## Bug 1: search requires both title and body to match
Symptom: GET /notes?q=milk returns nothing for a note whose body says
         "buy milk" (test_search_matches_body_only fails).
Cause: the query uses AND between the two LIKE clauses.
Diagnosis: the review ranked it High: a note must contain q in both its
           title and its body, so any search that only hits one field
           returns nothing.
Fix: change AND back to OR. Both search tests pass again.

## Bug 2: PATCH on an unknown id returns 500 instead of 404
Symptom: PATCH /notes/999 crashes with TypeError: 'NoneType' object is not
         subscriptable (test_patch_missing_is_404 fails).
Cause: update_note runs a plain SELECT, which returns None for an unknown
       id, and then reads row["title"].
Diagnosis: the review ranked it High: row is None, so row["title"] raises
           TypeError and the client gets a 500. Use _fetch_one, which
           raises the 404.
Fix: call _fetch_one(conn, note_id) again. test_patch_missing_is_404 passes.

## Bug 3: search treats % and _ as wildcards
Symptom: GET /notes?q=% returns every note instead of only notes that
         contain a percent sign.
Cause: q goes into the LIKE pattern without escaping, so % matches any
       text and _ matches any single character.
Diagnosis: the review ranked it Medium: q=% returns every note, and on a
           public API it lets a caller make the database do expensive work.
           No test covered it, so the whole suite passed.
Fix: test first (test_search_treats_wildcards_literally failed: 1 failed,
     12 passed). Then added _like_pattern(), which escapes \, % and _,
     and ESCAPE '\' on both LIKE clauses. 13 passed.

## Bug 4: database connections are never closed
Symptom: python3 -m pytest -q -W default::ResourceWarning on Python 3.13
         shows ResourceWarning: unclosed database after every run.
Cause: get_db() returned a plain connection used in `with` blocks, but
       sqlite3's context manager only commits or rolls back; it never
       closes.
Diagnosis: the review ranked it Medium: every request leaks one
           connection, so a busy server slowly runs out of resources.
Fix: get_db() is now a @contextmanager that commits or rolls back and
     closes the connection in a finally block. Call sites are unchanged.
     13 passed, no warnings.

## Not fixed
- No maximum length for title or body (review item 5, Low). A product
  decision, not a bug. Noted for the spec.
