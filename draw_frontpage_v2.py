#!/usr/bin/env python3
"""Draw the v2 front page for news-image-20261124: THE WORLD TODAY,
Tuesday 24 November 2026. 34 stories, drawn purely with Pillow.
Deterministic: no network, no randomness, no timestamps.
Stdlib + Pillow only. Run: python3 draw_frontpage_v2.py -> entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 231)
INK = (22, 22, 22)
RED = (172, 28, 28)
NAVY = (16, 36, 64)
NAVY2 = (24, 52, 88)
GOLD = (201, 162, 39)
GREEN = (32, 110, 58)
GREY = (96, 96, 96)
LGREY = (210, 205, 192)
DARK = (30, 30, 30)
WHITE = (250, 248, 242)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, f, width, fill, leading=None):
    if leading is None:
        leading = int(f.size * 1.28)
    for ln in wrap(d, text, f, width):
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def fit_lines(d, text, f, width, max_lines):
    """Wrap text, truncating to max_lines with an ellipsis if needed."""
    lines = wrap(d, text, f, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and d.textlength(lines[-1] + "\u2026", font=f) > width:
        lines[-1] = lines[-1][:-1]
    lines[-1] = lines[-1] + "\u2026"
    return lines


def draw_fitted(d, x, y, text, f, width, fill, max_lines, leading=None):
    if leading is None:
        leading = int(f.size * 1.28)
    for ln in fit_lines(d, text, f, width, max_lines):
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def badge(d, x, y, text, f, fg=WHITE, bg=RED, pad=4):
    w = int(d.textlength(text, font=f)) + pad * 2
    h = f.size + pad
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.text((x + pad, y + pad // 2), text, font=f, fill=fg)
    return w


def badge_right(d, x_right, y, text, f, fg=WHITE, bg=RED, pad=4):
    w = int(d.textlength(text, font=f)) + pad * 2
    return badge(d, x_right - w, y, text, f, fg, bg, pad)


# ---------------------------------------------------------------- stories
# certainty: C = confirmed (official source or 2+ outlets named)
#            S = stated (one party's claim, not checked)
#            U = unverified (unconfirmed, or attacker unknown)
LEADS = [
    dict(
        n=1, tag="KOREA \u00b7 AIR DEFENCE SCARE", cert="C",
        cert_text="CONFIRMED",
        head="Russian jets spark Korea alert",
        body=("Seoul scrambles jets after Russian planes enter the "
              "air-defence zone; Ulleung's shelter warning sounds at "
              "07:52, then lifts."),
        why=("Why it matters: the civil-defence warning was rare, and "
             "Moscow does not recognise the zone."),
        src="Reuters \u00b7 AP \u00b7 Yonhap",
        badge="ADIZ ALERT", scene="radar",
        place="SEOUL",
    ),
    dict(
        n=2, tag="ASIA \u00b7 MARKETS", cert="C",
        cert_text="CONFIRMED",
        head="Chip stocks soar across Asia",
        body=("A day after Nvidia brought Huang back, Asia's chip shares "
              "surge: TSMC +9.9%, Foxconn +10%, MediaTek +9.9%."),
        why=("Why it matters: the AI-trade rout reverses, and the rally "
             "spreads from Wall Street to Asia."),
        src="Reuters \u00b7 WSJ",
        badge="+9.9%", scene="chart",
        place="TAIPEI",
    ),
    dict(
        n=3, tag="GAZA \u00b7 WAR", cert="C",
        cert_text="CONFIRMED",
        head="Israeli strike kills three in Khan Younis",
        body=("An Israeli airstrike kills at least three Palestinians near "
              "a police outpost in Khan Younis, southern Gaza, on Tuesday, "
              "medics say."),
        why=("Why it matters: strikes go on despite the October 2025 "
             "truce; 1,600 Palestinians have been killed since."),
        src="Reuters",
        badge="3 KILLED", scene="gaza",
        place="KHAN YOUNIS",
    ),
]

CARDS = [
    dict(n=4, tag="USA \u00b7 WEATHER", cert="C",
         head="Thanksgiving storm; SF braces for tides",
         body=("Gulf storm builds; SF Bay flood warning, tides 2.8 ft "
               "over normal."),
         src="CNN \u00b7 NWS", badge="KING TIDES", scene="storm",
         place="SAN FRANCISCO"),
    dict(n=5, tag="BRAZIL \u00b7 POLITICS", cert="C",
         head="Lower house passes Lula's fiscal plan",
         body=("Brazil's lower house approves the main text of Lula's "
               "fiscal plan."),
         src="Reuters", badge="FISCAL PLAN", scene="brazil",
         place="BRASILIA"),
    dict(n=6, tag="TRADE \u00b7 TECH", cert="C",
         head="US blacklists Alibaba unit; firm to fight",
         body=("Alibaba's Singapore unit Apex blacklisted; firm denies "
               "diverting chips."),
         src="Reuters", badge="BLACKLIST", scene="alibaba",
         place="SINGAPORE"),
    dict(n=7, tag="SINGAPORE \u00b7 AI", cert="C",
         head="No one country decides AI rules, says Wong",
         body=("PM Wong: no country alone decides AI rules."),
         src="PMO wires", badge="AI RULES", scene="singapore",
         place="SINGAPORE"),
    dict(n=8, tag="UKRAINE \u00b7 WAR", cert="C",
         head="Nightly barrage goes on; Dymer toll 11",
         body=("Strikes go on overnight; Dymer toll hits 11 as rescuers "
               "dig on."),
         src="Reuters \u00b7 Al Jazeera", badge="11 DEAD", scene="ukraine",
         place="DYMER"),
    dict(n=9, tag="THAILAND \u00b7 POLITICS", cert="C",
         head="Court frees MP Ice on bail",
         body=("MP Ice freed on bail after her term is overturned."),
         src="Bangkok wires", badge="BAIL", scene="thailand",
         place="BANGKOK"),
    dict(n=10, tag="GERMANY \u00b7 POLITICS", cert="C",
         head="Bundestag passes emergency-care reform",
         body=("Parliament passes emergency-care reform for crowded ERs."),
         src="Bundestag wires", badge="REFORM", scene="germany",
         place="BERLIN"),
    dict(n=11, tag="ENGLAND \u00b7 CLIMATE", cert="C",
         head="Drought declared across 82% of England",
         body=("Drought now covers 82% of England after a hot summer."),
         src="Environment Agency", badge="82%", scene="drought",
         place="LONDON"),
    dict(n=12, tag="EUROPE \u00b7 UK", cert="S",
         head="EU shuts door on UK reset talks",
         body=("No UK talks until London decides on reversing Brexit, "
               "diplomats say."),
         src="The Guardian", badge="NO TALKS", scene="eu",
         place="BRUSSELS"),
    dict(n=13, tag="SPACE \u00b7 CHINA", cert="C",
         head="Shenzhou-23 astronaut stays a year in orbit",
         body=("Zhu Yangzhu will stay aboard the station for a year."),
         src="Xinhua wires", badge="1 YEAR", scene="space",
         place="JIUQUAN"),
    dict(n=14, tag="SPORT \u00b7 FOOTBALL", cert="C",
         head="Champions League: nine ties tonight",
         body=("Arsenal host Dortmund and Real Madrid face PSV among nine "
               "ties tonight."),
         src="UEFA", badge="9 TIES", scene="ucl",
         place="LONDON"),
    dict(n=15, tag="PACIFIC \u00b7 CLIMATE", cert="C",
         head="Vanuatu treaty dies over climate clauses",
         body=("Coalition kills Vanuatu treaty over climate clauses; "
               "Fiji shuts schools."),
         src="PINA", badge="TREATY DEAD", scene="pacific",
         place="PORT VILA"),
]

# briefs: (number, place, text, source) — each must fit ONE line
BRIEFS = [
    (16, "Beijing", "PBoC injects \u00a5516bn in overnight repos", "PBoC"),
    (17, "New Delhi", "India may import 2m tonnes of sugar",
     "Hindu BusinessLine"),
    (18, "New Delhi", "Pilots question DGCA action on SpiceJet",
     "Hindu BusinessLine"),
    (19, "Mumbai", "Bisleri: bromate tests within limits",
     "Hindu BusinessLine"),
    (20, "Bangkok", "Protesters march 16 km to refinery",
     "Bangkok wires"),
    (21, "Bangkok", "Anti-graft session turns chaotic",
     "Bangkok wires"),
    (22, "Berlin", "SPD, Greens, Left resume talks", "Berlin wires"),
    (23, "Berlin", "Intel agencies set for wider powers", "Berlin wires"),
    (24, "Berlin", "Merz announces electricity-tax cut", "Berlin wires"),
    (25, "Accra", "Steinmeier arrives for Ghana visit", "Accra wires"),
    (26, "Berlin", "Two held over Starlink station fire", "Police"),
    (27, "Berlin", "IMF lifts German growth forecast to 1.3%", "IMF"),
    (28, "Bayelsa", "Boat toll rises to 29", "NEMA"),
    (29, "Sydney", "UNSW unveils megafire simulator iFire", "UNSW"),
    (30, "Sydney", "Councils warn Minns over poker machines", "NSW wires"),
    (31, "Sydney", "Young locked in for switch to PNG Chiefs",
     "Rugby league wires"),
    (32, "Los Angeles", "Actor Stacy Keach dies at 85", "Wires"),
    (33, "Wellington", "Ashwin: India should be angry", "CricToday"),
    (34, "New York", "Amgen up at CICC; Zscaler cut", "Wires"),
]

NUMBERS = [
    ("3 MIN", "Ulleung alert lasted"),
    ("+9.9%", "TSMC shares jump"),
    ("\u00a5516BN", "PBoC injection"),
    ("11", "dead in Dymer"),
    ("82%", "of England in drought"),
    ("29", "dead in Bayelsa boat"),
    ("9", "UCL ties tonight"),
]

DATE_CHECK = [
    "COP31 ends with no deal \u2014 Sun 22 Nov, Antalya",
    "Nvidia reinstates Jensen Huang \u2014 Mon 23 Nov",
    "Cikande toll confirmed, 24 dead \u2014 Mon 23 Nov",
    "Guterres calls for AI rules \u2014 Mon 23 Nov",
    "Nepal PM Shah meets Modi \u2014 Mon 23 Nov, Delhi",
    "Wellington Test ends in a draw \u2014 Mon 23 Nov",
]

DONT_KNOW = [
    "Korea: how close did the jets get to Ulleung?",
    "Gaza: details of the Khan Younis strike pending.",
    "Chips: will the rally hold when US markets open?",
    "Football: tonight's UCL scores \u2014 after this edition.",
]

SOURCES_LINE = ("Sources: Reuters \u00b7 AP \u00b7 Yonhap \u00b7 AFP \u00b7 WSJ \u00b7 "
                "The Guardian \u00b7 UEFA \u00b7 PINA \u00b7 NWS \u00b7 CNN \u00b7 "
                "Xinhua \u00b7 PBoC \u00b7 IMF \u00b7 UNSW \u00b7 NEMA")


# ---------------------------------------------------------------- scenes
def scene_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 26, 48))
    cx, cy = x + w * 0.30, y + h * 0.55
    for r in (52, 38, 24):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 160, 110))
    d.line([cx, cy, cx + 44, cy - 26], fill=(90, 220, 140), width=2)
    for px, py in [(cx - 20, cy + 12), (cx + 16, cy - 6), (cx + 30, cy + 18)]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 70, 60))
    # jet silhouette
    jx, jy = x + w * 0.72, y + h * 0.34
    d.polygon([(jx, jy - 12), (jx + 26, jy + 4), (jx, jy + 6),
               (jx - 8, jy + 2)], fill=(220, 220, 220))
    d.text((x + 8, y + h - 16), "KADIZ", font=F(SANS_B, 11), fill=(140, 200, 160))


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 32, 24))
    base = y + h - 14
    bars = [14, 20, 16, 26, 22, 34, 30, 44, 40, 56]
    bw = w / len(bars)
    for i, v in enumerate(bars):
        bx = x + i * bw + 2
        d.rectangle([bx, base - v, bx + bw - 4, base], fill=(46, 190, 90))
    d.line([x + 6, base - 56, x + w - 6, base - 66], fill=(255, 210, 80),
           width=2)
    d.text((x + 8, y + 6), "TSMC +9.9%", font=F(SANS_B, 12),
           fill=(255, 210, 80))


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 22, 34))
    # skyline
    for bx, bw, bh in [(0, 26, 34), (30, 20, 52), (54, 30, 40), (88, 22, 58),
                       (114, 26, 44), (144, 30, 30), (178, 24, 48)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(52, 48, 66))
        for wy in range(y + h - bh + 6, y + h - 4, 10):
            for wx in range(x + bx + 4, x + bx + bw - 4, 9):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 200, 90))
    # smoke plume
    sx = x + w * 0.62
    for i, r in enumerate((16, 22, 28, 34)):
        d.ellipse([sx - r, y + 8 + i * 12 - r * 0.4, sx + r,
                   y + 8 + i * 12 + r * 0.4], fill=(120, 112, 104))
    d.ellipse([sx - 8, y + h - 78, sx + 8, y + h - 62], fill=(255, 120, 40))


def scene_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 30, 52))
    # rain
    for i in range(14):
        rx = x + 10 + i * 14
        d.line([rx, y + 8, rx - 6, y + 34], fill=(150, 190, 230), width=2)
    # wave
    for i in range(3):
        wy = y + h - 22 - i * 12
        d.arc([x + 6, wy - 8, x + w - 6, wy + 14], 180, 360,
              fill=(120, 200, 240), width=3)
    d.text((x + 8, y + h - 16), "2.8 FT ABOVE NORMAL", font=F(SANS_B, 11),
           fill=(180, 220, 250))


def scene_brazil(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 90, 44))
    # congress twin towers + dome
    d.rectangle([x + w * 0.18, y + h * 0.25, x + w * 0.30, y + h * 0.85],
                fill=(240, 240, 230))
    d.rectangle([x + w * 0.34, y + h * 0.25, x + w * 0.46, y + h * 0.85],
                fill=(240, 240, 230))
    d.pieslice([x + w * 0.52, y + h * 0.55, x + w * 0.72, y + h * 0.95],
               180, 360, fill=(240, 240, 230))
    d.pieslice([x + w * 0.76, y + h * 0.68, x + w * 0.92, y + h * 0.95],
               180, 360, fill=(240, 240, 230))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(255, 210, 60))


def scene_alibaba(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 16, 16))
    cx, cy = x + w // 2, y + h // 2
    d.rectangle([cx - 34, cy - 26, cx + 34, cy + 26], fill=(30, 30, 30),
                outline=(255, 210, 80), width=2)
    for i in range(-2, 3):
        d.rectangle([cx - 44, cy + i * 10 - 2, cx - 34, cy + i * 10 + 2],
                    fill=(255, 210, 80))
        d.rectangle([cx + 34, cy + i * 10 - 2, cx + 44, cy + i * 10 + 2],
                    fill=(255, 210, 80))
    d.text((cx - 24, cy - 9), "APEX", font=F(SANS_B, 13), fill=(255, 210, 80))


def scene_singapore(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 44, 84))
    for bx, bw, bh in [(0, 22, 44), (26, 18, 62), (48, 24, 50), (76, 20, 70),
                       (100, 22, 56), (126, 26, 40), (156, 22, 60)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                    fill=(180, 200, 230))
    d.ellipse([x + w - 34, y + 8, x + w - 8, y + 34], fill=(255, 210, 80))
    d.text((x + 8, y + 6), "AI", font=F(SANS_B, 15), fill=(255, 255, 255))


def scene_ukraine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 20, 40))
    # apartment block
    d.rectangle([x + w * 0.30, y + h * 0.30, x + w * 0.66, y + h],
                fill=(70, 64, 80))
    for r in range(3):
        for c in range(3):
            wx = x + w * 0.30 + 6 + c * 22
            wy = y + h * 0.30 + 8 + r * 20
            d.rectangle([wx, wy, wx + 12, wy + 10],
                        fill=(255, 190, 80) if (r, c) != (1, 1)
                        else (40, 36, 50))
    d.polygon([(x + w * 0.66, y + h * 0.30), (x + w * 0.80, y + h * 0.55),
               (x + w * 0.66, y + h * 0.80)], fill=(60, 54, 70))
    # fire glow + drone dots
    d.ellipse([x + w * 0.70, y + h - 34, x + w * 0.86, y + h - 8],
              fill=(255, 110, 30))
    for px, py in [(0.12, 0.2), (0.85, 0.16), (0.2, 0.42)]:
        d.ellipse([x + w * px - 2, y + h * py - 2, x + w * px + 2,
                   y + h * py + 2], fill=(255, 80, 60))


def scene_thailand(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 16, 44))
    # temple roofline
    d.polygon([(x + 6, y + h * 0.55), (x + w // 2, y + h * 0.25),
               (x + w - 6, y + h * 0.55)], fill=(255, 210, 90))
    d.rectangle([x + w * 0.30, y + h * 0.55, x + w * 0.70, y + h * 0.92],
                fill=(240, 230, 210))
    # scales
    cx, cy = x + w * 0.82, y + h * 0.68
    d.line([cx, cy - 22, cx, cy + 12], fill=(255, 255, 255), width=2)
    d.line([cx - 14, cy - 20, cx + 14, cy - 20], fill=(255, 255, 255), width=2)
    d.polygon([(cx - 18, cy - 12), (cx - 10, cy - 12), (cx - 14, cy - 2)],
              fill=(255, 210, 90))
    d.polygon([(cx + 10, cy - 12), (cx + 18, cy - 12), (cx + 14, cy - 2)],
              fill=(255, 210, 90))


def scene_germany(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 20))
    # Reichstag dome
    d.rectangle([x + w * 0.14, y + h * 0.62, x + w * 0.86, y + h * 0.92],
                fill=(200, 195, 180))
    d.pieslice([x + w * 0.36, y + h * 0.28, x + w * 0.64, y + h * 0.72],
               180, 360, fill=(200, 195, 180))
    d.rectangle([x + w * 0.485, y + h * 0.14, x + w * 0.515, y + h * 0.30],
                fill=(200, 195, 180))
    # red cross (medical)
    cx, cy = x + w * 0.82, y + h * 0.30
    d.rectangle([cx - 4, cy - 12, cx + 4, cy + 12], fill=(220, 40, 40))
    d.rectangle([cx - 12, cy - 4, cx + 12, cy + 4], fill=(220, 40, 40))


def scene_drought(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 132, 52))
    d.ellipse([x + w - 46, y + 8, x + w - 14, y + 40], fill=(255, 220, 120))
    # cracked earth
    for (x1, y1, x2, y2) in [(0.1, 0.55, 0.35, 0.75), (0.35, 0.75, 0.30, 0.95),
                             (0.35, 0.75, 0.62, 0.88), (0.62, 0.88, 0.85, 0.78),
                             (0.62, 0.88, 0.70, 1.0), (0.55, 0.5, 0.62, 0.88)]:
        d.line([x + w * x1, y + h * y1, x + w * x2, y + h * y2],
               fill=(120, 70, 20), width=2)


def scene_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 44, 110))
    cx, cy = x + w * 0.34, y + h * 0.52
    import math
    for i in range(12):
        a = math.pi * 2 * i / 12 - math.pi / 2
        sx, sy = cx + 30 * math.cos(a), cy + 30 * math.sin(a)
        d.polygon([(sx, sy - 5), (sx + 2, sy - 1), (sx + 5, sy), (sx + 2, sy + 1),
                   (sx, sy + 5), (sx - 2, sy + 1), (sx - 5, sy), (sx - 2, sy - 1)],
                  fill=(255, 210, 60))
    # door, ajar
    dx = x + w * 0.68
    d.rectangle([dx, y + h * 0.25, dx + 34, y + h * 0.92], fill=(240, 240, 230))
    d.polygon([(dx + 34, y + h * 0.25), (dx + 52, y + h * 0.32),
               (dx + 52, y + h * 0.85), (dx + 34, y + h * 0.92)],
              fill=(150, 150, 150))


def scene_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(4, 6, 18))
    for px, py in [(0.1, 0.2), (0.25, 0.12), (0.7, 0.18), (0.85, 0.3),
                   (0.4, 0.3), (0.92, 0.1)]:
        d.ellipse([x + w * px - 1, y + h * py - 1, x + w * px + 1,
                   y + h * py + 1], fill=(255, 255, 255))
    # earth arc
    d.pieslice([x + w * 0.05, y + h * 0.62, x + w * 0.95, y + h * 1.5],
               180, 360, fill=(40, 110, 190))
    d.pieslice([x + w * 0.05, y + h * 0.62, x + w * 0.95, y + h * 1.5],
               180, 360, outline=(120, 200, 255))
    # station
    sx, sy = x + w * 0.52, y + h * 0.34
    d.rectangle([sx - 26, sy - 4, sx + 26, sy + 4], fill=(200, 200, 200))
    d.rectangle([sx - 6, sy - 8, sx + 6, sy + 8], fill=(220, 220, 220))
    d.line([sx - 26, sy, sx + 26, sy], fill=(120, 120, 120), width=1)


def scene_ucl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 90, 40))
    for i in range(5):
        yy = y + i * (h // 5)
        d.line([x, yy, x + w, yy], fill=(30, 120, 60), width=1)
    d.ellipse([x + w * 0.5 - 12, y + h * 0.42, x + w * 0.5 + 12,
               y + h * 0.42 + 24], fill=(255, 255, 255),
              outline=(20, 20, 20), width=2)
    d.polygon([(x + w * 0.5 - 4, y + h * 0.42 + 8),
               (x + w * 0.5 + 4, y + h * 0.42 + 8),
               (x + w * 0.5, y + h * 0.42 + 16)], fill=(20, 20, 20))
    d.text((x + 8, y + 6), "MATCHDAY 5", font=F(SANS_B, 11),
           fill=(255, 255, 255))


def scene_pacific(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 80, 110))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(232, 214, 160))
    # palm
    px, py = x + w * 0.24, y + h * 0.72
    d.line([px, py, px + 6, py - 34], fill=(90, 60, 30), width=4)
    for dx, dy in [(-22, -30), (22, -32), (-14, -40), (16, -42)]:
        d.line([px + 6, py - 34, px + 6 + dx, py - 34 + dy],
               fill=(40, 140, 70), width=3)
    # treaty paper
    d.rectangle([x + w * 0.58, y + h * 0.30, x + w * 0.90, y + h * 0.82],
                fill=(250, 248, 240))
    for i in range(4):
        d.line([x + w * 0.62, y + h * 0.38 + i * 10,
                x + w * 0.86, y + h * 0.38 + i * 10], fill=(120, 120, 120),
               width=1)
    d.line([x + w * 0.58, y + h * 0.30, x + w * 0.90, y + h * 0.82],
           fill=(200, 40, 40), width=3)


SCENES = {
    "radar": scene_radar, "chart": scene_chart, "gaza": scene_gaza,
    "storm": scene_storm, "brazil": scene_brazil, "alibaba": scene_alibaba,
    "singapore": scene_singapore, "ukraine": scene_ukraine,
    "thailand": scene_thailand, "germany": scene_germany,
    "drought": scene_drought, "eu": scene_eu, "space": scene_space,
    "ucl": scene_ucl, "pacific": scene_pacific,
}


class _NoTextDraw:
    """Draw proxy that swallows text calls (for small card scenes)."""
    def __init__(self, d):
        self._d = d

    def __getattr__(self, name):
        return getattr(self._d, name)

    def text(self, *a, **k):
        pass


def draw_scene(img, d, kind, x, y, w, h, small=False):
    if small:
        # draw on a temp layer so anything outside the panel is clipped
        layer = Image.new("RGB", (w, h), (0, 0, 0))
        ld = ImageDraw.Draw(layer)
        SCENES[kind](_NoTextDraw(ld), 0, 0, w, h)
        img.paste(layer, (x, y))
        return
    SCENES[kind](d, x, y, w, h)


# ---------------------------------------------------------------- layout
def draw_frontpage():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 14                      # margin
    CW = W - 2 * M              # content width

    # ---- masthead ----
    y = 10
    f_top = F(SANS_B, 12)
    d.text((M, y), "THE WORLD TODAY \u00b7 CLOSING EDITION", font=f_top,
           fill=INK)
    rt = "34 STORIES \u00b7 8 REGIONS \u00b7 9 TOPICS"
    d.text((W - M - d.textlength(rt, font=f_top), y), rt, font=f_top,
           fill=INK)
    y += 18
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 6
    f_title = F(SERIF_B, 50)
    d.text((M, y), "THE WORLD TODAY", font=f_title, fill=INK)
    y += 58
    f_date = F(SANS_B, 20)
    d.text((M, y), "TUESDAY, 24 NOVEMBER 2026", font=f_date, fill=RED)
    f_note = F(SANS, 11)
    nt = "ALL STORIES DATED 24 NOV IN THEIR LOCAL TIME ZONE"
    d.text((W - M - d.textlength(nt, font=f_note), y + 7), nt,
           font=f_note, fill=GREY)
    y += 30
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 5
    # ticker
    f_tick = F(SANS_B, 12)
    tick = ("KOREA ALERT \u00b7 CHIP STOCKS SOAR \u00b7 GAZA STRIKE KILLS "
            "THREE \u00b7 THANKSGIVING STORM BUILDS \u00b7 BRAZIL PASSES "
            "FISCAL PLAN")
    d.text((M, y), tick, font=f_tick, fill=NAVY)
    y += 20
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 5
    # coverage strips
    f_cov = F(SANS, 11)
    d.text((M, y), "COVERAGE \u2014  East Asia 5 \u00b7 South East Asia 4 "
           "\u00b7 South Asia 3 \u00b7 Europe 10 \u00b7 Middle East 1 "
           "\u00b7 Africa 2 \u00b7 Americas 4 \u00b7 Pacific 5",
           font=f_cov, fill=INK)
    y += 14
    d.text((M, y), "TOPICS \u2014  Conflict 3 \u00b7 Politics 12 "
           "\u00b7 Economy 8 \u00b7 Disaster 3 \u00b7 Sport 3 "
           "\u00b7 Science 2 \u00b7 Culture 1 \u00b7 Society 1 "
           "\u00b7 Crime 1", font=f_cov, fill=INK)
    y += 16
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 4
    # ---- big numbers strip ----
    strip_h = 42
    d.rectangle([M, y, W - M, y + strip_h], fill=NAVY)
    cell = CW / len(NUMBERS)
    f_num = F(SANS_B, 20)
    f_lab = F(SANS, 9)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + cell * i + cell / 2
        nw = d.textlength(num, font=f_num)
        d.text((cx - nw / 2, y + 3), num, font=f_num, fill=GOLD)
        lw = d.textlength(lab, font=f_lab)
        d.text((cx - lw / 2, y + 26), lab, font=f_lab, fill=WHITE)
        if i:
            d.line([M + cell * i, y + 6, M + cell * i, y + strip_h - 6],
                   fill=(70, 90, 130), width=1)
    y += strip_h + 4

    # ---- leads ----
    lead_w = (CW - 2 * 10) // 3
    lead_h = 262
    lead_y = y
    f_ltag = F(SANS_B, 11)
    f_lhead = F(SERIF_B, 19)
    f_lbody = F(SANS, 12)
    f_lwhy = F(SANS, 11)
    f_lsrc = F(SANS, 10)
    for i, s in enumerate(LEADS):
        lx = M + i * (lead_w + 10)
        d.rectangle([lx, lead_y, lx + lead_w, lead_y + lead_h],
                    outline=INK, width=1)
        # illustration
        draw_scene(img, d, s["scene"], lx + 1, lead_y + 1, lead_w - 2, 100)
        # red badge over illustration, top right
        badge_right(d, lx + lead_w - 8, lead_y + 8, s["badge"],
                    F(SANS_B, 11))
        iy = lead_y + 106
        d.text((lx + 8, iy), s["tag"], font=f_ltag, fill=RED)
        iy += 15
        iy = draw_fitted(d, lx + 8, iy, s["head"], f_lhead, lead_w - 16,
                         INK, 2, leading=21)
        iy += 2
        iy = draw_fitted(d, lx + 8, iy, s["body"], f_lbody, lead_w - 16,
                         INK, 3, leading=15)
        iy += 4
        iy = draw_fitted(d, lx + 8, iy, s["why"], f_lwhy, lead_w - 16,
                         (60, 60, 60), 2, leading=14)
        d.text((lx + 8, lead_y + lead_h - 16),
               s["src"] + "  \u00b7  " + s["cert_text"], font=f_lsrc,
               fill=GREY)
    y = lead_y + lead_h + 6

    # ---- picture cards: 2 rows x 6 ----
    card_w = (CW - 5 * 8) // 6
    card_h = 116
    f_ctag = F(SANS_B, 10)
    f_chead = F(SANS_B, 11)
    f_cbody = F(SANS, 11)
    f_csrc = F(SANS, 9)
    for row in range(2):
        for col in range(6):
            s = CARDS[row * 6 + col]
            cx0 = M + col * (card_w + 8)
            cy0 = y + row * (card_h + 8)
            d.rectangle([cx0, cy0, cx0 + card_w, cy0 + card_h],
                        outline=INK, width=1)
            draw_scene(img, d, s["scene"], cx0 + 1, cy0 + 1, card_w - 2, 28,
                       small=True)
            badge_right(d, cx0 + card_w - 6, cy0 + 5, s["badge"],
                        F(SANS_B, 9))
            iy = cy0 + 34
            d.text((cx0 + 6, iy), s["tag"], font=f_ctag, fill=RED)
            iy += 12
            iy = draw_fitted(d, cx0 + 6, iy, s["head"], f_chead,
                             card_w - 12, INK, 2, leading=12)
            iy += 1
            iy = draw_fitted(d, cx0 + 6, iy, s["body"], f_cbody,
                             card_w - 12, INK, 3, leading=11)
            d.text((cx0 + 6, cy0 + card_h - 11), s["src"], font=f_csrc,
                   fill=GREY)
    y = y + 2 * card_h + 8 + 6
    return img, d, y


# ---------------------------------------------------------------- map + briefs
# Map box: x, y, w=300, h=168. lon -180..180, lat 80..-60.
MAP_PINS = {  # story number -> (lon, lat, dx, dy)
    1: (127.0, 37.5, 0, 0), 2: (121.0, 25.0, 0, 0),
    3: (34.5, 31.5, 0, 0), 4: (-122.0, 37.7, 0, 0),
    5: (-47.9, -15.8, 0, 0), 6: (103.8, 1.4, -6, -6),
    7: (103.8, 1.4, 7, 7), 8: (30.5, 50.5, 0, 0),
    9: (100.5, 13.8, 0, 0), 10: (13.4, 52.5, 0, 0),
    11: (-0.1, 51.5, -5, 4), 12: (4.4, 50.9, 6, -5),
    13: (98.5, 40.5, 0, 0), 14: (-3.7, 40.4, 0, 0),
    15: (168.3, -17.7, 0, 0),
}


def draw_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw, my + mh], fill=(214, 228, 236))
    # graticule
    for i in range(1, 6):
        gx = mx + mw * i / 6
        d.line([gx, my, gx, my + mh], fill=(190, 205, 214), width=1)
    for i in range(1, 4):
        gy = my + mh * i / 4
        d.line([mx, gy, mx + mw, gy], fill=(190, 205, 214), width=1)

    def P(lon, lat):
        return (mx + (lon + 180) / 360 * mw,
                my + (80 - lat) / 140 * mh)

    # stylised continents (rough polygons, equirectangular)
    land = (150, 178, 140)
    d.polygon([P(-168, 66), P(-140, 70), P(-125, 72), P(-110, 70),
               P(-95, 69), P(-80, 73), P(-60, 62), P(-55, 47),
               P(-70, 42), P(-75, 32), P(-80, 26), P(-90, 21),
               P(-97, 16), P(-105, 20), P(-117, 33), P(-125, 49),
               P(-140, 60), P(-155, 58), P(-168, 66)], fill=land)
    d.polygon([P(-80, 10), P(-60, 8), P(-52, 5), P(-44, -3),
               P(-35, -8), P(-40, -20), P(-48, -28), P(-58, -35),
               P(-65, -41), P(-70, -50), P(-73, -54), P(-70, -40),
               P(-77, -12), P(-81, -2), P(-80, 10)], fill=land)
    d.polygon([P(-10, 36), P(-9, 43), P(-2, 48), P(2, 51), P(8, 57),
               P(10, 59), P(18, 56), P(21, 55), P(28, 59), P(30, 62),
               P(28, 71), P(20, 70), P(12, 66), P(5, 58), P(-2, 50),
               P(-10, 36)], fill=land)
    d.polygon([P(-6, 35), P(10, 37), P(20, 32), P(32, 31), P(35, 28),
               P(43, 12), P(48, 11), P(51, 12), P(43, -1), P(40, -10),
               P(36, -18), P(33, -26), P(26, -34), P(19, -35),
               P(15, -27), P(12, -18), P(9, 4), P(-8, 4), P(-16, 12),
               P(-17, 21), P(-6, 35)], fill=land)
    d.polygon([P(30, 70), P(45, 68), P(60, 69), P(80, 73), P(100, 76),
               P(120, 73), P(140, 72), P(160, 69), P(178, 66),
               P(170, 60), P(158, 52), P(142, 50), P(140, 42),
               P(135, 35), P(127, 34), P(122, 30), P(120, 22),
               P(110, 12), P(105, 8), P(100, 8), P(98, 16), P(92, 16),
               P(88, 22), P(80, 13), P(77, 8), P(73, 20), P(66, 25),
               P(60, 25), P(57, 26), P(50, 29), P(44, 30), P(40, 37),
               P(35, 36), P(30, 36), P(28, 45), P(30, 55), P(28, 65),
               P(30, 70)], fill=land)
    d.polygon([P(114, -22), P(122, -14), P(130, -12), P(137, -12),
               P(142, -11), P(147, -19), P(150, -22), P(153, -27),
               P(150, -37), P(146, -39), P(140, -38), P(135, -35),
               P(129, -32), P(124, -33), P(115, -35), P(114, -30),
               P(114, -22)], fill=land)
    # pins for stories 1-15
    f_pin = F(SANS_B, 9)
    for n, (lon, lat, dx, dy) in MAP_PINS.items():
        px, py = P(lon, lat)
        px, py = px + dx, py + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=WHITE, width=1)
        t = str(n)
        tw = d.textlength(t, font=f_pin)
        d.text((px - tw / 2, py - 5), t, font=f_pin, fill=WHITE)


def draw_bottom(img, d, y):
    M = 14
    CW = W - 2 * M
    # ---- map + IN BRIEF ----
    top = y
    map_w, map_h = 300, 124
    f_sec = F(SANS_B, 13)
    d.text((M, top), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.text((M + map_w + 14, top), "IN BRIEF \u2014 STORIES 16\u201334",
           font=f_sec, fill=INK)
    top += 16
    draw_map(d, M, top, map_w, map_h)
    f_leg = F(SANS, 10)
    d.text((M, top + map_h + 3), "Pins: stories 1\u201315.  16\u201334 in "
           "the list.", font=f_leg, fill=GREY)
    # briefs in two columns, one line each
    bx0 = M + map_w + 14
    col_w = (W - M - bx0 - 8) // 2
    f_b = F(SANS, 11)
    half = (len(BRIEFS) + 1) // 2
    for ci in range(2):
        bx = bx0 + ci * (col_w + 8)
        by = top
        for n, place, text, src in BRIEFS[ci * half:(ci + 1) * half]:
            line = str(n) + ". " + place + " \u2014 " + text
            lines = fit_lines(d, line, f_b, col_w, 1)
            d.text((bx, by), lines[0], font=f_b, fill=INK)
            by += 13
    y = top + map_h + 14
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 5
    # ---- DATE CHECK + WHAT WE DON'T KNOW YET ----
    f_box = F(SANS_B, 11)
    f_txt = F(SANS, 11)
    dc_w = 620
    d.text((M, y), "DATE CHECK \u2014 LEFT OUT ON PURPOSE", font=f_box,
           fill=RED)
    d.text((M + dc_w + 10, y), "WHAT WE DON'T KNOW YET", font=f_box,
           fill=NAVY)
    y += 14
    dc_end = y
    for ci in range(2):
        bx = M + ci * (dc_w // 2 + 6)
        by = y
        for line in DATE_CHECK[ci * 3:(ci + 1) * 3]:
            by = draw_wrapped(d, bx, by, "\u2715  " + line, f_txt,
                              dc_w // 2 - 4, INK, leading=12)
        dc_end = max(dc_end, by)
    dk_end = y
    for line in DONT_KNOW:
        dk_end = draw_wrapped(d, M + dc_w + 10, dk_end, "?  " + line,
                              f_txt, CW - dc_w - 10, INK, leading=12)
    y = max(dc_end, dk_end) + 4
    d.line([M, y, W - M, y], fill=INK, width=1)
    y += 3
    # ---- legend + sources ----
    f_leg2 = F(SANS, 11)
    d.text((M, y), "HOW SURE:  \u2713 CONFIRMED = official source or 2+ "
           "outlets  \u00b7  STATED = one party's claim  \u00b7  "
           "UNVERIFIED = unconfirmed.  Drawings, not photos.",
           font=f_leg2, fill=INK)
    y += 14
    f_src = F(SANS, 10)
    d.text((M, y), SOURCES_LINE, font=f_src, fill=GREY)
    y += 12
    d.text((M, y), "Compiled from wire reports published Tue 24 Nov 2026; "
           "events dated 24 Nov in local time; other-day stories listed "
           "above.", font=f_src, fill=GREY)
    y += 12
    return y


def main():
    img, d, y = draw_frontpage()
    y = draw_bottom(img, d, y)
    print("final y:", y, "of", H)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
