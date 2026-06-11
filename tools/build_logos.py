#!/usr/bin/env python3
"""Generate the full NIYA brand identity: logos, variants and mockups.

v2 — engineered identity:
  * Mark: a monolithic letter N — two solid precast columns with masonry
    joint lines, an orange structural diagonal, a stepped tower crown and
    a deep-blue foundation slab.
  * Wordmark NIYA: fully custom squared industrial letterforms (drawn as
    polygons, no font), in the language of engineering corporations.

Small/utility text uses Liberation Sans converted to outlines with
fontTools, so every SVG is fully self-contained. PNG previews are
rendered with cairosvg.
"""

import math
import os

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GREY = "#4A4A4A"        # concrete grey
ORANGE = "#F97316"      # construction orange
BLUE = "#0F172A"        # deep blue
WHITE = "#FFFFFF"
BLACK = "#111111"
LIGHT = "#CBD5E1"

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


class TextEngine:
    """Renders text as SVG path outlines using a TTF font (utility text)."""

    def __init__(self, path):
        self.font = TTFont(path)
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upem = self.font["head"].unitsPerEm

    def _advance(self, ch):
        return self.glyphs[self.cmap[ord(ch)]].width

    def width(self, text, size, track_em=0.0):
        units = sum(self._advance(c) for c in text)
        return size * units / self.upem + track_em * size * max(len(text) - 1, 0)

    def fit_size(self, text, target_w, track_em=0.0):
        units = sum(self._advance(c) for c in text) / self.upem
        return target_w / (units + track_em * max(len(text) - 1, 0))

    def track_to_fit(self, text, size, target_w):
        """Letter-spacing (em) that justifies text to target_w."""
        base = self.width(text, size, 0.0)
        n = max(len(text) - 1, 1)
        return max((target_w - base) / (size * n), 0.0)

    def _glyph_d(self, ch):
        pen = SVGPathPen(self.glyphs)
        self.glyphs[self.cmap[ord(ch)]].draw(pen)
        return pen.getCommands()

    def text(self, text, size, x, y, fill, track_em=0.0, anchor="start"):
        s = size / self.upem
        w = self.width(text, size, track_em)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        out = [f'<g fill="{fill}">']
        cx = x
        for ch in text:
            adv = self._advance(ch) * s + track_em * size
            if ch != " ":
                d = self._glyph_d(ch)
                if d:
                    out.append(
                        f'<path transform="translate({cx:.2f} {y:.2f}) '
                        f'scale({s:.6f} {-s:.6f})" d="{d}"/>'
                    )
            cx += adv
        out.append("</g>")
        return "".join(out)

    def arc_text(self, text, size, cx, cy, r, fill, track_em=0.0, bottom=False):
        s = size / self.upem
        advs = [self._advance(c) * s + track_em * size for c in text]
        total = sum(advs) - (track_em * size if text else 0)
        theta = total / r
        out = [f'<g fill="{fill}">']
        acc = 0.0
        for ch, a in zip(text, advs):
            mid = acc + (a - track_em * size) / 2
            acc += a
            ang = (-theta / 2 + mid / r) if not bottom else (theta / 2 - mid / r)
            if ch == " ":
                continue
            d = self._glyph_d(ch)
            if not d:
                continue
            ypos = cy - r if not bottom else cy + r
            xoff = cx - (a - track_em * size) / 2
            out.append(
                f'<path transform="rotate({math.degrees(ang):.3f} {cx} {cy}) '
                f'translate({xoff:.2f} {ypos:.2f}) scale({s:.6f} {-s:.6f})" d="{d}"/>'
            )
        out.append("</g>")
        return "".join(out)


