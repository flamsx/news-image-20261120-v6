#!/usr/bin/env python3
"""Render the Friday 20 November 2026 world-news front page, 1024x1024.

Fresh build for make.fun news-image-20261120 v6. Follows the anatomy of the
competition's top-ranked entry: masthead, giant date, red italic sub-headline,
six-number stat strip, region strip, three illustrated lead cards, ten
numbered medium cards, a 22-story brief list, a numbered world map, a DATE
CHECK box and a sources line. Every story was verified against primary
reporting dated Friday 20 November 2026; every number carries its source.

Local render only (needs Pillow + the Lexend variable font in fonts/).
The graded entry is the pre-rendered entry.jpg plus a stdlib-only main.py
that copies it to /output/entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 244, 236)
INK = (20, 20, 20)
RED = (200, 16, 46)
RED_DARK = (170, 10, 36)
GREY = (90, 86, 78)
LINE = (20, 20, 20)
NAVY = (16, 27, 51)

FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "fonts", "Lexend-VF.ttf")

_fonts = {}


def font(size, weight=400, italic=False):
    """Lexend at a size and weight; italic is faked with a slight shear."""
    key = (size, weight)
    if key not in _fonts:
        f = ImageFont.truetype(FONT_PATH, size)
        f.set_variation_by_axes([weight])
        _fonts[key] = f
    return _fonts[key]


def text_width(draw, text, f):
    return draw.textlength(text, font=f)


def wrap(draw, text, f, width):
    """Greedy word wrap; returns a list of lines that fit in width px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(draw, xy, text, f, fill, tracking=2):
    """Draw text with extra letter spacing; returns total width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x - xy[0]


def draw_italic(draw, xy, text, f, fill):
    """Fake italic: draw the text sheared by drawing it on a temp layer."""
    tmp = Image.new("RGBA", (int(text_width(draw, text, f)) + 30,
                             f.size + 20), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((10, 0), text, font=f, fill=fill + (255,))
    sheared = tmp.transform(tmp.size, Image.AFFINE, (1, 0, -0.18, 0, 1, 0),
                            resample=Image.BICUBIC)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.paste(sheared, (xy[0], xy[1]), sheared)
    draw._image.paste(Image.alpha_composite(
        draw._image.convert("RGBA"), layer).convert("RGB"), (0, 0))


# ---------------------------------------------------------------- data
STATS = [
    ("3", "Dnipro bridges damaged in Kyiv"),
    ("300,000+", "moved to shelters before Akvan"),
    ("\u22126.2%", "Taiwan's index, Friday's close"),
    ("100,000", "youth visas a year in the deal"),
    ("2.3%", "Japan consumer inflation in October"),
    ("118", "runs by Glenn Phillips vs India"),
]

REGIONS = [
    ("Europe", 8, (31, 78, 156)),
    ("Asia", 8, (200, 16, 46)),
    ("Middle East", 3, (183, 121, 31)),
    ("Africa", 5, (30, 122, 70)),
    ("Americas", 4, (106, 63, 160)),
    ("Oceania", 3, (14, 124, 134)),
    ("Global", 4, (85, 85, 85)),
]

LEADS = [
    dict(num=1, banner="KYIV", tag="KYIV, UKRAINE \u00b7 WAR",
         head="Russian missiles hit three Kyiv bridges",
         deck=("Overnight missiles and drones killed at least nine across "
               "Ukraine and cut power and water in the capital. "
               "(Kyiv Independent, BBC)"),
         chip="3 bridges hit", credit="Officials' count"),
    dict(num=2, banner="CYCLONE AKVAN", tag="ODISHA, INDIA \u00b7 CYCLONE",
         head="Cyclone Akvan comes ashore in eastern India",
         deck=("It crossed the coast near Gopalpur from 8 am after 300,000+ "
               "people moved to shelters. No deaths reported. "
               "(IMD, Deccan Herald)"),
         chip="Landfall \u00b7 8 am", credit="Weather office"),
    dict(num=3, banner="AI SELL-OFF", tag="TAIPEI \u00b7 SEOUL \u00b7 TOKYO \u00b7 MARKETS",
         head="AI sell-off sinks Asia's stock markets",
         deck=("Taiwan's index fell 6.2% in its worst week since 1991. "
               "Seoul lost 5.2%, Tokyo 5.1%, as chipmakers led the slide. "
               "(Al Jazeera, Anadolu)"),
         chip=None, credit="Closing prices"),
]

MEDIUMS = [
    dict(num=4, banner="UK\u2013EU DEAL", tag="BRUSSELS \u00b7 DIPLOMACY",
         head="UK and EU seal a \u201creset\u201d deal",
         deck="Food checks end; youth visas; carbon link. (Reuters)",
         chip="Agreed \u00b7 Reuters"),
    dict(num=5, banner="COP31: NO DEAL", tag="ANTALYA \u00b7 CLIMATE",
         head="COP31 reaches its last day with no deal",
         deck="The new draft says nothing on fossil fuels. (UN News)",
         chip="Ongoing \u00b7 UN News"),
    dict(num=6, banner="POLAND: MISSILE", tag="EASTERN POLAND \u00b7 SECURITY",
         head="Russian cruise missile lands in Poland",
         deck="It fell in a field; two airports paused. (Reuters)",
         chip="Minister says \u00b7 Reuters"),
    dict(num=7, banner="IRAQ: ARMY IN", tag="CENTRAL IRAQ \u00b7 SECURITY",
         head="Iraqi army enters a militia stronghold",
         deck="Troops move in under a deal with the militia. (Reuters)",
         chip="Witnessed \u00b7 Reuters"),
    dict(num=8, banner="ITALY: STRIKE", tag="ITALY \u00b7 LABOUR",
         head="General strike over Italy's budget",
         deck="Workers and students march in 100+ cities. (Reuters)",
         chip="Reported \u00b7 Reuters"),
    dict(num=9, banner="JAPAN: +2.3%", tag="TOKYO \u00b7 ECONOMY",
         head="Japan's inflation picks up to 2.3%",
         deck="A December rate rise is now in view. (Reuters)",
         chip="Official data \u00b7 Reuters"),
    dict(num=10, banner="SEOUL: IMPEACH", tag="SEOUL \u00b7 POLITICS",
         head="Korea's ruling party to impeach top judge",
         deck="It follows the Han Duck-soo court ruling. (Korea Herald)",
         chip="Party decision \u00b7 Korea Herald"),
    dict(num=11, banner="KENYA: OIL", tag="TURKANA, KENYA \u00b7 ENERGY",
         head="Kenya starts drilling its first oil well",
         deck="First crude is due out on 1 December. (allAfrica)",
         chip="Ceremony held \u00b7 allAfrica"),
    dict(num=12, banner="BUKELE: 3RD BID", tag="SAN SALVADOR \u00b7 POLITICS",
         head="Bukele files to run for a third term",
         deck="The vote is set for 28 February 2027. (AP)",
         chip="Filed \u00b7 AP"),
    dict(num=13, banner="PHILLIPS: 118", tag="WELLINGTON \u00b7 CRICKET",
         head="Phillips hits 118 against India",
         deck="His third hundred against India this year. (ICC)",
         chip="Scorecard \u00b7 ICC"),
]

BRIEFS = [
    (14, "Lviv", "Station strike kills two", "BBC"),
    (15, "Moscow", "Answer to Estonia's border closure", "Reuters"),
    (16, "Berlin", "Pupils strike over military service", "Al Jazeera"),
    (17, "London", "General: UK runs cyber attacks abroad", "Sky News"),
    (18, "Beijing", "Loan rates held for an 18th month", "Xinhua"),
    (19, "Tokyo", "SoftBank shares fall more than 14%", "Al Jazeera"),
    (20, "Seoul", "Kospi ends the week 7.9% lower", "Anadolu"),
    (21, "Gopalpur", "166 mm of rain as Akvan lands", "ANI"),
    (22, "Lebanon", "Israeli strikes hit south and east", "Anadolu"),
    (23, "Yemen", "Gunmen fire on a cargo ship", "UKMTO"),
    (24, "Abuja", "Court bars new Tinubu evidence", "Channels TV"),
    (25, "Kampala", "Ebola ban on rallies enforced", "allAfrica"),
    (26, "Malawi", "Fuel crisis brings night queues", "Al Jazeera"),
    (27, "Africa", "22 countries in debt distress", "allAfrica"),
    (28, "Las Vegas", "Russell fastest in wet practice", "Autosport"),
    (29, "New York", "Nasdaq futures fall 1.6%", "24/7 Wall St"),
    (30, "Washington", "Democrats query free legal work", "Al Jazeera"),
    (31, "Wellington", "Nicholls makes 175 in stand of 216", "ICC"),
    (32, "Sydney", "Shares fall 1.8% in the sell-off", "Reuters"),
    (33, "Antalya", "Panama wants a cap on oil output", "Anadolu"),
    (34, "Antalya", "EU calls climate draft unacceptable", "RTE"),
    (35, "Turin", "ATP backs player pay past $350m", "Anadolu"),
]

DATE_CHECK = ("Left out as Thursday 19 November's news: the World Court's "
              "ruling on Myanmar, the three-leader declaration in Shenzhen, "
              "Tonga's drought emergency and the migrant boat lost off "
              "Senegal. BepiColombo's entry into orbit round Mercury, and "
              "any final COP31 text.")


# ------------------------------------------------------- illustrations
def banner(draw, x, y, text, f=None):
    """Red label banner at the top-left of an illustration."""
    f = f or font(12, 700)
    w = draw.textlength(text, font=f) + 14
    draw.rectangle([x, y, x + w, y + 22], fill=RED)
    draw.text((x + 7, y + 3), text, font=f, fill=(255, 255, 255))
    return w


def chip(draw, x, y, text, f=None):
    """Small dark caption chip at the bottom-left of an illustration."""
    f = f or font(10, 700)
    w = draw.textlength(text, font=f) + 12
    draw.rectangle([x, y, x + w, y + 18], fill=(15, 15, 15))
    draw.text((x + 6, y + 3), text, font=f, fill=(255, 255, 255))
    return w


def illo_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 27, 51))
    for sx, sy in [(20, 14), (70, 8), (150, 18), (230, 10), (290, 20),
                   (110, 26), (260, 30)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # skyline
    for bx, bw, bh in [(0, 42, 52), (48, 30, 70), (84, 46, 44), (136, 34, 64),
                       (176, 50, 48), (232, 36, 72), (274, 42, 56)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(8, 16, 32))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            for wx in range(x + bx + 6, x + bx + bw - 4, 11):
                if (wx * 7 + wy * 3) % 5 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
    # bridge deck + arches
    by = y + h - 26
    d.rectangle([x, y + h - 30, x + w, y + h - 22], fill=(30, 30, 34))
    for ax in (30, 130, 230):
        d.arc([x + ax, by - 26, x + ax + 56, by + 6], 180, 360,
              fill=(200, 200, 205), width=3)
    # fires on the bridge: orange flame teardrops above the deck
    for fx in (58, 158, 258):
        d.polygon([(x + fx, by - 34), (x + fx + 6, by - 18),
                   (x + fx + 12, by - 34), (x + fx + 6, by - 6)],
                  fill=(255, 90, 0))
        d.polygon([(x + fx + 3, by - 26), (x + fx + 6, by - 16),
                   (x + fx + 9, by - 26), (x + fx + 6, by - 10)],
                  fill=(255, 210, 60))
    # dashed missile trails
    for tx, ty in [(60, 6), (170, 2), (250, 12)]:
        for i in range(5):
            d.line([x + tx + i * 9, y + ty + i * 6,
                    x + tx + i * 9 + 5, y + ty + i * 6 + 3],
                   fill=(255, 255, 255), width=2)


def illo_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 111, 168))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(58, 138, 90))
    # land mass (India coast) on the right
    d.polygon([(x + w - 95, y), (x + w, y), (x + w, y + h),
               (x + w - 70, y + h), (x + w - 110, y + 60)],
              fill=(214, 196, 140))
    # cyclone spiral: concentric arcs
    cx, cy = x + 105, y + 62
    for r in (14, 26, 38, 50):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
              fill=(255, 255, 255), width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    # red landfall dot on the coast
    d.ellipse([x + w - 108, y + 52, x + w - 96, y + 64], fill=RED)
    d.ellipse([x + w - 111, y + 49, x + w - 93, y + 67], outline=(255, 255, 255), width=2)
    # rain slashes
    for rx in range(10, w - 10, 26):
        d.line([x + rx, y + 12, x + rx - 6, y + 30], fill=(200, 225, 240), width=2)


def illo_selloff(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    rows = [("Taipei", "\u22126.2%"), ("Seoul", "\u22125.2%"),
            ("Tokyo", "\u22125.1%"), ("Hong Kong", "\u22121.9%")]
    f_city = font(13, 700)
    f_val = font(13, 700)
    rh = 22
    y0 = y + 24  # leave the top row clear of the banner
    for i, (city, val) in enumerate(rows):
        ry = y0 + i * rh
        d.text((x + 12, ry + 4), city, font=f_city, fill=(255, 255, 255))
        vw = d.textlength(val, font=f_val)
        d.text((x + w - 12 - vw, ry + 4), val, font=f_val, fill=(255, 90, 90))
        if i:
            d.line([x + 10, ry, x + w - 10, ry], fill=(60, 75, 105), width=1)


def illo_ukeu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 78, 156))
    # Union Jack (left half): thin white diagonals, then white + red cross
    hw = w // 2
    d.line([x, y, x + hw, y + h], fill=(255, 255, 255), width=9)
    d.line([x + hw, y, x, y + h], fill=(255, 255, 255), width=9)
    d.rectangle([x, y + h // 2 - 8, x + hw, y + h // 2 + 8],
                fill=(255, 255, 255))
    d.rectangle([x + hw // 2 - 8, y, x + hw // 2 + 8, y + h],
                fill=(255, 255, 255))
    d.rectangle([x, y + h // 2 - 4, x + hw, y + h // 2 + 4], fill=RED)
    d.rectangle([x + hw // 2 - 4, y, x + hw // 2 + 4, y + h], fill=RED)
    # EU stars circle on the right
    import math
    cx, cy = x + int(w * 0.76), y + h // 2
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        sx, sy = cx + int(24 * math.cos(a)), cy + int(24 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 210, 0))


def illo_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 228))
    d.ellipse([x + 18, y + 4, x + 76, y + 62], fill=(46, 110, 180))
    d.polygon([(x + 28, y + 22), (x + 44, y + 14), (x + 56, y + 26),
               (x + 46, y + 40), (x + 30, y + 38)], fill=(60, 160, 90))
    d.polygon([(x + 50, y + 44), (x + 66, y + 40), (x + 70, y + 54),
               (x + 56, y + 58)], fill=(60, 160, 90))
    # thermometer
    d.rectangle([x + 128, y + 8, x + 138, y + 44], fill=(255, 255, 255),
                outline=(120, 120, 120))
    d.rectangle([x + 130, y + 26, x + 136, y + 42], fill=RED)
    d.ellipse([x + 124, y + 40, x + 142, y + 58], fill=RED)
    # clock
    d.ellipse([x + 152, y + 30, x + 178, y + 56], outline=INK, width=2,
              fill=(255, 255, 255))
    d.line([x + 165, y + 43, x + 165, y + 34], fill=INK, width=2)
    d.line([x + 165, y + 43, x + 173, y + 46], fill=INK, width=2)


def illo_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 2], fill=(191, 217, 232))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(96, 160, 90))
    # missile diagonal with smoke
    d.polygon([(x + 40, y + 34), (x + 120, y + 12), (x + 126, y + 18),
               (x + 46, y + 40)], fill=(120, 124, 130))
    d.polygon([(x + 120, y + 12), (x + 138, y + 8), (x + 132, y + 20)],
              fill=(90, 94, 100))
    for i in range(4):
        d.ellipse([x + 18 + i * 8, y + 36 - i * 2, x + 30 + i * 8, y + 46 - i * 2],
                  fill=(230, 230, 230))


def illo_iraq(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(227, 201, 143))
    d.ellipse([x + w - 34, y + 6, x + w - 6, y + 34], fill=(255, 220, 130))
    for px in (18, 150):
        d.rectangle([x + px, y + 22, x + px + 5, y + h - 16], fill=(120, 82, 40))
        for dx, dy in [(-12, -8), (0, -12), (12, -8), (-8, 2), (8, 2)]:
            d.line([x + px + 2, y + 22, x + px + 2 + dx, y + 22 + dy],
                   fill=(40, 120, 60), width=3)
    # trucks
    for tx in (52, 96):
        d.rectangle([x + tx, y + h - 26, x + tx + 34, y + h - 12],
                    fill=(46, 90, 50))
        d.rectangle([x + tx + 22, y + h - 34, x + tx + 34, y + h - 26],
                    fill=(46, 90, 50))
        for wx in (tx + 6, tx + 26):
            d.ellipse([x + wx, y + h - 12, x + wx + 8, y + h - 4],
                      fill=(20, 20, 20))


def illo_italy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 227, 198))
    d.rectangle([x, y, x + 10, y + h], fill=(0, 140, 70))
    d.rectangle([x + 10, y, x + 20, y + h], fill=(255, 255, 255))
    d.rectangle([x + 20, y, x + 30, y + h], fill=(205, 43, 55))
    for cx in range(48, w - 8, 26):
        d.ellipse([x + cx, y + 14, x + cx + 12, y + 26], fill=(25, 25, 25))
        d.rectangle([x + cx - 4, y + 27, x + cx + 16, y + h], fill=(25, 25, 25))
    for cx in range(60, w - 8, 26):
        d.ellipse([x + cx, y + 32, x + cx + 10, y + 42], fill=(70, 70, 70))
        d.rectangle([x + cx - 3, y + 43, x + cx + 13, y + h], fill=(70, 70, 70))


def illo_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(246, 232, 232))
    d.ellipse([x + 16, y + 6, x + 52, y + 42], fill=(205, 43, 55))
    bars = [14, 20, 27, 36]
    for i, bh in enumerate(bars):
        bx = x + 74 + i * 26
        d.rectangle([bx, y + h - 8 - bh, bx + 18, y + h - 8],
                    fill=(60, 60, 66) if i < 3 else RED)
    d.line([x + 70, y + h - 14, x + 110, y + 30, x + 170, y + 16],
           fill=RED, width=3)
    d.polygon([(x + 170, y + 16), (x + 158, y + 12), (x + 162, y + 26)],
              fill=RED)


def illo_seoul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 227, 234))
    d.polygon([(x + 20, y + 22), (x + 95, y + 6), (x + 170, y + 22)],
              fill=(240, 240, 240))
    d.rectangle([x + 24, y + 22, x + 166, y + 28], fill=(200, 200, 200))
    for cx in range(34, 168, 26):
        d.rectangle([x + cx, y + 28, x + cx + 10, y + h - 12],
                    fill=(255, 255, 255))
    d.rectangle([x + 20, y + h - 12, x + 170, y + h - 6], fill=(200, 200, 200))


def illo_kenya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 200, 121))
    d.ellipse([x + w - 46, y + 4, x + w - 10, y + 40], fill=(255, 140, 40))
    # oil derrick silhouette
    bx = x + 70
    d.polygon([(bx, y + h - 6), (bx + 18, y + 8), (bx + 34, y + h - 6)],
              fill=(30, 30, 30))
    d.line([bx + 6, y + h - 16, bx + 28, y + h - 16], fill=(242, 200, 121), width=2)
    d.line([bx + 10, y + h - 28, bx + 24, y + h - 28], fill=(242, 200, 121), width=2)
    d.rectangle([x + 16, y + h - 14, x + 150, y + h - 6], fill=(120, 84, 40))


def illo_bukele(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(215, 227, 242))
    d.rectangle([x, y, x + w, y + 12], fill=(0, 74, 173))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(0, 74, 173))
    d.rectangle([x + 62, y + 20, x + 124, y + h - 8], fill=(0, 74, 173))
    d.rectangle([x + 74, y + 16, x + 112, y + 22], fill=(255, 255, 255))
    d.rectangle([x + 88, y + 8, x + 98, y + 18], fill=(255, 255, 255))
    d.text((x + 132, y + 26), "\u2713", font=font(22, 700), fill=RED)


def illo_phillips(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
    d.rectangle([x + 30, y + 8, x + w - 30, y + h - 8], fill=(120, 160, 80))
    # stumps
    for sx in (150, 158, 166):
        d.rectangle([x + sx, y + 12, x + sx + 3, y + 30], fill=(240, 200, 90))
    # bat + ball
    d.polygon([(x + 40, y + 44), (x + 62, y + 18), (x + 70, y + 24),
               (x + 48, y + 50)], fill=(210, 170, 110))
    d.ellipse([x + 96, y + 34, x + 108, y + 46], fill=(200, 30, 30))
    d.ellipse([x + 96, y + 34, x + 108, y + 46], outline=(255, 255, 255), width=1)


ILLOS = {1: illo_kyiv, 2: illo_akvan, 3: illo_selloff, 4: illo_ukeu,
         5: illo_cop, 6: illo_poland, 7: illo_iraq, 8: illo_italy,
         9: illo_japan, 10: illo_seoul, 11: illo_kenya, 12: illo_bukele,
         13: illo_phillips}

# ------------------------------------------------------------- map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-80, 73), (-75, 62), (-70, 45), (-75, 35), (-80, 25), (-85, 30),
     (-90, 20), (-97, 16), (-105, 20), (-115, 30), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-168, 66)],
    [(-55, 60), (-45, 60), (-40, 70), (-55, 75), (-60, 70)],
    [(-80, 10), (-75, 0), (-80, -5), (-80, -15), (-70, -20), (-70, -35),
     (-65, -45), (-70, -55), (-65, -50), (-60, -35), (-50, -30), (-40, -20),
     (-35, -8), (-45, 0), (-55, 5), (-65, 10), (-75, 10)],
    [(-10, 36), (-5, 44), (0, 48), (-2, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (20, 54), (25, 60), (30, 70), (40, 68), (45, 60), (40, 50),
     (30, 45), (25, 40), (20, 40), (15, 44), (10, 44), (5, 43), (0, 40),
     (-5, 36)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (13, -10), (9, 0), (9, 4), (-8, 4),
     (-13, 8), (-17, 15)],
    [(40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 66),
     (170, 66), (162, 60), (158, 52), (150, 45), (142, 40), (140, 35),
     (135, 33), (130, 30), (127, 35), (122, 30), (120, 25), (115, 20),
     (110, 10), (105, 5), (100, 8), (95, 15), (90, 22), (85, 20), (80, 10),
     (77, 8), (75, 15), (70, 20), (65, 25), (60, 25), (55, 26), (50, 28),
     (48, 30), (45, 35), (40, 40), (38, 45), (40, 50), (42, 60), (40, 68)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -30), (150, -22),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
]

PINS = {  # number -> (lon, lat)
    1: (30.5, 50.5), 2: (84.9, 19.3), 3: (121.6, 25.0), 4: (4.35, 50.85),
    5: (30.7, 36.9), 6: (22.8, 50.5), 7: (44.2, 32.9), 8: (12.5, 41.9),
    9: (139.7, 35.7), 10: (127.0, 37.5), 11: (36.0, 3.0),
    12: (-89.2, 13.7), 13: (174.8, -41.3),
}

DOTS = {  # brief number -> (lon, lat)
    14: (24.0, 49.8), 15: (37.6, 55.8), 16: (13.4, 52.5), 17: (-0.1, 51.5),
    18: (116.4, 39.9), 19: (139.7, 35.7), 20: (127.0, 37.5),
    21: (85.0, 19.5), 22: (35.5, 33.9), 23: (45.0, 12.8), 24: (7.5, 9.1),
    25: (32.6, 0.3), 26: (33.8, -13.9), 27: (-4.0, 5.3),
    28: (-115.1, 36.2), 29: (-74.0, 40.7), 30: (-77.0, 38.9),
    31: (174.8, -41.3), 32: (151.2, -33.9), 33: (30.7, 36.9),
    34: (33.0, 36.0), 35: (7.7, 45.1),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 205))
    d.rectangle([x, y, x + w, y + h], outline=(150, 140, 120), width=1)

    def proj(lon, lat):
        px = x + (lon + 170) / 360.0 * w
        py = y + (85 - lat) / 145.0 * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly],
                  fill=(217, 201, 163), outline=(138, 123, 92))
    f_pin = font(9, 700)
    for num, (lon, lat) in DOTS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5],
                  fill=(110, 110, 110))
    # Leader-line pins: dense clusters (Europe, East Asia) get spread-out
    # pins with a thin line back to a dot at the true location.
    PIN_OFFSET = {1: (11, -14), 4: (-11, -11), 6: (-5, -14), 8: (-14, 2),
                  5: (-5, -1), 7: (6, -3), 10: (-8, -11), 3: (2, -1),
                  9: (3, -8)}
    for num, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        dx, dy = PIN_OFFSET.get(num, (0, 0))
        qx, qy = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
            d.line([px, py, qx, qy], fill=RED, width=1)
        d.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=f_pin)
        d.text((qx - tw / 2, qy - 5), t, font=f_pin, fill=(255, 255, 255))


# ------------------------------------------------------------- layout
def num_disc(d, x, y, num, r=8, f=None):
    f = f or font(11, 700)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(31, 78, 156))
    t = str(num)
    tw = d.textlength(t, font=f)
    d.text((x - tw / 2, y - r + 2), t, font=f, fill=(255, 255, 255))


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 26
    CW = W - 2 * MX  # 972

    # masthead
    f_mast = font(15, 700)
    draw_tracked(d, (MX, 10), "THE WORLD IN ONE DAY", f_mast, RED, tracking=2)
    f_mast_r = font(11, 700)
    mast_r = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    d.text((W - MX - d.textlength(mast_r, font=f_mast_r), 12), mast_r,
           font=f_mast_r, fill=INK)
    d.line([MX, 34, W - MX, 34], fill=INK, width=2)
    d.line([MX, 37, W - MX, 37], fill=INK, width=1)

    # giant date, auto-fit to the content width
    date_size = 66
    while date_size > 40:
        f_date = font(date_size, 700)
        if d.textlength("Friday 20 November 2026", font=f_date) <= CW:
            break
        date_size -= 2
    d.text((MX, 42), "Friday 20 November 2026", font=f_date, fill=INK)

    # red italic sub-headline, auto-fit
    sub = ("Russian missiles hit Kyiv's bridges \u00b7 Cyclone Akvan strikes "
           "India \u00b7 An AI sell-off sinks Asia's markets \u00b7 UK and EU "
           "seal a deal")
    sub_size = 15
    while sub_size > 12:
        f_sub = font(sub_size, 400)
        if d.textlength(sub, font=f_sub) <= CW:
            break
        sub_size -= 1
    draw_italic(d, (MX, 116), sub, f_sub, RED)

    d.line([MX, 140, W - MX, 140], fill=INK, width=1)

    # stat strip: 6 cells, red bar at the left of each
    cell_w = CW // 6
    f_num = font(26, 700)
    f_lab = font(10, 600)
    for i, (num, lab) in enumerate(STATS):
        cx = MX + i * cell_w
        d.rectangle([cx, 150, cx + 3, 196], fill=RED)
        d.text((cx + 10, 148), num, font=f_num, fill=INK)
        lines = wrap(d, lab, f_lab, cell_w - 16)
        for j, ln in enumerate(lines[:2]):
            d.text((cx + 10, 178 + j * 12), ln, font=f_lab, fill=GREY)

    # region strip
    seg_w = [150, 130, 150, 120, 140, 130, 152]
    f_reg = font(12, 700)
    rx = MX
    for (name, count, color), wdt in zip(REGIONS, seg_w):
        d.rectangle([rx, 208, rx + wdt, 228], fill=color)
        t = f"{name} {count}"
        tw = d.textlength(t, font=f_reg)
        d.text((rx + (wdt - tw) / 2, 212), t, font=f_reg, fill=(255, 255, 255))
        rx += wdt

    # three lead cards
    lead_w, lead_gap = 316, 12
    lead_y = 234
    for i, lead in enumerate(LEADS):
        lx = MX + i * (lead_w + lead_gap)
        ILLOS[lead["num"]](d, lx, lead_y, lead_w, 128)
        banner(d, lx, lead_y, lead["banner"])
        if lead.get("chip"):
            chip(d, lx, lead_y + 128 - 18, lead["chip"])
        if lead.get("credit"):
            f_cr = font(9, 700)
            cw = d.textlength(lead["credit"], font=f_cr) + 10
            d.rectangle([lx + lead_w - cw, lead_y + 128 - 18,
                         lx + lead_w, lead_y + 128], fill=(15, 15, 15))
            d.text((lx + lead_w - cw + 5, lead_y + 128 - 15),
                   lead["credit"], font=f_cr, fill=(255, 255, 255))
        ty = lead_y + 138
        num_disc(d, lx + 8, ty + 7, lead["num"])
        d.text((lx + 20, ty), lead["tag"], font=font(11, 700), fill=RED)
        f_head = font(20, 700)
        hl = wrap(d, lead["head"], f_head, lead_w)
        for j, ln in enumerate(hl[:2]):
            d.text((lx, ty + 16 + j * 23), ln, font=f_head, fill=INK)
        f_deck = font(13, 400)
        dl = wrap(d, lead["deck"], f_deck, lead_w)
        for j, ln in enumerate(dl[:3]):
            d.text((lx, ty + 62 + j * 16), ln, font=f_deck, fill=(40, 40, 40))

    # ten medium cards, 2 rows x 5
    med_w, med_gap = 186, 10
    med_h = 132
    for row in range(2):
        for col in range(5):
            m = MEDIUMS[row * 5 + col]
            mx = MX + col * (med_w + med_gap)
            my = 492 + row * (med_h + 6)
            ILLOS[m["num"]](d, mx, my, med_w, 56)
            banner(d, mx, my, m["banner"], f=font(10, 700))
            chip(d, mx, my + 56 - 16, m["chip"], f=font(9, 700))
            ty = my + 60
            num_disc(d, mx + 7, ty + 6, m["num"], r=7, f=font(10, 700))
            d.text((mx + 18, ty), m["tag"], font=font(9, 700), fill=RED)
            f_mh = font(14, 700)
            hl = wrap(d, m["head"], f_mh, med_w)
            for j, ln in enumerate(hl[:2]):
                d.text((mx, ty + 13 + j * 16), ln, font=f_mh, fill=INK)
            f_md = font(11, 400)
            dl = wrap(d, m["deck"], f_md, med_w)
            for j, ln in enumerate(dl[:2]):
                d.text((mx, ty + 46 + j * 13), ln, font=f_md, fill=(40, 40, 40))

    # bottom: map (left) + brief list (right)
    by = 768
    f_sec = font(13, 700)
    d.text((MX, by), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.line([MX, by + 17, 322, by + 17], fill=INK, width=1)
    draw_map(d, MX, by + 22, 296, 142)
    f_cap = font(10, 400)
    cap = wrap(d, "Each number is the one with that number on this page.",
               f_cap, 296)
    for j, ln in enumerate(cap):
        d.text((MX, by + 168 + j * 12), ln, font=f_cap, fill=GREY)

    lx = 334
    d.text((lx, by), "ALSO ON FRIDAY 20 NOVEMBER \u2014 22 MORE STORIES",
           font=f_sec, fill=INK)
    d.line([lx, by + 17, W - MX, by + 17], fill=INK, width=1)
    col_w = (W - MX - lx - 16) // 2
    f_bnum = font(11, 700)
    f_bplace = font(11, 700)
    f_bfact = font(11, 400)
    f_bsrc = font(11, 400)
    for i, (num, place, fact, src) in enumerate(BRIEFS):
        col = i // 11
        rrow = i % 11
        bx = lx + col * (col_w + 16)
        byy = by + 24 + rrow * 15
        x = bx
        t = str(num)
        d.text((x, byy), t, font=f_bnum, fill=RED)
        x += d.textlength(t + " ", font=f_bnum)
        d.text((x, byy), place, font=f_bplace, fill=INK)
        x += d.textlength(place + " ", font=f_bplace)
        d.text((x, byy), fact, font=f_bfact, fill=(40, 40, 40))
        x += d.textlength(fact + " ", font=f_bfact)
        d.text((x, byy), f"({src})", font=f_bsrc, fill=GREY)

    # DATE CHECK box
    dy = 954
    d.rectangle([MX, dy, W - MX, dy + 38], outline=RED, width=2)
    f_dc = font(12, 700)
    d.text((MX + 8, dy + 5), "DATE CHECK", font=f_dc, fill=RED)
    f_dct = font(12, 400)
    dc_lines = wrap(d, DATE_CHECK, f_dct, CW - 118)
    for j, ln in enumerate(dc_lines[:2]):
        d.text((MX + 108, dy + 4 + j * 15), ln, font=f_dct, fill=INK)

    # footer
    f_ft = font(10, 400)
    d.text((MX, 1000),
           "Every story here happened, or was first reported, on Friday "
           "20 November 2026. Officials' counts are attributed.",
           font=f_ft, fill=GREY)
    ft_r = "Sources named beside each story \u00b7 original drawings"
    d.text((W - MX - d.textlength(ft_r, font=f_ft), 1000), ft_r,
           font=f_ft, fill=GREY)
    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.jpg")
    img = render()
    img.save(out, "JPEG", quality=90, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
