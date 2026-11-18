#!/usr/bin/env python3
"""Draw 'The World in One Page' - 33 verified stories from Tuesday 17 Nov 2026.

Dense broadsheet front page, 1024x1024 PNG, flat original vector-style drawings
(no photographs). Built for make.fun news-image-20261117. Run: python3 draw.py
Writes entry.png next to this file. Requires Pillow + DejaVu fonts (build-time only;
the entry program main.py just copies the finished PNG, stdlib only).
"""
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

CONT = {  # continent colours, as in the masthead legend
    "N. America": (192, 57, 43), "S. America": (230, 126, 34),
    "Europe": (36, 113, 163), "Africa": (39, 174, 96),
    "Asia": (14, 107, 92), "Oceania": (93, 173, 226), "Global": (120, 120, 118),
}


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


def para(draw, x, y, s, fnt, width, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.18)
    for ln in wrap(s, fnt, width, draw):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
HEROES = [
    dict(num=1, cont="Europe", kicker="UKRAINE WAR", art="bridge",
         head="Ukraine brings down Putin's Crimea bridge",
         deck="Second strike in two days drops the road span; Zelenskyy hails an \u201cunprecedented operation\u201d.",
         pin=(33, 45)),
    dict(num=2, cont="Asia", kicker="MIDDLE EAST \u00b7 HORMUZ", art="tanker",
         head="Mines hit Hormuz tankers; third carrier arrives",
         deck="Iran's Guard says two tankers struck mines and caught fire; a third US carrier arrives.",
         pin=(56, 26)),
    dict(num=3, cont="Asia", kicker="DIPLOMACY \u00b7 APEC", art="flags",
         head="Leaders gather ahead of Trump\u2013Xi\u2013Putin summit",
         deck="Trump lands in Manila for ASEAN; three-way talks set for Thursday in Shenzhen.",
         pin=(121, 14)),
]

MEDIUM = [
    dict(num=4, cont="Asia", kicker="JAPAN \u00b7 AIRSPACE", art="jet",
         head="Suspected Russian jets enter Japanese airspace",
         deck="Tokyo scrambles fighters and protests; first breach since September 2024."),
    dict(num=5, cont="Europe", kicker="EUROPE \u00b7 MIGRATION", art="house",
         head="Five EU states plan a migrant return hub in Rwanda",
         deck="First transfers aimed for 2027; rights groups object to the plan."),
    dict(num=6, cont="N. America", kicker="UNITED STATES \u00b7 MARKETS", art="chart",
         head="Nvidia beats in first earnings since Huang exit",
         deck="Revenue $115.8bn and EPS $2.68 top forecasts; S&P 500 falls 1% to 7,340."),
    dict(num=7, cont="N. America", kicker="UNITED STATES \u00b7 BANKING", art="bank",
         head="JPMorgan blames software bug for banking outage",
         deck="Banking, branches and Zelle slowed on Monday; bank says no cyberattack."),
    dict(num=8, cont="N. America", kicker="UNITED STATES \u00b7 OUTAGES", art="server",
         head="Outages pile up: Microsoft, United, Apple hit",
         deck="Microsoft blames a latent defect; United's systems fail; NSA net briefly down."),
    dict(num=9, cont="Europe", kicker="ESTONIA \u00b7 SECURITY", art="gate",
         head="Estonia to shut Russian border after sabotage plot",
         deck="Crossings close from 1 December after a foiled plot to bomb a drone plant."),
    dict(num=10, cont="N. America", kicker="UNITED STATES \u00b7 HEALTH", art="virus",
         head="US loses measles elimination status",
         deck="5,412 cases in 2026, most since 1991; 13 babies born with congenital measles."),
    dict(num=11, cont="N. America", kicker="UNITED STATES \u00b7 DEFENCE", art="pentagon",
         head="Pentagon fails its audit for a ninth straight year",
         deck="Auditors cannot verify accounts covering more than $4.8tn in assets."),
    dict(num=12, cont="N. America", kicker="UNITED STATES \u00b7 POLITICS", art="capitol",
         head="White House to vet all testimony to Congress",
         deck="Agencies must get approval before staff agree to appear before committees."),
    dict(num=13, cont="Africa", kicker="YEMEN \u00b7 WAR", art="desert",
         head="Houthis close in on Aden as rivals pull back",
         deck="Saudi-backed forces retreat from the Bab el-Mandeb coast; Aden holds."),
    dict(num=14, cont="Asia", kicker="ASIA \u00b7 TECHNOLOGY", art="chip",
         head="US moves to close AI chip loophole for China",
         deck="Nvidia warns customers over renting computing power to Chinese firms."),
    dict(num=15, cont="Europe", kicker="SPORT \u00b7 FOOTBALL", art="ball",
         head="Germany rout Dutch 5\u20130; England end Spain run",
         deck="England end Spain's 43-match unbeaten run in Madrid to top their group."),
]

