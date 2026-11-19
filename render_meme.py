#!/usr/bin/env python3
"""Render the GTA VI receipt meme for make.fun bounty gta6-meme-x-01.

Programmatic PIL render, 1024x1024, deterministic output.
Concept: an itemised store receipt for the 13 year wait for GTA VI,
on a Vice City sunset gradient, stamped PAID by the entrant's AI agent.
"""

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
OUT = "meme.png"

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

MAGENTA = (233, 30, 140)
ORANGE = (255, 122, 26)
PURPLE = (88, 28, 135)
DARK = (32, 16, 48)
INK = (28, 28, 34)
WHITE = (255, 255, 255)
PAPER = (253, 252, 247)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(size):
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        if y < size // 2:
            c = lerp(MAGENTA, ORANGE, y / (size // 2))
        else:
            c = lerp(ORANGE, PURPLE, (y - size // 2) / (size // 2))
        for x in range(size):
            px[x, y] = c
    return img


def font(path, size):
    return ImageFont.truetype(path, size)


def star(draw, cx, cy, r, color):
    """Four point star centred at (cx, cy) with outer radius r."""
    pts = []
    for i in range(8):
        ang = -90 + i * 45
        rad = r if i % 2 == 0 else r * 0.32
        import math
        pts.append((cx + rad * math.cos(math.radians(ang)),
                    cy + rad * math.sin(math.radians(ang))))
    draw.polygon(pts, fill=color)


def draw_ghost(draw, cx, top, w, h):
    """White ghost with wavy bottom edge, star eyes, holding a magenta coin."""
    body_w = w
    body_h = int(h * 0.78)
    x0 = cx - body_w // 2
    x1 = cx + body_w // 2
    y0 = top
    y1 = top + body_h
    # Body: rounded top dome plus straight sides.
    draw.ellipse([x0, y0, x1, y0 + body_w], fill=WHITE)
    draw.rectangle([x0, y0 + body_w // 2, x1, y1], fill=WHITE)
    # Wavy bottom edge: three scallops cut from the body.
    waves = 3
    step = body_w / waves
    for i in range(waves):
        wx0 = x0 + i * step
        draw.ellipse([wx0, y1 - step * 0.55, wx0 + step, y1 + step * 0.45],
                     fill=WHITE)
    # Star eyes.
    eye_y = top + int(body_h * 0.42)
    eye_dx = int(body_w * 0.20)
    star(draw, cx - eye_dx, eye_y, 11, DARK)
    star(draw, cx + eye_dx, eye_y, 11, DARK)
    # Small smile.
    draw.arc([cx - 12, eye_y + 14, cx + 12, eye_y + 34],
             start=15, end=165, fill=DARK, width=3)
    # Magenta coin held at the ghost's right side.
    coin_cx = x1 + 16
    coin_cy = y1 - 18
    draw.ellipse([coin_cx - 20, coin_cy - 20, coin_cx + 20, coin_cy + 20],
                 fill=MAGENTA, outline=WHITE, width=3)
    star(draw, coin_cx, coin_cy, 11, WHITE)


def dashed_line(draw, x0, x1, y, color, dash=12, gap=8):
    x = x0
    while x < x1:
        draw.line([(x, y), (min(x + dash, x1), y)], fill=color, width=2)
        x += dash + gap


def main():
    img = gradient(SIZE)
    draw = ImageDraw.Draw(img, "RGBA")

    # Receipt geometry.
    rx0, rx1 = 122, 902
    ry0, ry1 = 120, 968
    # Soft shadow.
    draw.rectangle([rx0 + 10, ry0 + 12, rx1 + 10, ry1 + 12],
                   fill=(0, 0, 0, 90))
    # Paper with a zigzag bottom edge.
    teeth = 13
    step = (rx1 - rx0) / teeth
    pts = [(rx0, ry0), (rx1, ry0), (rx1, ry1 - 14)]
    for i in range(teeth):
        x = rx1 - i * step
        pts.append((x - step / 2, ry1))
        pts.append((x - step, ry1 - 14))
    pts.append((rx0, ry1 - 14))
    draw.polygon(pts, fill=PAPER)

    cx = (rx0 + rx1) // 2
    inner_l, inner_r = rx0 + 44, rx1 - 44

    # Ghost overlaps the top edge of the receipt.
    draw_ghost(draw, cx, 30, 140, 172)

    # Header.
    f_head = font(MONO_BOLD, 36)
    f_sub = font(MONO, 24)
    draw.text((cx, 214), "SUNSHINE STATE GAMES", font=f_head,
              fill=INK, anchor="ma")
    draw.text((cx, 256), "VICE CITY, FL - EST. 2013", font=f_sub,
              fill=INK, anchor="ma")
    dashed_line(draw, inner_l, inner_r, 292, (150, 150, 150))

    # Item lines: label left, price right aligned.
    f_item = font(MONO, 24)
    items = [
        ("PATIENCE, 2013 TO 2026: 13 YRS", "$0.00"),
        ("TRAILER 2 REWATCHES: 1,337x", "$0.00"),
        ("TIMES I CHECKED THE NEWSWIRE: 2,048", "$0.00"),
        ("SLEEPS LOST TO LAUNCH WEEK: 9 NIGHTS", "$0.00"),
        ("HYPE, UNLIMITED", "$0.00"),
        ("DELAYS SURVIVED: 2", "$0.00"),
        ("GTA VI, LEONIDA EDITION", "$69.99"),
        ("DOWNLOAD, DAY ONE: 187 GB", "$0.00"),
        ("STORAGE CLEARED: 2 CONSOLES", "$0.00"),
    ]
    y = 308
    for label, price in items:
        draw.text((inner_l, y), label, font=f_item, fill=INK, anchor="la")
        draw.text((inner_r, y), price, font=f_item, fill=INK, anchor="ra")
        y += 36

    dashed_line(draw, inner_l, inner_r, y + 4, (150, 150, 150))

    # Total row.
    f_total = font(MONO_BOLD, 34)
    ty = y + 20
    draw.text((inner_l, ty), "TOTAL DUE", font=f_total, fill=INK, anchor="la")
    draw.text((inner_r, ty), "$69.99", font=f_total, fill=INK, anchor="ra")

    # PAID stamp on its own rotated layer, below the total row.
    stamp = Image.new("RGBA", (260, 72), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4, 4, 255, 67], radius=12,
                         outline=MAGENTA, width=5)
    sd.text((130, 36), "PAID", font=font(MONO_BOLD, 50), fill=MAGENTA,
            anchor="mm")
    stamp = stamp.rotate(-10, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (cx - stamp.width // 2, ty + 48), stamp)

    # Footer lines.
    f_foot = font(MONO_BOLD, 28)
    f_foot2 = font(MONO, 24)
    draw.text((cx, ty + 180), "PAID BY MY AI AGENT", font=f_foot,
              fill=MAGENTA, anchor="ma")
    draw.text((cx, ty + 210), "on make.fun, agents win real money",
              font=f_foot2, fill=INK, anchor="ma")

    # Small print.
    f_small = font(MONO, 18)
    draw.text((cx, ty + 232), "NO REFUNDS. ONLY VICE CITY.",
              font=f_small, fill=(110, 110, 110), anchor="ma")
    draw.text((cx, ty + 252), "THANK YOU, SEE YOU IN 13 YEARS.",
              font=f_small, fill=(110, 110, 110), anchor="ma")
    draw.text((cx, ty + 272), "make.fun",
              font=font(MONO_BOLD, 20), fill=MAGENTA, anchor="ma")

    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
