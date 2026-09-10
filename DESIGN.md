# GW OSCON 2027 — Design Specification

Visual system for the GW Open Source Conference 2027, built on the refreshed George Washington University brand (2026 guidelines) with an OSCON-specific extended accent palette. OSCON is a celebration of the open source community: assets should feel vibrant and energetic while staying unmistakably GW.

## 1. Color

### 1.1 Core (GW brand, verbatim)
| Name | Hex | Role |
|---|---|---|
| GW Blue | #033C5A | Primary anchor: wordmarks, headlines, dark shapes |
| Navy Yard | #00223E | Darkest tone: backgrounds, small dark shapes |
| Potomac | #0075C8 | Vivid blue accent: workhorse mid color |
| Row House | #EF4343 | Vivid red accent |
| White | #FFFFFF | Breathing room, knockout shapes |
| GW Buff | #D6BF91 | Warm neutral, formal contexts only |

### 1.2 OSCON extended accents (derived)
The refreshed brand's Parchment, Patina and Blossom are pastels. For OSCON's celebratory mood they are deepened to secondary-level chroma — same hue, boosted saturation and lowered value — mirroring how the 2025 identity extended the old palette (its invented purple #7337AA filled the red–blue hue gap at secondary saturation).

| Name | Hex | Derived from |
|---|---|---|
| OSCON Gold | #FFD34D | Parchment #FFEFAE, deepened |
| OSCON Green | #33A56E | Patina #ADCAB8, deepened |
| OSCON Orchid | #B04A8F | Blossom #D1A0B9, deepened |

### 1.3 Working palette (7 slots)
GW Blue · Potomac · Row House · OSCON Gold · OSCON Green · OSCON Orchid · White.
This is the set used in the 2027 logo squares and website pattern.

### 1.4 Usage rules
- Lead with GW Blue and white; extended accents are supporting players, never the dominant field of a whole composition (per GW "expressive spectrum" guidance).
- Max ~2 accent hues adjacent; separate saturated fields with white or GW Blue where a layout gets busy.
- The extended accents (Gold, Green, Orchid) are OSCON-only — never present them as university colors.
- Pastel originals (Parchment #FFEFAE, Patina #ADCAB8, Blossom #D1A0B9, Blue Fog #52C9E8, Buff tints) remain available for large quiet backgrounds and tints.

### 1.5 Accessibility (WCAG AA)
- Text on white: GW Blue, Navy Yard, Potomac ✓ (all sizes); Row House large-text only.
- Text on GW Blue / Navy Yard: white, Gold, and pastels ✓.
- Never set body text in OSCON Gold, Green, or Orchid on white; use them for shapes, fills, and large display type on dark grounds only after checking contrast.
- Digital assets must meet AA per GW accessibility standards.

## 2. Typography (GW refreshed brand)
Three brand typefaces (all on Adobe Fonts):

- **Gazzetta** (variable) — headlines and key marketing moments; bold, newspaper-inspired. Short headlines/phrases only. OSCON use: event titles, session-track names, big numerals ("2027").
- **Avenir Next** — primary sans; body copy, subheads, captions, call-outs, UI text.
- **Source Serif** — sparing emphasis: italic headline emphasis words, short callouts, pull quotes.

Rules:
- Pair two typefaces per asset (three permissible, never required); mix weights for visual interest.
- Web fallbacks: Gazzetta → 'Gazzetta', 'Arial Narrow', sans-serif (condensed); Avenir Next → 'Avenir Next', 'Avenir', 'Segoe UI', sans-serif; Source Serif → 'Source Serif 4', Georgia, serif.
- Suggested scale (1920×1080 slides): Gazzetta display 96–160; Avenir Next subhead 36–48; body 24–28 (never below 24); captions 24.
- Headline color: GW Blue on light grounds; white or Gold on GW Blue/Navy Yard.

## 3. Logo
- File: `GW_OSCON_horizontal_extended_2027.svg` (PNG: `GW_OSCON_horizontal_extended_2027.png`, 2160×792).
- Structure: 2×3 tile grid — GW monogram + "2027" square in GW Blue, five glyph squares (Potomac, Row House, Gold, Orchid, Green) with white knockout shapes — beside the "OPEN SOURCE CONFERENCE" wordmark in GW Blue.
- Knockouts are transparent: place on white or very light grounds only. A reversed/dark-ground variant does not exist yet.
- Clear space: at least one tile-width (the grid square) on all sides; minimum width ~200 px on screen.

## 4. Pattern
- File: `GW_OSCON_pattern_2027_B_extended.svg` (PNG: `GW_OSCON_pattern_2027_B_extended.png`, 4195×1680).
- 210 px modular tile grid (circles, half-rounds, diamonds, quarter-round leaves, S-curves, triangles, sparkles) using the 7-slot working palette.
- Use as banner/hero art, footers, or cropped strips; keep type off the pattern or on a solid panel over it. Tiles crop cleanly on the 210 px module.

## 5. Voice
Celebratory, community-first, plainspoken. Headlines short and declarative (Gazzetta); body copy warm and direct (Avenir Next); reserve Source Serif italic for a single emphasized word or a quote.
