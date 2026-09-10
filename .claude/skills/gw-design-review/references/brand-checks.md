# Brand checks

Testable checks derived from `DESIGN.md` (GW refreshed brand, 2026 guidelines, plus the
OSCON extended palette). Each check has a pass condition and the failure that actually
shows up in student work.

**Source of truth:** if the project has its own `DESIGN.md`, read it and let it override
anything here. Values below are a working copy so this skill functions outside the
`gwospo-design` repository.

---

## 1. Colour

### The palette

| Slot | Name | Hex | Role |
|---|---|---|---|
| Core | GW Blue | `#033C5A` | Primary anchor: wordmarks, headlines, dark shapes |
| Core | Navy Yard | `#00223E` | Darkest tone: backgrounds, small dark shapes |
| Core | Potomac | `#0075C8` | Vivid blue accent, the workhorse mid colour |
| Core | Row House | `#EF4343` | Vivid red accent |
| Core | White | `#FFFFFF` | Breathing room, knockout shapes |
| Core | GW Buff | `#D6BF91` | Warm neutral, formal contexts only |
| OSCON | OSCON Gold | `#FFD34D` | Extended accent (from Parchment) |
| OSCON | OSCON Green | `#33A56E` | Extended accent (from Patina) |
| OSCON | OSCON Orchid | `#B04A8F` | Extended accent (from Blossom) |

Pastels available for large quiet grounds and tints: Parchment `#FFEFAE`,
Patina `#ADCAB8`, Blossom `#D1A0B9`, Blue Fog `#52C9E8`, Buff tints.

The **7-slot working palette** — GW Blue, Potomac, Row House, Gold, Green, Orchid, White —
is the set used in the 2027 logo squares and the website pattern.

### Checks

**C1 — No off-palette colour.**
Pass: every flat colour in the graphic matches a palette value, or is a deliberate tint of
one. Run `scripts/palette_audit.py`. Photographs are exempt.
Common failure: a stock graphic, an icon set, or a headshot background introducing a colour
that appears nowhere else — the eye reads it as an accident even when nobody can name why.

**C2 — Lead with GW Blue and white.**
Pass: GW Blue and white carry the composition; accents are supporting players. No extended
accent is the dominant field of a whole composition.
Common failure: a saturated accent used as a full-page background because it looked
energetic. It reads as a different brand.

**C3 — Dark blue is punctuation, not wallpaper.**
Pass: dark fields (GW Blue / Navy Yard) are placed deliberately and are the minority of the
page area, so that landing on one means something.
Common failure: most pages sitting on dark blue, which leaves nothing for anything to stand
out against and makes photographs look muddy.

**C4 — At most two accent hues adjacent.**
Pass: saturated fields are separated by white or GW Blue where the layout gets busy.
Common failure: gold next to green next to orchid next to red, all touching.

**C5 — Extended accents are OSCON-only.**
Pass: Gold, Green, and Orchid appear only in OSCON materials, and are never labelled or
presented as university colours.
Common failure: reusing the OSCON palette on a general GW OSPO deliverable.

---

## 2. Typography

Three brand typefaces, all on Adobe Fonts:

| Face | Role | Web fallback stack |
|---|---|---|
| **Gazzetta** (variable) | Headlines and key marketing moments. Short phrases only. Event titles, track names, big numerals. | `'Gazzetta', 'Avenir Next Condensed', 'Arial Narrow', sans-serif` |
| **Avenir Next** | Body copy, subheads, captions, call-outs, UI text. | `'Avenir Next', 'Avenir', 'Segoe UI', sans-serif` |
| **Source Serif** | Sparing emphasis: italic emphasis words, short callouts, pull quotes. | `'Source Serif 4', Georgia, serif` |

Suggested scale for 1920×1080 slides: Gazzetta display 96–160 pt; Avenir Next subhead
36–48 pt; body 24–28 pt (never below 24); captions 24 pt. Scale proportionally for other
media — for US Letter print this lands near display 31 pt, subhead 12 pt, body 10 pt.

### Checks

**T1 — Two faces per asset, three at most.**
Pass: the piece pairs two of the three brand faces, mixing weights rather than families for
variety. Three is permissible but never required.
Common failure: a fourth face arriving with a template or a downloaded icon set.