BRIEFS = [
    (16, "Space", "SpaceX catches a Starship upper stage after orbit"),
    (17, "Health", "WHO validates Eritrea's elimination of trachoma"),
    (18, "Science", "Hera probe reveals the cratered side of asteroid Didymos"),
    (19, "Sport", "Alcaraz beats Tiafoe in his ATP Finals opener"),
    (20, "Sport", "Crystal Palace appoint Thomas Frank as manager"),
    (21, "Sport", "Edmonton Elks win the 113th Grey Cup"),
    (22, "Sport", "Lukaku retires from international football"),
    (23, "Music", "Raye leads the 2027 Grammy nominations"),
    (24, "Weather", "Cyclone Akvan nears India; Andhra Pradesh on alert"),
    (25, "Courts", "Top court lets stand ruling against Trump UC grant cuts"),
    (26, "Tech", "California sues OpenAI over the Hugging Face hack"),
    (27, "Energy", "Top 400 US data centres use power for 7m homes"),
    (28, "Justice", "Bahrain jails 64 for life over alleged Iran links"),
    (29, "Cricket", "Sri Lanka bowled out for 98 in Rawalpindi"),
    (30, "Markets", "Anthropic IPO set to price on Wednesday"),
    (31, "Politics", "House Democrats set out their opening agenda"),
    (32, "Israel", "Matan Kahana elected Speaker of Israel's Knesset"),
    (33, "Golf", "Tiger Woods to return at Hero World Challenge"),
]

PINS = [  # (num, lon, lat, dx, dy) for stories 1-15
    (1, 33, 45, 0, 0), (2, 56, 26, 0, 0), (3, 121, 14, 0, 0),
    (4, 139, 36, 0, 0), (5, 30, -2, 0, 0), (6, -74, 41, -16, -12),
    (7, -77, 39, -18, 8), (8, -122, 47, 0, 0), (9, 25, 59, 0, 0),
    (10, -77, 41, 18, 4), (11, -77, 39, 14, -14), (12, -77, 39, -2, 18),
    (13, 45, 13, 0, 0), (14, 104, 1, 0, 0), (15, 13, 52, 0, 0),
]


# ---------------------------------------------------------------- icons
def badge(d, x, y, num, cont, r=11):
    c = CONT[cont]
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=c, outline=(255, 255, 255), width=2)
    f = font(SANS_B, 13)
    t = str(num)
    d.text((x + r - d.textlength(t, font=f) / 2, y + r - 7), t, font=f, fill=(255, 255, 255))


def icon_bridge(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(188, 214, 232))
    d.rectangle([x, y + s * 0.62, x + s, y + s], fill=(46, 107, 138))
    d.rectangle([x, y + s * 0.55, x + s, y + s * 0.60], fill=(60, 60, 60))
    d.arc([x + s * 0.08, y + s * 0.18, x + s * 0.92, y + s * 0.95], 180, 360, fill=RED, width=5)
    d.rectangle([x + s * 0.18, y + s * 0.30, x + s * 0.24, y + s * 0.58], fill=(80, 80, 80))
    d.rectangle([x + s * 0.76, y + s * 0.30, x + s * 0.82, y + s * 0.58], fill=(80, 80, 80))
    d.ellipse([x + s * 0.60, y + s * 0.22, x + s * 0.72, y + s * 0.34], fill=(120, 120, 120))
    d.ellipse([x + s * 0.68, y + s * 0.14, x + s * 0.80, y + s * 0.26], fill=(150, 150, 150))


