"""Render an 8-slide carousel HTML (sections #s1..#s8, 1080x1350) to slide1..8.jpg.
Usage: python3 render.py <slides.html> <out_dir>
The HTML must reference logo files by relative path, so put it in toolkit/ or copy logos next to it."""
import sys, os
from playwright.sync_api import sync_playwright
from PIL import Image
src, out = os.path.abspath(sys.argv[1]), sys.argv[2]
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350})
    pg.goto("file://"+src); pg.wait_for_timeout(400)
    n = pg.locator("section.s").count()
    for i in range(1, n+1):
        png = f"{out}/slide{i}.png"
        pg.locator(f"#s{i}").screenshot(path=png)
        Image.open(png).convert("RGB").save(f"{out}/slide{i}.jpg", quality=82, optimize=True)
        os.remove(png)
    b.close()
print("rendered", n, "slides to", out)
