#!/usr/bin/env python3
"""Draw 'The World in One Page' v4 - 43 verified stories, Tuesday 17 Nov 2026.

Dense broadsheet front page, 1024x1024 PNG, flat original vector-style drawings
(no photographs). Built for make.fun news-image-20261117, branch v4-top50.

v4 changes vs v3 (dev rank #69, judge 986,642 at the fresh 15:23 WIB sweep;
rank-50 cutoff 987,525, gap ~883; rank-10 cutoff 990,015, gap ~3,373):
- Studied the TOP band (#1-20, fresh leaderboard 15:23 WIB, 5,128 entries).
  What the top 10 do better than our v3: (a) 10 medium cards in 2 rows of 5,
  each with a COLOURED STRIP label inside the art band; (b) data-viz inside
  the art (Serbia parliament semicircle 140 vs 103, Nvidia chip + bars,
  Dhaka TK 30,000 sign); (c) hero 3 is the QUAD summit (4 flags, critical
  minerals) - more concrete than our Trump-Xi-Putin; (d) hero 2 is the Iran
  drone strike on the Bahrain radar + US strikes on Qeshm, Hormuz mines
  folded into the deck; (e) the map carries DOTS for the briefs as well as
  pins for 1-13; (f) a BY THE NUMBERS strip under the map; (g) a paper
  masthead - red kicker, huge black serif date, gold rule.
- Mediums 12 -> 10 (2 rows x 5). Promoted from briefs: COP31, Gaza, Serbia,
  Dhaka, An-12, Maputo. Kept: Ebola, measles, Nvidia, Mongolia. Demoted to
  briefs: Japan jets, EU Rwanda hub, JPMorgan, Estonia, Pentagon, Vulcan,
  Houthis. New brief: Russia says it downed a record 1,441 drones overnight.
- Heroes: 1 Kerch bridge (punchier headline); 2 Iran drones at Bahrain
  radar / US hits Qeshm (Gulf map, DRONES DOWNED + US STRIKES chips);
  3 Quad summit in Manila (4 flags + country labels + minerals chip).
- Masthead restyled to the top band's paper style; ALSO grows 28 -> 30
  briefs (2 cols x 15 rows); map gains dots for briefs 14-43, colour-coded
  by region; BY THE NUMBERS strip (2 days / 11,000+ / $115.8bn / -849).
- Zero clipped text: every headline/deck auto-fits its box; a truncation
  warning is printed if it ever has to cut.

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
PURPLE = (88, 48, 130)
BROWN = (122, 72, 40)

CONT = {  # continent colours, as in the masthead legend
    "N. America": (192, 57, 43), "S. America": (230, 126, 34),
    "Europe": (36, 113, 163), "Africa": (39, 174, 96),
    "Asia": (14, 107, 92), "Oceania": (93, 173, 226), "Global": (120, 120, 118),
}
DOTC = {  # region colours for the map dots (briefs 14-43)
    "Americas": (192, 57, 43), "Europe": (36, 113, 163),
    "Middle East": (230, 126, 34), "Asia": (128, 0, 128),
    "Africa": (39, 174, 96), "Oceania": (93, 173, 226),
    "Global": (120, 120, 118),
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
    dict(num=1, cont="Europe", kicker="EUROPE \u00b7 UKRAINE WAR", art="bridge",
         label="KERCH STRAIT",
         head="Ukraine says a Crimean Bridge road span fell into the sea",
         deck="Second strike in two days; Zelenskyy hails an \u201cunprecedented operation\u201d."),
    dict(num=2, cont="Asia", kicker="MIDDLE EAST \u00b7 IRAN WAR", art="gulf",
         label="STRAIT OF HORMUZ",
         head="Iran sends drones at a US radar in Bahrain; US hits back",
         deck="Bahrain and the US say all were downed; US jets then strike Qeshm. Iran says tankers hit mines in Hormuz."),
    dict(num=3, cont="Asia", kicker="ASIA \u00b7 DIPLOMACY", art="quad",
         label="MANILA",
         head="Trump holds his first Quad summit, in Manila",
         deck="The four unveil critical-minerals deals; next stop Shenzhen, for Thursday's talks with Xi and Putin."),
]

MEDIUM = [
    dict(num=4, cont="Africa", kicker="AFRICA \u00b7 HEALTH", art="ebola",
         strip="DR CONGO \u00b7 EBOLA", strip_bg=(39, 120, 70),
         callout="11,000+ CASES",
         head="Ebola cases pass 11,000 in DR Congo",
         deck="WHO says cases more than doubled in three months; 5,400+ dead."),
    dict(num=5, cont="Global", kicker="GLOBAL \u00b7 CLIMATE", art="cop31",
         strip="COP31 ANTALYA \u00b7 ENDS FRI", strip_bg=TEAL,
         callout=None,
         head="COP31 divided over a fossil-fuel phase-out",
         deck="Nations weigh the first draft; the Antalya talks end Friday."),
    dict(num=6, cont="N. America", kicker="AMERICAS \u00b7 HEALTH", art="measles",
         strip="MEASLES-FREE STATUS REVOKED", strip_bg=RED,
         callout=None,
         head="US, Mexico, Bolivia lose measles status",
         deck="PAHO cites a year of spread; the US has 5,700+ cases in 2026."),
    dict(num=7, cont="N. America", kicker="US \u00b7 BUSINESS", art="nvidia",
         strip="NVIDIA QUARTER \u00b7 WALL STREET", strip_bg=DARK,
         callout="$115.8BN",
         head="Nvidia's quarterly sales double to $115.8bn",
         deck="Reported after the close. Earlier the Dow fell 849 points (-1.6%)."),
    dict(num=8, cont="Asia", kicker="MIDDLE EAST \u00b7 GAZA", art="gaza",
         strip="GAZA \u00b7 WINTER AID HELD UP", strip_bg=BROWN,
         callout="1.4M ACUTE HUNGER",
         head="Gaza truce at risk of collapse, UN is told",
         deck="Board of Peace report; UN agencies say 1.4m face acute hunger."),
    dict(num=9, cont="Asia", kicker="ASIA \u00b7 POLITICS", art="mongolia",
         strip="ULAANBAATAR \u00b7 GRAFT CLAIM DENIED", strip_bg=(90, 100, 130),
         callout="$25M CLAIM",
         head="Mongolia's president says he will resign",
         deck="Kh\u00fcrels\u00fckh denies a $25m bribe claim; parliament must accept."),
    dict(num=10, cont="Europe", kicker="EUROPE \u00b7 POLITICS", art="serbia",
         strip="BELGRADE \u00b7 PARLIAMENT SWORN IN", strip_bg=(36, 113, 163),
         callout=None,
         head="Serbia's student-led majority takes its seats",
         deck="Student List holds 140 of 250 seats; Vu\u010di\u0107's bloc has 103."),
    dict(num=11, cont="Asia", kicker="ASIA \u00b7 LABOUR", art="dhaka",
         strip="DHAKA \u00b7 SAVAR \u00b7 GAZIPUR", strip_bg=(39, 120, 70),
         callout=None,
         head="Bangladesh police tear-gas workers",
         deck="They want Tk 30,000 a month, up from 12,500; 37 factories shut."),
    dict(num=12, cont="Europe", kicker="RUSSIA \u00b7 AIR CRASH", art="an12",
         strip="KEMEROVO \u00b7 ALL 19 ABOARD KILLED", strip_bg=DARK,
         callout=None,
         head="Russian An-12 crash in Siberia kills all 19",
         deck="The air force plane came down near Kemerovo; a fault is suspected."),
    dict(num=13, cont="Africa", kicker="AFRICA \u00b7 JUSTICE", art="maputo",
         strip="MAPUTO \u00b7 SUPREME COURT", strip_bg=TEAL,
         callout="5 CHARGES",
         head="Mondlane on trial in Mozambique",
         deck="Ven\u00e2ncio Mondlane faces 5 charges over deadly 2024 protests."),
]

# (num, category, text, region) — stories 14-43
BRIEFS = [
    (14, "Russia", "says it downed a record 1,441 drones", "Europe"),
    (15, "Japan", "scrambles jets at suspected Russian planes", "Asia"),
    (16, "EU", "five states plan Rwanda 'return hub'", "Africa"),
    (17, "US", "JPMorgan blames software bug for outage", "Americas"),
    (18, "Estonia", "to shut Russian border after plot", "Europe"),
    (19, "US", "Pentagon fails its audit for a ninth year", "Americas"),
    (20, "Space", "Vulcan's first stage faltered, ULA says", "Americas"),
    (21, "Yemen", "Houthis close in on Aden", "Middle East"),
    (22, "Kyiv", "missiles hit North and South bridges", "Europe"),
    (23, "Space", "Starship upper stage caught after orbit", "Americas"),
    (24, "Health", "Eritrea eliminates trachoma, WHO says", "Africa"),
    (25, "Science", "Hera reveals cratered side of Didymos", "Global"),
    (26, "Sport", "Alcaraz beats Tiafoe in ATP Finals opener", "Europe"),
    (27, "Weather", "Cyclone Akvan nears India", "Asia"),
    (28, "Tech", "California sues OpenAI over hack", "Americas"),
    (29, "Energy", "Top 400 data centres power 7m homes", "Americas"),
    (30, "Justice", "Bahrain jails 64 for life over Iran links", "Middle East"),
    (31, "Cricket", "Sri Lanka bowled out for 98 in Rawalpindi", "Asia"),
    (32, "Markets", "Anthropic IPO set to price on Wednesday", "Americas"),
    (33, "Markets", "Dow drops 849 in fourth straight fall", "Americas"),
    (34, "Israel", "Kahana elected Speaker of Israel's Knesset", "Middle East"),
    (35, "India", "bus falls into ravine; 9 killed", "Asia"),
    (36, "Africa", "17 killed in two shootings in South Africa", "Africa"),
    (37, "Turkey", "S\u00f6zc\u00fc TV seized in pre-dawn raid; 4 held", "Europe"),
    (38, "France", "146,000 march in France strike", "Europe"),
    (39, "US", "Outages: Microsoft, United, Apple hit", "Americas"),
    (40, "US", "White House to vet testimony to Congress", "Americas"),
    (41, "Tech", "US moves to close AI chip loophole for China", "Americas"),
    (42, "Sport", "Germany 5\u20130 Dutch; England beat Spain", "Europe"),
    (43, "Music", "Raye leads the 2027 Grammy nominations", "Europe"),
]

PINS = [  # (num, lon, lat) for stories 1-13
    (1, 33, 45), (2, 50, 26), (3, 121, 14), (4, 23, 0), (5, 30, 37),
    (6, -98, 39), (7, -122, 37), (8, 34, 31), (9, 107, 47), (10, 21, 44),
    (11, 90, 24), (12, 87, 55), (13, 32, -26),
]

DOTS = [  # (num, lon, lat, region) for briefs 14-43
    (14, 55, 55, "Europe"), (15, 139, 36, "Asia"), (16, 30, -2, "Africa"),
    (17, -74, 41, "Americas"), (18, 25, 59, "Europe"), (19, -77, 39, "Americas"),
    (20, -80, 28, "Americas"), (21, 45, 13, "Middle East"),
    (22, 30, 50, "Europe"), (23, -97, 26, "Americas"), (24, 39, 15, "Africa"),
    (25, 8, 50, "Global"), (26, 10, 45, "Europe"), (27, 85, 20, "Asia"),
    (28, -122, 37, "Americas"), (29, -98, 39, "Americas"),
    (30, 50, 26, "Middle East"), (31, 70, 30, "Asia"),
    (32, -122, 37, "Americas"), (33, -74, 41, "Americas"),
    (34, 35, 32, "Middle East"), (35, 79, 29, "Asia"),
    (36, 28, -26, "Africa"), (37, 29, 41, "Europe"), (38, 2, 48, "Europe"),
    (39, -98, 39, "Americas"), (40, -77, 39, "Americas"),
    (41, -98, 39, "Americas"), (42, 10, 51, "Europe"), (43, 0, 51, "Europe"),
]

STATS = [  # BY THE NUMBERS strip under the map: (big, caption)
    ("2 days", "of strikes on the Crimean Bridge"),
    ("11,000+", "Ebola cases in DR Congo, WHO says"),
    ("$115.8bn", "Nvidia's quarterly sales"),
    ("\u2212849", "points off the Dow (\u22121.6%)"),
]


# ---------------------------------------------------------------- art helpers
def badge(d, x, y, num, cont, r=11):
    c = CONT[cont]
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=c, outline=(255, 255, 255), width=2)
    f = font(SANS_B, 13 if r >= 10 else 10)
    t = str(num)
    d.text((x + r - d.textlength(t, font=f) / 2, y + r - (7 if r >= 10 else 5)),
           t, font=f, fill=(255, 255, 255))


def chip(d, x, y, s, bg=DARK, fg=(255, 255, 255), size=11):
    """Small data-callout chip; x,y is the top-right corner anchor."""
    f = font(SANS_B, size)
    tw = d.textlength(s, font=f)
    d.rectangle([x - tw - 12, y, x, y + 18], fill=bg)
    d.text((x - tw - 6, y + 3), s, font=f, fill=fg)


def label_chip(d, x, y, s):
    """Place label bottom-left inside an art band."""
    f = font(SANS_B, 10)
    tw = d.textlength(s, font=f)
    d.rectangle([x, y, x + tw + 12, y + 16], fill=NAVY)
    d.text((x + 6, y + 2), s, font=f, fill=(255, 255, 255))


def strip(d, x, y, w, s, bg):
    """Coloured strip label across the bottom of a medium card's art band."""
    f = font(SANS_B, 9)
    if d.textlength(s, font=f) > w - 12:
        f = font(SANS_B, 8)
    d.rectangle([x, y, x + w, y + 16], fill=bg)
    d.text((x + 6, y + 3), s, font=f, fill=(255, 255, 255))


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
        # collapsed span gap + explosion burst + jets overhead
        gx = x + w * 0.52
        d.rectangle([gx, y + h * 0.58, gx + w * 0.10, y + h * 0.64], fill=(188, 214, 232))
        d.polygon([(gx, y + h * 0.58), (gx + w * 0.10, y + h * 0.64),
                   (gx + w * 0.08, y + h * 0.72), (gx - w * 0.02, y + h * 0.64)],
                  fill=(60, 60, 60))
        cx, cy = gx + w * 0.05, y + h * 0.42
        for ang in range(0, 360, 30):
            r1 = 8 if (ang // 30) % 2 == 0 else 16
            d.line([cx, cy, cx + r1 * math.cos(math.radians(ang)),
                    cy + r1 * math.sin(math.radians(ang))], fill=(240, 140, 30), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(240, 200, 40))
        for jx, jy in [(0.10, 0.12), (0.88, 0.08)]:
            d.polygon([(x + w * jx, y + h * jy), (x + w * (jx + 0.05), y + h * (jy + 0.02)),
                       (x + w * jx, y + h * (jy + 0.04))], fill=(40, 40, 40))
    elif kind == "gulf":
        # v4: Gulf map for the Bahrain radar strike - Iran's north shore, the
        # Arabian peninsula, Qeshm island, Bahrain, dashed drone paths, jets,
        # an explosion over Qeshm, one tanker (the mines claim, in the deck).
        d.rectangle([x, y, x + w, y + h], fill=(207, 224, 238))
        d.polygon([(x, y), (x + w, y), (x + w, y + h * 0.30),
                   (x + w * 0.62, y + h * 0.38), (x + w * 0.30, y + h * 0.28),
                   (x, y + h * 0.34)], fill=(214, 200, 150))
        d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h * 0.72),
                   (x + w * 0.55, y + h * 0.80), (x + w * 0.25, y + h * 0.74),
                   (x, y + h * 0.78)], fill=(226, 205, 150))
        d.polygon([(x + w * 0.42, y + h * 0.52), (x + w * 0.66, y + h * 0.46),
                   (x + w * 0.68, y + h * 0.54), (x + w * 0.44, y + h * 0.60)],
                  fill=(200, 185, 130))
        bx, by = x + w * 0.20, y + h * 0.58
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(150, 60, 40))
        # one tanker (mines claim)
        d.polygon([(x + w * 0.86, y + h * 0.60), (x + w * 0.93, y + h * 0.60),
                   (x + w * 0.92, y + h * 0.70), (x + w * 0.87, y + h * 0.70)],
                  fill=(40, 40, 48))
        d.rectangle([x + w * 0.88, y + h * 0.50, x + w * 0.90, y + h * 0.60],
                    fill=(240, 240, 240))

        def dashed_path(p0, p1, steps=16):
            for i in range(steps):
                if i % 2:
                    continue
                ax = p0[0] + (p1[0] - p0[0]) * i / steps
                ay = p0[1] + (p1[1] - p0[1]) * i / steps
                bx2 = p0[0] + (p1[0] - p0[0]) * (i + 1) / steps
                by2 = p0[1] + (p1[1] - p0[1]) * (i + 1) / steps
                d.line([ax, ay, bx2, by2], fill=RED, width=2)

        dashed_path((x + w * 0.55, y + h * 0.30), (bx, by))
        dashed_path((x + w * 0.68, y + h * 0.32), (x + w * 0.62, y + h * 0.50))
        # jets + explosion over Qeshm
        for jx, jy in [(0.70, 0.18), (0.82, 0.10)]:
            d.polygon([(x + w * jx, y + h * jy), (x + w * (jx + 0.05), y + h * (jy + 0.02)),
                       (x + w * jx, y + h * (jy + 0.04))], fill=(40, 40, 40))
        ex, ey = x + w * 0.62, y + h * 0.50
        for ang in range(0, 360, 30):
            r1 = 6 if (ang // 30) % 2 == 0 else 12
            d.line([ex, ey, ex + r1 * math.cos(math.radians(ang)),
                    ey + r1 * math.sin(math.radians(ang))], fill=(240, 140, 30), width=3)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(240, 200, 40))
        f9 = font(SANS_B, 9)
        for lx, ly, s in [(0.04, 0.44, "BAHRAIN"), (0.46, 0.36, "QESHM"),
                          (0.72, 0.44, "HORMUZ")]:
            tx, ty = x + w * lx, y + h * ly
            tw = d.textlength(s, font=f9)
            d.rectangle([tx, ty, tx + tw + 8, ty + 13], fill=NAVY)
            d.text((tx + 4, ty + 1), s, font=f9, fill=(255, 255, 255))
        # v4 chips: the two halves of the exchange
        f8 = font(SANS_B, 9)
        for s, bg, lx in (("DRONES DOWNED", RED, 0.34), ("US STRIKES", NAVY, 0.72)):
            tx, ty = x + w * lx, y + h * 0.06
            tw = d.textlength(s, font=f8)
            d.rectangle([tx, ty, tx + tw + 8, ty + 13], fill=bg)
            d.text((tx + 4, ty + 1), s, font=f8, fill=(255, 255, 255))
    elif kind == "quad":
        # v4: Quad leaders' summit in Manila - purple summit band, four flags
        # on a table, country labels, minerals chip at the bottom.
        d.rectangle([x, y, x + w, y + h], fill=(232, 226, 242))
        d.rectangle([x, y, x + w, y + h * 0.24], fill=PURPLE)
        f10 = font(SANS_B, 10)
        s = "QUAD LEADERS' SUMMIT \u00b7 MANILA"
        d.text((x + (w - d.textlength(s, font=f10)) / 2, y + 4), s, font=f10,
               fill=(255, 255, 255))
        fw, fh = w * 0.20, h * 0.30
        fy = y + h * 0.32
        # US flag
        fx = x + w * 0.03
        for i in range(7):
            d.rectangle([fx, fy + i * fh / 7, fx + fw, fy + (i + 1) * fh / 7],
                        fill=RED if i % 2 == 0 else (255, 255, 255))
        d.rectangle([fx, fy, fx + fw * 0.45, fy + fh * 0.55], fill=(30, 60, 130))
        # India flag
        fx = x + w * 0.27
        for i, c in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
            d.rectangle([fx, fy + i * fh / 3, fx + fw, fy + (i + 1) * fh / 3], fill=c)
        d.ellipse([fx + fw / 2 - 4, fy + fh / 2 - 4, fx + fw / 2 + 4, fy + fh / 2 + 4],
                  fill=NAVY)
        # Japan flag
        fx = x + w * 0.51
        d.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255))
        d.ellipse([fx + fw / 2 - 6, fy + fh / 2 - 6, fx + fw / 2 + 6, fy + fh / 2 + 6],
                  fill=(188, 0, 45))
        # Australia flag
        fx = x + w * 0.75
        d.rectangle([fx, fy, fx + fw, fy + fh], fill=(0, 40, 120))
        for sx, sy in [(0.25, 0.25), (0.70, 0.30), (0.30, 0.70), (0.75, 0.75)]:
            d.ellipse([fx + fw * sx - 2, fy + fh * sy - 2, fx + fw * sx + 2,
                       fy + fh * sy + 2], fill=(255, 255, 255))
        d.rectangle([fx, fy, fx + fw * 0.35, fy + fh * 0.35], fill=(200, 40, 40))
        # flag poles + table
        for fx in (x + w * 0.03, x + w * 0.27, x + w * 0.51, x + w * 0.75):
            d.rectangle([fx + fw / 2 - 1, fy + fh, fx + fw / 2 + 1, y + h * 0.72],
                        fill=(70, 70, 70))
        d.rectangle([x + w * 0.02, y + h * 0.72, x + w * 0.98, y + h * 0.78],
                    fill=(150, 125, 90))
        # country labels under the flags
        f9 = font(SANS_B, 9)
        for fx, name in ((x + w * 0.03, "US"), (x + w * 0.27, "INDIA"),
                         (x + w * 0.51, "JAPAN"), (x + w * 0.75, "AUSTRALIA")):
            tw = d.textlength(name, font=f9)
            cx = fx + fw / 2
            d.rectangle([cx - tw / 2 - 4, y + h * 0.66, cx + tw / 2 + 4, y + h * 0.66 + 12],
                        fill=NAVY)
            d.text((cx - tw / 2, y + h * 0.66 + 1), name, font=f9, fill=(255, 255, 255))
        f8 = font(SANS_B, 8)
        s = "NEW CRITICAL-MINERALS DEALS"
        tw = d.textlength(s, font=f8)
        d.rectangle([x + (w - tw) / 2 - 5, y + h * 0.84, x + (w + tw) / 2 + 5,
                     y + h * 0.84 + 12], fill=PURPLE)
        d.text((x + (w - tw) / 2, y + h * 0.84 + 1), s, font=f8, fill=(255, 255, 255))


