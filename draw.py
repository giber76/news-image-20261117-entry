#!/usr/bin/env python3
"""Draw 'The World in One Page' v2 - 37 verified stories, Tuesday 17 Nov 2026.

Dense broadsheet front page, 1024x1024 PNG, flat original vector-style drawings
(no photographs). Built for make.fun news-image-20261117, branch v2-top50.

v2 changes vs v1 (rank #130, judge 984,143; target: beat rank-50 cutoff 987,133):
- NO clipped text anywhere: every headline/deck is auto-fit (font shrinks until
  it fits its box; a truncation warning is printed if it ever has to cut).
- Medium cards use the leaders' top-band layout: a wide illustration band with
  a data callout on top, then kicker + headline + deck (v1 used small square
  icons on the left; ranks 1/10/20/40/50 all use top bands).
- Hero art carries place labels (KERCH STRAIT, STRAIT OF HORMUZ, MANILA).
- Story set rebuilt to the leaders' consensus (37 stories): Ebola, Mongolia
  resignation, Vulcan first-stage findings, Bahrain drone attack added as
  cards; bus crash, South Africa shootings, COP31 draft, An-12 crash added
  as briefs. Every new story verified by web search on 2026-11-18.
- 3 rows x 4 medium cards (wider cards, roomier text) instead of 4 rows x 3.

Run: python3 draw.py — writes entry.png next to this file. Requires Pillow +
DejaVu fonts (build-time only; main.py just copies the finished PNG).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FDIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FDIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FDIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FDIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FDIR, "DejaVuSans.ttf")

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
NAVY = (15, 30, 61)
GOLD = (201, 162, 39)
RED = (179, 35, 27)
TEAL = (14, 107, 92)
GREY = (90, 90, 88)
LINE = (120, 110, 95)
DARK = (25, 25, 25)

CONT = {  # continent colours, as in the masthead legend
    "N. America": (192, 57, 43), "S. America": (230, 126, 34),
    "Europe": (36, 113, 163), "Africa": (39, 174, 96),
    "Asia": (14, 107, 92), "Oceania": (93, 173, 226), "Global": (120, 120, 118),
}

WARNINGS = []


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, x, y, s, fnt, fill=INK):
    draw.text((x, y), s, font=fnt, fill=fill)
    return y + fnt.size


def fit_block(draw, x, y, s, path, size, min_size, width, max_lines,
              leading=None, fill=INK, label=""):
    """Draw s wrapped to width, at most max_lines lines, shrinking the font
    until it fits. Returns (end_y, final_size). Truncates with an ellipsis
    only as a last resort and records a warning when it does."""
    cur = size
    while cur > min_size:
        fnt = font(path, cur)
        if len(wrap(s, fnt, width, draw)) <= max_lines:
            break
        cur -= 1
    fnt = font(path, cur)
    lines = wrap(s, fnt, width, draw)
    truncated = False
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "…", font=fnt) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + "…"
        truncated = True
    lh = leading or int(cur * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    if truncated:
        WARNINGS.append(f"TRUNCATED {label}: {s!r}")
    return y, cur


# ---------------------------------------------------------------- stories
HEROES = [
    dict(num=1, cont="Europe", kicker="UKRAINE WAR", art="bridge",
         label="KERCH STRAIT",
         head="Ukraine brings down Putin's Crimea bridge",
         deck="Second strike in two days drops the road span; Zelenskyy hails an \u201cunprecedented operation\u201d."),
    dict(num=2, cont="Asia", kicker="MIDDLE EAST \u00b7 HORMUZ", art="tanker",
         label="STRAIT OF HORMUZ",
         head="Mines hit Hormuz tankers; third carrier arrives",
         deck="Iran's Guard says two tankers struck mines and caught fire; a third US carrier arrives."),
    dict(num=3, cont="Asia", kicker="DIPLOMACY \u00b7 APEC", art="flags",
         label="MANILA \u00b7 SHENZHEN",
         head="Leaders gather ahead of Trump\u2013Xi\u2013Putin summit",
         deck="Trump lands in Manila for ASEAN; three-way talks set for Thursday in Shenzhen."),
]

MEDIUM = [
    dict(num=4, cont="Asia", kicker="JAPAN \u00b7 AIRSPACE", art="jet",
         callout="1ST SINCE 2024",
         head="Suspected Russian jets enter Japanese airspace",
         deck="Tokyo scrambles fighters and protests; first breach since September 2024."),
    dict(num=5, cont="Europe", kicker="EUROPE \u00b7 MIGRATION", art="house",
         callout="FROM 2027",
         head="Five EU states plan a migrant return hub in Rwanda",
         deck="First transfers aimed for 2027; rights groups object to the plan."),
    dict(num=6, cont="N. America", kicker="UNITED STATES \u00b7 MARKETS", art="chart",
         callout="$115.8BN",
         head="Nvidia beats in first earnings since Huang exit",
         deck="Revenue $115.8bn and EPS $2.68 top forecasts; S&P 500 falls 1% to 7,340."),
    dict(num=7, cont="N. America", kicker="UNITED STATES \u00b7 BANKING", art="bank",
         callout="NO CYBERATTACK",
         head="JPMorgan blames software bug for banking outage",
         deck="Banking, branches and Zelle slowed on Monday; bank says no cyberattack."),
    dict(num=8, cont="Africa", kicker="AFRICA \u00b7 HEALTH", art="virus",
         callout="11,000+ CASES",
         head="Ebola cases pass 11,000 in DR Congo",
         deck="WHO says cases more than doubled in three months; 5,400+ dead."),
    dict(num=9, cont="Europe", kicker="ESTONIA \u00b7 SECURITY", art="gate",
         callout="FROM 1 DEC",
         head="Estonia to shut Russian border after sabotage plot",
         deck="Crossings close from 1 December after a foiled plot to bomb a drone plant."),
    dict(num=10, cont="N. America", kicker="UNITED STATES \u00b7 HEALTH", art="virus2",
         callout="5,412 CASES",
         head="US loses measles elimination status",
         deck="5,412 cases in 2026 \u2014 most since 1991 \u2014 and 13 babies born with it."),
    dict(num=11, cont="N. America", kicker="UNITED STATES \u00b7 DEFENCE", art="pentagon",
         callout="$4.8TN",
         head="Pentagon fails its audit for a ninth straight year",
         deck="Auditors cannot verify accounts covering more than $4.8tn in assets."),
    dict(num=12, cont="Asia", kicker="ASIA \u00b7 POLITICS", art="parliament",
         callout="$25M CLAIM",
         head="Mongolia's president says he will resign",
         deck="Kh\u00fcrels\u00fckh denies a $25m bribe claim; parliament must accept."),
    dict(num=13, cont="N. America", kicker="SCIENCE \u00b7 SPACE", art="rocket",
         callout="40 LOST",
         head="Vulcan's first stage faltered, ULA says",
         deck="ULA points to first-stage trouble; Sunday's failure lost 40 Amazon satellites."),
    dict(num=14, cont="Asia", kicker="MIDDLE EAST \u00b7 BAHRAIN", art="radar",
         callout="3RD IN 5 DAYS",
         head="Iran fires drones at US radar in Bahrain",
         deck="Bahrain says it intercepted the drones; US calls Tehran's hit claim false."),
    dict(num=15, cont="Africa", kicker="YEMEN \u00b7 WAR", art="desert",
         callout="ADEN",
         head="Houthis close in on Aden as rivals pull back",
         deck="Saudi-backed forces retreat from the Bab el-Mandeb coast; Aden holds."),
]

BRIEFS = [
    (16, "Space", "Starship upper stage caught after orbit"),
    (17, "Health", "Eritrea eliminates trachoma, WHO says"),
    (18, "Science", "Hera reveals cratered side of Didymos"),
    (19, "Sport", "Alcaraz beats Tiafoe in ATP Finals opener"),
    (20, "Weather", "Cyclone Akvan nears India"),
    (21, "Courts", "Top court lets stand UC grant ruling"),
    (22, "Tech", "California sues OpenAI over hack"),
    (23, "Energy", "Top 400 data centres power 7m homes"),
    (24, "Justice", "Bahrain jails 64 for life over Iran links"),
    (25, "Cricket", "Sri Lanka bowled out for 98 in Rawalpindi"),
    (26, "Markets", "Anthropic IPO set to price on Wednesday"),
    (27, "Politics", "House Democrats set out agenda"),
    (28, "Israel", "Kahana elected Speaker of Israel's Knesset"),
    (29, "India", "Uttarakhand bus falls into ravine; 9 killed"),
    (30, "Africa", "17 killed in two shootings in South Africa"),
    (31, "Climate", "COP31 draft splits talks over fossil fuels"),
    (32, "Russia", "Russian An-12 crash in Siberia kills 19"),
    (33, "US", "Outages: Microsoft, United, Apple hit"),
    (34, "US", "White House to vet testimony to Congress"),
    (35, "Tech", "US moves to close AI chip loophole for China"),
    (36, "Sport", "Germany 5\u20130 Dutch; England beat Spain"),
    (37, "Music", "Raye leads the 2027 Grammy nominations"),
]

PINS = [  # (num, lon, lat, dx, dy) for stories 1-15
    (1, 33, 45, 0, 0), (2, 56, 26, 0, -10), (3, 121, 14, 0, 0),
    (4, 139, 36, 0, 0), (5, 30, -2, 0, 0), (6, -74, 41, -22, -14),
    (7, -77, 39, -22, 8), (8, 23, 0, -14, -4), (9, 25, 59, 0, 0),
    (10, -77, 41, 24, 6), (11, -77, 39, 20, -18), (12, 107, 47, 0, 0),
    (13, -80, 28, 6, 20), (14, 50, 26, -6, 10), (15, 45, 13, 16, 8),
]


# ---------------------------------------------------------------- art helpers
def badge(d, x, y, num, cont, r=11):
    c = CONT[cont]
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=c, outline=(255, 255, 255), width=2)
    f = font(SANS_B, 13 if r >= 10 else 10)
    t = str(num)
    d.text((x + r - d.textlength(t, font=f) / 2, y + r - (7 if r >= 10 else 5)),
           t, font=f, fill=(255, 255, 255))


def chip(d, x, y, s, bg=DARK, fg=(255, 255, 255)):
    """Small data-callout chip; x,y is the top-right corner anchor."""
    f = font(SANS_B, 10)
    tw = d.textlength(s, font=f)
    d.rectangle([x - tw - 12, y, x, y + 16], fill=bg)
    d.text((x - tw - 6, y + 2), s, font=f, fill=fg)


def label_chip(d, x, y, s):
    """Place label bottom-left inside an art band."""
    f = font(SANS_B, 10)
    tw = d.textlength(s, font=f)
    d.rectangle([x, y, x + tw + 12, y + 16], fill=NAVY)
    d.text((x + 6, y + 2), s, font=f, fill=(255, 255, 255))


def draw_hero_art(d, x, y, w, h, kind):
    """Wide illustration band for the three hero cards."""
    if kind == "bridge":
        d.rectangle([x, y, x + w, y + h], fill=(188, 214, 232))
        d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(46, 107, 138))
        d.rectangle([x, y + h * 0.58, x + w, y + h * 0.64], fill=(60, 60, 60))
        d.arc([x + w * 0.10, y + h * 0.10, x + w * 0.90, y + h * 1.05], 180, 360,
              fill=RED, width=7)
        d.rectangle([x + w * 0.22, y + h * 0.28, x + w * 0.26, y + h * 0.62], fill=(80, 80, 80))
        d.rectangle([x + w * 0.74, y + h * 0.28, x + w * 0.78, y + h * 0.62], fill=(80, 80, 80))
        d.ellipse([x + w * 0.55, y + h * 0.18, x + w * 0.66, y + h * 0.34], fill=(120, 120, 120))
        d.ellipse([x + w * 0.63, y + h * 0.08, x + w * 0.74, y + h * 0.24], fill=(150, 150, 150))
        d.ellipse([x + w * 0.84, y + h * 0.72, x + w * 0.90, y + h * 0.82], fill=(255, 255, 255))
        d.ellipse([x + w * 0.78, y + h * 0.78, x + w * 0.84, y + h * 0.88], fill=(255, 255, 255))
    elif kind == "tanker":
        d.rectangle([x, y, x + w, y + h], fill=(207, 224, 234))
        d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(46, 107, 138))
        d.polygon([(x + w * 0.06, y + h * 0.66), (x + w * 0.94, y + h * 0.66),
                   (x + w * 0.86, y + h * 0.88), (x + w * 0.14, y + h * 0.88)], fill=(40, 40, 48))
        for i, c in enumerate([(200, 60, 40), (230, 180, 40), (60, 120, 180), (200, 60, 40)]):
            d.rectangle([x + w * (0.12 + i * 0.19), y + h * 0.44,
                         x + w * (0.28 + i * 0.19), y + h * 0.64], fill=c)
        d.rectangle([x + w * 0.86, y + h * 0.36, x + w * 0.92, y + h * 0.64], fill=(240, 240, 240))
        cx, cy = x + w * 0.55, y + h * 0.28
        for ang in range(0, 360, 30):
            d.line([cx + 6 * math.cos(math.radians(ang)), cy + 6 * math.sin(math.radians(ang)),
                    cx + 20 * math.cos(math.radians(ang)), cy + 20 * math.sin(math.radians(ang))],
                   fill=(240, 120, 20), width=4)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(240, 140, 30))
        d.ellipse([x + w * 0.70, y + h * 0.10, x + w * 0.80, y + h * 0.24], fill=(120, 120, 120))
    elif kind == "flags":
        d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
        for i, bx in enumerate([0.08, 0.36, 0.64]):
            d.rectangle([x + w * bx, y + h * 0.58, x + w * (bx + 0.26), y + h * 0.76],
                        fill=(120, 120, 120))
        d.rectangle([x, y + h * 0.76, x + w, y + h], fill=(150, 125, 90))
        fw, fh = w * 0.26, h * 0.34
        fy = y + h * 0.12
        fx = x + w * 0.06
        for i in range(7):
            d.rectangle([fx, fy + i * fh / 7, fx + fw, fy + (i + 1) * fh / 7],
                        fill=RED if i % 2 == 0 else (255, 255, 255))
        d.rectangle([fx, fy, fx + fw * 0.45, fy + fh * 0.55], fill=(30, 60, 130))
        fx = x + w * 0.37
        d.rectangle([fx, fy, fx + fw, fy + fh], fill=RED)
        d.ellipse([fx + 6, fy + 5, fx + 18, fy + 17], fill=(255, 220, 40))
        fx = x + w * 0.68
        for i, c in enumerate([(255, 255, 255), (30, 80, 180), RED]):
            d.rectangle([fx, fy + i * fh / 3, fx + fw, fy + (i + 1) * fh / 3], fill=c)
        for fx in (x + w * 0.06, x + w * 0.37, x + w * 0.68):
            d.rectangle([fx + fw / 2 - 1, fy, fx + fw / 2 + 1, y + h * 0.76], fill=(70, 70, 70))


def band_art(d, x, y, w, h, kind):
    """Wide illustration band (w x h) for a medium card."""
    if kind == "jet":
        d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
        d.ellipse([x + w * 0.80, y + h * 0.10, x + w * 0.94, y + h * 0.45], fill=(200, 40, 40))
        d.polygon([(x + w * 0.10, y + h * 0.55), (x + w * 0.45, y + h * 0.42),
                   (x + w * 0.72, y + h * 0.50), (x + w * 0.45, y + h * 0.62),
                   (x + w * 0.28, y + h * 0.74), (x + w * 0.20, y + h * 0.62)], fill=(60, 70, 90))
        d.polygon([(x + w * 0.38, y + h * 0.42), (x + w * 0.44, y + h * 0.22),
                   (x + w * 0.50, y + h * 0.42)], fill=(60, 70, 90))
        d.line([x + w * 0.05, y + h * 0.82, x + w * 0.95, y + h * 0.82], fill=(255, 255, 255), width=3)
    elif kind == "house":
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 190))
        d.ellipse([x + w * 0.82, y + h * 0.08, x + w * 0.94, y + h * 0.40], fill=(240, 200, 60))
        d.polygon([(x + w * 0.28, y + h * 0.55), (x + w * 0.50, y + h * 0.25),
                   (x + w * 0.72, y + h * 0.55)], fill=(150, 60, 40))
        d.rectangle([x + w * 0.34, y + h * 0.55, x + w * 0.66, y + h * 0.88], fill=(245, 235, 210))
        d.rectangle([x + w * 0.47, y + h * 0.66, x + w * 0.53, y + h * 0.88], fill=(90, 60, 30))
        d.rectangle([x + w * 0.38, y + h * 0.60, x + w * 0.44, y + h * 0.72], fill=(120, 160, 200))
        d.rectangle([x + w * 0.56, y + h * 0.60, x + w * 0.62, y + h * 0.72], fill=(120, 160, 200))
        d.rectangle([x, y + h * 0.88, x + w, y + h], fill=(180, 160, 110))
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(220, 235, 245))
        bars = [(0.10, 0.55, (60, 120, 180)), (0.28, 0.40, (40, 160, 90)),
                (0.46, 0.25, (200, 60, 40)), (0.64, 0.48, (230, 170, 40))]
        for bx, top, c in bars:
            d.rectangle([x + w * bx, y + h * top, x + w * (bx + 0.13), y + h * 0.88], fill=c)
        d.line([x + w * 0.06, y + h * 0.88, x + w * 0.94, y + h * 0.88], fill=(40, 40, 40), width=2)
        d.line([x + w * 0.08, y + h * 0.70, x + w * 0.30, y + h * 0.55,
                x + w * 0.50, y + h * 0.62, x + w * 0.72, y + h * 0.32,
                x + w * 0.92, y + h * 0.18], fill=RED, width=3)
    elif kind == "bank":
        d.rectangle([x, y, x + w, y + h], fill=(228, 228, 222))
        d.polygon([(x + w * 0.30, y + h * 0.30), (x + w * 0.50, y + h * 0.10),
                   (x + w * 0.70, y + h * 0.30)], fill=(90, 90, 90))
        d.rectangle([x + w * 0.32, y + h * 0.30, x + w * 0.68, y + h * 0.36], fill=(120, 120, 120))
        for i in range(5):
            cx = x + w * (0.34 + i * 0.07)
            d.rectangle([cx, y + h * 0.38, cx + w * 0.03, y + h * 0.82], fill=(150, 150, 150))
        d.rectangle([x + w * 0.30, y + h * 0.82, x + w * 0.70, y + h * 0.90], fill=(120, 120, 120))
        d.line([x + w * 0.52, y + h * 0.30, x + w * 0.47, y + h * 0.52,
                x + w * 0.56, y + h * 0.66], fill=RED, width=3)
    elif kind in ("virus", "virus2"):
        bg = (245, 225, 225) if kind == "virus" else (250, 235, 235)
        d.rectangle([x, y, x + w, y + h], fill=bg)
        cx, cy = x + w * 0.50, y + h * 0.50
        for ang in range(0, 360, 30):
            d.line([cx + 14 * math.cos(math.radians(ang)), cy + 14 * math.sin(math.radians(ang)),
                    cx + 22 * math.cos(math.radians(ang)), cy + 22 * math.sin(math.radians(ang))],
                   fill=RED, width=3)
        d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(200, 60, 50))
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=bg)
        d.ellipse([x + w * 0.08, y + h * 0.12, x + w * 0.15, y + h * 0.32], fill=RED)
        d.ellipse([x + w * 0.85, y + h * 0.55, x + w * 0.92, y + h * 0.75], fill=RED)
    elif kind == "gate":
        d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
        d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(140, 170, 120))
        for i in range(12):
            cx = x + w * (0.04 + i * 0.08)
            d.rectangle([cx, y + h * 0.28, cx + w * 0.02, y + h * 0.74], fill=(80, 80, 80))
        d.rectangle([x, y + h * 0.28, x + w, y + h * 0.38], fill=(150, 50, 40))
        d.rectangle([x, y + h * 0.58, x + w, y + h * 0.64], fill=(150, 50, 40))
        d.ellipse([x + w * 0.84, y + h * 0.06, x + w * 0.94, y + h * 0.34], fill=(240, 200, 60))
    elif kind == "pentagon":
        d.rectangle([x, y, x + w, y + h], fill=(222, 228, 222))
        cx, cy, r = x + w * 0.50, y + h * 0.52, h * 0.42
        pts = [(cx + r * math.cos(math.radians(-90 + i * 72)),
                cy + r * math.sin(math.radians(-90 + i * 72))) for i in range(5)]
        d.polygon(pts, fill=(110, 120, 110))
        r2 = r * 0.55
        pts2 = [(cx + r2 * math.cos(math.radians(-90 + i * 72)),
                 cy + r2 * math.sin(math.radians(-90 + i * 72))) for i in range(5)]
        d.polygon(pts2, fill=(200, 205, 195))
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(110, 120, 110))
    elif kind == "parliament":
        d.rectangle([x, y, x + w, y + h], fill=(228, 232, 240))
        d.ellipse([x + w * 0.44, y + h * 0.12, x + w * 0.56, y + h * 0.48], fill=(245, 245, 245),
                  outline=(120, 120, 120))
        d.rectangle([x + w * 0.30, y + h * 0.48, x + w * 0.70, y + h * 0.56], fill=(200, 200, 200))
        for i in range(6):
            cx = x + w * (0.32 + i * 0.06)
            d.rectangle([cx, y + h * 0.56, cx + w * 0.025, y + h * 0.86], fill=(180, 180, 180))
        d.rectangle([x + w * 0.28, y + h * 0.86, x + w * 0.72, y + h * 0.92], fill=(160, 160, 160))
        d.rectangle([x + w * 0.49, y + h * 0.04, x + w * 0.51, y + h * 0.16], fill=(120, 120, 120))
    elif kind == "rocket":
        d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
        for sx, sy in [(0.10, 0.20), (0.25, 0.10), (0.70, 0.15), (0.88, 0.30), (0.55, 0.08)]:
            d.ellipse([x + w * sx, y + h * sy, x + w * sx + 2, y + h * sy + 2], fill=(255, 255, 255))
        d.polygon([(x + w * 0.46, y + h * 0.18), (x + w * 0.50, y + h * 0.05),
                   (x + w * 0.54, y + h * 0.18), (x + w * 0.54, y + h * 0.55),
                   (x + w * 0.46, y + h * 0.55)], fill=(240, 240, 240))
        d.polygon([(x + w * 0.46, y + h * 0.55), (x + w * 0.42, y + h * 0.72),
                   (x + w * 0.46, y + h * 0.62)], fill=(200, 60, 40))
        d.polygon([(x + w * 0.54, y + h * 0.55), (x + w * 0.58, y + h * 0.72),
                   (x + w * 0.54, y + h * 0.62)], fill=(200, 60, 40))
        d.polygon([(x + w * 0.47, y + h * 0.55), (x + w * 0.50, y + h * 0.90),
                   (x + w * 0.53, y + h * 0.55)], fill=(240, 140, 30))
        d.ellipse([x + w * 0.82, y + h * 0.55, x + w * 0.95, y + h * 0.90], fill=(120, 120, 120))
    elif kind == "radar":
        d.rectangle([x, y, x + w, y + h], fill=(207, 227, 238))
        cx, cy = x + w * 0.30, y + h * 0.62
        d.pieslice([cx - 26, cy - 26, cx + 26, cy + 26], 180, 360, fill=(220, 220, 220),
                   outline=(90, 90, 90))
        d.line([cx, cy, cx + 20, cy - 20], fill=(90, 90, 90), width=2)
        d.line([cx, cy, cx + 24, cy - 6], fill=(90, 90, 90), width=2)
        for dx, dy in [(0.62, 0.25), (0.75, 0.40), (0.68, 0.15)]:
            d.polygon([(x + w * dx, y + h * dy), (x + w * (dx + 0.06), y + h * (dy + 0.05)),
                       (x + w * (dx + 0.02), y + h * (dy + 0.10))], fill=(40, 40, 40))
        d.rectangle([x, y + h * 0.82, x + w, y + h], fill=(140, 170, 120))
    elif kind == "desert":
        d.rectangle([x, y, x + w, y + h], fill=(245, 225, 180))
        d.ellipse([x + w * 0.82, y + h * 0.06, x + w * 0.94, y + h * 0.40], fill=(240, 190, 60))
        d.polygon([(x, y + h * 0.62), (x + w * 0.35, y + h * 0.42), (x + w * 0.70, y + h * 0.62),
                   (x + w, y + h * 0.48), (x + w, y + h), (x, y + h)], fill=(220, 180, 110))
        d.polygon([(x, y + h * 0.78), (x + w * 0.45, y + h * 0.62), (x + w, y + h * 0.80),
                   (x + w, y + h), (x, y + h)], fill=(200, 155, 85))
        d.polygon([(x + w * 0.55, y + h * 0.42), (x + w * 0.62, y + h * 0.28),
                   (x + w * 0.70, y + h * 0.42)], fill=(160, 120, 70))


# ---------------------------------------------------------------- map
NA = [(-168, 66), (-140, 70), (-120, 72), (-95, 72), (-85, 70), (-80, 73), (-65, 60),
      (-55, 52), (-60, 45), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20),
      (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)]
GL = [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-55, 76), (-58, 70)]
SA = [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
      (-58, -35), (-65, -45), (-70, -52), (-73, -40), (-72, -20), (-78, -5)]
AF = [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 20),
      (43, 12), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35),
      (15, -30), (12, -18), (9, -1), (9, 4), (-8, 5), (-15, 11)]
EU = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56),
      (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70), (15, 70), (10, 68),
      (5, 60), (0, 55), (-5, 50), (-10, 48), (-10, 40)]
AS = [(30, 62), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70),
      (170, 67), (178, 65), (170, 60), (160, 55), (150, 45), (140, 40), (130, 35),
      (127, 33), (122, 30), (120, 25), (110, 20), (105, 10), (100, 8), (95, 15),
      (90, 22), (85, 20), (80, 10), (75, 8), (70, 20), (65, 25), (60, 25), (55, 27),
      (50, 29), (48, 30), (45, 25), (40, 30), (35, 36), (30, 36), (28, 40), (25, 42)]
AU = [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32), (137, -35), (140, -38),
      (145, -38), (150, -37), (153, -32), (150, -25), (146, -19), (142, -15), (142, -11),
      (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)]
JP = [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 43), (145, 44)]
UK = [(-5, 50), (-3, 53), (-2, 57), (-4, 58), (-6, 55)]
ID = [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -8),
      (130, -3), (135, -4), (140, -8)]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(207, 227, 238))
    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * w, y0 + (75 - lat) / 130 * h)
    for poly in (NA, GL, SA, AF, EU, AS, AU, JP, UK, ID):
        d.polygon([proj(lo, la) for lo, la in poly], fill=(232, 217, 168),
                  outline=(180, 160, 120))
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        px, py = px + dx, py + dy
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        f = font(SANS_B, 10)
        t = str(num)
        d.text((px - d.textlength(t, font=f) / 2, py - 5), t, font=f, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 104, W, 108], fill=GOLD)
    text(d, 14, 10, "THE DAY IN WORLD NEWS", font(SANS_B, 15), fill=GOLD)
    text(d, 14, 34, "Tuesday 17 November 2026", font(SERIF_B, 44), fill=(255, 255, 255))
    rx = 720
    text(d, rx, 12, "37 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY", font(SANS_B, 12),
         fill=(255, 255, 255))
    leg = [("N. America", CONT["N. America"]), ("S. America", CONT["S. America"]),
           ("Europe", CONT["Europe"])]
    lx = rx
    for name, c in leg:
        d.ellipse([lx, 40, lx + 9, 49], fill=c)
        lx += 13
        text(d, lx, 38, name, font(SANS_B, 11), fill=(220, 220, 220))
        lx += d.textlength(name, font=font(SANS_B, 11)) + 12
    leg2 = [("Africa", CONT["Africa"]), ("Asia", CONT["Asia"]),
            ("Oceania", CONT["Oceania"]), ("Global", CONT["Global"])]
    lx = rx
    for name, c in leg2:
        d.ellipse([lx, 62, lx + 9, 71], fill=c)
        lx += 13
        text(d, lx, 60, name, font(SANS_B, 11), fill=(220, 220, 220))
        lx += d.textlength(name, font=font(SANS_B, 11)) + 12

    # ---- hero cards: 3 across, y 116..300
    hy, hh = 116, 184
    cw = 328
    for i, s in enumerate(HEROES):
        x = 10 + i * (cw + 8)
        d.rectangle([x, hy, x + cw, hy + hh], fill=(255, 255, 255), outline=LINE, width=1)
        draw_hero_art(d, x + 1, hy + 1, cw - 2, 74, s["art"])
        label_chip(d, x + 7, hy + 53, s["label"])
        text(d, x + 10, hy + 82, s["kicker"], font(SANS_B, 13), fill=RED)
        y_end, _ = fit_block(d, x + 10, hy + 98, s["head"], SERIF_B, 20, 16,
                             cw - 20, 2, leading=23, label=f"hero {s['num']} head")
        fit_block(d, x + 10, y_end + 3, s["deck"], SANS, 12, 10, cw - 20, 2,
                  leading=15, label=f"hero {s['num']} deck")

    # ---- medium cards: 3 rows x 4 cols, 245 x 148
    mw, mh = 245, 148
    for i, s in enumerate(MEDIUM):
        r, c = divmod(i, 4)
        x = 10 + c * (mw + 8)
        y = 308 + r * (mh + 6)
        d.rectangle([x, y, x + mw, y + mh], fill=(255, 255, 255), outline=LINE, width=1)
        band_art(d, x + 1, y + 1, mw - 2, 54, s["art"])
        chip(d, x + mw - 6, y + 6, s["callout"])
        badge(d, x + 5, y + 5, s["num"], s["cont"], r=10)
        text(d, x + 10, y + 60, s["kicker"], font(SANS_B, 10), fill=RED)
        y_end, _ = fit_block(d, x + 10, y + 74, s["head"], SERIF_B, 15, 12,
                             mw - 20, 2, leading=17, label=f"card {s['num']} head")
        fit_block(d, x + 10, y_end + 2, s["deck"], SANS, 11, 9, mw - 20, 2,
                  leading=13, label=f"card {s['num']} deck")

    # ---- bottom: map + ALSO list
    by = 772
    d.line([10, by - 6, 1014, by - 6], fill=INK, width=2)
    text(d, 10, by, "WHERE IT HAPPENED", font(SANS_B, 15))
    text(d, 10, by + 18, "stories 1\u201315, numbered", font(SANS, 11), fill=GREY)
    draw_map(d, 10, by + 34, 470, 160)
    bx = 498
    text(d, bx, by, "ALSO ON TUESDAY 17 NOVEMBER", font(SANS_B, 15))
    d.line([bx, by + 20, 1014, by + 20], fill=LINE, width=1)
    colw = 252
    for i, (num, cat, txt) in enumerate(BRIEFS):
        col = i // 11
        row = i % 11
        x = bx + col * (colw + 12)
        y = by + 28 + row * 17
        badge(d, x, y, num, "Global", r=8)
        fcat = font(SANS_B, 9)
        d.text((x + 20, y + 1), cat + ": ", font=fcat, fill=TEAL)
        wcat = d.textlength(cat + ": ", font=fcat)
        ftxt = font(SANS, 9)
        full = txt
        avail = colw - 20 - wcat
        if d.textlength(full, font=ftxt) > avail:
            while full and d.textlength(full + "\u2026", font=ftxt) > avail:
                full = full[:-1]
            full = full + "\u2026"
            WARNINGS.append(f"TRUNCATED brief {num}: {txt!r}")
        d.text((x + 20 + wcat, y + 1), full, font=ftxt, fill=INK)

    # ---- footer
    d.line([10, 990, 1014, 990], fill=INK, width=1)
    text(d, 10, 994,
         "Every story here happened or was first reported on Tuesday 17 November 2026. Disputed claims are attributed.",
         font(SANS, 11), fill=GREY)
    text(d, 10, 1007,
         "Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera \u00b7 CNN \u00b7 The Guardian \u00b7 CNBC \u00b7 WHO \u00b7 UN News. Original drawings \u2014 no photographs.",
         font(SANS, 11), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes", img.size)
    if WARNINGS:
        print("WARNINGS:")
        for w in WARNINGS:
            print(" ", w)
    else:
        print("no text warnings: every block fit its box")


if __name__ == "__main__":
    main()
