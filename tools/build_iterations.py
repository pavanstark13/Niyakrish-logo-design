#!/usr/bin/env python3
"""Phase 3 of the logo-designer skill: batch variations on the chosen
hexagon-N direction — vibrant, clean palettes and badge-shape twists.
Each iteration is a full 1024x512 lockup for fair comparison.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_logos as bl
from build_logos import WHITE, bold, brand, svg

TAGLINE = "STRENGTH DELIVERED"

# N geometry inside the 168x146 icon box (same as the hexagon mark)
def n_block(n_fill, diag_fill):
    return (f'<rect x="52" y="34" width="18" height="78" fill="{n_fill}"/>'
            f'<rect x="98" y="34" width="18" height="78" fill="{n_fill}"/>'
            f'<polygon points="72,34 96,80 96,112 72,66" fill="{diag_fill}"/>')


HEX_PTS = "0,73 42,0 126,0 168,73 126,146 42,146"


def shape_hex(fill):
    return f'<polygon points="{HEX_PTS}" fill="{fill}"/>'


def shape_hex_facet(fill, facet):
    return (f'<polygon points="{HEX_PTS}" fill="{fill}"/>'
            f'<polygon points="0,73 168,73 126,146 42,146" fill="{facet}"/>')


def shape_hex_outline(stroke):
    return (f'<polygon points="6,73 45,5 123,5 162,73 123,141 45,141" '
            f'fill="none" stroke="{stroke}" stroke-width="10" '
            f'stroke-linejoin="miter"/>')


def shape_squircle(fill):
    return f'<rect x="14" y="3" width="140" height="140" rx="34" fill="{fill}"/>'


def shape_circle(fill):
    return f'<circle cx="84" cy="73" r="71" fill="{fill}"/>'


def lockup(shape_svg, n_fill, diag_fill, word, accent, tag):
    s = 1.55
    body = [f'<g id="icon" transform="translate({230 - 84 * s:.2f} '
            f'{256 - 73 * s:.2f}) scale({s})">{shape_svg}'
            f'{n_block(n_fill, diag_fill)}</g>']
    cap = 120
    body.append(f'<g id="wordmark">{bl.wordmark(452, 268, cap, word, accent, track_em=0.16)}</g>')
    tw = bl.wm_full_width(cap)
    track = bold.track_to_fit(TAGLINE, 26, tw)
    body.append(f'<g id="tagline">{bold.text(TAGLINE, 26, 454, 324, tag, track)}</g>')
    return svg(1024, 512, "".join(body))


def typographic(word, keystone, dot, tag):
    cap = 168
    s = cap / 100
    xw = bl.XW
    track = 0.16 * cap
    adv = [72 * xw * s + track, 24 * xw * s + track, (72 - 12) * xw * s + track]
    total = adv[0] + adv[1] + adv[2] + 78 * xw * s
    x = (1024 - (total + 0.40 * cap)) / 2
    base = 300
    g = ['<g id="wordmark" fill-rule="evenodd">']
    for ch, a in zip("NIY", adv):
        g.append(f'<path transform="translate({x:.2f} {base - cap:.2f}) '
                 f'scale({s * xw:.6f} {s:.6f})" d="{bl.GLYPHS[ch][1]}" fill="{word}"/>')
        x += a
    a_open = "M26 0 L52 0 L78 100 L55 100 L39 36 L23 100 L0 100 Z"
    g.append(f'<path transform="translate({x:.2f} {base - cap:.2f}) '
             f'scale({s * xw:.6f} {s:.6f})" d="{a_open}" fill="{word}"/>')
    g.append(f'<polygon points="31,56 47,56 39,82" fill="{keystone}" '
             f'transform="translate({x:.2f} {base - cap:.2f}) '
             f'scale({s * xw:.6f} {s:.6f})"/>')
    x += 78 * xw * s
    sq = 0.20 * cap
    g.append(f'<rect x="{x + 0.16 * cap:.2f}" y="{base - sq:.2f}" '
             f'width="{sq:.2f}" height="{sq:.2f}" fill="{dot}"/>')
    g.append("</g>")
    trk = bold.track_to_fit(TAGLINE, 27, total * 0.72)
    g.append(bold.text(TAGLINE, 27, 512, base + 68, tag, trk, "middle"))
    return svg(1024, 512, "".join(g))


ITERATIONS = {
    # name: builder
    "iteration-1-electric-blue": lambda: lockup(
        shape_hex("#2563EB"), WHITE, "#F59E0B", "#1E293B", "#F59E0B", "#64748B"),
    "iteration-2-emerald": lambda: lockup(
        shape_hex("#059669"), WHITE, "#F59E0B", "#064E3B", "#F59E0B", "#6B7280"),
    "iteration-3-coral-charcoal": lambda: lockup(
        shape_hex("#FF5A36"), WHITE, "#1F2937", "#1F2937", "#FF5A36", "#6B7280"),
    "iteration-4-blue-facet": lambda: lockup(
        shape_hex_facet("#1D4ED8", "#3B82F6"), WHITE, "#F59E0B",
        "#1E3A8A", "#F59E0B", "#64748B"),
    "iteration-5-outline": lambda: lockup(
        shape_hex_outline("#0F172A"), "#0F172A", "#F97316",
        "#0F172A", "#F97316", "#6B7280"),
    "iteration-6-indigo-cyan": lambda: lockup(
        shape_squircle("#4F46E5"), WHITE, "#22D3EE", "#312E81", "#22D3EE", "#64748B"),
    "iteration-7-sky-circle": lambda: lockup(
        shape_circle("#0EA5E9"), WHITE, "#0C4A6E", "#0C4A6E", "#0EA5E9", "#64748B"),
    "iteration-8-typographic-coral": lambda: typographic(
        "#1D4ED8", "#FF5A36", "#FF5A36", "#64748B"),
    "iteration-9-safety-yellow": lambda: lockup(
        shape_hex("#FACC15"), "#111827", "#111827", "#111827", "#FACC15", "#6B7280"),
}

CARD = """<div class="card"><div class="card-img">
<img src="{path}" alt="{label}"></div>
<div class="card-label">{label}</div></div>"""

FAV = """<div style="display:flex;flex-direction:column;align-items:center;gap:.5rem;">
<div style="font-size:.8rem;font-weight:500;">{label}</div>
<div style="display:flex;gap:1rem;align-items:end;">
<div><img src="{path}" width="64" height="64"><div style="font-size:.75rem;opacity:.6;">64px</div></div>
<div><img src="{path}" width="32" height="32"><div style="font-size:.75rem;opacity:.6;">32px</div></div>
<div><img src="{path}" width="16" height="16"><div style="font-size:.75rem;opacity:.6;">16px</div></div>
</div></div>"""


def main():
    cards, favs = [], []
    for name, fn in ITERATIONS.items():
        rel = f"logos/iterations/{name}.svg"
        bl.write(rel, fn())
        bl.render(rel, rel.replace(".svg", ".png"), 1200)
        cards.append(CARD.format(path=f"iterations/{name}.svg", label=name))
        favs.append(FAV.format(path=f"iterations/{name}.svg", label=name))
        print("built", rel)
    # concepts stay in the preview below the new iterations
    for c in sorted(os.listdir(os.path.join(bl.ROOT, "logos/concepts"))):
        if c.endswith(".svg"):
            cards.append(CARD.format(path=f"concepts/{c}", label=c[:-4]))
    import build_concepts
    html = build_concepts.PREVIEW.format(cards="".join(cards))
    html = html.replace("</body>", "<h2 style='margin:2rem 0 1rem'>Favicon Size Check"
                        "</h2><div style='display:flex;gap:2rem;flex-wrap:wrap;"
                        "align-items:end;'>" + "".join(favs) + "</div></body>")
    bl.write("logos/preview.html", html)


if __name__ == "__main__":
    main()
