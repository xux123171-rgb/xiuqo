"""Patrick v3: union of primitives. Preview mode prints ASCII; final writes art."""
import math

W_PX, H_PX = 40, 64

def tri_head(x, y):  # cone: tip (20,2) -> base (7,31)-(33,31), slightly rounded
    if y < 2 or y > 31:
        return False
    t = (y - 2) / 29
    half = 2.0 + t * 14.0
    return abs(x - 20) <= half

def arm_l(x, y):
    return ((x - 7) / 7.0) ** 2 + ((y - 35) / 4.5) ** 2 <= 1

def arm_r(x, y):
    return ((x - 33) / 7.0) ** 2 + ((y - 35) / 4.5) ** 2 <= 1

def body(x, y):
    return 12 <= x <= 28 and 30 <= y <= 53

def leg_l(x, y):
    return 13 <= x <= 19 and 52 <= y <= 62

def leg_r(x, y):
    return 21 <= x <= 27 and 52 <= y <= 62

def in_star(x, y):
    return tri_head(x, y) or arm_l(x, y) or arm_r(x, y) or body(x, y) or leg_l(x, y) or leg_r(x, y)

def feat(x, y):
    # eyes
    for ex in (15, 25):
        if (x - ex) ** 2 + (y - 21) ** 2 <= 4.4 ** 2:
            return "K" if (x - ex - (-1 if ex == 15 else 1)) ** 2 + (y - 22) ** 2 <= 1.9 ** 2 else "W"
    # brows
    for bx in (15, 25):
        if abs(y - 16) <= 0.7 and abs(x - bx) <= 3.4:
            return "D"
    # open smile (lower half of an ellipse)
    if 25 <= y <= 31 and ((x - 20) / 6.0) ** 2 + ((y - 25) / 6.0) ** 2 <= 1:
        return "M"
    # shorts
    if 45 <= y <= 54 and 12 <= x <= 28:
        for fx, fy in ((16, 48), (24, 50), (20, 46), (14, 52), (26, 47)):
            if (x - fx) ** 2 + (y - fy) ** 2 <= 1.4 ** 2:
                return "f"
        if (x + y) % 6 == 0:
            return "g"
        return "G"
    return None

grid = []
for y in range(H_PX):
    row = []
    for x in range(W_PX):
        f = feat(x, y)
        if f:
            row.append(f)
        elif in_star(x, y):
            row.append("P")
        else:
            edge = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W_PX and 0 <= ny < H_PX and in_star(nx, ny):
                    edge = True
                    break
            row.append("D" if edge else ".")
    grid.append(row)

if __name__ == "__main__":
    mp = {".": " ", "D": "o", "P": "#", "W": "W", "K": "@",
          "M": "m", "G": "%", "g": "%", "f": "*"}
    for row in grid:
        print("".join(mp[c] for c in row))
