"""Save a screenshot of a web page at a fixed window size."""
import argparse

from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("url", help="page to open, e.g. http://localhost:5001")
parser.add_argument("out", help="PNG file to write, e.g. render-1.png")
parser.add_argument("--width", type=int, default=1280)
parser.add_argument("--height", type=int, default=720)
args = parser.parse_args()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": args.width, "height": args.height})
    page.goto(args.url, wait_until="networkidle")
    page.screenshot(path=args.out)
    w, h = page.evaluate(
        "[document.documentElement.scrollWidth,"
        " document.documentElement.scrollHeight]")
    browser.close()

print(f"saved {args.out} ({args.width}x{args.height})")
if w > args.width:
    print(f"warning: the page is {w}px wide, so it scrolls sideways")
if h > args.height:
    print(f"note: the page is {h}px tall; anything below "
          f"{args.height}px is off-screen")
