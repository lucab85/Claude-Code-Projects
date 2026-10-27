---
name: visual-diff
description: Compare a design image with a screenshot and rank the gaps.
argument-hint: "[design.png] [render.png]"
arguments: design render
disable-model-invocation: true
---

# Visual diff

Image 1: $design (the design).
Image 2: $render (the current render).

List the gaps in priority order. For each gap:
- One-sentence description.
- The smallest patch that closes it.
Layout and missing content first; ignore fonts and sample data.
Stop after 5 items. Don't change any files.
