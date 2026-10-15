"""The brand palette, shared by contrast.py and palette_audit.py.

By default the palette comes from the skill's own brand/palette.json. Pass --design to use
a project's palette instead: either a palette.json in the same format, or a DESIGN.md whose
colour tables can be parsed. Every script prints which source it used.

load_palette() returns a Palette: .colors is a list of (name, hex, group) tuples, and
.groups maps each group to its description from palette.json (label, section, and, for
colours restricted to one context, a scope).
"""

import json
import os
import re
import sys
from collections import namedtuple

BUNDLED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", "palette.json")

Palette = namedtuple("Palette", "colors groups grounds source")

# Fewer colours than this from a DESIGN.md means the file is not laid out the way the parser
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


def _read_json(path):
    """Load and check a palette.json. Raises ValueError naming the problem."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}")
    groups = data.get("groups", {})
    colors = []
    for i, c in enumerate(data.get("colors", [])):
        missing = [k for k in ("name", "hex", "group") if k not in c]
        if missing:
            raise ValueError(f"{path}: colour #{i + 1} is missing {', '.join(missing)}")
        parse_hex(c["hex"])
        if c["group"] not in groups:
            raise ValueError(f"{path}: colour {c['name']!r} has group {c['group']!r}, "
                             f"which is not defined under \"groups\" ({', '.join(groups)})")
        colors.append((c["name"], c["hex"].upper(), c["group"]))
    if not colors:
        raise ValueError(f"{path} has no \"colors\"")
    return colors, groups, data.get("grounds", [])


def load_palette(design_path=None):
    """Return a Palette from palette.json (default), another palette.json, or a DESIGN.md.

    A malformed palette file ends the script with a message naming the problem.
    """
    try:
        return _load(design_path)
    except ValueError as exc:
        sys.exit(f"error: {exc}")


def _load(design_path):
    if not os.path.isfile(BUNDLED):
        sys.exit(f"error: the skill's palette is missing: {os.path.normpath(BUNDLED)}\n"
                 "  Reinstall the skill, or pass --design path/to/palette.json.")
    colors, groups, grounds = _read_json(BUNDLED)
    bundled = Palette(colors, groups, grounds, "brand/palette.json (bundled with the skill)")
    if not design_path:
        return bundled

    if not os.path.isfile(design_path):
        print(f"warning: {design_path} not found; using the bundled palette", file=sys.stderr)
        return bundled
    if design_path.lower().endswith(".json"):
        colors, groups, grounds = _read_json(design_path)
        return Palette(colors, groups, grounds, f"{design_path} ({len(colors)} colours)")

    with open(design_path, encoding="utf-8") as f:
        parsed = parse_design_md(f.read())
    if len(parsed) < MIN_PARSED:
        print(f"warning: found only {len(parsed)} colours in {design_path}; "
              "using the bundled palette", file=sys.stderr)
        return bundled
    # A DESIGN.md has no group descriptions or grounds; borrow the bundled ones where the
    # group names match, so scope notes such as "OSCON materials only" still print.
    return Palette(parsed, groups, grounds, f"{design_path} ({len(parsed)} colours)")