# ----------------------------------------------- custom brand typeface ----
# Squared industrial capitals drawn on a 100-unit cap-height grid,
# stroke weight 24. y grows downward, baseline at 100.
# Each entry: (advance, path-d). Holes use even-odd fill.
GLYPHS = {
    "N": (72, "M0 100 L0 0 L24 0 L48 52 L48 0 L72 0 L72 100 L48 100 "
              "L24 48 L24 100 Z"),
    "I": (24, "M0 0 L24 0 L24 100 L0 100 Z"),
    "Y": (72, "M0 0 L25 0 L36 26 L47 0 L72 0 L48 50 L48 100 L24 100 "
              "L24 50 Z"),
    "A": (78, "M26 0 L52 0 L78 100 L54 100 L48 80 L30 80 L24 100 L0 100 Z "
              "M34.5 60 L43.5 60 L39 36 Z"),
    "K": (76, "M0 0 L24 0 L24 36 L50 0 L76 0 L43 44 L76 100 L49 100 "
              "L24 64 L24 100 L0 100 Z"),
    "R": (76, "M0 0 L74 0 L74 54 L52 54 L76 100 L50 100 L29 54 L24 54 "
              "L24 100 L0 100 Z M24 20 L50 20 L50 34 L24 34 Z"),
    "S": (68, "M0 0 L68 0 L68 22 L22 22 L22 39 L68 39 L68 100 L0 100 "
              "L0 78 L46 78 L46 61 L0 61 Z"),
    "H": (72, "M0 0 L24 0 L24 39 L48 39 L48 0 L72 0 L72 100 L48 100 "
              "L48 61 L24 61 L24 100 L0 100 Z"),
}
XW = 1.08  # horizontal extension factor — premium "extended" stance
KERN = {("Y", "A"): -12, ("A", "Y"): -12}  # optical pair corrections


class BrandType:
    """The custom NIYA letterforms. Sizes are cap heights."""

    def _advance(self, ch):
        return GLYPHS[ch][0] * XW if ch in GLYPHS else 40.0

    def _advances(self, text):
        out = []
        for i, ch in enumerate(text):
            a = self._advance(ch)
            if i + 1 < len(text):
                a += KERN.get((ch, text[i + 1]), 0) * XW
            out.append(a)
        return out

    def width(self, text, cap, track_em=0.0):
        units = sum(self._advances(text))
        return cap * units / 100 + track_em * cap * max(len(text) - 1, 0)

    def fit_size(self, text, target_w, track_em=0.0):
        units = sum(self._advances(text)) / 100
        return target_w / (units + track_em * max(len(text) - 1, 0))

    def text(self, text, cap, x, y, fill, track_em=0.0, anchor="start"):
        s = cap / 100
        w = self.width(text, cap, track_em)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        out = [f'<g fill="{fill}" fill-rule="evenodd">']
        cx = x
        for ch, au in zip(text, self._advances(text)):
            adv = au * s + track_em * cap
            if ch in GLYPHS:
                out.append(
                    f'<path transform="translate({cx:.2f} {y - cap:.2f}) '
                    f'scale({s * XW:.6f} {s:.6f})" d="{GLYPHS[ch][1]}"/>'
                )
            cx += adv
        out.append("</g>")
        return "".join(out)

    def arc_text(self, text, cap, cx, cy, r, fill, track_em=0.0):
        s = cap / 100
        advs = [a * s + track_em * cap for a in self._advances(text)]
        total = sum(advs) - (track_em * cap if text else 0)
        theta = total / r
        out = [f'<g fill="{fill}" fill-rule="evenodd">']
        acc = 0.0
        for ch, a in zip(text, advs):
            mid = acc + (a - track_em * cap) / 2
            acc += a
            ang = -theta / 2 + mid / r
            if ch not in GLYPHS:
                continue
            xoff = cx - (a - track_em * cap) / 2
            out.append(
                f'<path transform="rotate({math.degrees(ang):.3f} {cx} {cy}) '
                f'translate({xoff:.2f} {cy - r - cap:.2f}) '
                f'scale({s * XW:.6f} {s:.6f})" d="{GLYPHS[ch][1]}"/>'
            )
        out.append("</g>")
        return "".join(out)


bold = TextEngine(BOLD)
reg = TextEngine(REGULAR)
brand = BrandType()


# ---------------------------------------------------------------- icon ----
# Design space of the mark: x 0..168, y 24..194 (w=168, h=170).
ICON_X, ICON_Y, ICON_W, ICON_H = 0, 24, 168, 170


def icon(grey=GREY, orange=ORANGE, blue=BLUE, tx=0.0, ty=0.0, s=1.0):
    """The NIYA mark, v2: a monolithic N — solid precast columns with
    masonry joints, structural diagonal, stepped tower crown, foundation."""
    g = [f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">']
    g.append(f'<rect x="12" y="40" width="42" height="136" fill="{grey}"/>')
    g.append(f'<rect x="114" y="52" width="42" height="124" fill="{grey}"/>')
    g.append(f'<rect x="114" y="24" width="28" height="24" fill="{grey}"/>')
    for y in (86, 130):                                  # precast joint lines
        g.append(f'<rect x="12" y="{y}" width="42" height="4" fill="{WHITE}"/>')
        g.append(f'<rect x="114" y="{y}" width="42" height="4" fill="{WHITE}"/>')
    g.append(f'<polygon points="12,40 54,40 156,176 114,176" fill="{orange}"/>')
    g.append(f'<rect x="0" y="182" width="168" height="12" fill="{blue}"/>')
    g.append("</g>")
    return "".join(g)


def svg(w, h, body, bg=None):
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}">'
    )
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return head + bgr + body + "</svg>"


