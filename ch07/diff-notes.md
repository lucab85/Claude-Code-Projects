# Visual diff notes: ch07 dashboard

Design: wireframe-sketch.png. Window: 1280x720.

## Round 1 (render-1.png)
1. Footer cut off at the bottom edge. FIXED: body is a flex column and
   .layout uses flex: 1 instead of min-height: calc(100vh - 90px).
2. Sidebar is a full-height strip, not a framed panel. KEPT: cosmetic.
3. Table has four columns; the sketch shows label and value. KEPT: the
   extra columns are what we want.
4. "+ New Note" is a filled button; the sketch shows an outline. KEPT:
   cosmetic.

## Round 2 (render-final.png)
No layout gaps left. Header, sidebar with 5 links, 3 KPI cards, a 5-row
table and the footer are all visible. Stopped after 2 rounds.
