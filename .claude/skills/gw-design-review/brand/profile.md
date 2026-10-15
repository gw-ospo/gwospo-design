# Brand profile — GW OSPO and GW OSCON

Who this brand is for, and what the review needs to know about it before it starts.

## Institution

The George Washington University (GW), Open Source Program Office (OSPO). The brand is the
GW refreshed brand (2026 guidelines), with an extended palette for the GW Open Source
Conference (OSCON).

## Contexts

Every piece belongs to one context, and the context decides which colours are allowed:

| Context | Covers | Palette |
|---|---|---|
| **GW OSCON** | The conference, e.g. call for papers, schedule, sponsorship prospectus, signage, slides, social posts | Core, pastels, and the OSCON extended accents (Gold, Green, Orchid) |
| **General GW OSPO** | Everything else the office makes, e.g. reports, workshop and event flyers, web pages | Core and pastels only. The extended accents are OSCON-only (`DESIGN.md` §1.4) |

Signs that a piece is OSCON: the conference name or year, the OSCON logo, or the pattern.
Do not count the extended accents as a sign — a general OSPO piece using them is exactly the
mistake check C5 exists to catch. If none of these settles it, ask.

## Who reads the review

Usually a student worker in the office who is learning design. The report has to teach,
not just grade, so findings explain why as well as what.

## Brand files

| File | What it is |
|---|---|
| `brand/DESIGN.md` | The design specification and the source of truth for brand rules. Cite it as `DESIGN.md` §x. |
| `brand/palette.json` | The colours from `DESIGN.md` §1 in machine-readable form. The scripts read it; it must match `DESIGN.md`. |
| `references/brand-checks.md` | Testable checks derived from `DESIGN.md`, each tagged with its source. |

If the project being reviewed has its own `DESIGN.md`, that file overrides `brand/DESIGN.md`.
