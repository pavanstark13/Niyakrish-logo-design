# NIYA — Brand Identity

Corporate identity for **NIYA**, a construction materials company:
Ready Mix Concrete (RMC), concrete blocks, aggregates, construction
materials and infrastructure supply.

**Tagline: STRENGTH DELIVERED**

![Primary logo](logos/png/niya-logo-primary.png)

## Design concept

The mark is a **hexagonal cell carrying a negative-space N**:

| Element | Meaning |
| --- | --- |
| Deep-blue hexagon | Aggregate stone, bolt head, engineered cell — industry and precision |
| Negative-space N | NIYA, carved out of solid material |
| Orange structural diagonal | Engineering energy, load transfer |

The direction was chosen from **five distinct concept explorations**
(`logos/concepts/`, preview at `logos/preview.html`) generated with the
open-source [logo-designer Claude skill](https://github.com/neonwatty/logo-designer-skill)
workflow: hexagon-N, aggregate peak, strata chevrons, pure typographic,
and drum-circle. The hexagon won on corporate weight, ownability, and
small-size legibility (still reads at 16 px).

## Custom letterforms

The **NIYA wordmark is a custom typeface**, not a font: squared
industrial capitals (N, I, Y, A — plus K, R, S, H in the kit) drawn as
vector polygons on a 100-unit cap grid with a 24-unit stroke, extended
stance, wide tracking and optical kerning. The orange block "full stop"
after NIYA is the brand's signature — a concrete block closing the name.
Utility text (taglines, contact lines) uses a neutral industrial
sans-serif converted to outlines, so every SVG is fully self-contained.

## Color palette

| Role | Name | Hex |
| --- | --- | --- |
| Primary | Concrete Grey | `#4A4A4A` |
| Secondary | Construction Orange | `#F97316` |
| Accent | Deep Blue | `#0F172A` |
| Background | White | `#FFFFFF` |

## Files

All masters are scalable SVG (`logos/svg`, `mockups/svg`); PNG renders are
provided for quick use (`logos/png`, `mockups/png`). The previous concept
iteration is kept in `archive/v1-concept` for comparison.

| File | Use |
| --- | --- |
| `niya-logo-primary` | Main corporate logo (icon above wordmark) |
| `niya-logo-horizontal` | Letterheads, website header, invoices, truck doors |
| `niya-logo-monogram` | Stand-alone N mark — helmets, favicons, watermarks |
| `niya-app-icon` | Mobile app / social media avatar (rounded square) |
| `niya-logo-emblem` | Premium circular emblem — seals, uniforms, badges |
| `niya-logo-primary-bw` / `-horizontal-bw` / `-monogram-bw` | Single-color print, stamps, engraving |
| `niya-logo-primary-reversed` | Dark backgrounds (deep blue) |
| `mockups/…truck-branding` | RMC mixer truck livery concept |
| `mockups/…factory-signboard` | Factory fascia signboard concept |
| `mockups/…business-card` | Business card concept, front & back (contact details are placeholders) |

## Usage rules

- **Clear space:** keep a margin equal to the foundation slab's height ×3
  around the logo on all sides.
- **Minimum sizes:** monogram 24 px, horizontal lockup 110 px wide.
- On photographs or colored surfaces use the reversed or B/W version —
  never recolor the mark outside the palette above.
- Don't rotate, outline, add shadows/gradients, or change the proportions
  between icon and wordmark.

## Rebuilding

Everything is generated from one script:

```bash
pip install fonttools cairosvg
python3 tools/build_logos.py
```
