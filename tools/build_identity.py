#!/usr/bin/env python3
"""NIYA identity v5 — "The Delta Standard" — designed from scratch.

CONCEPT
  Mark: an equilateral triangle (the strongest form in structural
  engineering) assembled from three mitred beams — one for each product
  line: concrete, blocks, aggregates — locked around an orange core:
  strength, delivered.
  Type: custom letterforms drawn on a single 1:2 diagonal grid. The A of
  NIYA is a wide triangular letter that repeats the mark's geometry and
  carries the same orange triangular core as its counter. Mark and name
  share one geometry.

PALETTE
  Engineering Blue #16418C  (vibrant, serious)
  Safety Orange    #FF7A1A
  Steel            #5B6B7C
  White / Ink #101418 for single-colour uses
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_logos as bl
from build_logos import bold, svg, write, render

NAVY = "#16418C"
ORANGE = "#FF7A1A"
STEEL = "#5B6B7C"
INK = "#101418"
WHITE = "#FFFFFF"
LIGHTB = "#BFD0EE"

WORD = "NIYA"
TAGLINE = "STRENGTH DELIVERED"

# ------------------------------------------------- letterforms (cap 100) --
# Stroke 26; every diagonal sits on the same 1:2 slope.
G5 = {
    "N": (74, "M0 100 L0 0 L26 0 L48 44 L48 0 L74 0 L74 100 L48 100 "
              "L26 56 L26 100 Z"),
    "I": (26, "M0 0 L26 0 L26 100 L0 100 Z"),
    "Y": (74, "M0 0 L26 0 L37 22 L48 0 L74 0 L50 48 L50 100 L24 100 "
              "L24 48 Z"),
    "A": (126, "M50 0 L76 0 L126 100 L100 100 L92 84 L34 84 L26 100 "
               "L0 100 Z M63 26 L81 62 L45 62 Z"),
}
K5 = {("Y", "A"): -22}
A_CORE = "63,30 78.4,59.2 47.6,59.2"      # orange counter, slightly inset


def _advances(text, cap, track_em):
    out = []
    for i, ch in enumerate(text):
        a = G5[ch][0]
        if i + 1 < len(text):
            a += K5.get((ch, text[i + 1]), 0)
        out.append(a * cap / 100 + (track_em * cap if i + 1 < len(text) else 0))
    return out


def word_width(cap, track_em=0.06):
    return sum(_advances(WORD, cap, track_em))


def wordmark(x, y, cap, fill, accent=ORANGE, anchor="start", track_em=0.06):
    """NIYA in the v5 letterforms; the A's counter carries the orange core."""
    w = word_width(cap, track_em)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    s = cap / 100
    out = [f'<g fill="{fill}" fill-rule="evenodd">']
    cx = x
    for ch, adv in zip(WORD, _advances(WORD, cap, track_em)):
        out.append(f'<path transform="translate({cx:.2f} {y - cap:.2f}) '
                   f'scale({s:.6f})" d="{G5[ch][1]}"/>')
        if ch == "A" and accent:
            out.append(f'<polygon points="{A_CORE}" fill="{accent}" '
                       f'transform="translate({cx:.2f} {y - cap:.2f}) '
                       f'scale({s:.6f})"/>')
        cx += adv
    out.append("</g>")
    return "".join(out)


# ------------------------------------------------------------- the mark --
# Box 168 x 147. Equilateral triangle of three mitred beams + orange core.
MW, MH = 168, 147
_V = [(84.0, 2.0), (3.0, 145.0), (165.0, 145.0)]
_C = (84.0, (2.0 + 145.0 + 145.0) / 3)


def _shrink(v, k):
    return (_C[0] + (v[0] - _C[0]) * k, _C[1] + (v[1] - _C[1]) * k)


