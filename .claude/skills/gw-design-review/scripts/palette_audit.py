#!/usr/bin/env python3
"""Find the flat colours in a graphic and match them against the GW / OSCON palette.

Usage
-----
    python3 palette_audit.py design.png
    python3 palette_audit.py slide.jpg --top 20 --min-share 0.5
    python3 palette_audit.py cover.png --include-neutral

What it does
------------
Quantises the image, then for each dominant colour reports the nearest brand colour and
the perceptual distance to it (CIE76 dE in Lab space):

    dE <  6   on palette (a match, or an imperceptible shift)
    dE < 16   near palette — probably a tint, a blend edge, or JPEG noise
    dE >= 16  OFF PALETTE — worth explaining

IMPORTANT: photographs are exempt from the palette. Skin tones, timber, sky, and clothing
will all read as off-palette and that is fine. Run this on graphics — covers, charts,
diagrams, title cards, social tiles — or crop the graphic region out of a mixed page
first. On a page that mixes both, read the result as "these colours exist here", not as a
list of violations.

Requires Pillow:  pip install Pillow
"""

import sys
from collections import Counter

try:
    from PIL import Image
except ImportError:
    sys.exit(
        "error: this script needs Pillow.\n"
        "  pip install Pillow      (or: python3 -m pip install --user Pillow)"
    )

PALETTE = [
    ("GW Blue",      "#033C5A"),
    ("Navy Yard",    "#00223E"),
    ("Potomac",      "#0075C8"),
    ("Row House",    "#EF4343"),
    ("GW Buff",      "#D6BF91"),
    ("White",        "#FFFFFF"),
    ("OSCON Gold",   "#FFD34D"),
    ("OSCON Green",  "#33A56E"),
    ("OSCON Orchid", "#B04A8F"),
    ("Parchment",    "#FFEFAE"),
    ("Patina",       "#ADCAB8"),
    ("Blossom",      "#D1A0B9"),
    ("Blue Fog",     "#52C9E8"),
    ("Black",        "#000000"),
]

MATCH, NEAR = 6.0, 16.0


def parse_hex(value):
    s = value.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


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


PALETTE_LAB = [(name, hx, to_lab(parse_hex(hx))) for name, hx in PALETTE]


def nearest(rgb):
    lab = to_lab(rgb)
    name, hx, best = min(
        ((n, h, delta_e(lab, plab)) for n, h, plab in PALETTE_LAB),
        key=lambda t: t[2],
    )
    return name, hx, best


def chroma(rgb):
    _, a, b = to_lab(rgb)
    return (a * a + b * b) ** 0.5


def audit(path, top=14, min_share=0.4, include_neutral=False):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    # Downsample for speed, then quantise to collapse gradients and compression noise.
    work = im.copy()
    work.thumbnail((600, 600), Image.LANCZOS)
    quant = work.quantize(colors=64, method=Image.MEDIANCUT).convert("RGB")
    pixels = list(quant.getdata())
    total = len(pixels)

    counts = Counter(pixels)
    rows, skipped_neutral = [], 0
    for rgb, n in counts.most_common():
        share = 100.0 * n / total
        if share < min_share:
            continue
        if not include_neutral and chroma(rgb) < 8 and 12 < to_lab(rgb)[0] < 96:
            skipped_neutral += 1        # mid greys: usually photo or antialiasing
            continue
        name, hx, d = nearest(rgb)
        rows.append((share, rgb, name, hx, d))
        if len(rows) >= top:
            break

    print(f"\n{path}   {w}x{h}")
    print(f"{'share':>7}  {'colour':<9}  {'nearest brand colour':<22}{'dE':>6}   status")
    print("-" * 76)
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
        print(f"{share:6.1f}%  {hexv:<9}  {name + ' ' + hx:<22}{d:6.1f}   {status}")

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
    print()


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    path = args[0]
    top = int(args[args.index("--top") + 1]) if "--top" in args else 14
    share = float(args[args.index("--min-share") + 1]) if "--min-share" in args else 0.4
    try:
        audit(path, top=top, min_share=share, include_neutral="--include-neutral" in args)
    except FileNotFoundError:
        print(f"error: no such file: {path}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