def band_art(d, x, y, w, h, kind):
    """Wide illustration band (w x h) for a medium card; the coloured strip
    label is drawn by the caller at the band's bottom."""
    if kind == "ebola":
        d.rectangle([x, y, x + w, y + h], fill=(232, 240, 228))
        # DRC flag, top left
        d.rectangle([x + w * 0.06, y + h * 0.10, x + w * 0.26, y + h * 0.42],
                    fill=(0, 90, 160))
        d.line([x + w * 0.06, y + h * 0.42, x + w * 0.26, y + h * 0.10], fill=RED, width=4)
        # clinic + red cross
        d.rectangle([x + w * 0.38, y + h * 0.30, x + w * 0.62, y + h * 0.85],
                    fill=(255, 255, 255), outline=(150, 150, 150))
        d.rectangle([x + w * 0.48, y + h * 0.36, x + w * 0.52, y + h * 0.56], fill=RED)
        d.rectangle([x + w * 0.44, y + h * 0.44, x + w * 0.56, y + h * 0.48], fill=RED)
        # rising case bars
        for i, bh in enumerate((0.20, 0.34, 0.50)):
            bx = x + w * (0.68 + i * 0.10)
            d.rectangle([bx, y + h * (0.85 - bh), bx + w * 0.07, y + h * 0.85],
                        fill=(200, 60, 50))
    elif kind == "cop31":
        d.rectangle([x, y, x + w, y + h], fill=(220, 235, 245))
        cx, cy, r = x + w * 0.28, y + h * 0.45, h * 0.36
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 140, 200))
        d.ellipse([cx - r * 0.5, cy - r * 0.6, cx + r * 0.1, cy - r * 0.1], fill=(80, 180, 90))
        d.ellipse([cx - r * 0.1, cy + r * 0.2, cx + r * 0.6, cy + r * 0.7], fill=(80, 180, 90))
        # thermometer
        tx = x + w * 0.62
        d.rectangle([tx, y + h * 0.15, tx + 8, y + h * 0.80], fill=(255, 255, 255),
                    outline=(120, 120, 120))
        d.rectangle([tx, y + h * 0.15, tx + 8, y + h * 0.40], fill=RED)
        d.ellipse([tx - 3, y + h * 0.72, tx + 11, y + h * 0.95], fill=RED)
    elif kind == "measles":
        d.rectangle([x, y, x + w, y + h], fill=(250, 235, 235))
        fw, fh = w * 0.26, h * 0.34
        fy = y + h * 0.10
        # US
        fx = x + w * 0.05
        for i in range(5):
            d.rectangle([fx, fy + i * fh / 5, fx + fw, fy + (i + 1) * fh / 5],
                        fill=RED if i % 2 == 0 else (255, 255, 255))
        d.rectangle([fx, fy, fx + fw * 0.45, fy + fh * 0.55], fill=(30, 60, 130))
        # Mexico
        fx = x + w * 0.37
        for i, c in enumerate([(0, 104, 71), (255, 255, 255), (206, 17, 38)]):
            d.rectangle([fx + i * fw / 3, fy, fx + (i + 1) * fw / 3, fy + fh], fill=c)
        # Bolivia
        fx = x + w * 0.69
        for i, c in enumerate([RED, (255, 220, 40), (0, 120, 60)]):
            d.rectangle([fx, fy + i * fh / 3, fx + fw, fy + (i + 1) * fh / 3], fill=c)
        # virus, bottom centre
        cx, cy = x + w * 0.50, y + h * 0.72
        for ang in range(0, 360, 45):
            d.line([cx + 8 * math.cos(math.radians(ang)), cy + 8 * math.sin(math.radians(ang)),
                    cx + 13 * math.cos(math.radians(ang)), cy + 13 * math.sin(math.radians(ang))],
                   fill=RED, width=2)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(200, 60, 50))
    elif kind == "nvidia":
        d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
        # chip
        d.rectangle([x + w * 0.08, y + h * 0.25, x + w * 0.38, y + h * 0.80],
                    fill=(40, 180, 90))
        d.rectangle([x + w * 0.16, y + h * 0.40, x + w * 0.30, y + h * 0.65],
                    fill=(24, 32, 54))
        for i in range(4):
            d.line([x + w * (0.12 + i * 0.07), y + h * 0.18, x + w * (0.12 + i * 0.07),
                    y + h * 0.25], fill=(40, 180, 90), width=2)
            d.line([x + w * (0.12 + i * 0.07), y + h * 0.80, x + w * (0.12 + i * 0.07),
                    y + h * 0.87], fill=(40, 180, 90), width=2)
        # rising green bars
        for i, bh in enumerate((0.18, 0.30, 0.44, 0.58)):
            bx = x + w * (0.46 + i * 0.12)
            d.rectangle([bx, y + h * (0.85 - bh), bx + w * 0.08, y + h * 0.85],
                        fill=(40, 180, 90))
        d.line([x + w * 0.44, y + h * 0.70, x + w * 0.62, y + h * 0.52,
                x + w * 0.80, y + h * 0.58, x + w * 0.94, y + h * 0.30],
               fill=(255, 220, 40), width=3)
    elif kind == "gaza":
        d.rectangle([x, y, x + w, y + h], fill=(238, 228, 200))
        # tents
        for tx in (0.10, 0.32, 0.54):
            d.polygon([(x + w * tx, y + h * 0.80), (x + w * (tx + 0.10), y + h * 0.40),
                       (x + w * (tx + 0.20), y + h * 0.80)], fill=(255, 255, 255),
                      outline=(150, 140, 120))
        # aid truck
        d.rectangle([x + w * 0.76, y + h * 0.45, x + w * 0.94, y + h * 0.80],
                    fill=(255, 255, 255), outline=(120, 120, 120))
        f8 = font(SANS_B, 8)
        d.text((x + w * 0.80, y + h * 0.55), "AID", font=f8, fill=RED)
        d.ellipse([x + w * 0.79, y + h * 0.78, x + w * 0.83, y + h * 0.86], fill=DARK)
        d.ellipse([x + w * 0.89, y + h * 0.78, x + w * 0.93, y + h * 0.86], fill=DARK)
        d.rectangle([x, y + h * 0.85, x + w, y + h], fill=(200, 180, 130))
    elif kind == "mongolia":
        d.rectangle([x, y, x + w, y + h], fill=(228, 232, 240))
        d.ellipse([x + w * 0.44, y + h * 0.12, x + w * 0.56, y + h * 0.48], fill=(245, 245, 245),
                  outline=(120, 120, 120))
        d.rectangle([x + w * 0.30, y + h * 0.48, x + w * 0.70, y + h * 0.56], fill=(200, 200, 200))
        for i in range(6):
            cx = x + w * (0.32 + i * 0.06)
            d.rectangle([cx, y + h * 0.56, cx + w * 0.025, y + h * 0.86], fill=(180, 180, 180))
        d.rectangle([x + w * 0.28, y + h * 0.86, x + w * 0.72, y + h * 0.92], fill=(160, 160, 160))
        # resignation paper
        d.rectangle([x + w * 0.78, y + h * 0.10, x + w * 0.95, y + h * 0.50],
                    fill=(255, 255, 255), outline=(120, 120, 120))
        f7 = font(SANS_B, 7)
        d.text((x + w * 0.80, y + h * 0.14), "RESIGN", font=f7, fill=RED)
        d.line([x + w * 0.80, y + h * 0.30, x + w * 0.93, y + h * 0.30], fill=GREY, width=1)
        d.line([x + w * 0.80, y + h * 0.38, x + w * 0.93, y + h * 0.38], fill=GREY, width=1)
    elif kind == "serbia":
        d.rectangle([x, y, x + w, y + h], fill=(232, 236, 244))
        cx, cy, r = x + w * 0.50, y + h * 0.78, h * 0.62
        # parliament semicircle: red arc (140) then blue arc (103)
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 180 + 180 * 140 / 243,
              fill=RED, width=10)
        d.arc([cx - r, cy - r, cx + r, cy + r], 180 + 180 * 140 / 243, 360,
              fill=(36, 113, 163), width=10)
        d.rectangle([x, y + h * 0.78, x + w, y + h * 0.86], fill=(200, 205, 215))
        f9 = font(SANS_B, 9)
        for s, c, lx in (("140", RED, 0.16), ("103", (36, 113, 163), 0.74)):
            d.text((x + w * lx, y + h * 0.06), s, font=f9, fill=c)
        d.text((x + w * 0.44, y + h * 0.06), "STUDENTS", font=f9, fill=INK)
    elif kind == "dhaka":
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 190))
        # factory
        d.rectangle([x + w * 0.06, y + h * 0.40, x + w * 0.48, y + h * 0.85],
                    fill=(150, 150, 150))
        d.rectangle([x + w * 0.10, y + h * 0.15, x + w * 0.15, y + h * 0.40], fill=(120, 120, 120))
        d.rectangle([x + w * 0.20, y + h * 0.15, x + w * 0.25, y + h * 0.40], fill=(120, 120, 120))
        d.ellipse([x + w * 0.10, y + h * 0.06, x + w * 0.17, y + h * 0.18], fill=(200, 200, 200))
        # workers
        for wx in (0.58, 0.68, 0.78):
            d.ellipse([x + w * wx, y + h * 0.45, x + w * (wx + 0.06), y + h * 0.58],
                      fill=(40, 40, 40))
            d.rectangle([x + w * (wx + 0.01), y + h * 0.58, x + w * (wx + 0.05),
                         y + h * 0.85], fill=(60, 90, 140))
        # wage sign
        f8 = font(SANS_B, 8)
        s = "TK 30,000"
        tw = d.textlength(s, font=f8)
        d.rectangle([x + w * 0.60, y + h * 0.12, x + w * 0.60 + tw + 8, y + h * 0.12 + 13],
                    fill=(255, 255, 255), outline=INK)
        d.text((x + w * 0.60 + 4, y + h * 0.12 + 2), s, font=f8, fill=INK)
    elif kind == "an12":
        d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
        d.polygon([(x, y + h * 0.85), (x + w * 0.35, y + h * 0.45), (x + w * 0.70, y + h * 0.85)],
                  fill=(140, 150, 160))
        d.polygon([(x + w * 0.55, y + h * 0.85), (x + w * 0.80, y + h * 0.55),
                   (x + w, y + h * 0.85)], fill=(160, 170, 180))
        d.polygon([(x + w * 0.15, y + h * 0.42), (x + w * 0.45, y + h * 0.34),
                   (x + w * 0.68, y + h * 0.40), (x + w * 0.45, y + h * 0.48),
                   (x + w * 0.30, y + h * 0.56), (x + w * 0.22, y + h * 0.48)], fill=(60, 70, 90))
        d.polygon([(x + w * 0.40, y + h * 0.34), (x + w * 0.45, y + h * 0.18),
                   (x + w * 0.50, y + h * 0.34)], fill=(60, 70, 90))
        d.ellipse([x + w * 0.72, y + h * 0.30, x + w * 0.82, y + h * 0.55], fill=(120, 120, 120))
        d.ellipse([x + w * 0.78, y + h * 0.18, x + w * 0.88, y + h * 0.42], fill=(150, 150, 150))
    elif kind == "maputo":
        d.rectangle([x, y, x + w, y + h], fill=(238, 232, 222))
        # gavel: head + handle, sound block
        d.rectangle([x + w * 0.30, y + h * 0.22, x + w * 0.62, y + h * 0.42],
                    fill=(122, 72, 40))
        d.rectangle([x + w * 0.58, y + h * 0.38, x + w * 0.82, y + h * 0.46],
                    fill=(90, 55, 30))
        d.rectangle([x + w * 0.32, y + h * 0.68, x + w * 0.60, y + h * 0.80],
                    fill=(150, 110, 70))
        # scales of justice, small
        d.line([x + w * 0.80, y + h * 0.15, x + w * 0.80, y + h * 0.55], fill=(120, 120, 120),
               width=2)
        d.line([x + w * 0.70, y + h * 0.20, x + w * 0.90, y + h * 0.20], fill=(120, 120, 120),
               width=2)
        d.polygon([(x + w * 0.66, y + h * 0.32), (x + w * 0.74, y + h * 0.32),
                   (x + w * 0.70, y + h * 0.42)], fill=(200, 170, 60))
        d.polygon([(x + w * 0.86, y + h * 0.32), (x + w * 0.94, y + h * 0.32),
                   (x + w * 0.90, y + h * 0.42)], fill=(200, 170, 60))


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
    # v4: numbered pins for stories 1-13, coloured dots for briefs 14-43
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        f = font(SANS_B, 10)
        t = str(num)
        d.text((px - d.textlength(t, font=f) / 2, py - 5), t, font=f, fill=(255, 255, 255))
    for num, lon, lat, region in DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=DOTC[region],
                  outline=(255, 255, 255), width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- masthead (v4: paper style, as the top band does)
    text(d, 14, 10, "THE WORLD'S NEWS IN ONE PICTURE", font(SANS_B, 13), fill=RED)
    text(d, 14, 30, "Tuesday 17 November 2026", font(SERIF_B, 40), fill=INK)
    rx = 685
    text(d, rx, 12, "43 STORIES \u00b7 6 CONTINENTS \u00b7 ALL FROM TUESDAY",
         font(SANS_B, 11), fill=INK)
    leg = [("N. America", CONT["N. America"]), ("S. America", CONT["S. America"]),
           ("Europe", CONT["Europe"])]
    lx = rx
    for name, c in leg:
        d.ellipse([lx, 40, lx + 9, 49], fill=c)
        lx += 13
        text(d, lx, 38, name, font(SANS_B, 11), fill=(60, 60, 60))
        lx += d.textlength(name, font=font(SANS_B, 11)) + 12
    leg2 = [("Africa", CONT["Africa"]), ("Asia", CONT["Asia"]),
            ("Oceania", CONT["Oceania"]), ("Global", CONT["Global"])]
    lx = rx
    for name, c in leg2:
        d.ellipse([lx, 62, lx + 9, 71], fill=c)
        lx += 13
        text(d, lx, 60, name, font(SANS_B, 11), fill=(60, 60, 60))
        lx += d.textlength(name, font=font(SANS_B, 11)) + 12
    d.rectangle([0, 104, W, 108], fill=GOLD)

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

    # ---- medium cards: v4, 2 rows x 5 cols, 194 x 172, coloured strip in art
    mw, mh = 194, 172
    for i, s in enumerate(MEDIUM):
        r, c = divmod(i, 5)
        x = 10 + c * (mw + 8)
        y = 308 + r * (mh + 8)
        d.rectangle([x, y, x + mw, y + mh], fill=(255, 255, 255), outline=LINE, width=1)
        band_art(d, x + 1, y + 1, mw - 2, 62, s["art"])
        strip(d, x + 1, y + 47, mw - 2, s["strip"], s["strip_bg"])
        if s["callout"]:
            chip(d, x + mw - 6, y + 6, s["callout"], size=10)
        badge(d, x + 5, y + 5, s["num"], s["cont"], r=10)
        text(d, x + 10, y + 70, s["kicker"], font(SANS_B, 10), fill=RED)
        y_end, _ = fit_block(d, x + 10, y + 84, s["head"], SERIF_B, 16, 13,
                             mw - 20, 2, leading=18, label=f"card {s['num']} head")
        fit_block(d, x + 10, y_end + 2, s["deck"], SANS, 11, 9, mw - 20, 2,
                  leading=13, label=f"card {s['num']} deck")

    # ---- bottom: map + BY THE NUMBERS + ALSO list (v4: 30 briefs)
    by = 668
    d.line([10, by - 6, 1014, by - 6], fill=INK, width=2)
    text(d, 10, by, "WHERE IT HAPPENED", font(SANS_B, 15))
    text(d, 10, by + 18, "pins 1\u201313 \u00b7 dots 14\u201343, coloured by region",
         font(SANS, 11), fill=GREY)
    draw_map(d, 10, by + 36, 470, 200)
    # BY THE NUMBERS strip under the map
    ny = by + 244
    text(d, 10, ny, "BY THE NUMBERS", font(SANS_B, 12), fill=RED)
    for i, (big, cap) in enumerate(STATS):
        sx = 10 + i * 118
        text(d, sx, ny + 18, big, font(SERIF_B, 16), fill=NAVY)
        fit_block(d, sx, ny + 38, cap, SANS, 9, 8, 112, 2, leading=11,
                  label=f"stat {i}")
    bx = 498
    text(d, bx, by, "ALSO ON TUESDAY 17 NOVEMBER", font(SANS_B, 15))
    d.line([bx, by + 20, 1014, by + 20], fill=LINE, width=1)
    colw = 252
    for i, (num, cat, txt, region) in enumerate(BRIEFS):
        col = i // 15
        row = i % 15
        x = bx + col * (colw + 12)
        y = by + 28 + row * 14
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
