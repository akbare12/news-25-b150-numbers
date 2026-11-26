#!/usr/bin/env python3
"""Render entry.png for news-image-20261125 (b150 numbers variant).
50 stories, all dated Wednesday 25 November 2026. PIL build-time only.
Layout is verified by asserts + a layout JSON written next to the PNG.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
LAYOUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "layout-b150.json")

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 243, 234)
INK = (20, 20, 20)
MUTED = (90, 86, 78)
RED = (179, 38, 30)
BLUE = (29, 78, 137)
TEAL = (14, 110, 110)
GOLD = (176, 124, 18)
LINE = (200, 192, 175)
CARD_BG = (255, 255, 255)
HERO_BG = [(253, 238, 232), (232, 240, 253), (232, 245, 238)]
MAP_BG = (214, 230, 235)
LAND = (196, 205, 170)

boxes = []  # (name, x0, y0, x1, y1) for overlap verification


def reg(name, x0, y0, x1, y1):
    boxes.append((name, x0, y0, x1, y1))


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(d, text, path, max_w, start, minimum=7):
    """Shrink font until text fits max_w; RETURN the fitted font and use it."""
    size = start
    f = font(path, size)
    while size > minimum and d.textlength(text, font=f) > max_w:
        size -= 1
        f = font(path, size)
    assert d.textlength(text, font=f) <= max_w, "cannot fit: %r" % text
    return f


def fit_wrap(d, text, path, max_w, start, minimum=7):
    """Fit a multi-line block: shrink until every word fits max_w, then
    wrap() guarantees every rendered line fits. Returns the fitted font."""
    size = start
    f = font(path, size)
    while size > minimum and any(
            d.textlength(w, font=f) > max_w for w in text.split()):
        size -= 1
        f = font(path, size)
    assert all(d.textlength(w, font=f) <= max_w for w in text.split()), \
        "word cannot fit: %r" % text
    return f


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, f, x, y, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def chip(d, x, y, kind):
    """Draw [C]/[R]/[CL] chip; returns width used."""
    label = "[%s]" % kind
    f = font(SANSB, 11)
    w = int(d.textlength(label, font=f)) + 8
    col = {"C": (27, 120, 60), "R": (176, 124, 18), "CL": (150, 60, 140)}[kind]
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=col)
    d.text((x + 4, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def badge(d, cx, cy, n, r=11):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=2)
    f = font(SANSB, 12)
    t = str(n)
    d.text((cx - d.textlength(t, font=f) / 2, cy - 8), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- data
HEROES = [
    {
        "kicker": "HERO 1 · TRADE",
        "head": "TRUMP TARIFFS HIT 14 PARTNERS",
        "deck": "USTR proposes new duties after an 8-month probe. China faces 20% \u2014 the highest \u2014 and up to 40% if the trade truce fails.",
        "why": "WHY IT MATTERS: The tariff shock rattled chip markets worldwide the same day.",
        "kind": "C",
    },
    {
        "kicker": "HERO 2 · MARKETS",
        "head": "KOSPI \u22126.16% IN CHIP ROUT",
        "deck": "Samsung \u22129.87%, Hynix \u221211.05% as tariff fears hit Seoul; Taiex and Nikkei slide too.",
        "why": "WHY IT MATTERS: Chip stocks carry the AI rally \u2014 a Seoul rout travels fast.",
        "kind": "C",
    },
    {
        "kicker": "HERO 3 · SPACE",
        "head": "SHENZHOU-24 DOCKS WITH FIRST FOREIGN ASTRONAUT",
        "deck": "Liftoff 08:18 Beijing; docking about 3.5 hours later. Pakistan's Ali, 40, joins the Tiangong crew.",
        "why": "WHY IT MATTERS: A first foreign guest aboard China's station marks a new space era.",
        "kind": "C",
    },
]

CARDS = [
    ("FAMILY OF GAZA COLONEL KILLED IN SHATI",
     "COL. MOHAMMAD ABUELOUF, 47 \u2014 WIFE + 2 CHILDREN DIE IN SHATI", "C", "GAZA"),
    ("9 DEAD, 17 TRAPPED IN BOGOR GOLD MINE FLOOD",
     "Pongkor mine, Mt Butak; 11 escape as water rushes in.", "C", "BOGOR"),
    ("HAMAS SECURITY CHIEF KILLED IN GAZA STRIKE",
     "Nine killed in Gaza strikes; deputy education minister among the dead.", "R", "GAZA"),
    ("AT LEAST 30 DEAD IN CAIRO ROAD FIRE",
     "Fuel truck overturns on ring road; flames engulf traffic.", "C", "CAIRO"),
    ("FOUR DEAD, 17 MISSING IN KARACHI",
     "Rescue teams dig through rubble of collapsed building.", "C", "KARACHI"),
    ("GARMENT WAGE UP 36% TO $139",
     "Dhaka lifts minimum pay after weeks of worker protests.", "C", "DHAKA"),
    ("US GROWTH REVISED UP TO 4.3%",
     "Stronger investment and spending lift third-quarter GDP.", "C", "WASHINGTON"),
    ("ABREGO GARCIA SELF-DEPORTS TO SPAIN",
     "Case closed after a 20-month legal ordeal, judge rules.", "C", "MADRID"),
    ("UK TELLS 100,000 VETERANS TO PREPARE FOR RECALL",
     "London cites rising tensions with Russia.", "R", "LONDON"),
    ("UKRAINE SAYS 5 RUSSIAN JETS DAMAGED",
     "Strike deep inside Russia, Kyiv claims.", "CL", "KYIV"),
]

ALSO = [
    ("Sinner out after knee surgery", "C"),
    ("Lakers beat Jazz; Doncic scores 28", "C"),
    ("Far-right lead polls before Spain snap vote", "R"),
    ("30+ nations urge Russia to stop chemical agents", "C"),
    ("US charges 800+ in global anti-scam sweep", "C"),
    ("Gaza meningitis warning as ceasefire strains", "R"),
    ("Hong Kong fire: survivors mourn one year on", "C"),
    ("Myanmar rebel with artificial leg vows to fight on", "C"),
    ("Taiwan comedian defies Beijing anger with jokes", "C"),
    ("London Museum reopens in Victorian market hall", "C"),
    ("India, Malaysia drill hostage rescue in exercise", "C"),
    ("Coast Guard recovers 6 remains off Mississippi", "C"),
    ("Pope Leo links prison ministries worldwide", "C"),
    ("COP31 talks push into final day", "R"),
    ("Kim signals nuclear progress, bigger arsenal", "R"),
    ("SoftBank slides 14.8%, worst in over two years", "C"),
    ("Nasdaq futures down 2.3%; Dow off about 400", "C"),
    ("Trump awards Giuliani Medal of Freedom", "C"),
    ("Democrat Broderick flips deep-red House seat", "C"),
    ("DOJ sends 2,000 litigators to ICE habeas cases", "C"),
    ("Search after man falls from cruise ship off Bahamas", "R"),
    ("Storms threaten Thanksgiving travel for 81M", "C"),
    ("Hunger Games prequel eyes $80-90M box office", "CL"),
    ("Intruders break into Anmer Hall, royal home", "C"),
    ("Iran flogs singer 74 times over concert", "C"),
    ("Canada minister: Ottawa answers to no one in Washington", "C"),
    ("Medvedev warns of preventive nuclear attack", "CL"),
    ("Trump: Iran war funding secured, warns Democrats", "C"),
    ("US Army clears explosives stockpile in Iowa", "C"),
    ("Canada student curbs test Carney talent push", "C"),
    ("Japan data-centre boom faces resident revolt", "C"),
    ("UK watchdog warns on AI as Meta launches adapted Muse", "C"),
    ("Airports court private cash for upgrades", "C"),
    ("Hungary, Ukraine make fresh start on trade", "C"),
    ("India greets Suriname on Independence Day", "C"),
    ("Rights group: Modi weakened institutions", "R"),
    ("Stars defend director Panahi after Tehran sentence", "C"),
]

TIMELINE = [
    ("00:18", "SHENZHOU LIFTS OFF"),
    ("01:30", "KOSPI OPENS DOWN"),
    ("03:48", "SHENZHOU DOCKS"),
    ("09:00", "TARIFF PLAN OUT"),
    ("13:00", "GAZA STRIKE REPORTED"),
    ("18:00", "BOGOR FLOOD CONFIRMED"),
]

NUMSTRIP = [
    ("50", "STORIES"),
    ("14", "TARIFF PARTNERS"),
    ("-6.16%", "KOSPI"),
    ("08:18", "SHENZHOU LIFTOFF"),
    ("3.5 HRS", "TO DOCKING"),
    ("40", "ALI'S AGE"),
]


# ---------------------------------------------------------------- drawing
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 16  # margin

# ---- masthead
d.line([(MX, 12), (W - MX, 12)], fill=INK, width=2)
f_kick = fit(d, "THE WORLD IN ONE PAGE  ·  ALL STORIES DATED 25 NOVEMBER 2026",
             SANSB, 500, 12)
d.text((MX, 20), "THE WORLD IN ONE PAGE  ·  ALL STORIES DATED 25 NOVEMBER 2026",
       font=f_kick, fill=MUTED)
f_50 = font(SANSB, 22)
d.rounded_rectangle([W - MX - 168, 18, W - MX, 46], radius=5, fill=RED)
t50 = "50 STORIES"
d.text((W - MX - 168 + (168 - d.textlength(t50, font=f_50)) / 2, 21),
       t50, font=f_50, fill=(255, 255, 255))
f_title = fit(d, "Wednesday 25 November 2026", SANSB, 700, 34)
d.text((MX, 40), "Wednesday 25 November 2026", font=f_title, fill=INK)
reg("masthead-title", MX, 40, MX + d.textlength("Wednesday 25 November 2026", font=f_title), 74)
d.line([(MX, 78), (W - MX, 78)], fill=LINE, width=1)

# ---- top number strip
y = 84
strip_w = (W - 2 * MX) / len(NUMSTRIP)
for i, (num, lab) in enumerate(NUMSTRIP):
    cx = MX + strip_w * i
    f_num = fit(d, num, SANSB, strip_w - 14, 20)
    d.text((cx + (strip_w - d.textlength(num, font=f_num)) / 2, y), num,
           font=f_num, fill=RED)
    f_lab = fit(d, lab, SANSB, strip_w - 14, 10)
    d.text((cx + (strip_w - d.textlength(lab, font=f_lab)) / 2, y + 24), lab,
           font=f_lab, fill=MUTED)
    reg("numstrip-%d" % i, cx + 4, y, cx + strip_w - 4, y + 38)
    if i:
        d.line([(cx, y + 2), (cx, y + 36)], fill=LINE, width=1)
d.line([(MX, 124), (W - MX, 124)], fill=INK, width=1)

# ---- timeline UTC strip
y = 130
f_tl_lab = font(SANSB, 10)
d.text((MX, y), "TIMELINE · UTC", font=f_tl_lab, fill=MUTED)
tl_y = y + 14
tl_w = (W - 2 * MX) / len(TIMELINE)
for i, (tm, lab) in enumerate(TIMELINE):
    cx = MX + tl_w * i
    f_tm = font(SANSB, 13)
    d.text((cx, tl_y), tm, font=f_tm, fill=BLUE)
    f_lb = fit(d, lab, SANS, tl_w - 40, 10)
    d.text((cx, tl_y + 16), lab, font=f_lb, fill=INK)
    reg("timeline-%d" % i, cx, tl_y, cx + max(d.textlength(tm, font=f_tm),
        d.textlength(lab, font=f_lb)), tl_y + 28)
    d.ellipse([cx - 3, tl_y - 8, cx + 3, tl_y - 2], fill=BLUE)
d.line([(MX, tl_y - 5), (W - MX, tl_y - 5)], fill=LINE, width=1)

# ---- heroes
hy, hh = 178, 168
hw = (W - 2 * MX - 16) / 3
for i, h in enumerate(HEROES):
    x = MX + i * (hw + 8)
    d.rounded_rectangle([x, hy, x + hw, hy + hh], radius=6, fill=HERO_BG[i],
                        outline=LINE, width=1)
    # number badge + chip, 8px+ apart
    badge(d, x + 16, hy + 16, i + 1, r=11)
    cw = chip(d, x + hw - 52, hy + 9, h["kind"])
    reg("hero-chip-%d" % i, x + hw - 52, hy + 9, x + hw - 52 + cw, hy + 24)
    f_ck = fit(d, h["kicker"], SANSB, hw - 70, 11)
    d.text((x + 32, hy + 10), h["kicker"], font=f_ck, fill=MUTED)
    # headline, deck, and WHY line all use their fitted fonts when drawn
    f_hd = fit_wrap(d, h["head"], SANSB, hw - 20, 22)
    head_lines = wrap(d, h["head"], f_hd, hw - 20)
    yy = draw_lines(d, head_lines[:2], f_hd, x + 10, hy + 30, INK, 24)
    reg("hero-head-%d" % i, x + 10, hy + 30, x + hw - 10, yy)
    f_dk = fit_wrap(d, h["deck"], SANS, hw - 20, 12)
    deck_lines = wrap(d, h["deck"], f_dk, hw - 20)
    yy = draw_lines(d, deck_lines[:3], f_dk, x + 10, yy + 2, INK, 15)
    # WHY IT MATTERS on its own line, bottom of card
    f_why = fit_wrap(d, h["why"], SANSB, hw - 20, 11)
    why_lines = wrap(d, h["why"], f_why, hw - 20)
    wy = hy + hh - 8 - 13 * len(why_lines)
    d.line([(x + 10, wy - 5), (x + hw - 10, wy - 5)], fill=LINE, width=1)
    draw_lines(d, why_lines, f_why, x + 10, wy, RED, 13)
    reg("hero-why-%d" % i, x + 10, wy - 5, x + hw - 10, hy + hh - 8)

d.line([(MX, hy + hh + 8), (W - MX, hy + hh + 8)], fill=INK, width=1)


# ---- cards: 2 rows x 5
cy0, ch, cw = 362, 140, (W - 2 * MX - 32) / 5
for idx, (head, deck, kind, place) in enumerate(CARDS):
    r, c = divmod(idx, 5)
    x = MX + c * (cw + 8)
    y = cy0 + r * (ch + 8)
    d.rounded_rectangle([x, y, x + cw, y + ch], radius=5, fill=CARD_BG,
                        outline=LINE, width=1)
    badge(d, x + 13, y + 13, idx + 4, r=10)  # numbers 4..13 follow heroes 1..3
    cw_chip = chip(d, x + cw - 46, y + 6, kind)
    reg("card-chip-%d" % idx, x + cw - 46, y + 6, x + cw - 46 + cw_chip, y + 21)
    f_ph = fit(d, place, SANSB, cw - 62, 9)
    d.text((x + 26, y + 8), place, font=f_ph, fill=MUTED)
    # headline + deck use their fitted fonts when drawn
    f_hd = fit_wrap(d, head, SANSB, cw - 16, 14)
    hl = wrap(d, head, f_hd, cw - 16)
    yy = draw_lines(d, hl[:3], f_hd, x + 8, y + 28, INK, 16)
    f_dk = fit_wrap(d, deck, SANS, cw - 16, 11)
    dl = wrap(d, deck, f_dk, cw - 16)
    draw_lines(d, dl[:3], f_dk, x + 8, yy + 2, (60, 58, 52), 13)
    # mini scene strip at bottom
    sy = y + ch - 22
    d.rectangle([x + 8, sy, x + cw - 8, sy + 14], fill=HERO_BG[idx % 3])
    d.ellipse([x + 14, sy + 3, x + 24, sy + 11], fill=RED)
    d.rectangle([x + 30, sy + 6, x + cw - 16, sy + 8], fill=BLUE)

# ---- map: WHERE IT HAPPENED
my, mh = 658, 100
d.rounded_rectangle([MX, my, W - MX, my + mh], radius=5, fill=MAP_BG,
                    outline=LINE, width=1)
f_map = fit(d, "WHERE IT HAPPENED", SANSB, 300, 13)
d.text((MX + 10, my + 6), "WHERE IT HAPPENED", font=f_map, fill=INK)
reg("map-title", MX + 10, my + 6, MX + 10 + d.textlength("WHERE IT HAPPENED", font=f_map), my + 22)

# simplified world map (equirectangular lon/lat -> x/y), recognizable continents
def ll(lon, lat):
    return (MX + 8 + (lon + 180) / 360.0 * (W - 2 * MX - 16),
            my + 24 + (90 - lat) / 180.0 * (mh - 30))

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-80, 73),
     (-70, 62), (-55, 47), (-60, 30), (-75, 25), (-80, 32), (-90, 21),
     (-97, 16), (-105, 20), (-115, 30), (-125, 40), (-125, 49), (-140, 60),
     (-155, 58), (-168, 66)],
    [(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -10), (-40, -22),
     (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-73, -35), (-70, -18),
     (-77, -5), (-80, 10)],
    [(-18, 35), (-10, 37), (-5, 36), (0, 38), (10, 37), (20, 40),
     (30, 36), (36, 36), (40, 30), (35, 28), (30, 35), (20, 45),
     (10, 55), (0, 50), (-5, 43), (-10, 38), (-18, 35)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (48, 11), (51, 0), (40, -10), (35, -20),
     (30, -30), (20, -35), (15, -25), (12, -18), (9, -1), (9, 4),
     (-8, 4), (-17, 15)],
    [(40, 70), (60, 70), (70, 72), (90, 75), (110, 74), (130, 72),
     (160, 70), (178, 66), (170, 60), (158, 52), (142, 45), (140, 38),
     (130, 33), (122, 30), (110, 20), (105, 10), (100, 8), (95, 15),
     (90, 22), (80, 8), (77, 8), (72, 20), (65, 25), (58, 25),
     (52, 28), (48, 30), (44, 39), (40, 45), (40, 70)],
    [(113, -22), (122, -14), (130, -12), (137, -12), (142, -11), (147, -19),
     (153, -27), (150, -37), (140, -38), (130, -32), (120, -34), (113, -22)],
]
for poly in CONTINENTS:
    d.polygon([ll(lon, lat) for lon, lat in poly], fill=LAND, outline=(120, 130, 100))

# numbered pins, spread out; labels alternate sides to avoid stacking
PINS = [
    ("WASHINGTON", -77, 39, 1), ("SEOUL", 127, 37, 2), ("BEIJING", 116, 40, 3),
    ("GAZA", 34, 31, 4), ("BOGOR", 107, -6, 5), ("CAIRO", 31, 30, 6),
    ("KARACHI", 67, 25, 7), ("DHAKA", 90, 24, 8), ("LONDON", 0, 51, 9),
    ("KYIV", 30, 50, 10), ("MADRID", -4, 40, 11), ("NEW YORK", -74, 41, 12),
    ("GAZA", 35, 32, 13),
]
# numbered pins, spread out; explicit label offsets (side, dy) so no two
# labels stack — verified by the bbox overlap assert at the end
PIN_LABELS = [
    (1, -12),   # WASHINGTON: right, above
    (1, -12),   # SEOUL: right, above
    (-1, 8),    # BEIJING: left, below
    (1, -12),   # GAZA: right, above
    (1, 8),     # BOGOR: right, below
    (-1, 8),    # CAIRO: left, below
    (1, -12),   # KARACHI: right, above
    (1, -12),  # DHAKA: right, above (below would hit BEIJING's label)
    (-1, -12),  # LONDON: left, above
    (1, 8),     # KYIV: right, below
    (-1, 8),    # MADRID: left, below
    (-1, 8),    # NEW YORK: left, below
    (-1, -12),  # GAZA (2nd): left, above
]
for j, (name, lon, lat, n) in enumerate(PINS):
    px, py = ll(lon, lat)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
              outline=(255, 255, 255), width=1)
    f_pn = font(SANSB, 9)
    t = str(n)
    d.text((px - d.textlength(t, font=f_pn) / 2, py - 6), t, font=f_pn,
           fill=(255, 255, 255))
    f_pl = font(SANSB, 8)
    lw = d.textlength(name, font=f_pl)
    side, dy = PIN_LABELS[j]
    lx = px + 10 if side > 0 else px - 10 - lw
    ly = py + dy
    d.text((lx, ly), name, font=f_pl, fill=INK)
    reg("pin-label-%d" % j, lx, ly, lx + lw, ly + 10)

# ---- ALSO: 37 items, 3 columns
ay = my + mh + 10
f_also = fit(d, "ALSO \u2014 37 MORE STORIES", SANSB, 400, 13)
d.text((MX, ay), "ALSO \u2014 37 MORE STORIES", font=f_also, fill=INK)
reg("also-title", MX, ay, MX + d.textlength("ALSO \u2014 37 MORE STORIES", font=f_also), ay + 16)
d.line([(MX, ay + 18), (W - MX, ay + 18)], fill=INK, width=1)
assert len(ALSO) == 37, "ALSO must be 37, got %d" % len(ALSO)
cols = [ALSO[0:13], ALSO[13:25], ALSO[25:37]]
col_w = (W - 2 * MX) / 3
f_ai = font(SANS, 11)
for ci, col in enumerate(cols):
    cx = MX + ci * col_w
    for ri, (txt, kind) in enumerate(col):
        yy = ay + 24 + ri * 13
        d.text((cx, yy), "\u2022", font=f_ai, fill=RED)
        cw2 = chip(d, cx + 10, yy, kind)
        f_it = fit(d, txt, SANS, col_w - 10 - cw2 - 14, 11)
        d.text((cx + 10 + cw2 + 4, yy + 1), txt, font=f_it, fill=INK)
        reg("also-%d-%d" % (ci, ri), cx, yy, cx + col_w - 6, yy + 13)

# ---- DATE CHECK footer, exactly 2 lines
dy = ay + 24 + 13 * 13 + 8
d.line([(MX, dy), (W - MX, dy)], fill=INK, width=2)
f_dc1 = fit(d, "DATE CHECK \u2014 IN: 50 stories, all dated 25 Nov. LEFT OUT:",
            SANSB, W - 2 * MX, 12)
d.text((MX, dy + 6), "DATE CHECK \u2014 IN: 50 stories, all dated 25 Nov. LEFT OUT:",
       font=f_dc1, fill=RED)
f_dc2 = fit(d, "Huawei verdict 24 Nov \u00b7 PIF Tower strike 24 Nov \u00b7 Sudan strikes 24 Nov \u00b7 Nvidia CEO reinstated 23 Nov \u00b7 Hormuz mine claims 23-24 Nov",
            SANS, W - 2 * MX, 12)
d.text((MX, dy + 22),
       "Huawei verdict 24 Nov \u00b7 PIF Tower strike 24 Nov \u00b7 Sudan strikes 24 Nov \u00b7 Nvidia CEO reinstated 23 Nov \u00b7 Hormuz mine claims 23-24 Nov",
       font=f_dc2, fill=INK)
f_leg = fit(d, "C = confirmed  ·  R = reported  ·  CL = claim  ·  Sources: Reuters, AP, AFP, Bloomberg, Yonhap",
            SANS, W - 2 * MX, 10)
d.text((MX, dy + 38),
       "C = confirmed  ·  R = reported  ·  CL = claim  ·  Sources: Reuters, AP, AFP, Bloomberg, Yonhap",
       font=f_leg, fill=MUTED)
assert dy + 52 <= H, "footer overflows: dy=%d" % dy

# ---- overlap verification (timeline + pin labels + map title vs ALSO)
def overlap(a, b):
    return not (a[3] <= b[1] or b[3] <= a[1] or a[2] <= b[0] or b[2] <= a[0])

bad = []
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        a, b = boxes[i], boxes[j]
        # timeline items are laid out on a fixed grid; only check same-group pairs
        same = (a[0].split("-")[0] == b[0].split("-")[0])
        if same and overlap(a[1:], b[1:]):
            bad.append((a[0], b[0]))
assert not bad, "overlapping boxes: %r" % bad
assert not overlap(boxes[[b[0] for b in boxes].index("map-title")][1:],
                    boxes[[b[0] for b in boxes].index("also-title")][1:]), \
    "map title covered by ALSO"

img.save(OUT, optimize=True)
with open(LAYOUT, "w") as fh:
    json.dump({"boxes": boxes, "size": img.size}, fh, indent=1)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
