"""Draw THE WORLD TODAY — Monday 23 November 2026.

A newspaper front page summing up the day's world news, drawn entirely in
code with PIL. No external images. Outputs entry.png (1024x1024, under 1 MiB).
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024
MARGIN = 30
RIGHT = CANVAS_W - MARGIN

PAPER = (247, 242, 228)
INK = (22, 22, 22)
NAVY = (26, 40, 72)
RED = (168, 32, 34)
STEEL = (48, 92, 138)
MUTED = (96, 94, 86)
GOLD = (196, 146, 42)
SEA = (62, 108, 148)
TEAL = (30, 108, 94)
FLAME = (216, 112, 28)
SMOKE = (122, 120, 112)
GREEN = (28, 128, 60)

FONTS = "/usr/share/fonts/truetype/dejavu"


def get_font(size, bold=False, serif=True):
    if serif:
        fname = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        fname = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONTS, fname), size)


def text_wrap(d, text, fnt, width):
    """Greedy word wrap of one paragraph to a pixel width."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if d.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def draw_para(d, x, y, text, fnt, width, fill=INK, gap=None):
    """Draw wrapped paragraph; return y below the last line."""
    if gap is None:
        gap = int(fnt.size * 1.3)
    for line in text_wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += gap
    return y


def draw_rule(d, x0, x1, y, thick=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=thick)


def draw_tag(d, x, y, text, fill=RED):
    d.text((x, y), text, font=get_font(14, bold=True, serif=False), fill=fill)
    return y + 22


def starburst(d, cx, cy, radius, outer=(232, 122, 30), inner=(250, 210, 90)):
    pts = []
    for i in range(20):
        r = radius if i % 2 == 0 else radius * 0.45
        a = -math.pi / 2 + i * math.pi / 10
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=outer)
    pts = []
    for i in range(20):
        r = radius * 0.55 if i % 2 == 0 else radius * 0.28
        a = -math.pi / 2 + i * math.pi / 10
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=inner)


def draw_ship_panel(d, x, y, w, h):
    """Corvette listing in Benghazi harbour, sea drones closing in."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + int(h * 0.48)], fill=(212, 224, 230))
    d.rectangle([x, y + int(h * 0.48), x + w, y + h], fill=(118, 164, 198))
    d.text((x + 10, y + 5), "BENGHAZI, LIBYA", font=get_font(11, bold=True,
           serif=False), fill=NAVY)
    # quay
    d.rectangle([x + 8, y + int(h * 0.48) - 8, x + w - 8, y + int(h * 0.48)],
                fill=(158, 150, 136), outline=INK)
    # listing corvette, bow up
    d.polygon([(x + 60, y + int(h * 0.72)), (x + 330, y + int(h * 0.50)),
               (x + 370, y + int(h * 0.62)), (x + 100, y + int(h * 0.86))],
              fill=(88, 94, 102), outline=INK)
    d.rectangle([x + 230, y + int(h * 0.40), x + 272, y + int(h * 0.56)],
                fill=(205, 205, 205), outline=INK)
    starburst(d, x + 282, y + int(h * 0.50), 15)
    # smoke curls
    for sx, sy, sr in ((288, 22, 7), (300, 12, 9), (314, 6, 6)):
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=SMOKE)
    # two sea drones with wakes
    for dx in (x + 46, x + 130):
        d.ellipse([dx, y + h - 24, dx + 28, y + h - 13], fill=INK)
        d.line([(dx + 28, y + h - 18), (dx + 48, y + h - 18)], fill=INK,
               width=2)
    d.text((x + w - 104, y + h - 22), "MERKURY SUNK",
           font=get_font(11, bold=True, serif=False), fill=INK)
    d.text((x + 430, y + 5), "7 DRONES", font=get_font(11, bold=True,
           serif=False), fill=RED)


def draw_strait_panel(d, x, y, w, h):
    """Oil tanker in the Strait of Hormuz with naval mines below."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + int(h * 0.45)], fill=(216, 228, 232))
    d.rectangle([x, y + int(h * 0.45), x + w, y + h], fill=(146, 186, 212))
    d.text((x + 10, y + 5), "STRAIT OF HORMUZ", font=get_font(11, bold=True,
           serif=False), fill=NAVY)
    # tanker
    d.rectangle([x + 40, y + 52, x + w - 40, y + 66], fill=(120, 40, 40),
                outline=INK)
    d.rectangle([x + w - 120, y + 40, x + w - 92, y + 52], fill=(240, 240, 240),
                outline=INK)
    d.rectangle([x + 60, y + 40, x + 84, y + 52], fill=(240, 240, 240),
                outline=INK)
    # mines: spiked circles
    for mx, my in ((x + 90, y + h - 16), (x + 190, y + h - 12),
                   (x + 280, y + h - 18)):
        d.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=INK)
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            d.line([(mx + 8 * math.cos(rad), my + 8 * math.sin(rad)),
                    (mx + 13 * math.cos(rad), my + 13 * math.sin(rad))],
                   fill=INK, width=2)
    # waves
    for wy in (y + h - 32, y + h - 26):
        for wx in range(x + 8, x + w - 8, 36):
            d.arc([wx, wy, wx + 30, wy + 10], 180, 360, fill=SEA, width=2)
    d.text((x + w - 10 - d.textlength("BLOCKADE", font=get_font(11, bold=True,
           serif=False)), y + 5), "BLOCKADE", font=get_font(11, bold=True,
           serif=False), fill=RED)


