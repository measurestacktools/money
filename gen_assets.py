#!/usr/bin/env python3
"""Generate MeasureStack brand assets (no external tools/fonts-CDN).
Run: python gen_assets.py — outputs to assets/img/."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(IMG, exist_ok=True)

BLUE = (15, 95, 208)
INK = (13, 27, 46)
AMBER = (255, 191, 71)
WHITE = (255, 255, 255)
MUTED = (188, 208, 238)

ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="MeasureStack logo">
<rect x="2" y="2" width="60" height="60" rx="14" fill="#0f5fd0"/>
<rect x="16" y="16" width="32" height="7" rx="3.5" fill="#ffffff"/>
<rect x="20" y="28" width="24" height="7" rx="3.5" fill="#ffffff" opacity="0.92"/>
<rect x="24" y="40" width="16" height="7" rx="3.5" fill="#ffbf47"/>
</svg>
"""

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 64" role="img" aria-label="MeasureStack logo">
<rect x="2" y="2" width="60" height="60" rx="14" fill="#0f5fd0"/>
<rect x="18" y="18" width="32" height="7" rx="3.5" fill="#ffffff"/>
<rect x="22" y="30" width="24" height="7" rx="3.5" fill="#ffffff" opacity="0.92"/>
<rect x="26" y="42" width="16" height="7" rx="3.5" fill="#ffbf47"/>
<text x="74" y="42" font-family="system-ui, -apple-system, 'Segoe UI', Arial, sans-serif" font-size="30" font-weight="800" fill="#1a2230">MeasureStack</text>
</svg>
"""

def write(name, text):
    p = os.path.join(IMG, name)
    open(p, "w", encoding="utf-8", newline="\n").write(text)
    print("wrote", name, os.path.getsize(p), "bytes")

write("icon.svg", ICON_SVG)
write("favicon.svg", ICON_SVG)
write("logo.svg", LOGO_SVG)

def draw_icon(dr, s):
    """Draw the icon motif on a PIL canvas of size s (square)."""
    u = s / 64.0
    dr.rounded_rectangle([2 * u, 2 * u, 62 * u, 62 * u], radius=14 * u, fill=BLUE)
    dr.rounded_rectangle([16 * u, 16 * u, 48 * u, 23 * u], radius=3.5 * u, fill=WHITE)
    dr.rounded_rectangle([20 * u, 28 * u, 44 * u, 35 * u], radius=3.5 * u, fill=WHITE)
    dr.rounded_rectangle([24 * u, 40 * u, 40 * u, 47 * u], radius=3.5 * u, fill=AMBER)

def icon_png(size):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_icon(ImageDraw.Draw(im), size)
    return im

# Favicon PNGs + ICO
icon_png(180).convert("RGB").save(os.path.join(IMG, "apple-touch-icon.png"))
icon_png(192).convert("RGB").save(os.path.join(IMG, "icon-192.png"))
icon_png(512).convert("RGB").save(os.path.join(IMG, "icon-512.png"))
master = icon_png(256).convert("RGB")
master.save(os.path.join(IMG, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote favicon.ico / apple-touch-icon.png / icon-192.png / icon-512.png")

# OG image 1200x630
W, H = 1200, 630
og = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(og)
ARIAL = r"C:\Windows\Fonts\arial.ttf"
ARIALB = r"C:\Windows\Fonts\arialbd.ttf"
# text block (kept left of the icon: x 120..820)
def fit(text, path, start, maxw):
    size = start
    while size > 20 and ImageFont.truetype(path, size).getlength(text) > maxw:
        size -= 2
    return ImageFont.truetype(path, size)
f_title = fit("MeasureStack", ARIALB, 100, 690)
f_sub = fit("Construction Material Calculators", ARIAL, 48, 690)
f_line = fit("Concrete  •  Lumber  •  Tile  •  Roofing", ARIAL, 40, 690)
# left amber ruler strip with tick marks
d.rectangle([0, 0, 64, H], fill=AMBER)
for i, y in enumerate(range(30, H - 20, 44)):
    w = 40 if i % 2 == 0 else 26
    d.rectangle([0, y, w, y + 7], fill=INK)
# text block
d.text((120, 190), "MeasureStack", font=f_title, fill=WHITE)
d.text((124, 330), "Construction Material Calculators", font=f_sub, fill=MUTED)
d.text((124, 410), "Concrete  •  Lumber  •  Tile  •  Roofing", font=f_line, fill=MUTED)
# icon motif, right side (clear of text)
isc = 260
ox, oy = W - isc - 70, (H - isc) // 2
d.rounded_rectangle([ox, oy, ox + isc, oy + isc], radius=70, fill=BLUE)
d.rounded_rectangle([ox + 75, oy + 75, ox + 225, oy + 108], radius=16, fill=WHITE)
d.rounded_rectangle([ox + 94, oy + 131, ox + 206, oy + 164], radius=16, fill=WHITE)
d.rounded_rectangle([ox + 112, oy + 187, ox + 188, oy + 220], radius=16, fill=AMBER)
og.save(os.path.join(IMG, "og-image.png"))
print("wrote og-image.png", os.path.getsize(os.path.join(IMG, "og-image.png")), "bytes")
