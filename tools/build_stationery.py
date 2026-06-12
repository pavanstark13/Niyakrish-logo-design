#!/usr/bin/env python3
"""NIYAKRISH INDUSTRIES print stationery, built on the NIYA v5 identity.

Generates print-ready SVG masters (10 units = 1 mm), PNG previews and
vector PDFs for:
  * business card, 89 x 51 mm, front + back
  * tri-fold brochure, A4 landscape, outside + inside
  * DL envelope, 220 x 110 mm
  * A4 letterhead print master

Company details come from the GST registration certificate
(GSTIN 29AAKCN0823D1ZM). Phone / email / web are placeholders until
the company confirms them.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cairosvg
from pypdf import PdfWriter

import build_logos as bl
import build_identity as bi
from build_identity import mark, wordmark, word_width, MW, MH

NAVY = bi.NAVY
ORANGE = bi.ORANGE
STEEL = bi.STEEL
INK = bi.INK
WHITE = bi.WHITE
LIGHTB = bi.LIGHTB
TINT = "#EEF2F8"

bold, reg = bl.bold, bl.reg

COMPANY = "NIYAKRISH INDUSTRIES PRIVATE LIMITED"
TAGLINE = "STRENGTH DELIVERED"
PRODUCTS = "READY MIX CONCRETE   •   BLOCKS   •   AGGREGATES"
ADDR1 = "Survey No. 428, Hasige Hobli, Huliyur Durga,"
ADDR2 = "Kampalapura, Tumakuru, Karnataka – 572123, India"
GSTIN = "GSTIN: 29AAKCN0823D1ZM"
PHONE = "+91 XXXXX XXXXX"
EMAIL = "info@niyakrish.in"
WEB = "www.niyakrish.in"

ROOT = bl.ROOT


def svg_mm(w, h, body, bg=WHITE):
    """SVG sized in physical mm (viewBox at 10 units per mm)."""
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w / 10}mm" height="{h / 10}mm">'
    )
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return head + bgr + body + "</svg>"


def stack(eng, lines, size, x, y, fill, lh, anchor="start"):
    out = []
    for ln in lines:
        if ln:
            out.append(eng.text(ln, size, x, y, fill, anchor=anchor))
        y += lh
    return "".join(out), y


def tri(x, y, s, fill=ORANGE):
    """Small upward triangle bullet with its base on y."""
    return (f'<polygon points="{x},{y} {x + s},{y} {x + s / 2},{y - s * 0.87}" '
            f'fill="{fill}"/>')


def lockup(tx, ty, s, cap, fill=NAVY, tag_fill=STEEL, gap=46):
    """Mark + NIYA + justified tagline, top-left anchored at (tx, ty)."""
    out = [mark(NAVY if fill == NAVY else fill, WHITE, ORANGE, tx=tx, ty=ty,
                s=s)]
    x0 = tx + MW * s + gap
    base = ty + MH * s * 0.62
    out.append(wordmark(x0, base, cap, fill))
    tw = word_width(cap)
    tsize = cap * 0.19
    track = bold.track_to_fit(TAGLINE, tsize, tw)
    out.append(bold.text(TAGLINE, tsize, x0, base + cap * 0.32, tag_fill,
                         track))
    return "".join(out)


# ----------------------------------------------------- business card -----
def card_front():
    W, H = 890, 510
    b = []
    b.append(lockup(55, 48, 0.62, 78, gap=34))
    b.append('<rect x="55" y="205" width="120" height="5" fill="#FF7A1A"/>')
    b.append(bold.text("KRISHNA KAMPALAPURA", 37, 55, 282, NAVY, 0.04))
    b.append(reg.text("Director", 26, 55, 320, STEEL))
    items = [(PHONE, 372), (EMAIL, 412), (WEB, 452)]
    for txt, y in items:
        b.append(f'<rect x="55" y="{y - 17}" width="13" height="13" '
                 f'fill="{ORANGE}"/>')
        b.append(reg.text(txt, 24, 85, y, INK))
    b.append(reg.text(ADDR1, 19, 835, 372, STEEL, anchor="end"))
    b.append(reg.text(ADDR2.replace(", India", ""), 19, 835, 400, STEEL,
                      anchor="end"))
    b.append(reg.text(GSTIN, 19, 835, 428, STEEL, anchor="end"))
    b.append(f'<rect x="0" y="496" width="280" height="14" fill="{ORANGE}"/>')
    b.append(f'<rect x="280" y="496" width="610" height="14" fill="{NAVY}"/>')
    return svg_mm(W, H, "".join(b))


def card_back():
    W, H = 890, 510
    b = []
    s = 1.05
    b.append(mark(WHITE, NAVY, ORANGE, tx=W / 2 - MW * s / 2, ty=66, s=s))
    b.append(wordmark(W / 2, 330, 88, WHITE, anchor="middle"))
    tw = word_width(88)
    track = bold.track_to_fit(PRODUCTS, 20, tw + 160)
    b.append(bold.text(PRODUCTS, 20, W / 2, 396, LIGHTB, track,
                       anchor="middle"))
    b.append(f'<rect x="{W / 2 - 60}" y="432" width="120" height="5" '
             f'fill="{ORANGE}"/>')
    b.append(reg.text(GSTIN.replace("GSTIN: ", "GSTIN  "), 20, W / 2, 474,
                      LIGHTB, anchor="middle"))
    return svg_mm(W, H, "".join(b), bg=NAVY)


# -------------------------------------------------------- letterhead -----
def letterhead_a4():
    W, H = 2100, 2970
    b = []
    b.append(lockup(140, 120, 1.0, 118, gap=50))
    info = [
        (COMPANY, bold, 40, NAVY, 188),
        (ADDR1, reg, 26, STEEL, 238),
        (ADDR2, reg, 26, STEEL, 276),
        (GSTIN + "    |    CIN: [CIN Number]", reg, 26, STEEL, 314),
        (f"Phone: {PHONE}    |    Email: {EMAIL}", reg, 26, STEEL, 352),
    ]
    for txt, eng, size, fill, y in info:
        b.append(eng.text(txt, size, 1960, y, fill, anchor="end"))
    b.append(f'<rect x="140" y="430" width="1820" height="8" fill="{NAVY}"/>')
    b.append(f'<rect x="140" y="444" width="1820" height="3" fill="{ORANGE}"/>')
    b.append(f'<rect x="140" y="2820" width="1820" height="3" fill="{ORANGE}"/>')
    b.append(reg.text(f"Regd. Office: {ADDR1} {ADDR2}", 23, W / 2, 2866,
                      STEEL, anchor="middle"))
    foot = f"{GSTIN}    |    {WEB}    |    {TAGLINE}"
    b.append(reg.text(foot, 23, W / 2, 2900, STEEL, anchor="middle"))
    return svg_mm(W, H, "".join(b))


# ----------------------------------------------------------- envelope ----
def envelope_dl():
    W, H = 2200, 1100
    b = []
    b.append(lockup(110, 95, 0.78, 92, gap=40))
    addr, _ = stack(reg, [COMPANY, ADDR1, ADDR2], 25, 110, 360, STEEL, 38)
    b.append(addr)
    b.append(f'<rect x="0" y="1010" width="440" height="90" fill="{ORANGE}"/>')
    b.append(f'<rect x="440" y="1010" width="1760" height="90" fill="{NAVY}"/>')
    b.append(bold.text(TAGLINE, 30, 2090, 1068, WHITE, 0.22, anchor="end"))
    return svg_mm(W, H, "".join(b))


# ----------------------------------------------------------- brochure ----
PANEL = 990


def _panel_heading(b, x, y, text, fill=NAVY):
    b.append(bold.text(text, 44, x, y, fill, 0.03))
    b.append(f'<rect x="{x}" y="{y + 26}" width="150" height="6" '
             f'fill="{ORANGE}"/>')


def brochure_outside():
    W, H = 2970, 2100
    b = []
    # ---- left panel: WHY NIYA (folds inside) -----------------------------
    b.append(f'<rect width="{PANEL}" height="{H}" fill="{TINT}"/>')
    x = 120
    _panel_heading(b, x, 280, "WHY NIYA")
    bullets = [
        ("Lab-tested batches", "Quality checked on every pour,"
                               " with batch records you can audit."),
        ("On-time site delivery", "Transit mixers and tippers"
                                  " scheduled around your pour plan."),
        ("Consistent grading", "Clean, well-sourced materials,"
                               " screened and graded to spec."),
        ("GST-compliant supply", "Proper tax invoice and e-way bill"
                                 " with every consignment."),
    ]
    y = 470
    for title, desc in bullets:
        b.append(tri(x, y, 34))
        b.append(bold.text(title, 32, x + 56, y, NAVY))
        half = desc.find(" ", len(desc) // 2 - 6)
        seg, _ = stack(reg, [desc[:half], desc[half + 1:]], 25,
                       x + 56, y + 42, STEEL, 38)
        b.append(seg)
        y += 190
    b.append(bold.text(TAGLINE, 30, x, 1950, ORANGE, 0.18))
    # ---- middle panel: back cover / contact ------------------------------
    x = PANEL + 120
    _panel_heading(b, x, 280, "CONTACT US")
    rows = [
        ("Phone", PHONE), ("Email", EMAIL), ("Web", WEB),
    ]
    y = 460
    for label, val in rows:
        b.append(bold.text(label, 27, x, y, NAVY))
        b.append(reg.text(val, 27, x + 240, y, INK))
        y += 64
    b.append(bold.text("Works & Regd. Office", 27, x, y + 30, NAVY))
    seg, y2 = stack(reg, [COMPANY, ADDR1, ADDR2, GSTIN], 25, x, y + 76,
                    INK, 40)
    b.append(seg)
    s = 0.85
    b.append(mark(NAVY, WHITE, ORANGE, tx=PANEL + PANEL / 2 - MW * s / 2,
                  ty=1480, s=s))
    # ---- right panel: front cover ----------------------------------------
    b.append(f'<rect x="{2 * PANEL}" width="{PANEL}" height="{H}" '
             f'fill="{NAVY}"/>')
    cxp = 2 * PANEL + PANEL / 2
    s = 1.7
    b.append(mark(WHITE, NAVY, ORANGE, tx=cxp - MW * s / 2, ty=400, s=s))
    b.append(wordmark(cxp, 1130, 140, WHITE, anchor="middle"))
    tw = word_width(140)
    track = bold.track_to_fit(TAGLINE, 34, tw)
    b.append(bold.text(TAGLINE, 34, cxp - tw / 2, 1210, LIGHTB, track))
    b.append(f'<rect x="{cxp - 75}" y="1330" width="150" height="6" '
             f'fill="{ORANGE}"/>')
    track = bold.track_to_fit(PRODUCTS, 22, tw + 120)
    b.append(bold.text(PRODUCTS, 22, cxp, 1830, LIGHTB, track,
                       anchor="middle"))
    b.append(reg.text(COMPANY, 23, cxp, 1950, WHITE, anchor="middle"))
    return svg_mm(W, H, "".join(b))


def brochure_inside():
    W, H = 2970, 2100
    b = []
    for px in (PANEL, 2 * PANEL):
        b.append(f'<rect x="{px - 1}" y="120" width="2" height="{H - 240}" '
                 f'fill="#D7DEEA"/>')
    # ---- panel 1: about ---------------------------------------------------
    x = 120
    _panel_heading(b, x, 280, "ABOUT NIYAKRISH")
    about = [
        "NIYAKRISH INDUSTRIES PRIVATE",
        "LIMITED is a construction materials",
        "company based in Tumakuru,",
        "Karnataka, supplying Ready Mix",
        "Concrete, concrete blocks and",
        "graded aggregates to builders,",
        "contractors and infrastructure",
        "projects across the region.",
        "",
        "Every batch leaves our plant with",
        "one promise — the one in our name:",
    ]
    seg, y = stack(reg, about, 27, x, 420, INK, 46)
    b.append(seg)
    b.append(bold.text("Strength, delivered.", 34, x, y + 26, ORANGE))
    s = 0.62
    b.append(mark(NAVY, WHITE, ORANGE, tx=x, ty=1700, s=s))
    b.append(bold.text("The Delta Standard", 26, x + MW * s + 40, 1700 + 60,
                       NAVY))
    b.append(reg.text("One geometry, one promise.", 24, x + MW * s + 40,
                      1700 + 100, STEEL))
    # ---- panel 2: products -------------------------------------------------
    x = PANEL + 120
    _panel_heading(b, x, 280, "OUR PRODUCTS")
    prods = [
        ("READY MIX CONCRETE",
         ["Computer-batched RMC, grades", "M10 – M50, delivered fresh to",
          "site in transit mixers."]),
        ("CONCRETE BLOCKS",
         ["Solid and hollow blocks with", "consistent strength, size and",
          "cure for faster walling."]),
        ("AGGREGATES",
         ["Clean coarse and fine", "aggregates, screened and",
          "graded to specification."]),
    ]
    y = 440
    for title, desc in prods:
        b.append(tri(x, y, 38))
        b.append(bold.text(title, 33, x + 62, y, NAVY))
        seg, _ = stack(reg, desc, 26, x + 62, y + 46, STEEL, 42)
        b.append(seg)
        y += 250
    b.append(f'<rect x="{x}" y="{y + 10}" width="750" height="120" '
             f'fill="{TINT}"/>')
    b.append(reg.text("Custom grades and site trials", 26, x + 40, y + 60,
                      INK))
    b.append(reg.text("available on request.", 26, x + 40, y + 100, INK))
    # ---- panel 3: how we deliver + CTA -------------------------------------
    x = 2 * PANEL + 120
    _panel_heading(b, x, 280, "HOW WE DELIVER")
    steps = [
        ("1", "Share your requirement",
         "Grade, quantity, site and pour date."),
        ("2", "We schedule the batch",
         "Mix design confirmed, plant slot booked."),
        ("3", "Delivered to your site",
         "Tracked vehicles, on-time pour support."),
    ]
    y = 460
    for num, title, desc in steps:
        b.append(f'<circle cx="{x + 30}" cy="{y - 12}" r="32" fill="{NAVY}"/>')
        b.append(bold.text(num, 32, x + 30, y - 1, WHITE, anchor="middle"))
        b.append(bold.text(title, 30, x + 90, y - 12, NAVY))
        b.append(reg.text(desc, 24, x + 90, y + 28, STEEL))
        y += 170
    b.append(f'<rect x="{x}" y="{y + 20}" width="750" height="330" '
             f'fill="{NAVY}"/>')
    b.append(bold.text("REQUEST A QUOTE", 36, x + 375, y + 120, WHITE, 0.06,
                       anchor="middle"))
    b.append(f'<rect x="{x + 300}" y="{y + 150}" width="150" height="5" '
             f'fill="{ORANGE}"/>')
    b.append(reg.text(PHONE, 30, x + 375, y + 220, WHITE, anchor="middle"))
    b.append(reg.text(EMAIL, 28, x + 375, y + 280, LIGHTB, anchor="middle"))
    return svg_mm(W, H, "".join(b))


# --------------------------------------------------------------- build ---
def main():
    items = {
        "stationery/svg/niya-business-card-front.svg": (card_front(), 1063),
        "stationery/svg/niya-business-card-back.svg": (card_back(), 1063),
        "stationery/svg/niya-letterhead-a4.svg": (letterhead_a4(), 1200),
        "stationery/svg/niya-envelope-dl.svg": (envelope_dl(), 1600),
        "stationery/svg/niya-brochure-outside.svg": (brochure_outside(), 2400),
        "stationery/svg/niya-brochure-inside.svg": (brochure_inside(), 2400),
    }
    pdf_paths = {}
    for rel, (content, png_w) in items.items():
        bl.write(rel, content)
        png_rel = rel.replace("/svg/", "/png/").replace(".svg", ".png")
        os.makedirs(os.path.dirname(os.path.join(ROOT, png_rel)),
                    exist_ok=True)
        cairosvg.svg2png(url=os.path.join(ROOT, rel),
                         write_to=os.path.join(ROOT, png_rel),
                         output_width=png_w)
        pdf_rel = rel.replace("/svg/", "/pdf/").replace(".svg", ".pdf")
        os.makedirs(os.path.dirname(os.path.join(ROOT, pdf_rel)),
                    exist_ok=True)
        cairosvg.svg2pdf(url=os.path.join(ROOT, rel),
                         write_to=os.path.join(ROOT, pdf_rel))
        pdf_paths[rel] = pdf_rel
        print("built", rel)

    def merge(out_rel, parts):
        w = PdfWriter()
        for p in parts:
            w.append(os.path.join(ROOT, pdf_paths[p]))
        with open(os.path.join(ROOT, out_rel), "wb") as f:
            w.write(f)
        for p in parts:
            os.remove(os.path.join(ROOT, pdf_paths[p]))
        print("built", out_rel)

    merge("stationery/pdf/niya-business-card.pdf",
          ["stationery/svg/niya-business-card-front.svg",
           "stationery/svg/niya-business-card-back.svg"])
    merge("stationery/pdf/niya-brochure-trifold.pdf",
          ["stationery/svg/niya-brochure-outside.svg",
           "stationery/svg/niya-brochure-inside.svg"])


if __name__ == "__main__":
    main()