def draw_eu_panel(d, x, y, w, h):
    """A ring of EU stars over a bank building and a barred ship."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 240))
    d.text((x + 10, y + 4), "BRUSSELS", font=get_font(11, bold=True,
           serif=False), fill=NAVY)
    # ring of stars, kept clear of the BRUSSELS label
    cx, cy, rr = x + 70, y + h // 2 + 12, 20
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        sx, sy = cx + rr * math.cos(a), cy + rr * math.sin(a)
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
    # bank building, right
    bx0, by0 = x + 130, y + 18
    d.polygon([(bx0 + 60, by0), (bx0, by0 + 18), (bx0 + 120, by0 + 18)],
              fill=NAVY, outline=INK)
    d.rectangle([bx0 + 6, by0 + 18, bx0 + 114, y + h - 6], fill=(200, 205, 215),
                outline=INK)
    for col in range(4):
        d.rectangle([bx0 + 16 + col * 28, by0 + 26, bx0 + 30 + col * 28,
                     y + h - 14], fill=NAVY)
    # red ban cross over the bank
    d.line([(bx0 + 6, by0 + 18), (bx0 + 114, y + h - 6)], fill=RED, width=4)
    d.line([(bx0 + 114, by0 + 18), (bx0 + 6, y + h - 6)], fill=RED, width=4)
    d.text((x + w - 96, y + h - 20), "60 BANKS", font=get_font(11, bold=True,
           serif=False), fill=RED)


def draw_fire_panel(d, x, y, w, h):
    """Three-storey factory with flames and a smoke column."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    d.text((x + 10, y + 4), "CIKANDE, BANTEN", font=get_font(11, bold=True,
           serif=False), fill=NAVY)
    base = y + h
    d.rectangle([x + 44, y + 26, x + w - 44, base], fill=(178, 170, 148),
                outline=INK)
    for wy in range(y + 34, base - 8, 16):
        for wx in range(x + 56, x + w - 64, 30):
            d.rectangle([wx, wy, wx + 12, wy + 9], fill=(58, 58, 58))
    for fx, fh in ((170, 18), (210, 24), (250, 16), (290, 22)):
        d.polygon([(x + fx - 10, y + 26), (x + fx, y + 26 - fh),
                   (x + fx + 10, y + 26)], fill=FLAME, outline=RED)
    for sx, sy, sr in ((220, 12, 8), (240, 4, 10), (262, -2, 7)):
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=SMOKE)
    d.text((x + w - 76, y + h - 20), "24 DEAD", font=get_font(11, bold=True,
           serif=False), fill=RED)


