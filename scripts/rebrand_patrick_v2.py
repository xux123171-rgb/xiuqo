"""V2 rebrand art: real XIUQO figlet wordmark + high-detail Patrick Star hero.

- CLI: replaces XIUQO_AGENT_LOGO (still spells HERMES — figlet art survived rename)
       and XIUQO_CADUCEUS (chunky low-res Patrick).
- TUI : replaces LOGO_ART / LOGO_GRADIENT and PATRICK_HERO in ui-tui/src/banner.ts.

Patrick is rendered with braille cells (2x4 dots per char) => 4x vertical detail,
with outline/body/highlight/eyes/mouth/green flowered shorts shading bands.
"""
import re, math
from pathlib import Path
import pyfiglet

ROOT = Path(__file__).resolve().parent.parent

# ---------------- 1. wordmark ----------------
WORD = pyfiglet.figlet_format("XIUQO AGENT", font="ansi_shadow").rstrip("\n")
word_lines = WORD.split("\n")

# gold ramp per line position (top bright -> bottom bronze), like the original
def ramp(i, n):
    bands = ["[bold #FFD700]", "[bold #FFD700]", "[#FFBF00]", "[#FFBF00]",
             "[#CD7F32]", "[#CD7F32]", "[#B8860B]"]
    return bands[min(len(bands) - 1, int(i / max(1, n - 1) * (len(bands) - 1) + 0.34))]

def rich_word(esc=lambda s: s):
    out = []
    for i, ln in enumerate(word_lines):
        if not ln.strip():
            out.append("")
        else:
            out.append(f"{ramp(i, len(word_lines))}{esc(ln)}[/]")
    return "\n".join(out)

CLI_LOGO = rich_word()
TUI_LOGO_LINES = word_lines

# ---------------- 2. Patrick sprite (pixel grid) ----------------
W_PX, H_PX = 40, 64            # braille cells: 20 wide x 16 tall art
BG, D, P, L, WW, K, M, G, g, F = ".", "D", "P", "L", "W", "K", "M", "G", "g", "f"

def in_poly(x, y, pts):
    inside = False
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xin:
                inside = not inside
    return inside

# rounded 5-point star silhouette (head cone, stubby arms, legs)
BODY = [(20, 2), (27, 20), (38, 27), (30, 36), (31, 52), (24, 61),
        (20, 55), (16, 61), (9, 52), (10, 36), (2, 27), (13, 20)]

def dist(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by)

def classify(x, y):
    if not in_poly(x, y, BODY):
        # 1px dilation pass handled by neighbor check later
        return BG
    # shorts band
    if 44 <= y <= 52 and 8 <= x <= 31:
        # flower dots
        for fx, fy in ((13, 47), (20, 49), (27, 46)):
            if dist(x, y, fx, fy) <= 1.35:
                return F
        if (x + y) % 7 == 0:
            return g
        return G
    # eyes
    for ex, mirror in ((14, 0), (26, 0)):
        if dist(x, y, ex, 26) <= 4.2:
            if dist(x, y, ex + 1, 27) <= 1.8:
                return K
            return WW
    # mouth: open smile
    if 33 <= y <= 38 and 14 <= x <= 26:
        d = dist(x, y, 20, 32)
        if d <= 7 and y >= 33 + abs(x - 20) * 0.25:
            if dist(x, y, 20, 36) <= 4.5 and y > 33.5:
                return M
            return D
    # highlight: left-lit body
    if x < 15 and y < 44 and in_poly(x - 2, y, BODY):
        return L
    return P

def render_px(x, y):
    c = classify(x, y)
    if c == BG:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= x + dx < W_PX and 0 <= y + dy < H_PX and classify(x + dx, y + dy) != BG:
                return D
    return c

grid = [[render_px(x, y) for x in range(W_PX)] for y in range(H_PX)]

