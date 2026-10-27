# Chapter 1: Getting Started with Claude Code and the AI Coding Loop

Project 1 sets up `claude-code-projects`, the Git repository that holds every
project in the book, and takes you once around the five-step loop (Plan,
Implement, Test, Review, Commit). The result is a `ch01` folder with a record
of your toolchain and the loop explained in your own words. The files here are
examples of what yours should look like. Don't copy them: your versions and
your wording will differ.

| File | What it is | Used in |
|---|---|---|
| `environment.txt` | Python, Git and Claude Code versions, one per line | Capturing your environment |
| `loop-notes.md` | The five-step loop in one paragraph, revised so that all three review rules pass | Reviewing and rewriting the answer; Checking your work and committing |

## How to check your own files

From the root of your workspace, regenerate the environment record and read
both files back:

```bash
{ python3 --version; git --version; claude --version; } > ch01/environment.txt
cat ch01/environment.txt ch01/loop-notes.md
```

Then run the review prompt from *Checking your work and committing* in Claude
Code and confirm that every rule reports PASS. Finally, check the commit:

```bash
git log --oneline
git show --stat HEAD
```
