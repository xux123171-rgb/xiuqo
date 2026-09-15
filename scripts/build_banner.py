"""Retro pixel banner: XIUQO-AGENT — gradient fill + offset neon frame, dark bg."""
from PIL import Image, ImageDraw, ImageChops

F = {
 'X':["1...1","1...1",".1.1.","..1..",".1.1.","1...1","1...1"],
 'I':["11111","..1..","..1..","..1..","..1..","..1..","11111"],
 'U':["1...1","1...1","1...1","1...1","1...1","1...1",".111."],
 'Q':[".111.","1...1","1...1","1...1","1...1","1...1","..1.1"],
 'O':[".111.","1...1","1...1","1...1","1...1","1...1",".111."],
 'A':["..1..",".1.1.","1...1","11111","1...1","1...1","1...1"],
 'G':[".111.","1...1","1....","1.111","1...1","1...1",".111."],
 'E':["11111","1....","1....","1111.","1....","1....","11111"],
 'N':["1...1","11..1","1.1.1","1..11","1...1","1...1","1...1"],
 'T':["11111","..1..","..1..","..1..","..1..","..1..","..1.."],
 'R':["1111.","1...1","1...1","1111.","1.1..","1..1.","1..11"],
 'M':["1...1","11.11","1.1.1","1.1.1","1...1","1...1","1...1"],
 ' ':[".....",".....",".....",".....",".....",".....","....."],
 '-':[".....",".....",".....","11111",".....",".....","....."],
}
TEXT, S, W, H = "XIUQO-AGENT", 15, 1145, 196

def word_mask(text):
    wpx = len(text) * 5 * S + (len(text) - 1) * S
    m = Image.new("L", (wpx, 7 * S), 0)
    dd = ImageDraw.Draw(m)
    x = 0
    for ch in text:
        for r, row in enumerate(F[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    dd.rectangle([x + c*S, r*S, x + c*S + S - 2, r*S + S - 2], fill=255)
        x += 6 * S
    return m

mask = word_mask(TEXT)
img = Image.new("RGB", (W, H), (24, 24, 26))

bands = [(255, 214, 0), (255, 191, 0), (255, 158, 32), (208, 130, 48), (176, 106, 46)]
grad = Image.new("RGB", (1, H))
grad.putdata([bands[min(4, int(y / H * 5))] for y in range(H)])
grad = grad.resize((W, H))

ox = (W - mask.width) // 2
oy = (H - mask.height) // 2 - 4

inner = Image.new("L", (W, H), 0)
inner.paste(mask, (ox, oy))

outline = Image.new("L", (W, H), 0)
for dx, dy in ((-3, -3), (4, 4)):
    shifted = Image.new("L", (W, H), 0)
    shifted.paste(mask, (ox + dx, oy + dy))
    outline = ImageChops.lighter(outline, shifted)
frame = ImageChops.subtract(outline, inner)

brown = Image.new("RGB", (W, H), (176, 106, 46))
img = Image.composite(brown, img, frame)
img = Image.composite(grad, img, inner)

img.save("D:/projects/xiuqo/assets/banner.png")
print("saved 1145x196")
