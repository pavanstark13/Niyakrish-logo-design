# NIYA — Brand Identity

Corporate identity for **NIYA**, a construction materials company:
Ready Mix Concrete (RMC), concrete blocks, construction materials and
infrastructure supply.

![Primary logo](logos/png/niya-logo-primary.png)

## Design concept

The mark is a **precision-engineered letter N** — neat, solid, corporate:

| Element | Meaning |
| --- | --- |
| Two monolithic columns | Strength, industrial scale, permanence |
| Orange structural diagonal | Engineering excellence, energy, load transfer |
| Hairline expansion joints between the components | Precision manufacturing |
| Slim deep-blue foundation bar | Solid foundations, durability, trust |

The icon is the wordmark's N enlarged — symbol and name share one
geometry, so the brand stays coherent from a favicon to a fascia sign.
The identity follows the visual language of major building-materials
corporations (Cemex, Holcim, Heidelberg Materials) and current industrial
branding practice: solid geometric masses, deliberate negative space, a
restrained palette with one accent color, and bold engineered typography.
No gradients, no decoration — fully recognizable in a single color.

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