def mark(beam=NAVY, joint=WHITE, core=ORANGE, tx=0.0, ty=0.0, s=1.0):
    r = 145.0 - _C[1]                      # inradius of the outer triangle
    k_in = (r - 28) / r                    # ring thickness 28
    k_core = (r - 28 - 6.5) / r            # 6.5 joint gap around the core
    inner = [_shrink(v, k_in) for v in _V]
    corev = [_shrink(v, k_core) for v in _V]
    P = lambda pts: " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    g = [f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">']
    g.append(f'<polygon points="{P(_V)}" fill="{beam}"/>')
    g.append(f'<polygon points="{P(inner)}" fill="{joint}"/>')
    for v, vi in zip(_V, inner):           # mitre joints between the beams
        g.append(f'<line x1="{v[0]:.1f}" y1="{v[1]:.1f}" '
                 f'x2="{vi[0]:.1f}" y2="{vi[1]:.1f}" '
                 f'stroke="{joint}" stroke-width="3.6"/>')
    g.append(f'<polygon points="{P(corev)}" fill="{core}"/>')
    g.append("</g>")
    return "".join(g)


def tag_under(x, y, cap, fill, tsize, text=TAGLINE):
    track = bold.track_to_fit(text, tsize, word_width(cap))
    return bold.text(text, tsize, x, y, fill, track)


# ------------------------------------------------------------- lockups --
def logo_primary(beam, joint, core, word_fill, accent, tag, bg=None):
    W, H = 560, 446
    s = 1.12
    body = [mark(beam, joint, core, tx=W / 2 - MW / 2 * s, ty=34, s=s)]
    cap = 100
    body.append(wordmark(W / 2, 350, cap, word_fill, accent, "middle"))
    body.append(tag_under(W / 2 - word_width(cap) / 2 + 1, 400, cap, tag, 21))
    return svg(W, H, "".join(body), bg)


def logo_horizontal(beam, joint, core, word_fill, accent, tag, div, bg=None):
    W, H = 700, 300
    s = 1.05
    body = [mark(beam, joint, core, tx=52, ty=(H - MH * s) / 2, s=s)]
    x0 = 52 + MW * s + 56
    body.append(f'<rect x="{x0 - 29}" y="64" width="3" height="172" fill="{div}"/>')
    cap = 112
    body.append(wordmark(x0, 178, cap, word_fill, accent))
    body.append(tag_under(x0 + 1, 230, cap, tag, 22))
    return svg(W, H, "".join(body), bg)


def logo_monogram(beam, joint, core, bg=None):
    W, s = 240, 1.25
    return svg(W, W, mark(beam, joint, core, tx=(W - MW * s) / 2,
                          ty=(W - MH * s) / 2, s=s), bg)


def logo_app_icon():
    W, s = 512, 2.15
    body = [f'<rect width="{W}" height="{W}" rx="100" fill="{NAVY}"/>']
    body.append(mark(WHITE, NAVY, ORANGE, tx=W / 2 - MW / 2 * s,
                     ty=W / 2 - MH / 2 * s, s=s))
    return svg(W, W, "".join(body))


def logo_emblem():
    W = 420
    c = W / 2
    body = [
        f'<circle cx="{c}" cy="{c}" r="200" fill="{NAVY}"/>',
        f'<circle cx="{c}" cy="{c}" r="148" fill="{WHITE}"/>',
        f'<circle cx="{c}" cy="{c}" r="155" fill="none" stroke="{ORANGE}" stroke-width="4"/>',
    ]
    s = 1.25
    body.append(mark(NAVY, WHITE, ORANGE, tx=c - MW / 2 * s,
                     ty=c - MH / 2 * s - 4, s=s))
    # NIYA on the top arc in the brand letterforms
    cap, r = 34, 164
    advs = _advances(WORD, cap, 0.55)
    total = sum(advs) - 0.55 * cap
    theta = total / r
    import math
    acc = 0.0
    arc = ['<g fill="#FFFFFF" fill-rule="evenodd">']
    for ch, a in zip(WORD, advs):
        gw = G5[ch][0] * cap / 100
        ang = math.degrees(-theta / 2 + (acc + gw / 2) / r)
        acc += a
        arc.append(f'<path transform="rotate({ang:.2f} {c} {c}) '
                   f'translate({c - gw / 2:.2f} {c - r - cap:.2f}) '
                   f'scale({cap / 100:.5f})" d="{G5[ch][1]}"/>')
    arc.append("</g>")
    body.append("".join(arc))
    body.append(bold.arc_text(TAGLINE, 22, c, c, 186, LIGHTB, 0.14, bottom=True))
    for sgn in (-1, 1):
        x = c + sgn * 177
        body.append(f'<polygon points="{x},{c - 9} {x + 8},{c + 7} {x - 8},{c + 7}" '
                    f'fill="{ORANGE}"/>')
    return svg(W, W, "".join(body))


