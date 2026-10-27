# Claude Code Projects

Code repository for *Claude Code Projects* by Luca Berton, published by Packt.

Each chapter of the book is a hands-on project. This repository has one folder per chapter with every script, prompt, test and sample file the chapter uses, plus the reference solutions to compare your own work against.

## How to use this repository

You build your own work in a separate folder, `~/claude-code-projects`, as *Chapter 1* explains. Clone this repository next to it and use it as a reference:

```bash
cd ~
git clone https://github.com/lucab85/Claude-Code-Projects.git
```

When a chapter tells you to copy a file from the book's code repository, copy it from the matching `chNN` folder. Try each project yourself first, and open the reference solution only when you've finished, especially in `ch12`.

## Chapters

| Folder | Chapter |
|---|---|
| [`ch01`](ch01) | 1. Getting Started with Claude Code and the AI Coding Loop |
| [`ch02`](ch02) | 2. Prompting Like a Tech Lead with GCOE |
| [`ch03`](ch03) | 3. Giving Claude Project Context with CLAUDE.md |
| [`ch04`](ch04) | 4. Building Faster with Best-of-N |
| [`ch05`](ch05) | 5. Testing, Debugging and Self-Review of AI-Generated Code |
| [`ch06`](ch06) | 6. Safe Git Workflows for AI-Assisted Development |
| [`ch07`](ch07) | 7. Multimodal Development: From Wireframe to Working UI |
| [`ch08`](ch08) | 8. Constrained Refactoring and Documentation from the Diff |
| [`ch09`](ch09) | 9. Packaging Your Workflows as Reusable Skills |
| [`ch10`](ch10) | 10. Extending Claude Code with Hooks, MCP and Multi-Agent Workflows |
| [`ch11`](ch11) | 11. Production Readiness Reviews for AI-Built Software |
| [`ch12`](ch12) | 12. From Workshop to Workplace: Habits, Anti-Patterns and a Capstone Project |
| [`skills`](skills) | The companion library of twelve reusable skills (*Chapter 9* onward) |

## Requirements

- Claude Code 2.1 or later, with a Claude Pro, Max, Team or Enterprise subscription or a Claude Console account
- Git 2.30 or later
- Python 3.11 or later
- A Bash shell: your usual terminal on macOS and Linux, WSL or Git Bash on Windows
- Chapter-specific packages, listed in each chapter's README

Results from AI tools vary between runs and versions. Where a chapter shows sample output, yours will differ in the details; the scripts and tests in this repository are what to check against.

## License

The code in this repository is released under the [MIT License](LICENSE). The skills library carries its own MIT license in [`skills/LICENSE`](skills/LICENSE).
