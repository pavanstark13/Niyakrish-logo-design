#!/usr/bin/env python3
"""Round 3 concept exploration — deliberately NOT letter-in-badge marks.

  A keystone    — the stone that locks an arch: strength, materials
  B arch bridge — infrastructure span
  C iso block   — 3D building block / materials unit
  D dynamic N   — forward-leaning two-tone N, motion of delivery
  E mixer swirl — two rotating segments, RMC drum energy
  F pour        — funnel pouring into a cast column

Each rendered as a 1024x512 combination lockup for fair comparison.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_logos as bl
from build_logos import bold, svg

TAGLINE = "STRENGTH DELIVERED"
NAVY = "#0F172A"
VBLUE = "#1D4ED8"      # vibrant blue
ORANGE = "#F97316"
SLATE = "#334155"
SKY = "#3B82F6"


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy - r * math.sin(a))


def stone(cx, cy, r_out, r_in, a0, a1, fill):
    """Straight-edged annular segment (arch voussoir)."""
    p = [pt(cx, cy, r_out, a0), pt(cx, cy, r_out, a1),
         pt(cx, cy, r_in, a1), pt(cx, cy, r_in, a0)]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in p)
    return f'<polygon points="{pts}" fill="{fill}"/>'


def arc_band(cx, cy, r_out, r_in, a0, a1, fill):
    """True annular segment with curved edges."""
    o0, o1 = pt(cx, cy, r_out, a0), pt(cx, cy, r_out, a1)
    i0, i1 = pt(cx, cy, r_in, a0), pt(cx, cy, r_in, a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    return (f'<path d="M{o0[0]:.1f},{o0[1]:.1f} '
            f'A{r_out},{r_out} 0 {large} 0 {o1[0]:.1f},{o1[1]:.1f} '
            f'L{i1[0]:.1f},{i1[1]:.1f} '
            f'A{r_in},{r_in} 0 {large} 1 {i0[0]:.1f},{i0[1]:.1f} Z" '
            f'fill="{fill}"/>')


def lockup(icon_svg, word=NAVY, accent=ORANGE, tag="#64748B"):
    s = 1.5
    body = [f'<g id="icon" transform="translate({230 - 84 * s:.2f} '
            f'{256 - 80 * s:.2f}) scale({s})">{icon_svg}</g>']
    cap = 120
    body.append(f'<g id="wordmark">{bl.wordmark(452, 268, cap, word, accent, track_em=0.16)}</g>')
    tw = bl.wm_full_width(cap)
    track = bold.track_to_fit(TAGLINE, 26, tw)
    body.append(f'<g id="tagline">{bold.text(TAGLINE, 26, 454, 324, tag, track)}</g>')
    return svg(1024, 512, "".join(body))


# ---------------------------------------------------------------- icons ---
def icon_keystone():
    """Arch of faceted stones; the orange keystone locks the span."""
    cx, cy = 84, 152
    g = []
    for a0, a1, fill in ((180, 148, VBLUE), (144, 112, VBLUE),
                         (108, 72, ORANGE), (68, 36, VBLUE), (32, 0, VBLUE)):
        g.append(stone(cx, cy, 128, 76, a0, a1, fill))
    g.append(f'<rect x="8" y="158" width="152" height="11" fill="{NAVY}"/>')
    return "".join(g)


def icon_arch():
    """Bridge: orange deck riding a navy arch on two abutments."""
    g = [f'<rect x="2" y="42" width="164" height="16" fill="{ORANGE}"/>']
    g.append(arc_band(84, 152, 92, 64, 0, 180, NAVY))
    g.append(f'<rect x="0" y="140" width="32" height="20" fill="{NAVY}"/>')
    g.append(f'<rect x="136" y="140" width="32" height="20" fill="{NAVY}"/>')
    return "".join(g)


def icon_block():
    """Isometric building block — one cast unit of material."""
    return (
        f'<polygon points="84,16 152,50 84,84 16,50" fill="{ORANGE}"/>'
        f'<polygon points="16,50 84,84 84,156 16,122" fill="{NAVY}"/>'
        f'<polygon points="152,50 84,84 84,156 152,122" fill="{SLATE}"/>'
    )


def icon_dynamic_n():
    """Forward-leaning two-tone N — the motion of delivery."""
    return (
        '<g transform="translate(14 0) skewX(-12) translate(8 0)">'
        f'<rect x="24" y="18" width="27" height="124" fill="{NAVY}"/>'
        f'<rect x="95" y="18" width="27" height="124" fill="{NAVY}"/>'
        f'<polygon points="55,18 92,88 92,142 55,72" fill="{ORANGE}"/>'
        "</g>"
    )


def icon_swirl():
    """Two segments chasing each other — the turn of the mixer drum."""
    g = [arc_band(84, 80, 72, 40, -65, 105, NAVY)]
    g.append(arc_band(84, 80, 72, 40, 115, 285, ORANGE))
    g.append(f'<circle cx="84" cy="80" r="14" fill="{ORANGE}"/>')
    return "".join(g)


def icon_pour():
    """Funnel pouring aggregates into a cast column."""
    return (
        f'<polygon points="20,16 148,16 100,72 68,72" fill="{ORANGE}"/>'
        f'<rect x="77" y="76" width="14" height="22" fill="{ORANGE}"/>'
        f'<rect x="56" y="104" width="56" height="42" fill="{NAVY}"/>'
        f'<rect x="44" y="150" width="80" height="10" fill="{NAVY}"/>'
    )


CONCEPTS = {
    "round3-A-keystone": icon_keystone,
    "round3-B-arch-bridge": icon_arch,
    "round3-C-iso-block": icon_block,
    "round3-D-dynamic-n": icon_dynamic_n,
    "round3-E-mixer-swirl": icon_swirl,
    "round3-F-pour": icon_pour,
}


def main():
    for name, fn in CONCEPTS.items():
        rel = f"logos/concepts/{name}.svg"
        bl.write(rel, lockup(fn()))
        bl.render(rel, rel.replace(".svg", ".png"), 1200)
        print("built", rel)


if __name__ == "__main__":
    main()
