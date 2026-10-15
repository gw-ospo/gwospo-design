#!/usr/bin/env python3
"""Check that the skill's brand/palette.json matches the colours in brand/DESIGN.md.

DESIGN.md is the source of truth for people; palette.json is what the scripts read. This
fails (exit 1) and lists every difference if they have drifted apart. build-skill-zip.sh
runs it before packaging.

Run from the repository root:   python3 scripts/check-palette.py
"""

import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILL = os.path.join(ROOT, ".claude", "skills", "gw-design-review")
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from gw_palette import _read_json, parse_design_md  # noqa: E402

design = os.path.join(SKILL, "brand", "DESIGN.md")
palette = os.path.join(SKILL, "brand", "palette.json")

with open(design, encoding="utf-8") as f:
    from_md = {hx: (name, group) for name, hx, group in parse_design_md(f.read())}
from_json = {hx: (name, group) for name, hx, group in _read_json(palette)[0]}

problems = []
for hx in sorted(from_md.keys() - from_json.keys()):
    problems.append(f"in DESIGN.md but not palette.json: {from_md[hx][0]} {hx}")
for hx in sorted(from_json.keys() - from_md.keys()):
    problems.append(f"in palette.json but not DESIGN.md: {from_json[hx][0]} {hx}")
for hx in sorted(from_md.keys() & from_json.keys()):
    if from_md[hx] != from_json[hx]:
        problems.append(f"{hx}: DESIGN.md has {from_md[hx]}, palette.json has {from_json[hx]}")

if problems:
    print("error: brand/palette.json does not match brand/DESIGN.md:", file=sys.stderr)
    for p in problems:
        print(f"  {p}", file=sys.stderr)
    sys.exit(1)
print(f"OK: palette.json matches DESIGN.md ({len(from_json)} colours).")
