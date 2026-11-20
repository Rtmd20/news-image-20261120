#!/usr/bin/env python3
"""Draw the v2 news-image entry: 'THE WORLD LEDGER' front page for
Friday 20 November 2026. Every letter is rendered text (Pillow), so no
word can garble. Output: entry.png, 1024x1024, well under 1 MiB.
Run: python3 draw.py  (writes entry.png next to this file)
"""
import glob
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (248, 243, 230)
INK = (25, 25, 25)
NAVY = (22, 54, 92)
RED = (166, 28, 28)
GOLD = (185, 138, 29)
TEAL = (14, 107, 92)
LIGHT = (238, 231, 211)
GREY = (90, 90, 90)
CREAM_LINE = (210, 198, 170)


def find_font(bold=False, serif=False):
    """Locate a usable TTF on this machine; fall back to Pillow's default."""
    if serif and bold:
        cands = ["**/NotoSerifDisplay-Black.ttf", "**/NotoSerif-Bold.ttf",
                 "**/DejaVuSerif-Bold.ttf", "**/LiberationSerif-Bold.ttf"]
    elif serif:
        cands = ["**/NotoSerif-Regular.ttf", "**/DejaVuSerif.ttf",
                 "**/LiberationSerif-Regular.ttf"]
    elif bold:
        cands = ["**/NotoSans-Bold.ttf", "**/DejaVuSans-Bold.ttf",
                 "**/LiberationSans-Bold.ttf"]
    else:
        cands = ["**/NotoSans-Regular.ttf", "**/DejaVuSans.ttf",
                 "**/LiberationSans-Regular.ttf"]
    for pat in cands:
        hits = sorted(glob.glob(os.path.join("/usr/share/fonts", pat),
                                recursive=True))
        if hits:
            return hits[0]
    return None


_FONTS = {}