def write(relpath, content):
    path = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return path


def render(svg_rel, png_rel, width):
    cairosvg.svg2png(
        url=os.path.join(ROOT, svg_rel),
        write_to=os.path.join(ROOT, png_rel),
        output_width=width,
    )


# ------------------------------------------------------- logo lockups ----
WORD = "NIYA"
TAG_SHORT = "CONSTRUCTION MATERIALS"
TAG_FULL = "CONCRETE  •  BLOCKS  •  INFRASTRUCTURE"


def wordmark(x, y, cap, fill, accent, anchor="start", track_em=0.18):
    """NIYA in the custom letterforms, with the orange block full-stop."""
    w = brand.width(WORD, cap, track_em)
    sq = 0.22 * cap
    full = w + 0.18 * cap + sq
    if anchor == "middle":
        x -= full / 2
    elif anchor == "end":
        x -= full
    parts = [brand.text(WORD, cap, x, y, fill, track_em)]
    parts.append(
        f'<rect x="{x + w + 0.18 * cap:.2f}" y="{y - sq:.2f}" '
        f'width="{sq:.2f}" height="{sq:.2f}" fill="{accent}"/>'
    )
    return "".join(parts)


def wm_full_width(cap, track_em=0.18):
    return brand.width(WORD, cap, track_em) + 0.40 * cap


def logo_primary(grey, orange, blue, tag_fill, bg=None):
    W, H = 480, 540
    body = []
    s = 1.5
    body.append(icon(grey, orange, blue,
                     tx=W / 2 - (ICON_X + ICON_W / 2) * s, ty=40 - ICON_Y * s, s=s))
    cap = 95
    body.append(wordmark(W / 2, 450, cap, blue, orange, anchor="middle"))
    tsize = 20
    tw = wm_full_width(cap) - 6
    track = bold.track_to_fit(TAG_SHORT, tsize, tw)
    body.append(bold.text(TAG_SHORT, tsize, W / 2, 502, tag_fill, track, "middle"))
    return svg(W, H, "".join(body), bg)


def logo_horizontal(grey, orange, blue, tag_fill, bg=None):
    W, H = 900, 340
    body = []
    s = 1.45
    body.append(icon(grey, orange, blue, tx=64 - ICON_X * s,
                     ty=H / 2 - (ICON_Y + ICON_H / 2) * s, s=s))
    x0 = 64 + ICON_W * s + 68
    body.append(f'<rect x="{x0 - 34}" y="58" width="3" height="224" fill="#D1D5DB"/>')
    cap = 128
    body.append(wordmark(x0, 190, cap, blue, orange, track_em=0.16))
    tsize = 22
    tw = brand.width(WORD, cap, 0.16) + 0.40 * cap
    track = bold.track_to_fit(TAG_SHORT, tsize, tw)
    body.append(bold.text(TAG_SHORT, tsize, x0 + 2, 248, tag_fill, track))
    return svg(W, H, "".join(body), bg)


def logo_monogram(grey, orange, blue, bg=None):
    W = 240
    body = icon(grey, orange, blue, tx=(W - ICON_W) / 2 - ICON_X,
                ty=(W - ICON_H) / 2 - ICON_Y, s=1.0)
    return svg(W, W, body, bg)


def logo_app_icon():
    W = 512
    body = [f'<rect width="{W}" height="{W}" rx="100" fill="{BLUE}"/>']
    s = 1.55
    body.append(icon(WHITE, ORANGE, WHITE,
                     tx=W / 2 - (ICON_X + ICON_W / 2) * s,
                     ty=W / 2 - (ICON_Y + ICON_H / 2) * s, s=s))
    return svg(W, W, "".join(body))