BRAILLE_BITS = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]
def cell(cx, cy):
    """Return (glyph, dominant_class) for braille cell at (cx*2, cy*4)."""
    dots = 0
    counts = {}
    for i, (dx, dy) in enumerate(BRAILLE_BITS):
        v = grid[cy * 4 + dy][cx * 2 + dx]
        if v != BG:
            dots |= 1 << i
            counts[v] = counts.get(v, 0) + 1
    if not counts:
        return "\u2800", BG
    dom = max(counts, key=counts.get)
    return chr(0x2800 + dots), dom

COLOR = {D: "#B23A68", P: "#F784AC", L: "#FFAEC9", WW: "#FFFFFF",
         K: "#1E1E1E", M: "#8C2846", G: "#79C267", g: "#3E7A34", F: "#FF69B4"}

def art_rows():
    lines = []
    for cy in range(H_PX // 4):
        out, i, n = [], 0, W_PX // 2
        cells = [cell(cx, cy) for cx in range(n)]
        j = 0
        while j < n:
            ch = cells[j][1]
            k = j
            while k < n and cells[k][1] == ch:
                k += 1
            glyphs = "".join(cells[t][0] for t in range(j, k))
            if ch == BG:
                out.append(glyphs)
            else:
                out.append(f"[{COLOR[ch]}]{glyphs}[/]")
            j = k
        lines.append("".join(out))
    return lines

CLI_HERO = "\n".join(art_rows())

# plain (silhouette) version kept in sync for nothing in particular: skip.

# ---------------- 3. patch CLI banner.py ----------------
bp = ROOT / "xiuqo_cli/banner.py"
src = bp.read_text(encoding="utf-8")
src, n1 = re.subn(r'XIUQO_AGENT_LOGO = """.*?"""',
                  'XIUQO_AGENT_LOGO = """' + CLI_LOGO.replace("\\", "\\\\") + '"""',
                  src, count=1, flags=re.S)
src, n2 = re.subn(r'XIUQO_CADUCEUS = """.*?"""',
                  'XIUQO_CADUCEUS = """' + CLI_HERO + '"""',
                  src, count=1, flags=re.S)
assert n1 == 1 and n2 == 1, (n1, n2)
bp.write_text(src, encoding="utf-8")
print("CLI logo + hero replaced")

# ---------------- 4. patch TUI banner.ts ----------------
tp = ROOT / "ui-tui/src/banner.ts"
ts = tp.read_text(encoding="utf-8")

# strip any previous PATRICK_HERO const
ts = re.sub(r"const PATRICK_HERO = `.*?`\n", "", ts, flags=re.S)

js_logo = ",\n  ".join("'" + ln.replace("\\", "\\\\").replace("'", "\\'") + "'"
                       for ln in TUI_LOGO_LINES)
ts, m1 = re.subn(r"const LOGO_ART = \[.*?\]",
                 f"const LOGO_ART = [\n  {js_logo},\n]", ts, count=1, flags=re.S)
grad = [0, 0, 1, 1, 2, 2]
# map ramp bands onto gradient indexes for the theme palette (0 primary,1 accent,2 border)
gi = []
for i in range(len(word_lines)):
    if not word_lines[i].strip():
        gi.append(2)
    else:
        gi.append(min(2, i // 3))
ts, m2 = re.subn(r"const LOGO_GRADIENT = \[.*?\] as const",
                 "const LOGO_GRADIENT = [" + ", ".join(map(str, gi)) + "] as const",
                 ts, count=1, flags=re.S)
hero_const = "const PATRICK_HERO = `" + CLI_HERO.replace("`", "\\`") + "`\n"
ts = hero_const + ts
assert m1 == 1 and m2 == 1, (m1, m2)
# caduceus() already routes through parseRichMarkup(customHero || PATRICK_HERO)
tp.write_text(ts, encoding="utf-8")
print("TUI LOGO_ART + PATRICK_HERO replaced")

# ---------------- 5. logo width sanity ----------------
w = max(len(ln) for ln in TUI_LOGO_LINES)
print(f"wordmark lines={len(TUI_LOGO_LINES)} maxwidth={w}; hero rows={H_PX//4} cols={W_PX//2}")