def font(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _FONTS:
        path = find_font(bold, serif)
        if path:
            _FONTS[key] = ImageFont.truetype(path, size)
        else:
            _FONTS[key] = ImageFont.load_default()
    return _FONTS[key]


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, s, f, x, y, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, s, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(f.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- icons
def icon_bridge(d, x, y, s, col):
    d.line([(x, y + s * 0.62), (x + s, y + s * 0.62)], fill=col, width=3)
    for cx in (x + s * 0.25, x + s * 0.75):
        d.arc([cx - s * 0.22, y + s * 0.30, cx + s * 0.22, y + s * 0.95],
              start=180, end=360, fill=col, width=3)
    d.line([(x + s * 0.10, y + s * 0.30), (x + s * 0.10, y + s * 0.62)],
           fill=col, width=3)
    d.line([(x + s * 0.90, y + s * 0.30), (x + s * 0.90, y + s * 0.62)],
           fill=col, width=3)


def icon_cyclone(d, x, y, s, col):
    for i, r in enumerate((0.48, 0.36, 0.24)):
        d.arc([x + s * (0.5 - r), y + s * (0.5 - r),
               x + s * (0.5 + r), y + s * (0.5 + r)],
              start=20 + i * 70, end=300 + i * 70, fill=col, width=3)


def icon_missile(d, x, y, s, col):
    pts = [(x + s * 0.5, y + s * 0.05), (x + s * 0.72, y + s * 0.45),
           (x + s * 0.60, y + s * 0.80), (x + s * 0.40, y + s * 0.80),
           (x + s * 0.28, y + s * 0.45)]
    d.polygon(pts, fill=col)
    d.line([(x + s * 0.5, y + s * 0.82), (x + s * 0.5, y + s * 0.98)],
           fill=(220, 120, 40), width=3)


def icon_chart(d, x, y, s, col):
    d.line([(x + s * 0.08, y + s * 0.85), (x + s * 0.92, y + s * 0.85)],
           fill=col, width=2)
    d.line([(x + s * 0.08, y + s * 0.85), (x + s * 0.08, y + s * 0.10)],
           fill=col, width=2)
    pts = [(x + s * 0.10, y + s * 0.25), (x + s * 0.35, y + s * 0.45),
           (x + s * 0.60, y + s * 0.35), (x + s * 0.88, y + s * 0.75)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(x + s * 0.88, y + s * 0.75), (x + s * 0.80, y + s * 0.68),
               (x + s * 0.82, y + s * 0.82)], fill=RED)


def icon_leaf(d, x, y, s, col):
    d.ellipse([x + s * 0.12, y + s * 0.12, x + s * 0.88, y + s * 0.88],
              outline=col, width=3)
    d.polygon([(x + s * 0.5, y + s * 0.28), (x + s * 0.72, y + s * 0.55),
               (x + s * 0.5, y + s * 0.72), (x + s * 0.28, y + s * 0.55)],
              fill=col)


def icon_flags(d, x, y, s, col):
    d.rectangle([x + s * 0.06, y + s * 0.18, x + s * 0.44, y + s * 0.62],
                fill=(255, 255, 255), outline=col, width=2)
    d.line([(x + s * 0.06, y + s * 0.40), (x + s * 0.44, y + s * 0.40)],
           fill=RED, width=3)
    d.line([(x + s * 0.25, y + s * 0.18), (x + s * 0.25, y + s * 0.62)],
           fill=RED, width=3)
    d.rectangle([x + s * 0.56, y + s * 0.18, x + s * 0.94, y + s * 0.62],
                fill=(30, 60, 140))
    for dx, dy in ((0.66, 0.30), (0.75, 0.28), (0.84, 0.32), (0.70, 0.42),
                   (0.80, 0.45)):
        d.ellipse([x + s * dx - 2, y + s * dy - 2, x + s * dx + 2,
                   y + s * dy + 2], fill=GOLD)


def icon_placard(d, x, y, s, col):
    d.rectangle([x + s * 0.12, y + s * 0.10, x + s * 0.88, y + s * 0.52],
                fill=(255, 255, 255), outline=col, width=2)
    d.line([(x + s * 0.5, y + s * 0.52), (x + s * 0.5, y + s * 0.95)],
           fill=col, width=3)
    d.text((x + s * 0.40, y + s * 0.14), "!", font=font(int(s * 0.32), True),
           fill=RED)


def icon_bars(d, x, y, s, col):
    for i, h in enumerate((0.30, 0.50, 0.72)):
        bx = x + s * (0.12 + i * 0.30)
        d.rectangle([bx, y + s * (0.92 - h), bx + s * 0.20, y + s * 0.92],
                    fill=col)


def icon_ship(d, x, y, s, col):
    d.polygon([(x + s * 0.05, y + s * 0.55), (x + s * 0.95, y + s * 0.55),
               (x + s * 0.82, y + s * 0.85), (x + s * 0.18, y + s * 0.85)],
              fill=col)
    d.rectangle([x + s * 0.30, y + s * 0.30, x + s * 0.48, y + s * 0.55],
                fill=(200, 80, 40))
    d.rectangle([x + s * 0.52, y + s * 0.30, x + s * 0.70, y + s * 0.55],
                fill=GOLD)


def icon_flame(d, x, y, s, col):
    d.polygon([(x + s * 0.5, y + s * 0.05), (x + s * 0.78, y + s * 0.45),
               (x + s * 0.85, y + s * 0.75), (x + s * 0.60, y + s * 0.95),
               (x + s * 0.30, y + s * 0.95), (x + s * 0.15, y + s * 0.70),
               (x + s * 0.28, y + s * 0.45)], fill=col)


def icon_bat(d, x, y, s, col):
    d.line([(x + s * 0.30, y + s * 0.85), (x + s * 0.70, y + s * 0.15)],
           fill=col, width=5)
    d.ellipse([x + s * 0.62, y + s * 0.62, x + s * 0.88, y + s * 0.88],
              fill=RED)


def icon_car(d, x, y, s, col):
    d.rectangle([x + s * 0.08, y + s * 0.45, x + s * 0.92, y + s * 0.68],
                fill=col)
    d.polygon([(x + s * 0.30, y + s * 0.45), (x + s * 0.38, y + s * 0.25),
               (x + s * 0.62, y + s * 0.25), (x + s * 0.70, y + s * 0.45)],
              fill=col)
    for cx in (0.28, 0.72):
        d.ellipse([x + s * (cx - 0.09), y + s * 0.62,
                   x + s * (cx + 0.09), y + s * 0.80], fill=INK)


def icon_calendar(d, x, y, s, col):
    d.rectangle([x + s * 0.10, y + s * 0.15, x + s * 0.90, y + s * 0.90],
                fill=(255, 255, 255), outline=col, width=2)
    d.rectangle([x + s * 0.10, y + s * 0.15, x + s * 0.90, y + s * 0.35],
                fill=RED)
    d.text((x + s * 0.28, y + s * 0.42), "20", font=font(int(s * 0.34), True),
           fill=INK)


ICONS = {1: icon_bridge, 2: icon_cyclone, 3: icon_missile, 4: icon_chart,
         5: icon_leaf, 6: icon_flags, 7: icon_placard, 8: icon_bars,
         9: icon_ship, 10: icon_flame, 11: icon_bat, 12: icon_car,
         13: icon_calendar}

# ---------------------------------------------------------------- data
# 13 drawn stories: (number, place, source, band colour, headline, deck)
STORIES = [
    (1, "KYIV", "KYIV INDEPENDENT", NAVY,
     "RUSSIA'S NIGHT BARRAGE HITS THREE KYIV BRIDGES",
     "84 cruise and 27 ballistic missiles, 404 drones; power and water cut, at least nine dead."),
    (2, "ODISHA", "IMD", TEAL,
     "CYCLONE AKVAN SLAMS INTO INDIA'S EAST COAST",
     "Landfall near Gopalpur at 70-80 km/h; 372,000 people moved to shelters; no major damage yet."),
    (3, "POLAND", "REUTERS", RED,
     "RUSSIAN MISSILES LAND IN POLAND",
     "Kh-101 lands in Poland; Tusk calls it a provocation."),
    (4, "ASIA MARKETS", "AL JAZEERA", (122, 60, 20),
     "ASIA'S AI STOCKS TUMBLE",
     "Taipei -6.2%, Seoul -5.2%, Nikkei -5.1%."),
    (5, "ANTALYA", "CARBON BRIEF", (46, 110, 60),
     "COP31 TALKS STALL ON FINAL DAY",
     "Draft drops fossil-fuel phase-out and $120bn target."),
    (6, "BRUSSELS", "THE TIMES", NAVY,
     "BRITAIN AND EU AGREE POST-BREXIT RESET",
     "100,000 youth visas a year each way; food checks eased."),
    (7, "ITALY", "REUTERS", (90, 40, 110),
     "ITALY STOPS FOR A DAY",
     "CGIL strike fills 100-plus cities over wages."),
    (8, "TOKYO", "REUTERS", (122, 60, 20),
     "JAPAN'S PRICES KEEP CLIMBING",
     "Core inflation 2.2%; a December rate rise is expected."),
    (9, "HODEIDAH", "THE NATIONAL", (90, 60, 20),
     "GULF TENSIONS SPILL INTO YEMEN'S PORT",
     "Coalition strikes Houthi arms smuggling at Hodeidah."),
    (10, "MALAWI", "AL JAZEERA", (140, 70, 20),
     "MALAWI'S FUEL QUEUES TURN VIOLENT",
     "Petrol rationed to 20 litres a day; a queue turns deadly."),
    (11, "WELLINGTON", "REUTERS", (20, 90, 90),
     "PHILLIPS 118 LIFTS NEW ZEALAND",
     "Nicholls 175* as NZ make 368; a format first."),
    (12, "LAS VEGAS", "FORMULA 1", (60, 60, 60),
     "RUSSELL FASTEST IN WET VEGAS PRACTICE",
     "1:47.272 tops a rain-hit FP2; FP1 washed out."),
    (13, "WASHINGTON", "SCMP", (90, 40, 40),
     "TRUMP: NO RUSH ON IRAN",
     "No decision on strikes until the new year."),
]

KPIS = [("3", "KYIV BRIDGES HIT"), ("404", "DRONES IN THE BARRAGE"),
        ("372,000", "EVACUATED IN INDIA"), ("-6.2%", "TAIPEI STOCKS"),
        ("100,000", "YOUTH VISAS A YEAR"), ("$120bn", "CLIMATE CASH DROPPED")]

REGIONS = [("EUROPE", 12, NAVY), ("AMERICAS", 6, RED), ("ASIA", 5, GOLD),
           ("MIDDLE EAST", 5, TEAL), ("AFRICA", 3, (122, 74, 33)),
           ("WORLD", 3, (102, 102, 102)), ("OCEANIA", 1, (46, 125, 138))]

BRIEFS = [
    "Gaza: Israeli strikes kill six across Gaza on Friday",
    "Sudan: drone strike kills 10 at a gold mine",
    "Senegal: migrant boat capsizes off Yenne; dozens missing",
    "Georgia: gas blast collapses a housing block; six dead",
    "Estonia to shut its border with Russia for six months",
    "Denmark approves a US-Greenland security deal",
    "Germany's Merz rejects a great-power deal over Europe",
    "White House fires its cyber chief after tech outages",
    "Trump bought up to $265,000 of Nvidia stock in September",
    "Mamdani unveils a plan to close New York's Rikers jail",
    "US and Venezuela sign a new military cooperation pact",
    "Haiti police report 34 suspected gang members killed",
    "IAEA: North Korea is expanding uranium enrichment",
    "China's rare-earth magnet exports to US and EU fall",
    "Board of Peace: Israel and Hamas both miss truce terms",
    "Mosque set on fire in northern Israel",
    "Voyager 1 phones home from a light-day away",
    "BepiColombo: commands sent for Saturday's Mercury burn",
    "French TV apologises after pundits call all Chinese spies",
    "European youth strike over living costs in 25 countries",
    "Ukraine's allies meet in Berlin, ready to talk to Russia",
    "Daytime barrage hits embassies and a cathedral in Kyiv",
]
BRIEF_SOURCES = ["AFP", "RADIO DABANGA", "REUTERS", "SCMP", "SCMP",
                 "AL JAZEERA", "KYIV POST", "REUTERS", "SCMP", "REUTERS",
                 "AP", "REUTERS", "REUTERS", "SCMP", "AL JAZEERA",
                 "AL JAZEERA", "SCMP", "ESA", "SCMP", "CNN", "REUTERS",
                 "SCMP"]

# map pins: (story number, lon, lat, label dx, dy)
PINS = [(1, 30.5, 50.4, 0, -4), (2, 22.8, 50.5, -16, -2),
        (3, 84.9, 19.3, 6, -12), (4, 127.0, 37.0, 4, -14),
        (5, 33.5, 36.9, 8, 6), (6, 4.4, 50.9, -14, -2),
        (7, 12.5, 41.9, 2, 16), (8, 139.7, 35.7, 8, -10),
        (9, 42.9, 14.8, 6, 8), (10, 35.0, -15.8, 8, -6),
        (11, 174.8, -41.3, -18, -10), (12, -115.1, 36.2, -14, 6),
        (13, -77.0, 38.9, 6, -12)]

# rough continent polygons in (lon, lat)
LAND = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-97, 26),
     (-105, 20), (-95, 16), (-85, 12), (-92, 15), (-105, 22), (-117, 33),
     (-125, 40), (-125, 49), (-140, 60), (-158, 58), (-168, 66)],
    # Greenland
    [(-58, 64), (-45, 60), (-32, 68), (-40, 76), (-58, 76), (-62, 70)],
    # South America
    [(-78, 8), (-62, 10), (-52, 5), (-44, -3), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -42), (-70, -52), (-74, -40),
     (-72, -20), (-80, -5), (-80, 2), (-78, 8)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (32, -28),
     (20, -35), (15, -27), (12, -18), (9, 0), (-8, 5), (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 58), (10, 58), (18, 56),
     (21, 55), (28, 60), (30, 70), (45, 68), (60, 69), (75, 73), (90, 75),
     (110, 74), (130, 72), (150, 70), (170, 67), (178, 65), (162, 60),
     (158, 52), (142, 50), (140, 40), (130, 35), (122, 30), (120, 22),
     (108, 12), (105, 9), (100, 7), (95, 15), (90, 22), (85, 19),
     (80, 8), (76, 10), (72, 20), (66, 25), (58, 25), (52, 28), (48, 30),
     (44, 29), (40, 36), (36, 36), (30, 36), (22, 37), (18, 40), (12, 44),
     (3, 43), (-2, 37), (-9, 38), (-10, 36)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51), (-5, 50)],
    # Japan
    [(130, 31), (132, 34), (136, 35), (140, 38), (141, 42), (144, 44),
     (140, 40), (136, 36), (132, 33), (130, 31)],
    # SE Asia islands
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -3), (135, -4), (140, -8), (135, -2), (125, 0),
     (115, 2), (105, 2), (98, 6), (95, 5)],
    # Australia
    [(113, -22), (114, -30), (118, -35), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -27),
     (150, -22), (146, -19), (142, -11), (135, -12), (130, -13),
     (125, -14), (120, -20), (113, -22)],
    # New Zealand
    [(167, -45), (170, -42), (174, -38), (178, -38), (175, -41),
     (170, -44), (167, -45)],
]


