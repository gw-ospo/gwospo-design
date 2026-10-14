"""The GW / OSCON palette, shared by contrast.py and palette_audit.py.

A project's DESIGN.md is the source of truth. load_palette(path) reads the colours out of
it; with no path (or if parsing finds too little), the built-in copy below is used. Every
script prints which source it used, so a stale copy never passes silently.

Each entry is (name, hex, group), where group is "core", "oscon", or "pastel".
"""

import os
import re
import sys

BUILTIN = [
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

# Fewer colours than this from DESIGN.md means the file is not laid out the way the parser
# expects (tables of | Name | #HEX |), so falling back is safer than auditing against a
# half-empty palette.
MIN_PARSED = 6

_HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
# A capitalised name directly before a hex value in prose: "Blue Fog #52C9E8".
_INLINE = re.compile(r"\b([A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)*) \(?(#[0-9A-Fa-f]{6})\b")


def parse_hex(value):
    s = value.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6 or any(c not in "0123456789abcdefABCDEF" for c in s):
        raise ValueError(f"not a hex colour: {value!r} (expected e.g. #033C5A)")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def parse_design_md(text):
    """Pull (name, hex, group) entries out of a DESIGN.md.

    Table rows (| Name | #HEX | ...) give core or OSCON colours, depending on whether the
    section heading mentions "extended" or "OSCON". Other "Name #HEX" mentions in prose are
    treated as pastels / tints. The first name seen for a hex value wins.
    """
    entries, seen = [], set()
    group_for_tables = "core"

    def add(name, hx, group):
        key = hx.upper()
        if key not in seen:
            seen.add(key)
            entries.append((name.strip(), key, group))

    for line in text.splitlines():
        if line.lstrip().startswith("#") and not _HEX.match(line.strip()):
            heading = line.lower()
            group_for_tables = "oscon" if ("extended" in heading or "oscon" in heading) else "core"
            continue
        if line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and _HEX.fullmatch(cells[1]):
                add(cells[0], cells[1], group_for_tables)
        # Inline mentions, including ones inside a table's third column ("Parchment #FFEFAE").
        for name, hx in _INLINE.findall(line):
            add(name, hx, "pastel")
    return entries


def load_palette(design_path=None):
    """Return (palette, source_description)."""
    if not design_path:
        return BUILTIN, "built-in copy (pass --design path/to/DESIGN.md to use the project's)"
    if not os.path.isfile(design_path):
        print(f"warning: {design_path} not found; using the built-in palette", file=sys.stderr)
        return BUILTIN, "built-in copy (DESIGN.md not found)"
    with open(design_path, encoding="utf-8") as f:
        parsed = parse_design_md(f.read())
    if len(parsed) < MIN_PARSED:
        print(f"warning: found only {len(parsed)} colours in {design_path}; "
              "using the built-in palette", file=sys.stderr)
        return BUILTIN, f"built-in copy ({design_path} could not be parsed)"
    return parsed, f"{design_path} ({len(parsed)} colours)"
