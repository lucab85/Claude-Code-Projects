# Chapter 7: Multimodal Development: From Wireframe to Working UI

This folder holds a one-page Flask dashboard built from a wireframe sketch.
The prompt let the image define the layout and used words for the stack,
the data, the port and the window size. A Playwright script takes identical
1280x720 screenshots, and a short visual diff loop found and fixed a footer
that was cut off at the bottom of the window. The folder also contains the
Word brief used to practise converting documents to Markdown with markitdown.

## Files

| File | What it is | Section |
| --- | --- | --- |
| `CLAUDE.md` | Folder rules: Flask only, plain CSS, Playwright for screenshots only | Setting up the ch07 folder |
| `app.py` | The Flask app with static sample data, on port 5001, localhost only | Reviewing what Claude generated |
| `templates/index.html` | The page, as a Jinja template | Reviewing what Claude generated |
| `static/styles.css` | All the styling, after the round 1 footer fix | Fixing the top gap |
| `round-1/styles.css` | The stylesheet as first generated, before the footer fix | Taking a screenshot with Playwright; Asking for a ranked gap list |
| `shot.py` | Saves a screenshot at a fixed window size and reports overflow | Taking a screenshot with Playwright |
| `wireframe-sketch.png` | The design you build from | Looking at the wireframe first |
| `wireframe.png` | The same dashboard rendered from Mermaid | Exercise 7.1 |
| `wireframe.mmd` | The Mermaid source of `wireframe.png` | Exercise 7.1 |
| `render-final.png` | The final screenshot, 1280x720 | Knowing when to stop |
| `diff-notes.md` | What each comparison round found, FIXED or KEPT | Recording the rounds in diff-notes.md |
| `brief.docx` | One-page product brief in Word format | Bringing documents into context with markitdown |
| `brief.md` | `brief.docx` converted with markitdown | Bringing documents into context with markitdown; Exercise 7.4 |
| `tests/test_dashboard.py` | Structural tests: 3 KPI cards, 5 rows, 5 links, footer | Exercise 7.3 |
| `exercises/ex7-2-media-query.css` | The phone-size media query to append to `static/styles.css` | Exercise 7.2 |

## Run

From the `claude-code-projects` workspace, with the Chapter 4 virtual
environment:

```bash
source ch04/.venv/bin/activate
pip install flask playwright
python3 -m playwright install chromium
cd ch07
python3 app.py                   # serves http://127.0.0.1:5001
```

In a second terminal, from `ch07`:

```bash
python3 shot.py http://localhost:5001 render.png
```

The final page prints only `saved render.png (1280x720)`. To reproduce the
first round of the visual diff loop, which reports a 737px-tall page, copy
`round-1/styles.css` over `static/styles.css` (Flask picks up the change on
the next page load).

## Test

```bash
python3 -m pytest -q ch07/tests  # from the workspace root: 4 passed
```

## Convert the brief

```bash
pip install 'markitdown[all]'
markitdown ch07/brief.docx > ch07/brief.md
```

The result is 774 bytes and should match the `brief.md` in this folder.
