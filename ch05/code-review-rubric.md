# Code review rubric for AI-generated code

- [ ] Boundaries: are empty, zero, negative and very large inputs handled
      and tested?
- [ ] Error paths: does every except do something useful (no silent pass)?
- [ ] Types: can None sneak through anywhere without an explicit check?
- [ ] Resources: is every file, connection and lock closed on every path?
- [ ] User input in queries: is it parameterized and, for LIKE, escaped?
- [ ] Spec formats: do bodies and status codes match the spec exactly?
- [ ] Tests: does at least one test fail if I break this change on purpose?

Pass only if every box is checked. One unchecked box means a targeted
fix prompt, not a merge.
