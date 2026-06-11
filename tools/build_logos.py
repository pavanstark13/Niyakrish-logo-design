#!/usr/bin/env python3
"""Generate the full Niyakrish brand identity: logos, variants and mockups.

Lettering is converted to vector outlines (Liberation Sans Bold) with
fontTools, so every SVG is fully self-contained. PNG previews are rendered
with cairosvg.
"""

import math
import os

import cairosvg
from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
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
    """Renders text as SVG path outlines using a TTF font."""

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

    def _glyph_d(self, ch):
        pen = SVGPathPen(self.glyphs)
        self.glyphs[self.cmap[ord(ch)]].draw(pen)
        return pen.getCommands()

    def text(self, text, size, x, y, fill, track_em=0.0, anchor="start"):
        """Text laid out on baseline y. anchor: start|middle|end."""
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
        """Text along a circle. Top arc reads clockwise, bottom arc upright."""
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


bold = TextEngine(BOLD)
reg = TextEngine(REGULAR)


# ---------------------------------------------------------------- icon ----
# Design space of the icon: x 28..172, y 30..192 (w=144, h=162) in a 200 grid.
ICON_X, ICON_Y, ICON_W, ICON_H = 28, 30, 144, 162


def icon(grey=GREY, orange=ORANGE, blue=BLUE, tx=0.0, ty=0.0, s=1.0):
    """The Niyakrish mark: an N built from concrete blocks, a structural
    diagonal beam, a stepped tower top and a foundation slab."""
    blocks = []
    for y in (150, 120, 90, 60):                     # left column - 4 courses
        blocks.append((40, y, 36, 26))
    for y in (150, 120, 90, 60):                     # right column - 4 courses
        blocks.append((124, y, 36, 26))
    blocks.append((124, 30, 24, 26))                 # tower setback course
    g = [f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">']
    for x, y, w, h in blocks:
        g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{grey}"/>')
    g.append(f'<polygon points="40,60 76,60 160,176 124,176" fill="{orange}"/>')
    g.append(f'<rect x="28" y="180" width="144" height="12" fill="{blue}"/>')
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
        write_to=os.path.join(ROOT, png_rel.replace("svg", "png", 1)
                              if False else png_rel),
        output_width=width,
    )


# ------------------------------------------------------- logo lockups ----
WORD = "NIYAKRISH"
TAGLINE = "CONCRETE  •  BLOCKS  •  INFRASTRUCTURE"


def wordmark(x, y, size, fill, accent, anchor="start", track_em=0.06):
    """NIYAKRISH wordmark with the orange block full-stop."""
    w = bold.width(WORD, size, track_em)
    if anchor == "middle":
        x -= (w + 0.30 * size) / 2
    elif anchor == "end":
        x -= w + 0.30 * size
    sq = 0.16 * size
    parts = [bold.text(WORD, size, x, y, fill, track_em)]
    parts.append(
        f'<rect x="{x + w + 0.14 * size:.2f}" y="{y - sq:.2f}" '
        f'width="{sq:.2f}" height="{sq:.2f}" fill="{accent}"/>'
    )
    return "".join(parts)


def logo_primary(grey, orange, blue, tag_fill, bg=None):
    W, H = 760, 560
    body = []
    s = 1.62
    body.append(icon(grey, orange, blue,
                     tx=W / 2 - (ICON_X + ICON_W / 2) * s, ty=40 - ICON_Y * s, s=s))
    size = bold.fit_size(WORD, 540, 0.06)
    body.append(wordmark(W / 2, 430, size, blue, orange, anchor="middle"))
    tsize = 23.5
    body.append(bold.text(TAGLINE, tsize, W / 2, 488, tag_fill, 0.14, "middle"))
    return svg(W, H, "".join(body), bg)


def logo_horizontal(grey, orange, blue, tag_fill, bg=None):
    W, H = 1280, 330
    body = []
    s = 1.52
    body.append(icon(grey, orange, blue, tx=64 - ICON_X * s,
                     ty=H / 2 - (ICON_Y + ICON_H / 2) * s, s=s))
    x0 = 64 + ICON_W * 1.52 + 64
    body.append(f'<rect x="{x0 - 32}" y="55" width="3" height="220" fill="#D1D5DB"/>')
    size = bold.fit_size(WORD, 820, 0.05)
    body.append(wordmark(x0, 192, size, blue, orange, track_em=0.05))
    body.append(bold.text(TAGLINE, 27, x0 + 4, 248, tag_fill, 0.135))
    return svg(W, H, "".join(body), bg)


def logo_monogram(grey, orange, blue, bg=None):
    W = 240
    body = icon(grey, orange, blue, tx=(W - ICON_W) / 2 - ICON_X,
                ty=(W - ICON_H) / 2 - ICON_Y, s=1.0)
    return svg(W, W, body, bg)


