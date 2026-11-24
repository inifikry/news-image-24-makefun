#!/usr/bin/env python3
"""Draw the front page for Tuesday 24 November 2026 and write entry.png.

Pure Pillow, no network, deterministic: the same input always produces the
same bytes. Run: python3 draw_frontpage.py  (writes entry.png next to it)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1024, 1024
PAPER = (248, 245, 238)
INK = (17, 17, 17)
RED = (176, 42, 32)
NAVY = (20, 33, 61)
GREY = (110, 108, 100)
GREEN = (14, 42, 30)
GREEN_LINE = (46, 125, 91)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centre(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top red rule + masthead -------------------------------------
    d.rectangle([36, 24, 988, 28], fill=RED)
    centre(d, 40, "THE WORLD TODAY", font(SERIF_B, 84), INK)
    centre(d, 140, "TUESDAY,  24  NOVEMBER  2026", font(SANS_B, 30), RED)
    d.rectangle([36, 184, 988, 188], fill=INK)
    d.rectangle([36, 194, 988, 195], fill=INK)

    # ---- lead story ---------------------------------------------------
    d.text((36, 210), "KOREA  —  AIR DEFENCE SCARE", font=font(SANS_B, 23), fill=RED)
    d.text((36, 240), "RUSSIAN JETS SPARK", font=font(SERIF_B, 64), fill=INK)
    d.text((36, 308), "KOREA ALERT", font=font(SERIF_B, 64), fill=INK)

    sub = ("Seoul scrambles fighter jets after Russian warplanes enter "
           "the air-defence zone, and islanders on Ulleung are told "
           "to take shelter.")
    lines = wrap(d, sub, font(SANS, 24), 620)
    draw_lines(d, 36, 392, lines, font(SANS, 24), INK, 32)

    # radar panel: dark green scope, sweep, blips, jet silhouette
    px0, py0, px1, py1 = 700, 384, 988, 496
    d.rectangle([px0, py0, px1, py1], fill=GREEN, outline=INK, width=2)
    cx, cy = 844, 440
    for r in (52, 36, 20):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GREEN_LINE, width=2)
    d.line([cx - 52, cy, cx + 52, cy], fill=GREEN_LINE, width=2)
    d.line([cx, cy - 52, cx, cy + 52], fill=GREEN_LINE, width=2)
    d.polygon([(cx, cy), (cx + 46, cy - 26), (cx + 52, cy - 6)],
              fill=(120, 200, 160))
    for bx, by in ((806, 414), (872, 470), (824, 462)):
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 80, 60))
    # simple jet silhouette
    d.polygon([(900, 408), (962, 428), (900, 436), (916, 428)],
              fill=(240, 240, 230))
    d.polygon([(916, 420), (930, 408), (934, 420)], fill=(240, 240, 230))
    d.polygon([(916, 436), (930, 448), (934, 436)], fill=(240, 240, 230))

    d.rectangle([36, 516, 988, 517], fill=INK)

    # ---- middle: two columns ------------------------------------------
    # left column: Anchorage summit
    d.text((36, 534), "ALASKA  —  DIPLOMACY", font=font(SANS_B, 21), fill=RED)
    d.text((36, 562), "TRUMP, PUTIN MEET", font=font(SERIF_B, 36), fill=INK)
    d.text((36, 600), "IN ANCHORAGE", font=font(SERIF_B, 36), fill=INK)
    d.text((36, 638), "TODAY", font=font(SERIF_B, 36), fill=INK)
    body2 = ("High-stakes summit on the Ukraine war as the two leaders "
             "meet face to face.")
    lines = wrap(d, body2, font(SANS, 21), 464)
    draw_lines(d, 36, 690, lines, font(SANS, 21), INK, 27)

    # flags: USA (left) and Russia (right), 216 x 64 each
    fx, fy, fw, fh = 36, 748, 216, 64
    stripe = fh / 13.0
    for i in range(13):
        y0 = fy + i * stripe
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([fx, y0, fx + fw, y0 + stripe + 1], fill=col)
    d.rectangle([fx, fy, fx + 88, fy + 34], fill=(60, 59, 110))
    for sx in (14, 36, 58):
        for sy in (9, 24):
            d.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3, fy + sy + 3],
                      fill=(255, 255, 255))
    d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=1)
    centre_x = fx + fw / 2
    lw = d.textlength("UNITED STATES", font=font(SANS_B, 13))
    d.text((centre_x - lw / 2, fy + fh + 6), "UNITED STATES",
           font=font(SANS_B, 13), fill=GREY)

    rx = 284
    d.rectangle([rx, fy, rx + fw, fy + fh / 3], fill=(255, 255, 255))
    d.rectangle([rx, fy + fh / 3, rx + fw, fy + 2 * fh / 3], fill=(0, 57, 166))
    d.rectangle([rx, fy + 2 * fh / 3, rx + fw, fy + fh], fill=(213, 0, 50))
    d.rectangle([rx, fy, rx + fw, fy + fh], outline=INK, width=1)
    lw = d.textlength("RUSSIA", font=font(SANS_B, 13))
    d.text((rx + fw / 2 - lw / 2, fy + fh + 6), "RUSSIA",
           font=font(SANS_B, 13), fill=GREY)

    # right column: Thanksgiving travel, then Indonesia factory fire
    d.text((524, 534), "USA  —  THANKSGIVING", font=font(SANS_B, 21), fill=RED)
    d.text((524, 562), "STORMS THREATEN", font=font(SERIF_B, 36), fill=INK)
    d.text((524, 600), "HOLIDAY GETAWAY", font=font(SERIF_B, 36), fill=INK)
    body3 = ("Storms and airline glitches threaten a messy Thanksgiving "
             "week for travellers.")
    lines = wrap(d, body3, font(SANS, 21), 464)
    draw_lines(d, 524, 650, lines, font(SANS, 21), INK, 27)

    d.rectangle([524, 716, 988, 717], fill=GREY)
    d.text((524, 730), "INDONESIA  —  DISASTER", font=font(SANS_B, 21), fill=RED)
    d.text((524, 758), "24 CONFIRMED DEAD", font=font(SERIF_B, 32), fill=INK)
    d.text((524, 792), "IN FACTORY FIRE", font=font(SERIF_B, 32), fill=INK)
    body4 = ("Families await DNA tests after the Cikande candy plant "
             "blaze; dozens still missing.")
    lines = wrap(d, body4, font(SANS, 19), 464)
    draw_lines(d, 524, 830, lines, font(SANS, 19), INK, 24)

    # ---- ALSO TODAY strip ----------------------------------------------
    d.rectangle([36, 890, 988, 992], fill=NAVY)
    d.text((56, 904), "ALSO TODAY", font=font(SANS_B, 22), fill=(255, 255, 255))
    items = [
        ("UN chief: agree AI risk rules within a year",
         "Nepal PM in Delhi for energy, trade talks"),
        ("Ibaraki holds first nuclear-waste briefing",
         "Thai court upholds verdict for opposition MP"),
    ]
    y = 936
    for left, right in items:
        for x, text in ((56, left), (524, right)):
            d.rectangle([x, y + 5, x + 10, y + 15], fill=RED)
            d.text((x + 20, y), text, font=font(SANS, 19),
                   fill=(235, 235, 235))
        y += 30

    # ---- footer ---------------------------------------------------------
    centre(d, 1002, "THE WORLD TODAY  •  TUESDAY, 24 NOVEMBER 2026",
           font(SANS, 15), GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
