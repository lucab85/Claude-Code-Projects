#!/usr/bin/env python3
"""Dashboard page built from the Chapter 7 wireframe."""
from flask import Flask, render_template

app = Flask(__name__)

KPIS = [
    {"label": "Total notes", "value": 128},
    {"label": "Open tasks", "value": 42},
    {"label": "Avg cycle", "value": "7d"},
]

ROWS = [
    {"id": 1, "title": "Spec drafted", "owner": "lb", "status": "open"},
    {"id": 2, "title": "API skeleton", "owner": "lb", "status": "open"},
    {"id": 3, "title": "Tests scaffolded", "owner": "ay", "status": "done"},
    {"id": 4, "title": "PR description", "owner": "lb", "status": "done"},
    {"id": 5, "title": "Readiness review", "owner": "ay", "status": "open"},
]


@app.route("/")
def index():
    """Render the dashboard with the static sample data."""
    return render_template("index.html", kpis=KPIS, rows=ROWS,
                           version="1.0.0")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