def draw_chip_panel(d, x, y, w, h):
    """A green chip with a steep rising arrow — Nvidia's rebound."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + h], fill=(224, 238, 226))
    d.text((x + 10, y + 4), "SANTA CLARA", font=get_font(11, bold=True,
           serif=False), fill=NAVY)
    # chip
    cx0, cy0 = x + 30, y + 24
    d.rectangle([cx0, cy0, cx0 + 74, cy0 + 54], fill=(30, 30, 30), outline=INK)
    d.rectangle([cx0 + 18, cy0 + 16, cx0 + 56, cy0 + 38], fill=GREEN,
                outline=(200, 230, 200))
    for pin in range(4):
        d.line([(cx0 + 8 + pin * 18, cy0 - 6), (cx0 + 8 + pin * 18, cy0)],
               fill=INK, width=2)
        d.line([(cx0 + 8 + pin * 18, cy0 + 54),
                (cx0 + 8 + pin * 18, cy0 + 60)], fill=INK, width=2)
    # rising arrow, climbing steadily to the top right
    ax0, ay0 = x + 130, y + h - 18
    d.line([(ax0, ay0), (ax0 + 60, ay0 - 22), (ax0 + 100, ay0 - 28),
            (x + w - 16, y + 18)], fill=GREEN, width=5, joint="curve")
    d.polygon([(x + w - 16, y + 18), (x + w - 34, y + 16),
               (x + w - 20, y + 34)], fill=GREEN)
    lbl = "+33% IN A DAY"
    d.text((x + w - 10 - d.textlength(lbl, font=get_font(12, bold=True,
           serif=False)), y + h - 18), lbl, font=get_font(12, bold=True,
           serif=False), fill=GREEN)


def draw_peace_panel(d, x, y, w, h):
    """Two halves of a map joined by a white dove — Armenia / Azerbaijan."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + h], fill=(236, 230, 214))
    d.text((x + 10, y + 4), "YEREVAN", font=get_font(11, bold=True,
           serif=False), fill=NAVY)
    # left half (red/blue/orange stripes) and right half (blue/red/green)
    mid = x + w // 2
    for i, col in enumerate(((210, 60, 60), (60, 90, 170), (230, 140, 40))):
        d.rectangle([x + 14, y + 22 + i * 14, mid - 6, y + 36 + i * 14],
                    fill=col)
    for i, col in enumerate(((60, 110, 200), (210, 60, 60), (40, 140, 80))):
        d.rectangle([mid + 6, y + 22 + i * 14, x + w - 14, y + 36 + i * 14],
                    fill=col)
    # handshake line between the halves
    d.line([(mid, y + 22), (mid, y + h - 6)], fill=INK, width=2)
    # dove: simple white bird over the stripes
    dx, dy = x + w // 2, y + 44
    d.ellipse([dx - 22, dy - 6, dx + 10, dy + 6], fill=(255, 255, 255),
              outline=INK)
    d.ellipse([dx + 6, dy - 12, dx + 18, dy - 2], fill=(255, 255, 255),
              outline=INK)
    d.polygon([(dx + 14, dy - 12), (dx + 30, dy - 20), (dx + 26, dy - 4)],
              fill=(255, 255, 255), outline=INK)
    d.polygon([(dx - 22, dy - 2), (dx - 38, dy - 10), (dx - 34, dy + 4)],
              fill=(255, 255, 255), outline=INK)
    lbl = "PEACE DEAL NEXT"
    d.text((x + w - 10 - d.textlength(lbl, font=get_font(11, bold=True,
           serif=False)), y + 4), lbl, font=get_font(11, bold=True,
           serif=False), fill=TEAL)