def logo_emblem():
    W = 420
    c = W / 2
    body = [
        f'<circle cx="{c}" cy="{c}" r="200" fill="{BLUE}"/>',
        f'<circle cx="{c}" cy="{c}" r="148" fill="{WHITE}"/>',
        f'<circle cx="{c}" cy="{c}" r="155" fill="none" stroke="{ORANGE}" stroke-width="4"/>',
    ]
    body.append(icon(GREY, ORANGE, BLUE,
                     tx=c - (ICON_X + ICON_W / 2) * 0.96,
                     ty=c - (ICON_Y + ICON_H / 2) * 0.96, s=0.96))
    body.append(brand.arc_text(WORD, 34, c, c, 164, WHITE, 0.85))
    body.append(bold.arc_text("CONSTRUCTION MATERIALS", 22, c, c, 186,
                              LIGHT, 0.12, bottom=True))
    for sgn in (-1, 1):
        x = c + sgn * 177
        body.append(
            f'<rect x="{x - 7}" y="{c - 7}" width="14" height="14" '
            f'fill="{ORANGE}" transform="rotate(45 {x} {c})"/>'
        )
    return svg(W, W, "".join(body))


# ------------------------------------------------------------ mockups ----
def mockup_truck():
    W, H = 1400, 800
    b = [f'<rect width="{W}" height="{H}" fill="#E8EDF3"/>']
    # road
    b.append(f'<rect y="640" width="{W}" height="160" fill="#3A3F46"/>')
    for x in range(40, W, 160):
        b.append(f'<rect x="{x}" y="712" width="80" height="8" fill="#9CA3AF"/>')

    wheel_y = 640

    def wheel(cx, r=58):
        return (
            f'<circle cx="{cx}" cy="{wheel_y}" r="{r}" fill="#1A1D21"/>'
            f'<circle cx="{cx}" cy="{wheel_y}" r="{r * 0.52:.0f}" fill="#9CA3AF"/>'
            f'<circle cx="{cx}" cy="{wheel_y}" r="{r * 0.2:.0f}" fill="#4B5563"/>'
        )

    # chassis rail
    b.append(f'<rect x="300" y="560" width="880" height="34" fill="#1F2937"/>')
    b.append(f'<rect x="300" y="594" width="880" height="10" fill="#111827"/>')

    # cab (facing left)
    b.append(
        f'<path d="M150,594 L150,400 Q150,330 220,330 L390,330 L390,594 Z" fill="{BLUE}"/>'
    )
    b.append('<path d="M172,440 L172,360 Q172,348 188,348 L350,348 L350,440 Z" fill="#94A3B8"/>')
    b.append('<rect x="258" y="348" width="6" height="92" fill="#0B1120"/>')
    b.append(f'<rect x="138" y="530" width="24" height="64" fill="{ORANGE}"/>')
    b.append('<rect x="146" y="480" width="14" height="26" fill="#FACC15"/>')
    b.append('<rect x="290" y="348" width="5" height="246" fill="#0B1120"/>')
    b.append(icon(WHITE, ORANGE, WHITE, tx=302, ty=460, s=0.36))

    # rear pedestal + charge hopper
    b.append('<polygon points="915,560 1055,560 1025,420 945,420" fill="#4A4A4A"/>')
    b.append('<polygon points="945,355 1025,355 1005,420 965,420" fill="#6B7280"/>')
    b.append('<rect x="939" y="332" width="92" height="26" fill="#4A4A4A"/>')
    # front pedestal
    b.append('<polygon points="500,560 630,560 600,460 530,460" fill="#4A4A4A"/>')

    # drum
    cx, cy = 720, 400
    b.append(f'<g transform="rotate(-8 {cx} {cy})">')
    drum = (
        f'M{cx - 230},{cy - 58} L{cx - 160},{cy - 105} L{cx + 130},{cy - 105} '
        f'L{cx + 215},{cy - 52} L{cx + 215},{cy + 52} L{cx + 130},{cy + 105} '
        f'L{cx - 160},{cy + 105} L{cx - 230},{cy + 58} Z'
    )
    b.append(f'<defs><clipPath id="drum"><path d="{drum}"/></clipPath></defs>')
    b.append(f'<path d="{drum}" fill="{WHITE}" stroke="#9CA3AF" stroke-width="4"/>')
    b.append(f'<g clip-path="url(#drum)">')
    b.append(f'<rect x="{cx - 235}" y="{cy - 120}" width="74" height="240" '
             f'fill="{ORANGE}" transform="rotate(18 {cx - 190} {cy})"/>')
    b.append(f'<rect x="{cx + 168}" y="{cy - 120}" width="64" height="240" '
             f'fill="{BLUE}" transform="rotate(18 {cx + 195} {cy})"/>')
    b.append("</g>")
    b.append(wordmark(cx + 5, cy + 12, 62, BLUE, ORANGE, anchor="middle",
                      track_em=0.16))
    b.append(bold.text("READY MIX CONCRETE", 22, cx + 5, cy + 52, ORANGE, 0.12, "middle"))
    b.append("</g>")

    # wheels & guards
    b.append('<path d="M165,640 A70,70 0 0 1 305,640 L290,640 A55,55 0 0 0 180,640 Z" fill="#0B1120"/>')
    b.append(wheel(235))
    for cxw in (900, 1010, 1120):
        b.append(wheel(cxw))
    b.append('<rect x="830" y="566" width="360" height="14" fill="#111827"/>')

    b.append(bold.text("NIYA READY MIX CONCRETE  •  TRUCK BRANDING CONCEPT",
                       20, W / 2, 770, "#9CA3AF", 0.1, "middle"))
    return svg(W, H, "".join(b))


