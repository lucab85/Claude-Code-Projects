# Decisions behind the reference solution

The brief leaves these questions open. Your answers can differ; what
matters is that you decided them before any code existed and wrote them
into PROMPT.md. These are the choices the reference made, and why.

| Question | Reference choice | Why |
|---|---|---|
| Is the tag required? | Yes. A bookmark without a tag can't be found by the only search the brief asks for. | The brief says "with a title and a tag". |
| Several tags per bookmark? | No, exactly one. | "a tag", singular. Several tags need a second table or a list column, which is a bigger design than the brief asks for. |
| What is a valid tag? | One word with no spaces, 1 to 50 characters. | Spaces in a tag make `?tag=` URLs awkward and invite near-duplicates such as `my tag` and `my  tag`. |
| Exact or partial filter? | Exact. | The contract says "exactly this tag", and partial matching on short tags (`py` matching `pyramid`) surprises people. |
| Case-sensitive? | Yes: `?tag=Misc` doesn't match `misc`. | Simplest rule to state and test, and it matches what was stored. Folding case can be added later without breaking anyone; removing it can't. |
| Empty `?tag=` | Matches nothing (returns `[]`). | No bookmark has an empty tag, so an exact match on it is empty. Treating it as "no filter" was a review finding (REVIEW.md, finding 2). |
| Which URLs are valid? | Absolute `http` or `https` URLs with a host, at most 2,048 characters, no whitespace. The scheme is case-insensitive. | A `javascript:` link runs script when a client renders it as a link; `data:`, `ftp://`, `mailto:` and relative paths aren't web pages to bookmark. 2,048 is a common practical limit for URLs. |
| Normalize URLs? | No. Stored exactly as sent. | Normalizing (adding a trailing slash, lowercasing the host) changes what the user saved and makes duplicates harder to reason about. |
| Duplicate URLs? | Allowed. | With one tag per bookmark, saving the same page under two tags needs two rows. A duplicate check is easy to add later if users ask. |
| Update route? | None. | Not in the brief. Exercise 12.1 adds `PATCH /bookmarks/{id}` with the full loop. |
| Title rules | Required, not blank, at most 200 characters. | The same limit the Notes API got in Exercise 11.3. The boundary test pins it. |
| 404 body | Exactly `{"error": "not found"}`. | The same contract as the Notes API, so clients and smoke tests work the same way. |
| Delete response | 204 with an empty body. | The contract and the smoke test expect 204. |
| List order and paging | Oldest first (by id); no paging yet. | Predictable for tests. Paging was deferred in review (REVIEW.md, finding 3). |
| Authentication | None. | Not in the brief; recorded as the blocker in READINESS.md. |