def draw_mexico_panel(d, x, y, w, h):
    """Desert road in Sinaloa, a helicopter above, burning truck below."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + int(h * 0.5)], fill=(222, 226, 232))
    d.rectangle([x, y + int(h * 0.5), x + w, y + h], fill=(214, 186, 138))
    d.text((x + 10, y + 4), "GUASAVE, SINALOA", font=get_font(11, bold=True,
           serif=False), fill=NAVY)
    # helicopter, below the label, right of centre
    hx, hy = x + 200, y + 34
    d.ellipse([hx - 26, hy - 8, hx + 26, hy + 8], fill=(70, 74, 80),
              outline=INK)
    d.line([(hx + 26, hy), (hx + 52, hy - 4)], fill=INK, width=3)
    d.line([(hx - 52, hy - 10), (hx + 52, hy - 10)], fill=INK, width=3)
    d.line([(hx, hy + 8), (hx, hy + 16)], fill=INK, width=3)
    # road with dashes
    d.rectangle([x, y + int(h * 0.62), x + w, y + int(h * 0.78)],
                fill=(70, 70, 70))
    for rx in range(x + 12, x + w - 12, 44):
        d.rectangle([rx, y + int(h * 0.70), rx + 22, y + int(h * 0.70) + 3],
                    fill=(240, 220, 80))
    # burning truck on the road
    tx, ty = x + 90, y + int(h * 0.62)
    d.rectangle([tx, ty - 12, tx + 80, ty + 2], fill=(120, 40, 40),
                outline=INK)
    for fx, fh in ((tx + 16, 14), (tx + 40, 18), (tx + 62, 12)):
        d.polygon([(fx - 9, ty - 12), (fx, ty - 12 - fh), (fx + 9, ty - 12)],
                  fill=FLAME)
    lbl = "20 DEAD IN RAID"
    d.text((x + w - 10 - d.textlength(lbl, font=get_font(11, bold=True,
           serif=False)), y + 4), lbl, font=get_font(11, bold=True,
           serif=False), fill=RED)


def build_page():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    mast = "THE WORLD TODAY"
    mf = get_font(62, bold=True)
    d.text(((CANVAS_W - d.textlength(mast, font=mf)) / 2, 12), mast, font=mf,
           fill=INK)
    draw_rule(d, MARGIN, RIGHT, 86, 3)
    draw_rule(d, MARGIN, RIGHT, 91, 1)

    # --- date band ---
    d.rectangle([MARGIN, 100, RIGHT, 140], fill=NAVY)
    date_line = "MONDAY  23  NOVEMBER  2026"
    df = get_font(28, bold=True)
    d.text(((CANVAS_W - d.textlength(date_line, font=df)) / 2, 106), date_line,
           font=df, fill=(255, 255, 255))

    # --- deck ---
    deck = ("Kyiv claims warship sunk off Libya  •  Iran defies blockade  •  "
            "Nvidia brings Huang back")
    deckf = get_font(15, serif=False)
    d.text(((CANVAS_W - d.textlength(deck, font=deckf)) / 2, 148), deck,
           font=deckf, fill=MUTED)
    draw_rule(d, MARGIN, RIGHT, 172, 2)

    # --- ROW A: lead (Merkury) + Iran ---
    y = 182
    y = draw_tag(d, MARGIN, y, "WAR AT SEA  —  BENGHAZI, LIBYA")
    y = draw_para(d, MARGIN, y, "KYIV: OUR SEA DRONES SANK RUSSIAN WARSHIP",
                  get_font(38, bold=True), 590, gap=44)
    y = draw_para(d, MARGIN, y + 4,
                  "Zelenskyy says seven naval drones sank the corvette "
                  "Merkury and hit a weapons cargo ship — 2,400 km from the "
                  "front line.", get_font(16), 590, gap=21)
    draw_ship_panel(d, MARGIN, y + 8, 590, 96)
    lead_end = y + 8 + 96

    y2 = 182
    y2 = draw_tag(d, 648, y2, "GULF CRISIS  —  TEHRAN")
    y2 = draw_para(d, 648, y2, "IRAN VOWS TO DEFY U.S. BLOCKADE",
                   get_font(25, bold=True), 346, gap=30)
    y2 = draw_para(d, 648, y2 + 4,
                   "Tehran says it will use 'all available tools' against "
                   "the oil blockade. Washington sanctions its shadow banks.",
                   get_font(15), 346, gap=20)
    draw_strait_panel(d, 648, y2 + 8, 346, 96)
    iran_end = y2 + 8 + 96

    row_a_end = max(lead_end, iran_end)
    draw_rule(d, MARGIN, RIGHT, row_a_end + 10, 2)

    # --- ROW B: EU sanctions + Indonesia fire ---
    y = row_a_end + 20
    y = draw_tag(d, MARGIN, y, "EUROPE  —  BRUSSELS")
    y = draw_para(d, MARGIN, y, "EU UNVEILS 22ND SANCTIONS PACKAGE",
                  get_font(22, bold=True), 460, gap=27)
    y = draw_para(d, MARGIN, y + 4,
                  "60 more banks cut from SWIFT, crypto crackdown, 70 more "
                  "shadow-fleet ships, Russian flag banned at EU sport.",
                  get_font(14), 460, gap=18)
    draw_eu_panel(d, MARGIN, y + 8, 460, 66)
    eu_end = y + 8 + 66

    y2 = row_a_end + 20
    y2 = draw_tag(d, 522, y2, "DISASTER  —  INDONESIA")
    y2 = draw_para(d, 522, y2, "FACTORY FIRE: 24 DEAD, 30 STILL MISSING",
                   get_font(22, bold=True), 472, gap=27)
    y2 = draw_para(d, 522, y2 + 4,
                   "Rescuers pick through the burned candy plant in Cikande; "
                   "families wait for DNA results to name the dead.",
                   get_font(14), 472, gap=18)
    draw_fire_panel(d, 522, y2 + 8, 472, 66)
    fire_end = y2 + 8 + 66

    row_b_end = max(eu_end, fire_end)
    draw_rule(d, MARGIN, RIGHT, row_b_end + 10, 2)

    # --- ROW C: Nvidia + Armenia + Mexico ---
    y = row_b_end + 20
    y = draw_tag(d, MARGIN, y, "MARKETS  —  WALL STREET")
    y = draw_para(d, MARGIN, y, "HUANG IS BACK AT NVIDIA; SHARES SOAR",
                  get_font(19, bold=True), 300, gap=23)
    y = draw_para(d, MARGIN, y + 4,
                  "Board reinstates its founder as CEO 11 days after he "
                  "quit. Shares jump about a third.",
                  get_font(13), 300, gap=17)
    draw_chip_panel(d, MARGIN, y + 8, 300, 70)
    nv_end = y + 8 + 70

    y2 = row_b_end + 20
    y2 = draw_tag(d, 362, y2, "DIPLOMACY  —  YEREVAN")
    y2 = draw_para(d, 362, y2, "ARMENIA DRAFTS CHARTER FOR PEACE",
                   get_font(19, bold=True), 300, gap=23)
    y2 = draw_para(d, 362, y2 + 4,
                   "New constitution drops the Karabakh claim Baku objected "
                   "to. Pashinyan stakes his job on the vote.",
                   get_font(13), 300, gap=17)
    draw_peace_panel(d, 362, y2 + 8, 300, 70)
    am_end = y2 + 8 + 70

    y3 = row_b_end + 20
    y3 = draw_tag(d, 694, y3, "MEXICO  —  SINALOA")
    y3 = draw_para(d, 694, y3, "U.S. DRONE HELPED CATCH DRUG LORD",
                   get_font(19, bold=True), 300, gap=23)
    y3 = draw_para(d, 694, y3 + 4,
                   "'El Chapo Isidro', an FBI most-wanted fugitive, seized "
                   "in Guasave. Cartel violence kills 20.",
                   get_font(13), 300, gap=17)
    draw_mexico_panel(d, 694, y3 + 8, 300, 70)
    mx_end = y3 + 8 + 70

    row_c_end = max(nv_end, am_end, mx_end)

    # --- markets strip ---
    sy = row_c_end + 12
    d.rectangle([MARGIN, sy, RIGHT, sy + 38], outline=INK, width=2)
    d.text((MARGIN + 12, sy + 10), "MARKETS", font=get_font(15, bold=True,
           serif=False), fill=RED)
    strip = ("NVIDIA +33%  •  NASDAQ +7%  •  S&P 500 +5%  •  OIL AT 3-MONTH LOW")
    d.text((MARGIN + 118, sy + 11), strip, font=get_font(14, bold=True,
           serif=False), fill=INK)

    # --- footer ---
    foot = ("THE WORLD TODAY  •  Monday 23 November 2026  •  All stories first "
            "reported on this day  •  Sources: Reuters  •  AP  •  NPR  •  "
            "European Commission  •  U.S. Treasury")
    footf = get_font(12, serif=False)
    d.text(((CANVAS_W - d.textlength(foot, font=footf)) / 2, sy + 50), foot,
           font=footf, fill=MUTED)

    print(f"rows end: A={row_a_end} B={row_b_end} C={row_c_end} "
          f"strip={sy} footer={sy + 50}")
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    page = build_page()
    page.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {page.size[0]}x{page.size[1]}, {size} bytes")
    if size > 1048576:
        print("ERROR: over the 1 MiB limit", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