def mockup_signboard():
    W, H = 1400, 800
    b = [f'<rect width="{W}" height="{H}" fill="#DDE5EE"/>']
    b.append(f'<rect y="620" width="{W}" height="180" fill="#C2C7CE"/>')
    # building facade
    b.append('<rect x="80" y="200" width="1240" height="420" fill="#D8DADD"/>')
    b.append('<rect x="80" y="184" width="1240" height="20" fill="#6B7280"/>')
    for x in range(100, 1320, 40):
        b.append(f'<rect x="{x}" y="430" width="3" height="190" fill="#C4C7CB"/>')
    # high windows
    for x0 in (130, 850):
        for i in range(5):
            b.append(f'<rect x="{x0 + i * 85}" y="445" width="58" height="44" fill="#AEB6C2"/>')
    # roller door
    b.append('<rect x="630" y="430" width="180" height="190" fill="#6B7280"/>')
    for y in range(450, 620, 24):
        b.append(f'<rect x="630" y="{y}" width="180" height="4" fill="#5B6470"/>')
    # fascia sign
    b.append(f'<rect x="80" y="230" width="1240" height="160" fill="{BLUE}"/>')
    b.append(f'<rect x="80" y="390" width="1240" height="12" fill="{ORANGE}"/>')
    s = 0.72
    ix = 400
    b.append(icon(WHITE, ORANGE, WHITE, tx=ix - ICON_X * s,
                  ty=310 - (ICON_Y + ICON_H / 2) * s, s=s))
    x0 = ix + ICON_W * s + 52
    cap = 86
    b.append(wordmark(x0, 326, cap, WHITE, ORANGE, track_em=0.16))
    tw = brand.width(WORD, cap, 0.16) + 0.40 * cap
    track = bold.track_to_fit(TAG_FULL, 17, tw)
    b.append(bold.text(TAG_FULL, 17, x0 + 1, 358, LIGHT, track))
    # block pallets in the yard
    for px, py in ((150, 560), (330, 585)):
        for r in range(3):
            for c in range(4):
                b.append(f'<rect x="{px + c * 34}" y="{py - r * 22}" width="30" '
                         f'height="18" fill="#9CA3AF"/>')
        b.append(f'<rect x="{px - 6}" y="{py + 20}" width="148" height="10" fill="#7C5A3A"/>')
    b.append(bold.text("FACTORY SIGNBOARD CONCEPT", 20, W / 2, 760, "#9CA3AF", 0.12, "middle"))
    return svg(W, H, "".join(b))


