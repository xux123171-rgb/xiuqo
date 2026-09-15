"""Build Patrick-Star banner + purge user-visible Hermes strings, then rebuild TUI.

Steps:
 1. patch apps/shared/src/json-rpc-channel.ts  (Hermes RPC failed -> Xiuqo)
 2. regenerate assets/banner.png as a Patrick Star pixel hero beside XIUQO-AGENT
 3. rebuild ui-tui dist
Run from repo root.
"""
import re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops

ROOT = Path(__file__).resolve().parent.parent

# ---------- 1. string fixes ----------
p = ROOT / "apps/shared/src/json-rpc-channel.ts"
s = p.read_text(encoding="utf-8")
if "Hermes RPC failed" in s:
    p.write_text(s.replace("Hermes RPC failed", "Xiuqo RPC failed"), encoding="utf-8")
    print("patched json-rpc-channel.ts")
else:
    print("json-rpc-channel.ts already clean")

# ---------- 2. Patrick Star banner ----------
# 16x16-ish classic Patrick (bottom-heavy starfish), hot-pink palette.
# legend: .=bg  P=pink fill  D=dark pink outline/cheek  W=white  B=black pupil
PAT = [
"...D........D....",
"..DPD......DPD...",
".DPPPDP..DPPPBD..",
".DPPPPPDPPPPPPBD.",
"DPPPPPPPPPPPPPPBD",
"DPPWWPPPPPPWWPPBD",
"DPPWBPPPPPPWBPPBD",
"DPPWWPPPPPPWWPPBD",
"DPPPPPPPPPPPPPPBD",
"DPPPPDDDDPPPPPPBD",
".DPPPPPPPPPPPPBD.",
".DPPPPPPPPPPPBD..",
"..DPPPPPPPPPBD...",
"...DPPPPPPPBD....",
"....DPPPPPBD.....",
".....DDBBBD......",
]
PINK = (247, 132, 172); DARK = (178, 58, 104)
WHITE = (245, 245, 245); BLACK = (30, 30, 30)
MOUTH = (140, 40, 70)

def render_patrick(scale=11, ox=0, oy=0, onto=None):
    w, h = len(PAT[0]) * scale, len(PAT) * scale
    im = Image.new("RGB", (w, h), (24, 24, 26))
    for r, row in enumerate(PAT):
        for c, ch in enumerate(row):
            col = {".": None, "D": DARK, "P": PINK, "B": DARK,
                   "W": WHITE, "p": PINK}.get(ch)
            if col is None: continue
            if ch == "p": col = PINK
            ImageDraw.Draw(im).rectangle(
                [c*scale, r*scale, c*scale+scale-2, r*scale+scale-2], fill=col)
    # mouth row tweak: the DDDD band -> mouth color
    ImageDraw.Draw(im).rectangle(
        [5*scale, 9*scale, 8*scale+scale-2, 9*scale+scale-2], fill=MOUTH)
    if onto is not None:
        onto.paste(im, (ox, oy))
    return im

# letters font: import only the glyph dict from scripts/build_banner.py
sys.path.insert(0, str(ROOT / "scripts"))
import importlib.util
_spec = importlib.util.spec_from_file_location("_bb_src", ROOT / "scripts/build_banner.py")
_bb = importlib.util.module_from_spec(_spec)
_code = _spec.loader.get_data(_spec.origin).decode("utf-8")
_code = _code.split("mask = word_mask")[0]          # keep defs only, skip rendering
exec(compile(_code, "build_banner_defs", "exec"), _bb.__dict__)
F = _bb.F | {' ': [".....",".....",".....",".....",".....",".....","....."]}
TEXT = "XIUQO AGENT"
S, W, H = 13, 1145, 196

def word_mask(text, s=S):
    wpx = len(text) * 5 * s + (len(text) - 1) * s
    m = Image.new("L", (wpx, 7 * s), 0)
    dd = ImageDraw.Draw(m)
    x = 0
    for ch in text:
        for r, row in enumerate(F[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    dd.rectangle([x + c*s, r*s, x + c*s + s - 2, r*s + s - 2], fill=255)
        x += 6 * s
    return m

img = Image.new("RGB", (W, H), (24, 24, 26))
# hero: patrick on the left
render_patrick(scale=11, ox=18, oy=(H - 16*11)//2, onto=img)
# text block shifted right of patrick
mask = word_mask(TEXT)
ox = 200
oy = (H - mask.height) // 2 - 4
bands = [(255, 214, 0), (255, 191, 0), (255, 158, 32), (208, 130, 48), (176, 106, 46)]
grad = Image.new("RGB", (1, H))
grad.putdata([bands[min(4, int(y / H * 5))] for y in range(H)])
grad = grad.resize((W, H))
inner = Image.new("L", (W, H), 0); inner.paste(mask, (ox, oy))
outline = Image.new("L", (W, H), 0)
for dx, dy in ((-3, -3), (4, 4)):
    sh = Image.new("L", (W, H), 0); sh.paste(mask, (ox + dx, oy + dy))
    outline = ImageChops.lighter(outline, sh)
frame = ImageChops.subtract(outline, inner)
img = Image.composite(Image.new("RGB", (W, H), (176, 106, 46)), img, frame)
img = Image.composite(grad, img, inner)
img.save(ROOT / "assets/banner.png")
print("banner regenerated with Patrick")

# ---------- 3. rebuild TUI ----------
r = subprocess.run(["npm", "run", "build"], cwd=ROOT / "ui-tui",
                   capture_output=True, text=True, timeout=300)
print("tui build:", "OK" if r.returncode == 0 else r.stderr[-300:])
if r.returncode == 0:
    d = (ROOT / "ui-tui/dist/entry.js").read_text(encoding="utf-8", errors="ignore")
    left = re.findall(r"Hermes[A-Za-z ]{2,20}", d)
    print("remaining Hermes-ish tokens in dist:", sorted(set(left))[:8] or "none visible")
