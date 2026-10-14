#!/usr/bin/env python3
"""Find the flat colours in a graphic and match them against the GW / OSCON palette.

Usage
-----
    python3 palette_audit.py design.png
    python3 palette_audit.py prospectus.pdf                 every page (rendered first)
    python3 palette_audit.py slide.jpg --top 20 --min-share 0.5
    python3 palette_audit.py cover.png --include-neutral
    python3 palette_audit.py cover.png --design DESIGN.md   use the project's palette

What it does
------------
Quantises the image, then for each dominant colour reports the nearest brand colour and
the perceptual distance to it (CIE76 dE in Lab space):

    dE <  6   on palette (a match, or an imperceptible shift)
    dE < 16   near palette — probably a tint, a blend edge, or JPEG noise
    dE >= 16  OFF PALETTE — worth explaining

Black is not a brand colour, so pure black type or fills report as off palette (nearest
Navy Yard). That is deliberate: it is a common substitute for GW Blue or Navy Yard.

Photographs are exempt from the palette. Skin tones, timber, sky, and clothing will all
read as off-palette and that is fine. Run this on graphics — covers, charts, diagrams,
title cards, social tiles — or crop the graphic region out of a mixed page first. On a
page that mixes both, read the result as "these colours exist here", not as a list of
violations.

Requires Pillow (pip install Pillow). PDF input also needs a renderer; see rasterize.py.
"""

import argparse
import os
import shutil
import sys
import tempfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # also works under python -I
from gw_palette import load_palette, parse_hex  # noqa: E402

try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    sys.exit(
        "error: palette_audit.py needs Pillow.\n"
        "  pip install Pillow      (or: python3 -m pip install --user Pillow)\n"
        "If it cannot be installed here, skip the palette audit and list it as not run.")

# Thresholds in CIE76 dE. ~2.3 is a just-noticeable difference; 6 allows for export and
# colour-profile shifts on a true match, and 16 separates "a tint or blend edge of a brand
# colour" from "a different colour".
MATCH, NEAR = 6.0, 16.0

# The image is shrunk to fit 600x600 before quantising: flat fills survive any downsample,
# and this keeps a full-page render to about a second.
WORK_SIZE = 600
# 64 buckets is enough to keep every palette colour distinct while collapsing gradients
# and JPEG noise into the fill they belong to.
QUANT_COLOURS = 64

# Low-chroma mid-tones are almost always photo content or antialiasing, not a fill choice.
# Chroma < 8 is visually grey; L* 12-96 excludes near-black and near-white, which are
# reported because they can be real (and off-brand) fills.
NEUTRAL_CHROMA, NEUTRAL_L_MIN, NEUTRAL_L_MAX = 8, 12, 96

# Pages are rendered at 72 dpi for the audit: the image is downsampled to WORK_SIZE anyway,
# so a higher resolution only costs time.
AUDIT_DPI = 72

SUPPORTED = "PNG, JPEG, GIF, WebP, TIFF, BMP, or PDF"


def to_lab(rgb):
    """sRGB (0-255) -> CIE L*a*b*, D65."""
    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.00000
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t) + (16 / 116)
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(lab1, lab2):
    return sum((a - b) ** 2 for a, b in zip(lab1, lab2)) ** 0.5


def chroma(lab):
    _, a, b = lab
    return (a * a + b * b) ** 0.5