# ------------------------------------------------------------- mockups --
def patch_and_build_mockups():
    """Re-skin the scene mockups with the v5 mark, type and palette."""
    bl.GLYPHS.clear(); bl.GLYPHS.update(G5)
    bl.KERN.clear(); bl.KERN.update(K5)
    bl.XW = 1.0
    bl.icon = lambda a=NAVY, b=WHITE, c=ORANGE, tx=0.0, ty=0.0, s=1.0: \
        mark(a, b, c, tx, ty, s)
    bl.ICON_W, bl.ICON_H = MW, MH
    bl.wordmark = lambda x, y, cap, fill, accent, anchor="start", track_em=0.06: \
        wordmark(x, y, cap, fill, accent, anchor)
    bl.wm_full_width = lambda cap, track_em=0.06: word_width(cap)
    bl.BLUE, bl.ORANGE, bl.LIGHT = NAVY, ORANGE, LIGHTB
    bl.TAGLINE = TAGLINE
    return {
        "mockups/svg/niya-truck-branding.svg": bl.mockup_truck(),
        "mockups/svg/niya-factory-signboard.svg": bl.mockup_signboard(),
        "mockups/svg/niya-business-card.svg": bl.mockup_business_card(),
    }


# --------------------------------------------------------------- build --
def main():
    files = {
        "logos/svg/niya-logo-primary.svg":
            logo_primary(NAVY, WHITE, ORANGE, NAVY, ORANGE, STEEL),
        "logos/svg/niya-logo-horizontal.svg":
            logo_horizontal(NAVY, WHITE, ORANGE, NAVY, ORANGE, STEEL, "#C9D4E4"),
        "logos/svg/niya-logo-monogram.svg": logo_monogram(NAVY, WHITE, ORANGE),
        "logos/svg/niya-logo-emblem.svg": logo_emblem(),
        "logos/svg/niya-app-icon.svg": logo_app_icon(),
        "logos/svg/niya-logo-primary-bw.svg":
            logo_primary(INK, WHITE, INK, INK, None, INK, bg=WHITE),
        "logos/svg/niya-logo-horizontal-bw.svg":
            logo_horizontal(INK, WHITE, INK, INK, None, INK, INK, bg=WHITE),
        "logos/svg/niya-logo-monogram-bw.svg":
            logo_monogram(INK, WHITE, INK, bg=WHITE),
        "logos/svg/niya-logo-primary-reversed.svg":
            logo_primary(WHITE, NAVY, ORANGE, WHITE, ORANGE, LIGHTB, bg=NAVY),
    }
    files.update(patch_and_build_mockups())
    widths = {"niya-app-icon": 512, "niya-logo-monogram": 720,
              "niya-logo-monogram-bw": 720, "niya-logo-emblem": 1000}
    for rel, content in files.items():
        write(rel, content)
        name = os.path.splitext(os.path.basename(rel))[0]
        png_rel = rel.replace("/svg/", "/png/").replace(".svg", ".png")
        os.makedirs(os.path.dirname(os.path.join(bl.ROOT, png_rel)), exist_ok=True)
        render(rel, png_rel, widths.get(name, 1600))
        print("built", rel)


if __name__ == "__main__":
    main()