def logo_app_icon():
    W = 512
    body = [f'<rect width="{W}" height="{W}" rx="100" fill="{BLUE}"/>']
    s = 1.72
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
                     tx=c - (ICON_X + ICON_W / 2) * 1.06,
                     ty=c - (ICON_Y + ICON_H / 2) * 1.06, s=1.06))
    body.append(bold.arc_text(WORD, 40, c, c, 166, WHITE, 0.14))
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
    b.append(icon(WHITE, ORANGE, WHITE, tx=300, ty=455, s=0.42))

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
    size = bold.fit_size(WORD, 270, 0.05)
    b.append(wordmark(cx + 5, cy + 8, size, BLUE, ORANGE, anchor="middle", track_em=0.05))
    b.append(bold.text("READY MIX CONCRETE", 21, cx + 5, cy + 48, ORANGE, 0.12, "middle"))
    b.append("</g>")

    # wheels & guards
    b.append('<path d="M165,640 A70,70 0 0 1 305,640 L290,640 A55,55 0 0 0 180,640 Z" fill="#0B1120"/>')
    b.append(wheel(235))
    for cxw in (900, 1010, 1120):
        b.append(wheel(cxw))
    b.append('<rect x="830" y="566" width="360" height="14" fill="#111827"/>')

    b.append(bold.text("NIYAKRISH READY MIX CONCRETE  •  TRUCK BRANDING CONCEPT",
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
    s = 0.78
    ix = 330
    b.append(icon(WHITE, ORANGE, WHITE, tx=ix - ICON_X * s,
                  ty=310 - (ICON_Y + ICON_H / 2) * s, s=s))
    size = bold.fit_size(WORD, 520, 0.06)
    b.append(wordmark(ix + ICON_W * s + 50, 330, size, WHITE, ORANGE))
    b.append(bold.text(TAGLINE, 19, ix + ICON_W * s + 54, 362, LIGHT, 0.13))
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
    front.append(icon(GREY, ORANGE, BLUE, tx=36 - ICON_X * 0.5, ty=34 - ICON_Y * 0.5, s=0.5))
    front.append(wordmark(128, 76, 34, BLUE, ORANGE, track_em=0.05))
    front.append(bold.text("CONCRETE • BLOCKS • INFRASTRUCTURE", 11.5, 130, 98, GREY, 0.1))
    front.append(bold.text("PAVAN KUMAR", 25, 36, 182, BLUE, 0.04))
    front.append(reg.text("Managing Director", 16, 36, 206, GREY))
    rows = [
        ("+91 98765 43210", 244),
        ("info@niyakrish.com   •   www.niyakrish.com", 268),
        ("Plot 42, Industrial Area Phase II", 292),
    ]
    for txt, y in rows:
        front.append(f'<rect x="36" y="{y - 9}" width="9" height="9" fill="{ORANGE}"/>')
        front.append(reg.text(txt, 14.5, 56, y, "#374151"))

    # back
    back = [f'<rect width="{CW}" height="{CH}" rx="16" fill="{BLUE}"/>']
    s = 0.62
    back.append(icon(WHITE, ORANGE, WHITE, tx=CW / 2 - (ICON_X + ICON_W / 2) * s,
                     ty=44 - ICON_Y * s, s=s))
    back.append(wordmark(CW / 2, 218, 36, WHITE, ORANGE, anchor="middle", track_em=0.05))
    back.append(f'<rect x="{CW / 2 - 50}" y="238" width="100" height="3" fill="{ORANGE}"/>')
    back.append(bold.text("READY MIX CONCRETE • BLOCKS • PAVERS", 13, CW / 2, 268,
                          LIGHT, 0.1, "middle"))

    b.append(card(140, 150, -3, "".join(front)))
    b.append(card(700, 320, 3, "".join(back)))
    b.append(bold.text("BUSINESS CARD CONCEPT — FRONT & BACK", 20, W / 2, 760,
                       "#9CA3AF", 0.12, "middle"))
    return svg(W, H, "".join(b))


# -------------------------------------------------------------- build ----
def main():
    files = {
        "logos/svg/niyakrish-logo-primary.svg":
            logo_primary(GREY, ORANGE, BLUE, GREY),
        "logos/svg/niyakrish-logo-horizontal.svg":
            logo_horizontal(GREY, ORANGE, BLUE, GREY),
        "logos/svg/niyakrish-logo-monogram.svg":
            logo_monogram(GREY, ORANGE, BLUE),
        "logos/svg/niyakrish-logo-emblem.svg": logo_emblem(),
        "logos/svg/niyakrish-app-icon.svg": logo_app_icon(),
        "logos/svg/niyakrish-logo-primary-bw.svg":
            logo_primary(BLACK, BLACK, BLACK, BLACK, bg=WHITE)
            .replace(BLUE, BLACK),
        "logos/svg/niyakrish-logo-horizontal-bw.svg":
            logo_horizontal(BLACK, BLACK, BLACK, BLACK, bg=WHITE)
            .replace(BLUE, BLACK).replace("#D1D5DB", BLACK),
        "logos/svg/niyakrish-logo-monogram-bw.svg":
            logo_monogram(BLACK, BLACK, BLACK, bg=WHITE).replace(BLUE, BLACK),
        "logos/svg/niyakrish-logo-primary-reversed.svg":
            logo_primary(WHITE, ORANGE, WHITE, LIGHT, bg=BLUE),
        "mockups/svg/niyakrish-truck-branding.svg": mockup_truck(),
        "mockups/svg/niyakrish-factory-signboard.svg": mockup_signboard(),
        "mockups/svg/niyakrish-business-card.svg": mockup_business_card(),
    }
    widths = {"niyakrish-app-icon": 512, "niyakrish-logo-monogram": 720,
              "niyakrish-logo-monogram-bw": 720, "niyakrish-logo-emblem": 1000}
    for rel, content in files.items():
        write(rel, content)
        name = os.path.splitext(os.path.basename(rel))[0]
        png_rel = rel.replace("/svg/", "/png/").replace(".svg", ".png")
        os.makedirs(os.path.dirname(os.path.join(ROOT, png_rel)), exist_ok=True)
        render(rel, png_rel, widths.get(name, 1600))
        print("built", rel)


if __name__ == "__main__":
    main()