def icon_tanker(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(207, 224, 234))
    d.rectangle([x, y + s * 0.62, x + s, y + s], fill=(46, 107, 138))
    d.polygon([(x + s * 0.10, y + s * 0.62), (x + s * 0.88, y + s * 0.62),
               (x + s * 0.80, y + s * 0.80), (x + s * 0.18, y + s * 0.80)], fill=(40, 40, 48))
    for i, c in enumerate([(200, 60, 40), (230, 180, 40), (60, 120, 180)]):
        d.rectangle([x + s * (0.16 + i * 0.22), y + s * 0.44, x + s * (0.34 + i * 0.22), y + s * 0.60], fill=c)
    d.rectangle([x + s * 0.74, y + s * 0.38, x + s * 0.82, y + s * 0.60], fill=(240, 240, 240))
    for ang in range(0, 360, 45):
        import math
        r0, r1 = 4, 13
        cx, cy = x + s * 0.55, y + s * 0.28
        d.line([cx + r0 * math.cos(math.radians(ang)), cy + r0 * math.sin(math.radians(ang)),
                cx + r1 * math.cos(math.radians(ang)), cy + r1 * math.sin(math.radians(ang))],
               fill=(240, 120, 20), width=3)
    d.ellipse([x + s * 0.50, y + s * 0.23, x + s * 0.60, y + s * 0.33], fill=(240, 140, 30))


def icon_flags(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 226, 238))
    for i, bx in enumerate([0.12, 0.38, 0.64]):
        d.rectangle([x + s * bx, y + s * 0.55, x + s * (bx + 0.24), y + s * 0.72], fill=(120, 120, 120))
    d.rectangle([x, y + s * 0.72, x + s, y + s], fill=(150, 125, 90))
    # US flag
    fx, fy, fw, fh = x + s * 0.06, y + s * 0.14, s * 0.26, s * 0.17
    for i in range(7):
        d.rectangle([fx, fy + i * fh / 7, fx + fw, fy + (i + 1) * fh / 7],
                    fill=RED if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, fy, fx + fw * 0.45, fy + fh * 0.55], fill=(30, 60, 130))
    # China flag
    fx = x + s * 0.37
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=RED)
    d.ellipse([fx + 3, fy + 3, fx + 11, fy + 11], fill=(255, 220, 40))
    # Russia flag
    fx = x + s * 0.68
    for i, c in enumerate([(255, 255, 255), (30, 80, 180), RED]):
        d.rectangle([fx, fy + i * fh / 3, fx + fw, fy + (i + 1) * fh / 3], fill=c)
    for fx in (x + s * 0.06, x + s * 0.37, x + s * 0.68):
        d.rectangle([fx + fw / 2 - 1, fy, fx + fw / 2 + 1, y + s * 0.72], fill=(70, 70, 70))


def icon_jet(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 226, 238))
    d.ellipse([x + s * 0.62, y + s * 0.12, x + s * 0.88, y + s * 0.38], fill=(200, 40, 40))
    d.polygon([(x + s * 0.10, y + s * 0.55), (x + s * 0.55, y + s * 0.45),
               (x + s * 0.88, y + s * 0.52), (x + s * 0.55, y + s * 0.62),
               (x + s * 0.30, y + s * 0.72), (x + s * 0.22, y + s * 0.62)], fill=(60, 70, 90))
    d.polygon([(x + s * 0.42, y + s * 0.45), (x + s * 0.50, y + s * 0.28),
               (x + s * 0.58, y + s * 0.45)], fill=(60, 70, 90))
    d.line([x + s * 0.05, y + s * 0.80, x + s * 0.95, y + s * 0.80], fill=(255, 255, 255), width=3)
    d.line([x + s * 0.15, y + s * 0.88, x + s * 0.85, y + s * 0.88], fill=(255, 255, 255), width=2)


def icon_house(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(232, 222, 190))
    d.polygon([(x + s * 0.14, y + s * 0.55), (x + s * 0.50, y + s * 0.28), (x + s * 0.86, y + s * 0.55)],
              fill=(150, 60, 40))
    d.rectangle([x + s * 0.22, y + s * 0.55, x + s * 0.78, y + s * 0.85], fill=(245, 235, 210))
    d.rectangle([x + s * 0.44, y + s * 0.64, x + s * 0.56, y + s * 0.85], fill=(90, 60, 30))
    d.rectangle([x + s * 0.28, y + s * 0.60, x + s * 0.38, y + s * 0.70], fill=(120, 160, 200))
    d.rectangle([x + s * 0.62, y + s * 0.60, x + s * 0.72, y + s * 0.70], fill=(120, 160, 200))
    d.ellipse([x + s * 0.70, y + s * 0.10, x + s * 0.88, y + s * 0.28], fill=(240, 200, 60))


