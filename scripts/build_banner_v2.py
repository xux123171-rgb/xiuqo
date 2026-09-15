"""Xiuqo banner v2: NOT a Hermes clone.

Design: deep ocean-blue gradient background, Patrick Star leaning at the left
(silhouette + pink), chunky rounded white wordmark "xiuqo" with a pink
starfish-amber underline stroke, tagline row in muted gray. Clean modern
look instead of retro gold figlet.
"""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from patrick_v3 import grid, W_PX, H_PX

ROOT = Path(__file__).resolve().parent.parent
W, H = 1145, 196
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# --- ocean gradient (deep blue -> slate) ---
top = (16, 24, 48)
bottom = (38, 52, 78)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))

# subtle diagonal light streak
for i in range(40):
    x0 = 380 + i * 12
    a = max(0, 26 - abs(i - 20))
    if a:
        d.line([(x0, H), (x0 + 90, 0)], fill=(70, 92, 130, ))

# --- patrick silhouette on left (pink blocks, scaled down) ---
S = 9
PX, PY = 34, (H - H_PX * S) // 2 + 4
COL = {".": None, "D": (214, 86, 140), "P": (247, 132, 172), "L": (255, 174, 201),
       "W": (250, 250, 252), "K": (24, 24, 32), "M": (190, 60, 100),
       "G": (110, 190, 120), "g": (80, 150, 90), "f": (255, 210, 90)}
for y in range(H_PX):
    for x in range(W_PX):
        c = COL.get(grid[y][x])
        if c:
            d.rectangle([PX + x*S, PY + y*S, PX + x*S + S - 1, PY + y*S + S - 1], fill=c)

# --- wordmark: rounded bold lowercase "xiuqo" using system font ---
def font(sz):
    for cand in ("arialbd.ttf", "segoeuib.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(cand, sz)
        except OSError:
            continue
    return ImageFont.load_default()

f_big = font(84)
f_small = font(21)

TXT_X = 470
tw = d.textlength("xiuqo", font=f_big)
d.text((TXT_X, 34), "xiuqo", font=f_big, fill=(248, 249, 252))
# pink underline swoosh under the word
d.rounded_rectangle([TXT_X + 4, 128, TXT_X + tw - 6, 137], radius=5, fill=(247, 132, 172))
# tagline
d.text((TXT_X + 6, 148), "the self-improving terminal agent", font=f_small,
       fill=(158, 172, 198))
# right side: tiny braille patrick echo + ☤ star
d.text((W - 120, 40), "MIT", font=f_small, fill=(120, 135, 160))
d.ellipse([W - 118 + 14, 92, W - 118 + 30, 108], outline=(247, 132, 172), width=3)
d.ellipse([W - 118 + 18, 96, W - 118 + 26, 104], fill=(247, 132, 172))

out = ROOT / "assets/banner.png"
img.save(out)
print("saved", img.size)
