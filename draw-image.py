#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news image (1024x1024 PNG).

Fresh build: navy masthead + 2x3 panel grid, each panel with a hand-drawn
PIL icon, a self-contained headline and the key fact.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
INK = (24, 24, 28)
GREY = (74, 74, 82)
WHITE = (255, 255, 255)
FOOT_BG = (20, 33, 61)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
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


def centre(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


# ---------------------------------------------------------------- icons
def icon_globe(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=5)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=col, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=col, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          0, 360, fill=col, width=3)
    d.arc([cx - r, cy - r * 0.95, cx + r, cy + r * 0.95],
          200, 340, fill=col, width=3)
    d.arc([cx - r, cy - r * 0.95, cx + r, cy + r * 0.95],
          20, 160, fill=col, width=3)


def icon_scales(d, cx, cy, r, col):
    # pillar
    d.line([cx, cy - r, cx, cy + r], fill=col, width=5)
    d.line([cx - r * 0.7, cy + r, cx + r * 0.7, cy + r], fill=col, width=5)
    # beam
    d.line([cx - r, cy - r * 0.55, cx + r, cy - r * 0.55], fill=col, width=5)
    d.ellipse([cx - 5, cy - r - 5, cx + 5, cy - r + 5], fill=col)
    for sx in (-1, 1):
        px = cx + sx * r * 0.82
        top = cy - r * 0.55
        d.line([px, top, px - 14, top + 26], fill=col, width=3)
        d.line([px, top, px + 14, top + 26], fill=col, width=3)
        d.arc([px - 20, top + 12, px + 20, top + 44], 0, 180, fill=col, width=4)


def icon_bridge(d, cx, cy, r, col):
    # deck
    d.line([cx - r, cy + r * 0.45, cx + r, cy + r * 0.45], fill=col, width=6)
    # two pylons
    for px in (cx - r * 0.55, cx + r * 0.55):
        d.line([px, cy - r * 0.8, px, cy + r * 0.45], fill=col, width=5)
    # cables from pylon tops to mid-deck
    d.line([cx - r * 0.55, cy - r * 0.8, cx - r * 0.1, cy + r * 0.45],
           fill=col, width=3)
    d.line([cx + r * 0.55, cy - r * 0.8, cx + r * 0.1, cy + r * 0.45],
           fill=col, width=3)
    # red zigzag crack splitting the deck at the centre
    d.line([(cx - 10, cy + r * 0.45 - 8), (cx - 2, cy + r * 0.45 + 2),
            (cx - 8, cy + r * 0.45 + 12), (cx + 2, cy + r * 0.45 + 22)],
           fill=(198, 40, 40), width=4, joint="curve")
    # small red burst above the crack
    import math
    bx, by = cx, cy - r * 0.25
    for ang in (0, 60, 120, 180, 240, 300):
        x2 = bx + 13 * math.cos(math.radians(ang))
        y2 = by + 13 * math.sin(math.radians(ang))
        d.line([bx, by, x2, y2], fill=(198, 40, 40), width=3)
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(198, 40, 40))


def icon_chart(d, cx, cy, r, col):
    d.line([cx - r, cy + r * 0.7, cx + r, cy + r * 0.7], fill=col, width=4)
    d.line([cx - r, cy + r * 0.7, cx - r, cy - r], fill=col, width=4)
    pts = [(cx - r + 4, cy + r * 0.45), (cx - r * 0.35, cy + r * 0.1),
           (cx, cy + r * 0.35), (cx + r * 0.4, cy - r * 0.25),
           (cx + r - 6, cy - r * 0.7)]
    d.line(pts, fill=col, width=5, joint="curve")
    ax, ay = pts[-1]
    # dollar mark tucked in the top-left corner, clear of the arrow
    d.text((cx - r + 2, cy - r - 2), chr(36), font=font(SANS_B, 22),
           fill=col)


def icon_probe(d, cx, cy, r, col):
    # stars
    for sx, sy in [(cx - r, cy - r * 0.8), (cx + r * 0.85, cy - r * 0.55),
                   (cx + r * 0.6, cy + r * 0.9), (cx - r * 0.7, cy + r * 0.75)]:
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=col)
    # dish: wide open arc facing up-left
    d.arc([cx - 44, cy - 34, cx - 4, cy + 6], 90, 270, fill=col, width=5)
    d.line([cx - 24, cy - 14, cx - 6, cy + 4], fill=col, width=4)
    # body: a clear diamond
    d.polygon([(cx + 2, cy - 16), (cx + 24, cy + 2), (cx + 2, cy + 20),
               (cx - 16, cy + 2)], fill=col)
    # antenna from the body to the top-right + signal arcs
    d.line([cx + 20, cy - 6, cx + 40, cy - 24], fill=col, width=3)
    for rr in (7, 15):
        d.arc([cx + 40 - rr, cy - 24 - rr, cx + 40 + rr, cy - 24 + rr],
              -70, 50, fill=col, width=3)