def icon_chart(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(220, 235, 245))
    d.rectangle([x + s * 0.12, y + s * 0.55, x + s * 0.26, y + s * 0.85], fill=(60, 120, 180))
    d.rectangle([x + s * 0.32, y + s * 0.42, x + s * 0.46, y + s * 0.85], fill=(40, 160, 90))
    d.rectangle([x + s * 0.52, y + s * 0.28, x + s * 0.66, y + s * 0.85], fill=(200, 60, 40))
    d.rectangle([x + s * 0.72, y + s * 0.52, x + s * 0.86, y + s * 0.85], fill=(230, 170, 40))
    d.line([x + s * 0.08, y + s * 0.85, x + s * 0.92, y + s * 0.85], fill=(40, 40, 40), width=2)
    d.line([x + s * 0.10, y + s * 0.70, x + s * 0.30, y + s * 0.55, x + s * 0.50, y + s * 0.62,
            x + s * 0.70, y + s * 0.35, x + s * 0.90, y + s * 0.22], fill=RED, width=3)


def icon_bank(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(228, 228, 222))
    d.polygon([(x + s * 0.10, y + s * 0.30), (x + s * 0.50, y + s * 0.12), (x + s * 0.90, y + s * 0.30)],
              fill=(90, 90, 90))
    d.rectangle([x + s * 0.14, y + s * 0.30, x + s * 0.86, y + s * 0.36], fill=(120, 120, 120))
    for i in range(4):
        cx = x + s * (0.20 + i * 0.20)
        d.rectangle([cx, y + s * 0.38, cx + s * 0.08, y + s * 0.78], fill=(150, 150, 150))
    d.rectangle([x + s * 0.10, y + s * 0.78, x + s * 0.90, y + s * 0.86], fill=(120, 120, 120))
    d.line([x + s * 0.55, y + s * 0.30, x + s * 0.45, y + s * 0.50, x + s * 0.60, y + s * 0.62],
           fill=RED, width=3)


def icon_server(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(40, 48, 64))
    for i in range(3):
        yy = y + s * (0.14 + i * 0.26)
        d.rectangle([x + s * 0.14, yy, x + s * 0.86, yy + s * 0.18], fill=(90, 105, 130))
        d.ellipse([x + s * 0.20, yy + s * 0.05, x + s * 0.28, yy + s * 0.13], fill=(80, 220, 120))
        d.ellipse([x + s * 0.32, yy + s * 0.05, x + s * 0.40, yy + s * 0.13], fill=(240, 60, 40))
    d.polygon([(x + s * 0.50, y + s * 0.62), (x + s * 0.68, y + s * 0.88), (x + s * 0.32, y + s * 0.88)],
              fill=(240, 190, 40))
    d.rectangle([x + s * 0.48, y + s * 0.72, x + s * 0.52, y + s * 0.82], fill=(40, 48, 64))
    d.ellipse([x + s * 0.47, y + s * 0.83, x + s * 0.53, y + s * 0.87], fill=(40, 48, 64))


def icon_gate(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 226, 238))
    d.rectangle([x, y + s * 0.68, x + s, y + s], fill=(140, 170, 120))
    for i in range(6):
        cx = x + s * (0.12 + i * 0.15)
        d.rectangle([cx, y + s * 0.30, cx + s * 0.05, y + s * 0.72], fill=(80, 80, 80))
    d.rectangle([x + s * 0.08, y + s * 0.30, x + s * 0.92, y + s * 0.38], fill=(150, 50, 40))
    d.rectangle([x + s * 0.08, y + s * 0.58, x + s * 0.92, y + s * 0.64], fill=(150, 50, 40))
    d.ellipse([x + s * 0.66, y + s * 0.08, x + s * 0.90, y + s * 0.26], fill=(240, 200, 60))


def icon_virus(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(245, 225, 225))
    import math
    cx, cy = x + s * 0.50, y + s * 0.52
    for ang in range(0, 360, 30):
        d.line([cx + 16 * math.cos(math.radians(ang)), cy + 16 * math.sin(math.radians(ang)),
                cx + 26 * math.cos(math.radians(ang)), cy + 26 * math.sin(math.radians(ang))],
               fill=RED, width=3)
    d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=(200, 60, 50))
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(245, 225, 225))
    d.ellipse([x + s * 0.16, y + s * 0.16, x + s * 0.26, y + s * 0.26], fill=RED)
    d.ellipse([x + s * 0.76, y + s * 0.20, x + s * 0.84, y + s * 0.28], fill=RED)
    d.ellipse([x + s * 0.74, y + s * 0.72, x + s * 0.82, y + s * 0.80], fill=RED)


