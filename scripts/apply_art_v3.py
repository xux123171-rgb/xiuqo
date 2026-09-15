"""Apply v3 art: one-row XIUQO AGENT figlet + Patrick v3 braille, into CLI & TUI."""
import re, math
from pathlib import Path
import pyfiglet
import sys
sys.path.insert(0, str(Path(__file__).parent))
from patrick_v3 import grid, W_PX, H_PX

ROOT = Path(__file__).resolve().parent.parent

# ---- wordmark ----
def fig(text):
    lines = pyfiglet.figlet_format(text, font="ansi_shadow").rstrip("\n").split("\n")
    width = max(len(l) for l in lines)
    return [l.ljust(width) for l in lines]

a, b = fig("XIUQO"), fig("AGENT")
word_lines = [ (x + "  " + y).rstrip() for x, y in zip(a, b) ]

BANDS = ["[bold #FFD700]", "[bold #FFD700]", "[#FFBF00]", "[#FFBF00]", "[#CD7F32]", "[#CD7F32]"]
CLI_LOGO = "\n".join(f"{BANDS[min(5,i)]}{ln}[/]" for i, ln in enumerate(word_lines))

# ---- patrick -> braille rich ----
BITS = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3)]
COLOR = {"D":"#B23A68","P":"#F784AC","W":"#FFFFFF","K":"#1E1E1E",
         "M":"#8C2846","G":"#79C267","g":"#4E9440","f":"#FF69B4"}

def cell(cx, cy):
    dots, counts = 0, {}
    for i,(dx,dy) in enumerate(BITS):
        v = grid[cy*4+dy][cx*2+dx]
        if v != ".":
            dots |= 1 << i
            counts[v] = counts.get(v,0)+1
    if not counts:
        return "\u2800", "."
    # priority colors so small features aren't drowned by body pink
    order = ["K","W","M","f","g","G","D","P"]
    dom = next(c for c in order if c in counts)
    return chr(0x2800+dots), dom

rows = []
for cy in range(H_PX//4):
    cells = [cell(cx, cy) for cx in range(W_PX//2)]
    out, j, n = [], 0, len(cells)
    while j < n:
        ch = cells[j][1]; k = j
        while k < n and cells[k][1] == ch:
            k += 1
        g = "".join(cells[t][0] for t in range(j,k))
        out.append(g if ch == "." else f"[{COLOR[ch]}]{g}[/]")
        j = k
    rows.append("".join(out))
CLI_HERO = "\n".join(rows)

# ---- patch CLI ----
bp = ROOT/"xiuqo_cli/banner.py"
src = bp.read_text(encoding="utf-8")
src, n1 = re.subn(r'XIUQO_AGENT_LOGO = """.*?"""',
                  'XIUQO_AGENT_LOGO = """'+CLI_LOGO+'"""', src, count=1, flags=re.S)
src, n2 = re.subn(r'XIUQO_CADUCEUS = """.*?"""',
                  'XIUQO_CADUCEUS = """'+CLI_HERO+'"""', src, count=1, flags=re.S)
assert n1 == n2 == 1, (n1, n2)
bp.write_text(src, encoding="utf-8")
print("CLI patched")

# ---- patch TUI ----
tp = ROOT/"ui-tui/src/banner.ts"
ts = tp.read_text(encoding="utf-8")
ts = re.sub(r"const PATRICK_HERO = `.*?`\n", "", ts, flags=re.S)
js_logo = ",\n  ".join("'"+ln.replace("\\","\\\\").replace("'","\\'")+"'" for ln in word_lines)
ts, m1 = re.subn(r"const LOGO_ART = \[.*?\]",
                 f"const LOGO_ART = [\n  {js_logo},\n]", ts, count=1, flags=re.S)
gi = [min(2, i//3) for i in range(len(word_lines))]
ts, m2 = re.subn(r"const LOGO_GRADIENT = \[.*?\] as const",
                 "const LOGO_GRADIENT = ["+", ".join(map(str,gi))+"] as const", ts, count=1, flags=re.S)
assert m1 == m2 == 1, (m1, m2)
ts = "const PATRICK_HERO = `"+CLI_HERO.replace("`","\\`")+"`\n" + ts
tp.write_text(ts, encoding="utf-8")
print("TUI patched; logo single-row width:", max(len(l) for l in word_lines))