def mockup_business_card():
    W, H = 1400, 800
    b = [f'<rect width="{W}" height="{H}" fill="#E9ECF0"/>']
    CW, CH = 560, 320

    def card(tx, ty, rot, inner):
        return (
            f'<g transform="translate({tx} {ty}) rotate({rot})">'
            f'<rect x="10" y="14" width="{CW}" height="{CH}" rx="16" fill="#000" opacity="0.12"/>'
            + inner + "</g>"
        )

    # front
    front = [f'<rect width="{CW}" height="{CH}" rx="16" fill="{WHITE}"/>']
    front.append(f'<defs><clipPath id="cardf"><rect width="{CW}" height="{CH}" rx="16"/></clipPath></defs>')
    front.append(f'<g clip-path="url(#cardf)">'
                 f'<rect y="{CH - 16}" width="{CW}" height="16" fill="{ORANGE}"/>'
                 f'<rect y="{CH - 16}" width="150" height="16" fill="{BLUE}"/></g>')
    front.append(icon(GREY, ORANGE, BLUE, tx=36 - ICON_X * 0.42,
                      ty=32 - ICON_Y * 0.42, s=0.42))
    front.append(wordmark(124, 76, 34, BLUE, ORANGE, track_em=0.16))
    front.append(bold.text("CONSTRUCTION MATERIALS", 12.5, 126, 96, GREY, 0.12))
    front.append(bold.text("PAVAN KUMAR", 25, 36, 182, BLUE, 0.04))
    front.append(reg.text("Managing Director", 16, 36, 206, GREY))
    rows = [
        ("+91 98765 43210", 244),
        ("info@niya.in   •   www.niya.in", 268),
        ("Plot 42, Industrial Area Phase II", 292),
    ]
    for txt, y in rows:
        front.append(f'<rect x="36" y="{y - 9}" width="9" height="9" fill="{ORANGE}"/>')
        front.append(reg.text(txt, 14.5, 56, y, "#374151"))

    # back
    back = [f'<rect width="{CW}" height="{CH}" rx="16" fill="{BLUE}"/>']
    s = 0.56
    back.append(icon(WHITE, ORANGE, WHITE, tx=CW / 2 - (ICON_X + ICON_W / 2) * s,
                     ty=46 - ICON_Y * s, s=s))
    back.append(wordmark(CW / 2, 226, 36, WHITE, ORANGE, anchor="middle",
                         track_em=0.16))
    back.append(f'<rect x="{CW / 2 - 50}" y="244" width="100" height="3" fill="{ORANGE}"/>')
    back.append(bold.text("READY MIX CONCRETE • BLOCKS • PAVERS", 13, CW / 2, 274,
                          LIGHT, 0.1, "middle"))

    b.append(card(140, 150, -3, "".join(front)))
    b.append(card(700, 320, 3, "".join(back)))
    b.append(bold.text("BUSINESS CARD CONCEPT — FRONT & BACK", 20, W / 2, 760,
                       "#9CA3AF", 0.12, "middle"))
    return svg(W, H, "".join(b))


# -------------------------------------------------------------- build ----
def main():
    files = {
        "logos/svg/niya-logo-primary.svg":
            logo_primary(GREY, ORANGE, BLUE, GREY),
        "logos/svg/niya-logo-horizontal.svg":
            logo_horizontal(GREY, ORANGE, BLUE, GREY),
        "logos/svg/niya-logo-monogram.svg":
            logo_monogram(GREY, ORANGE, BLUE),
        "logos/svg/niya-logo-emblem.svg": logo_emblem(),
        "logos/svg/niya-app-icon.svg": logo_app_icon(),
        "logos/svg/niya-logo-primary-bw.svg":
            logo_primary(BLACK, BLACK, BLACK, BLACK, bg=WHITE),
        "logos/svg/niya-logo-horizontal-bw.svg":
            logo_horizontal(BLACK, BLACK, BLACK, BLACK, bg=WHITE)
            .replace("#D1D5DB", BLACK),
        "logos/svg/niya-logo-monogram-bw.svg":
            logo_monogram(BLACK, BLACK, BLACK, bg=WHITE),
        "logos/svg/niya-logo-primary-reversed.svg":
            logo_primary(WHITE, ORANGE, WHITE, LIGHT, bg=BLUE),
        "mockups/svg/niya-truck-branding.svg": mockup_truck(),
        "mockups/svg/niya-factory-signboard.svg": mockup_signboard(),
        "mockups/svg/niya-business-card.svg": mockup_business_card(),
    }
    widths = {"niya-app-icon": 512, "niya-logo-monogram": 720,
              "niya-logo-monogram-bw": 720, "niya-logo-emblem": 1000}
    for rel, content in files.items():
        write(rel, content)
        name = os.path.splitext(os.path.basename(rel))[0]
        png_rel = rel.replace("/svg/", "/png/").replace(".svg", ".png")
        os.makedirs(os.path.dirname(os.path.join(ROOT, png_rel)), exist_ok=True)
        render(rel, png_rel, widths.get(name, 1600))
        print("built", rel)


if __name__ == "__main__":
    main()
