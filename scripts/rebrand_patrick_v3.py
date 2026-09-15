"""V3 art: single-row XIUQO AGENT wordmark + proper starfish-silhouette Patrick."""
import re, math
from pathlib import Path
import pyfiglet

ROOT = Path(__file__).resolve().parent.parent

# ---------------- 1. one-row wordmark ----------------
def fig(text):
    lines = pyfiglet.figlet_format(text, font="ansi_shadow").rstrip("\n").split("\n")
    width = max(len(l) for l in lines)
    return [l.ljust(width) for l in lines]

a, b = fig("XIUQO"), fig("AGENT")
assert len(a) == len(b)
word_lines = [x + " " + y for x, y in zip(a, b)]          # side by side = one row
word_lines = [l.rstrip() for l in word_lines]
for l in word_lines:
    assert "█" not in l or l.strip(" ")

def rich_line(i):
    bands = ["[bold #FFD700]", "[bold #FFD700]", "[#FFBF00]",
             "[#FFBF00]", "[#CD7F32]", "[#CD7F32]"]
    return bands[min(5, i)]

CLI_LOGO = "\n".join(f"{rich_line(i)}{ln}[/]" for i, ln in enumerate(word_lines))

# ---------------- 2. Patrick v3 ----------------
W_PX, H_PX = 40, 64

def in_poly(x, y, pts):
    inside = False
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xin:
                inside = not inside
    return inside

# proper starfish: tall cone head, stubby arms with NOTCHES, slim waist, split legs
BODY = [
 (20, 1),            # head tip
 (24, 13),           # right cone edge
 (27, 20),           # right shoulder
 (37, 24),           # right arm top tip
 (39, 30),           # right arm bottom tip
 (29, 35),           # right armpit notch (concave)
 (27, 42),           # right waist
 (28, 52),           # right hip
 (26, 62),           # right leg outer
 (21, 62),           # right leg inner
 (20, 53),           # crotch (concave point)
 (19, 62),           # left leg inner
 (14, 62),           # left leg outer
 (12, 52),           # left hip
 (13, 42),           # left waist
 (11, 35),           # left armpit notch
 (1, 30),            # left arm bottom tip
 (3, 24),            # left arm top tip
 (13, 20),           # left shoulder
 (16, 13),           # left cone edge
]

def dist(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by)

BG, D, P, L, WW, K, M, G, g, F = ".", "D", "P", "L", "W", "K", "M", "G", "g", "f"

def classify(x, y):
    if not in_poly(x, y, BODY):
        return BG
    # green flowered shorts (hips/upper legs)
    if 44 <= y <= 56:
        for fx, fy in ((16, 48), (24, 50), (20, 45), (14, 53), (26, 45)):
            if dist(x, y, fx, fy) <= 1.2:
                return F
        if (x + y) % 6 == 0:
            return g
        return G
    # eyes (big, low-set like Patrick) with pupils
    for ex in (15, 25):
        d = dist(x, y, ex, 24)
        if d <= 4.6:
            if dist(x, y, ex + (1 if ex == 15 else -1), 25) <= 1.9:
                return K
            return WW
    # brows: two short dark strokes above eyes
    for bx, by in ((14, 19), (25, 19)):
        if abs(y - by) <= 0.6 and abs(x - bx) <= 3.2:
            return D
    # open smile below eyes
    if 30 <= y <= 36 and 14 <= x <= 26:
        if dist(x, y, 20, 29) <= 7.5 and y >= 30 + abs(x - 20) * 0.3:
            if dist(x, y, 20, 32) <= 4.2 and y >= 31:
                return M
            return D
    # left-lit highlight band
    if in_poly(x - 3, y, BODY) and not in_poly(x - 6, y, BODY) and y < 44:
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

BITS = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]
def cell(cx, cy):
    dots, counts = 0, {}
    for i, (dx, dy) in enumerate(BITS):
        v = grid[cy * 4 + dy][cx * 2 + dx]
        if v != BG:
            dots |= 1 << i
            counts[v] = counts.get(v, 0) + 1
    if not counts:
        return "\u2800", BG
    return chr(0x2800 + dots), max(counts, key=counts.get)

COLOR = {D: "#B23A68", P: "#F784AC", L: "#FFAEC9", WW: "#FFFFFF",
         K: "#1E1E1E", M: "#8C2846", G: "#79C267", g: "#4E9440", F: "#FF69B4"}

rows = []
for cy in range(H_PX // 4):
    cells = [cell(cx, cy) for cx in range(W_PX // 2)]
    out, j, n = [], 0, len(cells)
    while j < n:
        ch = cells[j][1]; k = j
        while k < n and cells[k][1] == ch:
            k += 1
        g = "".join(cells[t][0] for t in range(j, k))
        out.append(g if ch == BG else f"[{COLOR[ch]}]{g}[/]")
        j = k
    rows.append("".join(out))
CLI_HERO = "\n".join(rows)

# ---------------- 3. patch CLI ----------------
bp = ROOT / "xiuqo_cli/banner.py"
src = bp.read_text(encoding="utf-8")
src, n1 = re.subn(r'XIUQO_AGENT_LOGO = """.*?"""',
                  'XIUQO_AGENT_LOGO = """' + CLI_LOGO + '"""', src, count=1, flags=re.S)
src, n2 = re.subn(r'XIUQO_CADUCEUS = """.*?"""',
                  'XIUQO_CADUCEUS = """' + CLI_HERO + '"""', src, count=1, flags=re.S)
assert n1 == n2 == 1
bp.write_text(src, encoding="utf-8")
print("CLI patched: one-row logo + Patrick v3")

# ---------------- 4. patch TUI ----------------
tp = ROOT / "ui-tui/src/banner.ts"
ts = tp.read_text(encoding="utf-8")
ts = re.sub(r"const PATRICK_HERO = `.*?`\n", "", ts, flags=re.S)
js_logo = ",\n  ".join("'" + ln.replace("\\", "\\\\").replace("'", "\\'") + "'"
                       for ln in word_lines)
ts, m1 = re.subn(r"const LOGO_ART = \[.*?\]",
                 f"const LOGO_ART = [\n  {js_logo},\n]", ts, count=1, flags=re.S)
gi = [0, 0, 1, 1, 2, 2]
ts, m2 = re.subn(r"const LOGO_GRADIENT = \[.*?\] as const",
                 "const LOGO_GRADIENT = [" + ", ".join(map(str, gi)) + "] as const",
                 ts, count=1, flags=re.S)
assert m1 == m2 == 1
ts = "const PATRICK_HERO = `" + CLI_HERO.replace("`", "\\`") + "`\n" + ts
tp.write_text(ts, encoding="utf-8")
print("TUI patched")

# ---------------- 5. README banner ----------------
fpp = ROOT / "scripts/build_banner.py"
s = fpp.read_text(encoding="utf-8")
print("wordmark width:", max(len(l) for l in word_lines), "rows:", len(word_lines))
