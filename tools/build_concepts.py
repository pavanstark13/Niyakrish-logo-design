#!/usr/bin/env python3
"""Phase 2 of the logo-designer skill: five DISTINCT concept directions
for the NIYA mark, rendered as combination lockups (1024x512).

Concepts:
  1 hexagon-n      — deep-blue hexagon (aggregate stone / bolt head),
                     negative-space N, orange structural diagonal
  2 aggregate-peak — faceted stone/peak built from three angular planes
  3 strata-chevron — three stacked upward chevrons: graded material
                     layers building upward
  4 typographic    — the wordmark IS the logo; open-counter A with a
                     floating orange keystone
  5 drum-circle    — circle sliced by a rotating diagonal band (mixer
                     drum / motion)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_logos as bl
from build_logos import BLUE, GREY, LIGHT, ORANGE, WHITE, bold, brand, svg

ROOT = bl.ROOT
TAGLINE = "STRENGTH DELIVERED"


def lockup_text(x0, cap=120, baseline=268, fill=BLUE, accent=ORANGE,
                tag_fill=GREY):
    """Shared wordmark + tagline block for icon-led concepts."""
    parts = [bl.wordmark(x0, baseline, cap, fill, accent, track_em=0.16)]
    tw = brand.width(bl.WORD, cap, 0.16) + 0.40 * cap
    tsize = 26
    track = bold.track_to_fit(TAGLINE, tsize, tw)
    parts.append(bold.text(TAGLINE, tsize, x0 + 2, baseline + 56, tag_fill, track))
    return "".join(parts)


def c1_hexagon():
    cx, cy, R = 230, 256, 162
    h = R * 0.8660
    pts = (f"{cx - R},{cy} {cx - R / 2},{cy - h} {cx + R / 2},{cy - h} "
           f"{cx + R},{cy} {cx + R / 2},{cy + h} {cx - R / 2},{cy + h}")
    g = [f'<g id="icon"><polygon points="{pts}" fill="{BLUE}"/>']
    # negative-space N, cap 150, stems 34, gap 56
    n_x, n_y = cx - 62, cy - 75
    g.append(f'<rect x="{n_x}" y="{n_y}" width="34" height="150" fill="{WHITE}"/>')
    g.append(f'<rect x="{n_x + 90}" y="{n_y}" width="34" height="150" fill="{WHITE}"/>')
    g.append(f'<polygon points="{n_x + 37},{n_y} {n_x + 87},{n_y + 88} '
             f'{n_x + 87},{n_y + 150} {n_x + 37},{n_y + 62}" fill="{ORANGE}"/>')
    g.append("</g>")
    g.append(lockup_text(452))
    return svg(1024, 512, "".join(g))


def c2_peak():
    g = ['<g id="icon">']
    g.append(f'<polygon points="95,372 218,128 290,272 246,372" fill="{GREY}"/>')
    g.append(f'<polygon points="218,128 365,372 246,372 252,268" fill="{BLUE}"/>')
    g.append(f'<polygon points="180,372 252,240 324,372" fill="{ORANGE}"/>')
    g.append(f'<rect x="88" y="384" width="284" height="12" fill="{BLUE}"/>')
    g.append("</g>")
    g.append(lockup_text(452))
    return svg(1024, 512, "".join(g))


def c3_chevrons():
    cx = 230

    def chevron(yapex, fill, half_w=128, drop=86, t=40):
        return (f'<polygon points="{cx - half_w},{yapex + drop} {cx},{yapex} '
                f'{cx + half_w},{yapex + drop} {cx + half_w},{yapex + drop + t} '
                f'{cx},{yapex + t} {cx - half_w},{yapex + drop + t}" '
                f'fill="{fill}"/>')

    g = ['<g id="icon">']
    g.append(chevron(118, ORANGE))
    g.append(chevron(196, GREY))
    g.append(chevron(274, BLUE))
    g.append("</g>")
    g.append(lockup_text(452))
    return svg(1024, 512, "".join(g))


def c4_typographic():
    cap = 168
    s = cap / 100
    xw = bl.XW
    # widths in units: N 72, I 24, Y 72(+kern -12 before A), A 78
    track = 0.16 * cap
    adv = [72 * xw * s + track, 24 * xw * s + track, (72 - 12) * xw * s + track]
    total = adv[0] + adv[1] + adv[2] + 78 * xw * s
    x = (1024 - (total + 0.40 * cap)) / 2
    base = 300
    g = ['<g id="wordmark" fill-rule="evenodd">']
    for ch, a in zip("NIY", adv):
        d = bl.GLYPHS[ch][1]
        g.append(f'<path transform="translate({x:.2f} {base - cap:.2f}) '
                 f'scale({s * xw:.6f} {s:.6f})" d="{d}" fill="{BLUE}"/>')
        x += a
    # open-counter A (no crossbar) + floating orange keystone
    a_open = ("M26 0 L52 0 L78 100 L55 100 L39 36 L23 100 L0 100 Z")
    g.append(f'<path transform="translate({x:.2f} {base - cap:.2f}) '
             f'scale({s * xw:.6f} {s:.6f})" d="{a_open}" fill="{BLUE}"/>')
    g.append(f'<polygon points="31,56 47,56 39,82" fill="{ORANGE}" '
             f'transform="translate({x:.2f} {base - cap:.2f}) '
             f'scale({s * xw:.6f} {s:.6f})"/>')
    x += 78 * xw * s
    sq = 0.20 * cap
    g.append(f'<rect x="{x + 0.16 * cap:.2f}" y="{base - sq:.2f}" '
             f'width="{sq:.2f}" height="{sq:.2f}" fill="{ORANGE}"/>')
    g.append("</g>")
    tw = total + 0.40 * cap
    tsize = 27
    trk = bold.track_to_fit(TAGLINE, tsize, tw * 0.7)
    g.append(bold.text(TAGLINE, tsize, 512, base + 68, GREY, trk, "middle"))
    return svg(1024, 512, "".join(g))


def c5_drum():
    cx, cy, R = 230, 256, 152
    g = ['<g id="icon">']
    g.append('<defs><clipPath id="c5"><circle cx="%d" cy="%d" r="%d"/></clipPath></defs>'
             % (cx, cy, R))
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{BLUE}"/>')
    g.append(f'<g clip-path="url(#c5)" transform="rotate(-32 {cx} {cy})">')
    g.append(f'<rect x="{cx - 44}" y="{cy - R - 20}" width="88" '
             f'height="{2 * R + 40}" fill="{WHITE}"/>')
    g.append(f'<rect x="{cx - 28}" y="{cy - R - 20}" width="56" '
             f'height="{2 * R + 40}" fill="{ORANGE}"/>')
    g.append("</g></g>")
    g.append(lockup_text(452))
    return svg(1024, 512, "".join(g))


CARD = """<div class="card"><div class="card-img">
<img src="{path}" alt="{label}"></div>
<div class="card-label">{label}</div></div>"""

PREVIEW = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NIYA Logo Preview — Concepts</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
padding:2rem;transition:background-color .3s,color .3s}}
body.light{{background:#f5f5f5;color:#333}}body.dark{{background:#1a1a1a;color:#eee}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem}}
h1{{font-size:1.5rem;font-weight:600}}
.toggle{{padding:.5rem 1rem;border:1px solid currentColor;border-radius:6px;
background:transparent;color:inherit;cursor:pointer;font-size:.875rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.5rem}}
.card{{border:1px solid rgba(128,128,128,.3);border-radius:12px;overflow:hidden}}
.card-img{{display:flex;align-items:center;justify-content:center;padding:2rem;min-height:240px}}
body.light .card-img{{background:#fff}}body.dark .card-img{{background:#2a2a2a}}
.card-img img{{max-width:100%;max-height:200px}}
.card-label{{padding:.75rem 1rem;font-size:.875rem;font-weight:500;
border-top:1px solid rgba(128,128,128,.3)}}
body.light .card-label{{background:#fafafa}}body.dark .card-label{{background:#222}}
</style></head><body class="light">
<div class="header"><h1>NIYA Logo Preview — Concepts</h1>
<button class="toggle" onclick="document.body.classList.toggle('dark');
document.body.classList.toggle('light');
this.textContent=document.body.classList.contains('dark')?'☀️ Light':'🌙 Dark';">
🌙 Dark</button></div>
<div class="grid">{cards}</div></body></html>"""


def main():
    concepts = {
        "concept-1-hexagon-n": c1_hexagon(),
        "concept-2-aggregate-peak": c2_peak(),
        "concept-3-strata-chevron": c3_chevrons(),
        "concept-4-typographic": c4_typographic(),
        "concept-5-drum-circle": c5_drum(),
    }
    cards = []
    for name, content in concepts.items():
        rel = f"logos/concepts/{name}.svg"
        bl.write(rel, content)
        bl.render(rel, rel.replace(".svg", ".png"), 1200)
        cards.append(CARD.format(path=f"concepts/{name}.svg", label=name))
        print("built", rel)
    bl.write("logos/preview.html", PREVIEW.format(cards="".join(cards)))


if __name__ == "__main__":
    main()