**T2 — Gazzetta earns its place.**
Pass: Gazzetta carries short, declarative headlines and numerals only.
Common failure: a full sentence or a paragraph set in Gazzetta. It is condensed and
newspaper-derived; at length it stops being readable.

**T3 — Nothing below the floor.**
Pass: no body text below 24 pt on a 1920×1080 slide, or below roughly 9 pt in Letter-size
print. Captions and legal type still have to be legible at arm's length.
Common failure: shrinking body copy to make content fit. The fix is less content or another
page, never smaller type.

**T4 — Headline colour.**
Pass: GW Blue on light grounds; white or Gold on GW Blue / Navy Yard.

**T5 — Source Serif stays rare.**
Pass: Source Serif italic marks a single emphasised word, a pull quote, or a short callout.
Common failure: using it for a whole body column, which flattens the contrast it exists to
create.

**T6 — Letter-spacing on condensed type and small caps.**
Pass: uppercase labels are letter-spaced (roughly 0.12–0.2 em); tight numerals in Gazzetta
get a little tracking so digit pairs do not collide.
Common failure: `01` in Gazzetta at small size reading as a single mark.

---

## 3. Logo

File: `GW_OSCON_horizontal_extended_2027.svg` (PNG 2160×792). Structure: a 2×3 tile grid —
GW monogram plus a "2027" square in GW Blue, and five glyph squares (Potomac, Row House,
Gold, Orchid, Green) with **white knockout shapes** — beside the "OPEN SOURCE CONFERENCE"
wordmark in GW Blue.

**L1 — Clear space.**
Pass: at least one tile width (one grid square) of empty space on all four sides.
Common failure: type or a photo edge crowding the mark.

**L2 — Light grounds only.**
Pass: the logo sits on white or a very light ground.
Common failure: placing it on GW Blue, on a photograph, or on the pattern. The knockouts are
transparent, so whatever is behind shows through the shapes and destroys the mark. **A
reversed dark-ground variant does not exist yet** — if one is needed, that is a request to
the design lead, not something to improvise.

**L3 — Minimum size.**
Pass: at least ~200 px wide on screen. In print, keep the "2027" in the monogram tile
legible.

**L4 — No modification.**
Pass: the mark is placed as supplied — vector where possible, never stretched, recoloured,
rotated, outlined, shadowed, or rebuilt from parts.
Common failure: retyping the wordmark, or lifting the tile grid out to use as decoration.

**L5 — Repetition count.**
Pass: in a multi-page document, the logo bookends — cover and back cover — or appears once
per standalone piece.
Common failure: placing the mark on every page to fill a corner. A logo that repeats stops
being a mark and becomes wallpaper. If a corner needs something, it needs a **structural**
element (a rule, a running head, a colour tab), not the logo. See `design-principles.md`,
Repetition.

**L6 — Host identity.**
Pass: where the GW Open Source Program Office needs to be credited, the OSPO lockup
(`gw_iddol_ospo_1c.png`) carries it. That mark is single-colour with transparency, so it can
be recoloured white for reversed use on GW Blue.

---

## 4. Pattern

File: `GW_OSCON_pattern_2027_B_extended.svg` (PNG 4195×1680). A **210 px modular tile grid**
— circles, half-rounds, diamonds, quarter-round leaves, S-curves, triangles, sparkles — in
the 7-slot working palette. The full artwork is 10 tiles wide by 4 tall.

**P1 — Crop on the module.**
Pass: bands and strips break at a 210 px tile boundary, so shapes are whole at the edge.
Technique for a full-width band in CSS: the artwork is 10×4 tiles, so
`background-size: 100% 400%` shows exactly one tile row (band height = width ÷ 10), and
`100% 200%` shows two rows (height = width ÷ 5). `background-position-y` at `0%`, `33.3%`,
`66.7%`, `100%` selects which row.
Common failure: an arbitrary crop that slices circles in half at the page edge.

**P2 — Keep type off the pattern.**
Pass: text sits on a solid panel placed over the pattern, or beside it — never directly on
it.

