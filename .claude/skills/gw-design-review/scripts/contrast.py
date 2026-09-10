#!/usr/bin/env python3
"""WCAG 2.x contrast ratios for the GW / OSCON palette.

Usage
-----
    python3 contrast.py "#033C5A" "#FFFFFF"     one pair
    python3 contrast.py --palette               every brand colour vs the common grounds
    python3 contrast.py --palette --all         full matrix, every pair

Thresholds: 4.5:1 for normal text, 3.0:1 for large text (>=18pt, or >=14pt bold),
3.0:1 for UI components and meaningful graphical objects.

No third-party dependencies.
"""

import sys

PALETTE = [
    ("GW Blue",       "#033C5A", "core"),
    ("Navy Yard",     "#00223E", "core"),
    ("Potomac",       "#0075C8", "core"),
    ("Row House",     "#EF4343", "core"),
    ("GW Buff",       "#D6BF91", "core"),
    ("White",         "#FFFFFF", "core"),
    ("OSCON Gold",    "#FFD34D", "oscon"),
    ("OSCON Green",   "#33A56E", "oscon"),
    ("OSCON Orchid",  "#B04A8F", "oscon"),
    ("Parchment",     "#FFEFAE", "pastel"),
    ("Patina",        "#ADCAB8", "pastel"),
    ("Blossom",       "#D1A0B9", "pastel"),
    ("Blue Fog",      "#52C9E8", "pastel"),
]

GROUNDS = ["#FFFFFF", "#033C5A", "#00223E"]


def parse_hex(value):
    s = value.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"not a hex colour: {value!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    def channel(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg_hex, bg_hex):
    l1 = relative_luminance(parse_hex(fg_hex))
    l2 = relative_luminance(parse_hex(bg_hex))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def verdict(ratio):
    """Plain-language result, phrased as what the colour may be used for."""
    if ratio >= 7.0:
        return "AAA  — any size"
    if ratio >= 4.5:
        return "AA   — any size"
    if ratio >= 3.0:
        return "AA   — LARGE text only (>=18pt / >=14pt bold); also OK for shapes and rules"
    return "FAIL — shapes and fills only, never text"


def name_for(hex_value):
    target = parse_hex(hex_value)
    for name, hx, _ in PALETTE:
        if parse_hex(hx) == target:
            return name
    return hex_value.upper()


def report_pair(fg, bg):
    ratio = contrast_ratio(fg, bg)
    print(f"{name_for(fg)} ({fg.upper()}) on {name_for(bg)} ({bg.upper()})")
    print(f"  ratio  {ratio:6.2f}:1")
    print(f"  {verdict(ratio)}")


def report_palette(full=False):
    grounds = [hx for _, hx, _ in PALETTE] if full else GROUNDS
    for bg in grounds:
        print(f"\nOn {name_for(bg)} ({bg.upper()})")
        print(f"  {'colour':<16}{'hex':<10}{'ratio':>8}   verdict")
        print("  " + "-" * 74)
        for name, hx, group in PALETTE:
            if parse_hex(hx) == parse_hex(bg):
                continue
            ratio = contrast_ratio(hx, bg)
            tag = "*" if group == "oscon" else " "
            print(f"  {name + tag:<16}{hx.upper():<10}{ratio:>7.2f}:1   {verdict(ratio)}")
    print("\n  * OSCON extended accent — OSCON materials only, never a university colour.")
    print("  Thresholds: 4.5:1 normal text, 3.0:1 large text and graphical objects.\n")


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--palette":
        report_palette(full="--all" in args)
        return 0
    if len(args) != 2:
        print("error: give two hex colours, or --palette\n", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        return 2
    try:
        report_pair(args[0], args[1])
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