def icon_cyclone(d, cx, cy, r, col):
    for k in range(5):
        r0 = 8 + k * 7
        start = k * 55
        d.arc([cx - r0, cy - r0, cx + r0, cy + r0], start, start + 250,
              fill=col, width=5)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=col)
    # wind streaks
    for yy, ln in [(-r * 0.9, 26), (r * 0.9, 30)]:
        d.line([cx - r - 6, cy + yy, cx - r - 6 + ln, cy + yy],
               fill=col, width=4)


ICONS = {
    "globe": icon_globe,
    "scales": icon_scales,
    "bridge": icon_bridge,
    "chart": icon_chart,
    "probe": icon_probe,
    "cyclone": icon_cyclone,
}

PANELS = [
    ("globe", (20, 33, 61),
     "TRUMP, XI & PUTIN MEET IN SHENZHEN",
     "First-ever trilateral summit ends with a four-point declaration. No deal on Ukraine."),
    ("scales", (0, 121, 107),
     "ICJ: MYANMAR COMMITTED GENOCIDE",
     "Court rules 9\u20136 against Myanmar over the Rohingya. Reparations ordered."),
    ("bridge", (176, 74, 20),
     "CRIMEA BRIDGE HIT A THIRD TIME",
     "Neptune missiles damage the rail span. Traffic halted across the strait."),
    ("chart", (46, 125, 50),
     "ANTHROPIC IPO: $81.3BN, A RECORD",
     "Priced at $83, first trade $111.50, closed $97.17 \u2014 up 17% on Nasdaq."),
    ("probe", (74, 44, 130),
     "VOYAGER 1: ONE LIGHT-DAY AWAY",
     "NASA confirms the probe is 16 billion miles out, 50 years after launch."),
    ("cyclone", (2, 119, 189),
     "CYCLONE AKVAN NEARS INDIA",
     "Landfall due Friday on the east coast, with winds up to 110 km/h."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 140], fill=NAVY)
    d.rectangle([0, 140, W, 146], fill=GOLD)
    centre(d, W // 2, 22, "19 NOVEMBER 2026", font(SERIF_B, 62), WHITE)
    centre(d, W // 2, 100, "T H U R S D A Y  \u00b7  T H E  W O R L D  I N  O N E  I M A G E",
           font(SANS_B, 21), GOLD)

    # ---- grid ----
    margin, gap = 16, 12
    pw = (W - 2 * margin - gap) // 2          # 492
    ph = (H - 152 - 56 - 2 * gap) // 3        # 264
    top0 = 158
    head_f = font(SANS_B, 28)
    body_f = font(SANS, 20)

    for i, (icon, col, headline, body) in enumerate(PANELS):
        col_i, row_i = i % 2, i // 2
        x0 = margin + col_i * (pw + gap)
        y0 = top0 + row_i * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=(200, 194, 178),
                    width=2)
        d.rectangle([x0, y0, x1, y0 + 9], fill=col)
        # icon in a tinted disc
        cx, cy = x0 + pw // 2, y0 + 62
        d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(238, 236, 228))
        d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], outline=col, width=3)
        ICONS[icon](d, cx, cy, 34, col)
        # headline, centred, up to 2 lines
        hlines = wrap(d, headline, head_f, pw - 36)
        hy = y0 + 122
        for ln in hlines[:2]:
            centre(d, x0 + pw // 2, hy, ln, head_f, INK)
            hy += 33
        # body, centred, up to 2 lines
        blines = wrap(d, body, body_f, pw - 44)
        by = y0 + 196
        for ln in blines[:2]:
            centre(d, x0 + pw // 2, by, ln, body_f, GREY)
            by += 26

    # ---- footer ----
    d.rectangle([0, H - 56, W, H], fill=FOOT_BG)
    centre(d, W // 2, H - 44,
           "Every story above happened or was first reported on 19 November 2026.",
           font(SANS, 21), WHITE)

    img.save(OUT, optimize=True)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