def icon_pentagon(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(222, 228, 222))
    cx, cy, r = x + s * 0.50, y + s * 0.52, s * 0.34
    import math
    pts = [(cx + r * math.cos(math.radians(-90 + i * 72)),
            cy + r * math.sin(math.radians(-90 + i * 72))) for i in range(5)]
    d.polygon(pts, fill=(110, 120, 110))
    r2 = r * 0.55
    pts2 = [(cx + r2 * math.cos(math.radians(-90 + i * 72)),
             cy + r2 * math.sin(math.radians(-90 + i * 72))) for i in range(5)]
    d.polygon(pts2, fill=(200, 205, 195))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(110, 120, 110))


def icon_capitol(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(228, 232, 240))
    d.ellipse([x + s * 0.38, y + s * 0.22, x + s * 0.62, y + s * 0.52], fill=(245, 245, 245),
              outline=(120, 120, 120))
    d.rectangle([x + s * 0.42, y + s * 0.48, x + s * 0.58, y + s * 0.56], fill=(200, 200, 200))
    d.rectangle([x + s * 0.16, y + s * 0.56, x + s * 0.84, y + s * 0.62], fill=(220, 220, 220))
    for i in range(5):
        cx = x + s * (0.20 + i * 0.15)
        d.rectangle([cx, y + s * 0.62, cx + s * 0.06, y + s * 0.82], fill=(180, 180, 180))
    d.rectangle([x + s * 0.12, y + s * 0.82, x + s * 0.88, y + s * 0.88], fill=(160, 160, 160))
    d.rectangle([x + s * 0.48, y + s * 0.12, x + s * 0.52, y + s * 0.24], fill=(120, 120, 120))


def icon_desert(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(245, 225, 180))
    d.ellipse([x + s * 0.68, y + s * 0.08, x + s * 0.88, y + s * 0.28], fill=(240, 190, 60))
    d.polygon([(x, y + s * 0.62), (x + s * 0.35, y + s * 0.42), (x + s * 0.70, y + s * 0.62),
               (x + s, y + s * 0.48), (x + s, y + s), (x, y + s)], fill=(220, 180, 110))
    d.polygon([(x, y + s * 0.78), (x + s * 0.45, y + s * 0.62), (x + s, y + s * 0.80),
               (x + s, y + s), (x, y + s)], fill=(200, 155, 85))
    d.polygon([(x + s * 0.55, y + s * 0.42), (x + s * 0.62, y + s * 0.28), (x + s * 0.70, y + s * 0.42)],
              fill=(160, 120, 70))


def icon_chip(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(220, 235, 245))
    for i in range(4):
        d.rectangle([x + s * (0.18 + i * 0.18), y + s * 0.06, x + s * (0.24 + i * 0.18), y + s * 0.22],
                    fill=(90, 90, 90))
        d.rectangle([x + s * (0.18 + i * 0.18), y + s * 0.78, x + s * (0.24 + i * 0.18), y + s * 0.94],
                    fill=(90, 90, 90))
        d.rectangle([x + s * 0.06, y + s * (0.18 + i * 0.18), x + s * 0.22, y + s * (0.24 + i * 0.18)],
                    fill=(90, 90, 90))
        d.rectangle([x + s * 0.78, y + s * (0.18 + i * 0.18), x + s * 0.94, y + s * (0.24 + i * 0.18)],
                    fill=(90, 90, 90))
    d.rectangle([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78], fill=(30, 45, 70))
    d.rectangle([x + s * 0.32, y + s * 0.32, x + s * 0.68, y + s * 0.68], fill=(60, 140, 180))
    d.rectangle([x + s * 0.42, y + s * 0.42, x + s * 0.58, y + s * 0.58], fill=(200, 220, 240))


def icon_ball(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(120, 180, 110))
    d.rectangle([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92], outline=(255, 255, 255), width=2)
    d.ellipse([x + s * 0.08, y + s * 0.30, x + s * 0.92, y + s * 0.70], outline=(255, 255, 255), width=2)
    d.line([x + s * 0.50, y + s * 0.08, x + s * 0.50, y + s * 0.92], fill=(255, 255, 255), width=2)
    cx, cy, r = x + s * 0.50, y + s * 0.50, s * 0.20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=(40, 40, 40), width=2)
    import math
    for i in range(5):
        a = math.radians(-90 + i * 72)
        d.polygon([(cx, cy), (cx + r * 0.45 * math.cos(a - 0.35), cy + r * 0.45 * math.sin(a - 0.35)),
                   (cx + r * 0.45 * math.cos(a + 0.35), cy + r * 0.45 * math.sin(a + 0.35))], fill=(40, 40, 40))


