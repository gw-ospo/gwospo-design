#!/usr/bin/env python3
"""WCAG 2.x contrast ratios for the GW / OSCON palette.

Usage
-----
    python3 contrast.py "#033C5A" "#FFFFFF"     one pair (foreground, background)
    python3 contrast.py --palette               every brand colour vs the common grounds
    python3 contrast.py --palette --all         full matrix, every pair
    python3 contrast.py --palette --design DESIGN.md   use the project's palette

Thresholds: 4.5:1 for normal text, 3.0:1 for large text (>=18pt, or >=14pt bold),
3.0:1 for UI components and meaningful graphical objects.

No third-party dependencies.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # also works under python -I
from gw_palette import load_palette, parse_hex  # noqa: E402

# The grounds most GW pieces actually sit on. Names, so a DESIGN.md palette can supply them.
GROUND_NAMES = ["White", "GW Blue", "Navy Yard"]


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


def name_for(hex_value, palette):
    target = parse_hex(hex_value)
    for name, hx, _ in palette:
        if parse_hex(hx) == target:
            return name
    return f"#{hex_value.lstrip('#').upper()} (not in palette)"


def report_pair(fg, bg, palette):
    ratio = contrast_ratio(fg, bg)
    print(f"{name_for(fg, palette)} on {name_for(bg, palette)}")
    print(f"  ratio  {ratio:6.2f}:1")
    print(f"  {verdict(ratio)}")


def report_palette(palette, full=False):
    if full:
        grounds = [hx for _, hx, _ in palette]
    else:
        by_name = {name: hx for name, hx, _ in palette}
        grounds = [by_name[n] for n in GROUND_NAMES if n in by_name]
        if not grounds:     # a DESIGN.md that renamed the grounds: use lightest and darkest
            ordered = sorted(palette, key=lambda e: relative_luminance(parse_hex(e[1])))
            grounds = [ordered[-1][1], ordered[0][1]]
    for bg in grounds:
        print(f"\nOn {name_for(bg, palette)} ({bg.upper()})")
        print(f"  {'colour':<16}{'hex':<10}{'ratio':>8}   verdict")
        print("  " + "-" * 74)
        for name, hx, group in palette:
            if parse_hex(hx) == parse_hex(bg):
                continue
            ratio = contrast_ratio(hx, bg)
            tag = "*" if group == "oscon" else " "
            print(f"  {name + tag:<16}{hx.upper():<10}{ratio:>7.2f}:1   {verdict(ratio)}")
    print("\n  * OSCON extended accent — OSCON materials only, never a university colour.")
    print("  Thresholds: 4.5:1 normal text, 3.0:1 large text and graphical objects.\n")


def main(argv):
    parser = argparse.ArgumentParser(
        description="WCAG contrast ratios for the GW / OSCON palette.",
        epilog='example: contrast.py "#FFD34D" "#FFFFFF"')
    parser.add_argument("colours", nargs="*", metavar="HEX",
                        help="foreground and background, e.g. '#033C5A' '#FFFFFF'")
    parser.add_argument("--palette", action="store_true",
                        help="every palette colour against White, GW Blue and Navy Yard")
    parser.add_argument("--all", action="store_true", help="with --palette: every pair")
    parser.add_argument("--design", metavar="DESIGN.md",
                        help="read the palette from the project's DESIGN.md")
    args = parser.parse_args(argv[1:])

    palette, source = load_palette(args.design)

    if args.palette:
        print(f"Palette: {source}")
        report_palette(palette, full=args.all)
        return 0
    if len(args.colours) != 2:
        parser.error("give two hex colours (foreground, background), or --palette")
    try:
        report_pair(args.colours[0], args.colours[1], palette)
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