def draw_map(d, x0, y0, w, h):
    """World map: solid land silhouettes with a dotted texture and pins."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(233, 226, 205),
                outline=CREAM_LINE)
    lon0, lon1, lat0, lat1 = -180, 180, 72, -48

    def px(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * w,
                y0 + (lat0 - lat) / (lat0 - lat1) * h)

    def lx(lon, lat):
        return ((lon - lon0) / (lon1 - lon0) * w,
                (lat0 - lat) / (lat0 - lat1) * h)

    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    for poly in LAND:
        md.polygon([lx(lo, la) for lo, la in poly], fill=255)
    for poly in LAND:
        d.polygon([px(lo, la) for lo, la in poly], fill=(154, 162, 142))
    step = 7
    for gy in range(0, h - 2, step):
        for gx in range(0, w - 2, step):
            if mask.getpixel((gx + 2, gy + 2)):
                d.ellipse([x0 + gx, y0 + gy, x0 + gx + 2, y0 + gy + 2],
                          fill=(120, 130, 118))
    for num, lon, lat, dx, dy in PINS:
        cx, cy = px(lon, lat)
        cx += dx
        cy += dy
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = font(9, True)
        tw = d.textlength(str(num), font=f)
        d.text((cx - tw / 2, cy - 5), str(num), font=f,
               fill=(255, 255, 255))


def story_cell(d, x, y, w, h, num, place, source, color, headline, deck,
               hl_size, deck_size):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=CREAM_LINE)
    band = 26 if h < 100 else 30
    d.rectangle([x, y, x + w, y + band], fill=color)
    isz = band - 6
    ICONS[num](d, x + w - isz - 5, y + 3, isz, (255, 255, 255))
    f_band = font(12, True)
    label = f"{num} · {place} — {source}"
    while text_w(d, label, f_band) > w - isz - 14 and " " in label:
        label = label.rsplit(" ", 1)[0]
    d.text((x + 8, y + band / 2 - 6), label, font=f_band,
           fill=(255, 255, 255))
    ty = y + band + 6
    f_hl = font(hl_size, True)
    ty = draw_wrapped(d, headline, f_hl, x + 8, ty, w - 16, INK,
                      leading=hl_size + 2, max_lines=2)
    f_dk = font(deck_size)
    draw_wrapped(d, deck, f_dk, x + 8, ty + 2, w - 16, (60, 60, 60),
                 leading=deck_size + 2, max_lines=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin

    # masthead
    d.line([(M, 5), (W - M, 5)], fill=INK, width=2)
    f_mast = font(40, True, serif=True)
    name = "THE WORLD LEDGER"
    tw = text_w(d, name, f_mast)
    d.text(((W - tw) / 2, 8), name, font=f_mast, fill=INK)
    f_small = font(11, True)
    d.text((M, 24), "ONE DAY · ONE PAGE", font=f_small, fill=GREY)
    r = "FRIDAY EDITION"
    d.text((W - M - text_w(d, r, f_small), 24), r, font=f_small, fill=GREY)
    d.line([(M, 54), (W - M, 54)], fill=INK, width=3)
    d.line([(M, 58), (W - M, 58)], fill=INK, width=1)

    # date as the largest headline
    f_date = font(50, True)
    date = "Friday 20 November 2026"
    tw = text_w(d, date, f_date)
    d.text(((W - tw) / 2, 62), date, font=f_date, fill=NAVY)

    # red subhead naming the leads
    f_sub = font(17, True)
    sub = "KYIV BRIDGES HIT  ·  CYCLONE AKVAN LANDFALL  ·  ASIAN STOCKS TUMBLE  ·  COP31 TALKS STALL"
    tw = text_w(d, sub, f_sub)
    d.text(((W - tw) / 2, 120), sub, font=f_sub, fill=RED)

    # KPI strip
    y = 142
    kw = (W - 2 * M - 5 * 6) / 6
    for i, (num, lab) in enumerate(KPIS):
        x = M + i * (kw + 6)
        d.rectangle([x, y, x + kw, y + 40], fill=(255, 255, 255),
                    outline=CREAM_LINE)
        f_n = font(22, True)
        nw = text_w(d, num, f_n)
        d.text((x + (kw - nw) / 2, y + 1), num, font=f_n, fill=NAVY)
        f_l = font(10, True)
        lw = text_w(d, lab, f_l)
        d.text((x + (kw - lw) / 2, y + 27), lab, font=f_l, fill=GREY)

    # region bar
    y = 190
    total = sum(c for _, c, _ in REGIONS)
    bx, bw = M, W - 2 * M
    cx = bx
    for name, count, col in REGIONS:
        seg = bw * count / total
        d.rectangle([cx, y, cx + seg - 1, y + 12], fill=col)
        cx += seg
    f_r = font(12, True)
    leg = "  ·  ".join(f"{n} {c}" for n, c, _ in REGIONS)
    leg += f"   —   {total} STORIES IN ALL"
    tw = text_w(d, leg, f_r)
    d.text(((W - tw) / 2, y + 15), leg, font=f_r, fill=INK)

    # 13 drawn stories
    grid_top = 218
    gap = 4
    col_w4 = (W - 2 * M - 3 * gap) / 4
    col_w2 = (W - 2 * M - gap) / 2
    col_w3 = (W - 2 * M - 2 * gap) / 3
    rows = [(grid_top, 116, [0, 1], col_w2, 21, 13),
            (grid_top + 120, 108, [2, 3, 4, 5], col_w4, 18, 12),
            (grid_top + 232, 108, [6, 7, 8, 9], col_w4, 18, 12),
            (grid_top + 344, 100, [10, 11, 12], col_w3, 18, 13)]
    for ry, rh, idxs, cw, hl, dk in rows:
        for j, si in enumerate(idxs):
            x = M + j * (cw + gap)
            num, place, src, col, head, deck = STORIES[si]
            story_cell(d, x, ry, cw, rh, num, place, src, col, head, deck,
                       hl, dk)

    # map
    my = grid_top + 448
    f_sec = font(16, True)
    d.text((M, my), "WHERE IT HAPPENED — 13 STORIES, 13 PINS", font=f_sec,
           fill=INK)
    draw_map(d, M, my + 21, W - 2 * M, 72)

    # briefs tail
    by = my + 101
    d.text((M, by), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES", font=f_sec,
           fill=INK)
    f_b = font(12)
    f_bn = font(12, True)
    colw = (W - 2 * M - 16) / 2
    for i, brief in enumerate(BRIEFS):
        col = i // 11
        row = i % 11
        x = M + col * (colw + 16)
        yy = by + 21 + row * 12
        num = str(14 + i) + "."
        d.text((x, yy), num, font=f_bn, fill=RED)
        line = f"{brief} — {BRIEF_SOURCES[i]}"
        while text_w(d, line, f_b) > colw - 26 and len(line) > 20:
            line = line[:-1].rstrip()
        d.text((x + 26, yy), line, font=f_b, fill=INK)

    # DATE CHECK
    cy = by + 21 + 11 * 12 + 8
    d.rectangle([M, cy, W - M, cy + 74], fill=(255, 240, 238),
                outline=RED, width=2)
    f_dc = font(14, True)
    d.text((M + 10, cy + 6), "DATE CHECK — WHAT WE LEFT OUT, AND WHY",
           font=f_dc, fill=RED)
    f_dcb = font(13)
    body = ("Thursday 19 November: the World Court's Myanmar ruling; the "
            "Trump–Xi–Putin summit in Shenzhen; Anthropic's Nasdaq debut; "
            "the GTA 6 launch; the Riyadh tower strike; the Gaza Yellow "
            "Line raid ended. Earlier: the Nvidia SEC probe (17 Nov); "
            "Kenya's Ebola discharge (11 Nov). Not yet happened: "
            "BepiColombo's Mercury orbit burn (Saturday) and any final "
            "COP31 text.")
    draw_wrapped(d, body, f_dcb, M + 10, cy + 26, W - 2 * M - 20, INK,
                 leading=16, max_lines=3)

    # footer
    f_f = font(13, True)
    foot = ("FRIDAY 20 NOVEMBER 2026 — THE WORLD LEDGER — Every story here "
            "happened, or was first reported, on Friday 20 November 2026.")
    tw = text_w(d, foot, f_f)
    d.text(((W - tw) / 2, H - 21), foot, font=f_f, fill=INK)
    if cy + 74 > H - 21:
        print("WARNING: DATE CHECK box bottom", cy + 74, "overlaps footer")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