**P3 — Pattern is punctuation.**
Pass: used as hero art, a footer, or a cropped strip. Not tiled behind a whole page of
content.

---

## 5. Accessibility

Digital assets must meet **WCAG AA**: 4.5:1 for normal text, 3.0:1 for large text (≥18 pt,
or ≥14 pt bold). Verify with `scripts/contrast.py` rather than judging by eye.

**A1 — Text on white.**
Pass: GW Blue (11.68:1), Navy Yard (16.17:1), and Potomac (4.80:1) all clear AA at any
size. Row House is **large text only** (3.78:1).

**A2 — Text on GW Blue / Navy Yard.**
Pass: white, Gold, and the pastels all clear AA.

**A3 — Never set body text in an extended accent on white.**
This is where the brand rule is **stricter than WCAG**, and the brand rule wins. Gold on
white is 1.43:1 and effectively invisible. Green (3.11:1) and Orchid (4.97:1) would clear
the raw WCAG bar at large or any size respectively — but `DESIGN.md` §1.5 still reserves
all three for shapes, fills, and large display type on dark grounds. Do not argue a green
headline onto a white page with a contrast number.
Common failure: section headings set in OSCON Green on white because it looked fresh.

**A4 — Colour is never the only channel.**
Pass: charts, statuses, and categories carry a label, a value, or a shape in addition to
their colour.
Common failure: a pie chart whose only key is a colour legend.

**A5 — Digital pieces carry text alternatives.**
Pass: images have meaningful alt text; text lives as text, not baked into a JPEG.

---

## 6. Voice

`DESIGN.md` §5: celebratory, community-first, plainspoken. Headlines short and declarative
(Gazzetta); body copy warm and direct (Avenir Next); Source Serif italic reserved for a
single emphasised word or a quote.

Copy is design material, so it is in scope — but review it for **fit with the typographic
system**, not for style generally. Rewriting the client's message is not your job.

**V1 — Headlines are short and declarative.**
Pass: headlines are phrases, not sentences with subordinate clauses. A Gazzetta headline
that wraps to four lines is a copy problem wearing a typography costume.
Common failure: a full sentence set as a display headline, which forces the point size down
and destroys the contrast the headline existed to create.

**V2 — Body copy is warm and direct.**
Pass: plain language, active voice, second person where it fits the audience.
Common failure: institutional register ("this conference provides attendees with the
opportunity to engage") where plain speech would be shorter and warmer.

**V3 — Labels say what they are.**
Pass: buttons, captions, and eyebrows name the thing in the reader's words, and a control
says exactly what it does.

**V4 — Emphasis is rationed.**
Pass: one emphasised word per callout, not three. If everything is emphasised, nothing is.
This is the Contrast principle applied to language.

---

## Quick reference: contrast against white

| Colour | Ratio | WCAG | Brand rule (`DESIGN.md` §1.5) |
|---|---|---|---|
| Navy Yard `#00223E` | 16.17:1 | AAA any size | Text OK |
| GW Blue `#033C5A` | 11.68:1 | AAA any size | Text OK |
| Potomac `#0075C8` | 4.80:1 | AA any size | Text OK |
| Row House `#EF4343` | 3.78:1 | Large text only | Large text only |
| OSCON Orchid `#B04A8F` | 4.97:1 | AA any size | **Shapes and fills only** |
| OSCON Green `#33A56E` | 3.11:1 | Large text only | **Shapes and fills only** |
| GW Buff `#D6BF91` | 1.79:1 | Fail | Shapes and fills only |
| OSCON Gold `#FFD34D` | 1.43:1 | Fail | Shapes and fills only |

Note the two rows where the brand rule is tighter than WCAG. Passing a contrast check is
not permission to use an extended accent as text on white.

### On GW Blue

White 11.68:1, Parchment 10.13:1, OSCON Gold 8.16:1, Patina 6.63:1, GW Buff 6.52:1,
Blue Fog 6.05:1, Blossom 5.25:1 — all fine for text. Potomac (2.44:1) and Orchid (2.35:1)
are **not** legible on GW Blue; this is the most common failure in reversed panels.

Regenerate any of this with `python3 scripts/contrast.py --palette` (add `--all` for the
full matrix).