def audit(path, palette_lab, label=None, top=14, min_share=0.4, include_neutral=False):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    work = im.copy()
    work.thumbnail((WORK_SIZE, WORK_SIZE), Image.LANCZOS)
    quant = work.quantize(colors=QUANT_COLOURS, method=Image.MEDIANCUT).convert("RGB")
    pixels = list(quant.getdata())
    total = len(pixels)

    rows, skipped_neutral = [], 0
    for rgb, n in Counter(pixels).most_common():
        share = 100.0 * n / total
        if share < min_share:
            continue
        lab = to_lab(rgb)
        if (not include_neutral and chroma(lab) < NEUTRAL_CHROMA
                and NEUTRAL_L_MIN < lab[0] < NEUTRAL_L_MAX):
            skipped_neutral += 1
            continue
        name, hx, d = min(((pn, ph, delta_e(lab, pl)) for pn, ph, pl in palette_lab),
                          key=lambda t: t[2])
        rows.append((share, rgb, name, hx, d))
        if len(rows) >= top:
            break

    print(f"\n{label or path}   {w}x{h}")
    print(f"{'share':>7}  {'colour':<9}  {'nearest brand colour':<24}{'dE':>6}   status")
    print("-" * 78)
    off = []
    for share, rgb, name, hx, d in rows:
        hexv = "#%02X%02X%02X" % rgb
        if d < MATCH:
            status = "on palette"
        elif d < NEAR:
            status = "near — tint or blend?"
        else:
            status = "OFF PALETTE"
            off.append((hexv, share, name, d))
        print(f"{share:6.1f}%  {hexv:<9}  {name + ' ' + hx:<24}{d:6.1f}   {status}")

    if skipped_neutral and not include_neutral:
        print(f"\n({skipped_neutral} near-neutral colours skipped; --include-neutral to show them)")

    if off:
        print("\nOff-palette colours to account for:")
        for hexv, share, name, d in off:
            print(f"  {hexv}  {share:.1f}% of the image, nearest brand colour {name} (dE {d:.0f})")
        print("  If these come from a photograph, they are fine — photos are exempt.")
        print("  If they are flat graphic fills, replace them with a palette value.")
    else:
        print("\nNo off-palette flat colours found above the reporting threshold.")


def is_pdf(path):
    with open(path, "rb") as f:
        return f.read(5) == b"%PDF-"


def main(argv):
    parser = argparse.ArgumentParser(
        description="Match the dominant flat colours in a graphic against the brand palette.")
    parser.add_argument("path", help=f"the design file ({SUPPORTED})")
    parser.add_argument("--top", type=int, default=14,
                        help="report at most this many colours per image (default 14)")
    parser.add_argument("--min-share", type=float, default=0.4,
                        help="ignore colours covering less than this %% of the image (default 0.4)")
    parser.add_argument("--include-neutral", action="store_true",
                        help="also report greys, which are skipped by default")
    parser.add_argument("--design", metavar="DESIGN.md",
                        help="read the palette from the project's DESIGN.md")
    parser.add_argument("--pages", metavar="N or A-B", help="PDF only: which pages (default: all)")
    args = parser.parse_args(argv[1:])

    if not os.path.isfile(args.path):
        print(f"error: no such file: {args.path}", file=sys.stderr)
        return 2

    palette, source = load_palette(args.design)
    palette_lab = [(n, h, to_lab(parse_hex(h))) for n, h, _ in palette]
    print(f"Palette: {source}")
    opts = dict(top=args.top, min_share=args.min_share, include_neutral=args.include_neutral)

    if is_pdf(args.path):
        from rasterize import rasterize
        work = tempfile.mkdtemp(prefix="palette-audit-")
        try:
            pages = rasterize(args.path, out_dir=work, dpi=AUDIT_DPI, pages=args.pages)
            first = int(args.pages.split("-")[0]) if args.pages else 1
            for i, page in enumerate(pages):
                audit(page, palette_lab, label=f"{args.path} — page {first + i}", **opts)
        except (ValueError, RuntimeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        finally:
            shutil.rmtree(work, ignore_errors=True)
        print()
        return 0

    try:
        audit(args.path, palette_lab, **opts)
    except UnidentifiedImageError:
        ext = os.path.splitext(args.path)[1].lower()
        hint = ("  SVG is vector: export or screenshot it as PNG first.\n"
                if ext == ".svg" else "")
        print(f"error: cannot read {args.path} as an image. Supported: {SUPPORTED}.\n{hint}"
              "  For a design-tool link or web page, take a screenshot and audit that.",
              file=sys.stderr)
        return 2
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