ICONS = dict(bridge=icon_bridge, tanker=icon_tanker, flags=icon_flags, jet=icon_jet,
             house=icon_house, chart=icon_chart, bank=icon_bank, server=icon_server,
             gate=icon_gate, virus=icon_virus, pentagon=icon_pentagon, capitol=icon_capitol,
             desert=icon_desert, chip=icon_chip, ball=icon_ball)


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
        import math
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


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 104, W, 108], fill=GOLD)
    text(d, 14, 10, "THE DAY IN WORLD NEWS", font(SANS_B, 15), fill=GOLD)
    text(d, 14, 34, "Tuesday 17 November 2026", font(SERIF_B, 44), fill=(255, 255, 255))
    rx = 720
    text(d, rx, 12, "33 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY", font(SANS_B, 12),
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

    hy, hh = 116, 200
    cw = 328
    for i, s in enumerate(HEROES):
        x = 10 + i * (cw + 8)
        d.rectangle([x, hy, x + cw, hy + hh], fill=(255, 255, 255), outline=LINE, width=1)
        draw_hero_art(d, x + 1, hy + 1, cw - 2, 84, s["art"])
        d.rectangle([x, hy, x + cw, hy + 84], outline=LINE, width=1)
        text(d, x + 10, hy + 92, s["kicker"], font(SANS_B, 13), fill=RED)
        y_end = para(d, x + 10, hy + 110, s["head"], font(SERIF_B, 21), cw - 20, leading=24)
        para(d, x + 10, y_end + 3, s["deck"], font(SANS, 12), cw - 20, leading=15)

    gy, gh = 324, 100
    for i, s in enumerate(MEDIUM):
        r, c = divmod(i, 3)
        x = 10 + c * (cw + 8)
        y = gy + r * (gh + 6)
        d.rectangle([x, y, x + cw, y + gh], fill=(255, 255, 255), outline=LINE, width=1)
        ICONS[s["art"]](d, x + 6, y + 6, 76)
        d.rectangle([x + 6, y + 6, x + 82, y + 82], outline=LINE, width=1)
        badge(d, x + 6, y + 6, s["num"], s["cont"], r=10)
        tx = x + 90
        text(d, tx, y + 7, s["kicker"], font(SANS_B, 11), fill=RED)
        y_end = para(d, tx, y + 22, s["head"], font(SERIF_B, 16), cw - 98, leading=18)
        para(d, tx, y_end + 2, s["deck"], font(SANS, 11), cw - 98, leading=13)

    by = 756
    d.line([10, by - 6, 1014, by - 6], fill=INK, width=2)
    text(d, 10, by, "WHERE IT HAPPENED", font(SANS_B, 15))
    text(d, 10, by + 18, "numbers = stories 1\u201315 \u00b7 dots = briefs", font(SANS, 11), fill=GREY)
    draw_map(d, 10, by + 36, 470, 196)
    bx = 498
    text(d, bx, by, "ALSO ON TUESDAY 17 NOVEMBER", font(SANS_B, 15))
    d.line([bx, by + 20, 1014, by + 20], fill=LINE, width=1)
    colw = 252
    for i, (num, cat, txt) in enumerate(BRIEFS):
        col = i // 9
        row = i % 9
        x = bx + col * (colw + 12)
        y = by + 28 + row * 22
        badge(d, x, y, num, "Global", r=8)
        f = font(SANS_B, 10)
        d.text((x + 20, y + 1), cat + ": ", font=f, fill=TEAL)
        wcat = d.textlength(cat + ": ", font=f)
        para(d, x + 20 + wcat, y + 1, txt, font(SANS, 10), colw - 20 - wcat, leading=11)

    d.line([10, 990, 1014, 990], fill=INK, width=1)
    text(d, 10, 994,
         "Every story here happened or was first reported on Tuesday 17 November 2026. Disputed claims are attributed.",
         font(SANS, 11), fill=GREY)
    text(d, 10, 1007,
         "Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera \u00b7 CNN \u00b7 The Guardian \u00b7 CNBC. Original drawings \u2014 no photographs.",
         font(SANS, 11), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes", img.size)


if __name__ == "__main__":
    main()
