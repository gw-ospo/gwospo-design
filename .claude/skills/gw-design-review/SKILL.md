---
name: gw-design-review
description: Review a graphic design — poster, flyer, slide deck, prospectus, report, social graphic, banner, or web page — against the GW brand guidelines, the OSCON extended palette, and the four design principles (proximity, alignment, repetition, contrast), then issue a structured report with prioritized fixes. Use whenever someone asks to review, critique, check, audit, or give feedback on a design, layout, poster, flyer, deck, or asks whether something is on brand for GW OSPO or GW OSCON.
compatibility: Works in any Agent Skills client. The Python 3 helper scripts are optional — palette_audit.py needs Pillow, and rendering PDFs needs one of pdftoppm, Ghostscript, pypdfium2, or PyMuPDF. The review still works without them.
metadata:
  author: GW Open Source Program Office
  version: "1.1"
---

# GW design review

Produce a written review of a piece of graphic design: what works, what breaks a brand
rule, what breaks a design principle, and exactly what to change. The reader is usually a
student worker who is learning, so the report has to teach, not just grade.

## Before you start

Three facts shape almost every judgment that follows. Work them out from the file and the
request first:

1. **Medium and size.** Print (trim size, bleed), slide deck, web page, social post,
   roll-up banner. Page dimensions, pixel size, and aspect ratio usually settle it. Minimum
   type sizes, contrast tolerances, and margin advice all depend on this.
2. **Audience and the one action.** A sponsorship prospectus, a call for papers, and a
   schedule poster fail in different ways. The content usually makes this clear.
3. **OSCON or general GW OSPO work.** This decides whether the OSCON extended accents (Gold,
   Green, Orchid) are allowed at all — they are OSCON-only, never university colours.

Ask only about what the file and request leave open. State what you inferred in the report
header, so the student can correct a wrong assumption.

## Step 1 — Look at it properly

Review the piece at a size where its smallest text is readable; most layout problems only
show up in rendered output. Use whatever your client provides to get there:

- **PDF** — render each page to an image with `scripts/rasterize.py design.pdf` (see the
  table in Step 2). For fine detail such as captions or the logo's clear space, re-render at
  `--dpi 300` and look at a crop.
- **Image** — view it directly.
- **Web page or HTML** — open it in a browser and capture it at a desktop width (about
  1440 px) and a mobile width (about 390 px). If the page follows the system light/dark
  setting, capture both.
- **Canva, Figma, or Google Slides link** — open it in a browser, page through it, and
  extract the text layer where possible so you quote the copy accurately. Covers, tables
  drawn as graphics, and chart values are often missing from the text layer and have to be
  read from zoomed screenshots.

In Claude Code, for example, the Read tool views images and PDF pages and the built-in
browser handles web pages and design-tool links. If you have no way to view the piece, ask
for a PDF or PNG export rather than reviewing from a description.

Then do the **squint test**: view the whole page small, as a thumbnail. Write down what
reads first, second, third. If that order is not the order the message needs, that is your
headline finding and everything else is detail.

## Step 2 — Run the objective checks

Contrast ratios and palette matches are measurable, and estimates by eye are often wrong —
several ratios in this skill's own tables were wrong until a script measured them. Report
the numbers.

The scripts are in this skill's `scripts/` folder, so paths are relative to the skill's own
directory, not the user's. If your client shows the skill's base directory when it loads,
use that; otherwise find it:

```bash
SKILL=$(dirname "$(find . ~/.claude/skills ~/.agents/skills -maxdepth 6 -name SKILL.md -path '*gw-design-review*' 2>/dev/null | head -1)")
```

| Command | What it does | Needs |
|---|---|---|
| `python3 "$SKILL/scripts/rasterize.py" design.pdf [--pages 2-4] [--dpi 300]` | Renders PDF pages to PNGs and prints their paths, named by page number | One of pdftoppm, Ghostscript, pypdfium2, PyMuPDF |
| `python3 "$SKILL/scripts/contrast.py" "#FFD34D" "#FFFFFF"` | WCAG contrast for one foreground/background pair | Nothing |
| `python3 "$SKILL/scripts/contrast.py" --palette [--all]` | The whole brand palette against the usual grounds (or every pair) | Nothing |
| `python3 "$SKILL/scripts/palette_audit.py" design.png` | Dominant flat colours matched against the brand palette; also accepts a PDF | Pillow |

If the project has a `DESIGN.md`, add `--design path/to/DESIGN.md` to `contrast.py` and
`palette_audit.py` so they use its palette; both print which palette they used.

Run `palette_audit.py` on graphics rather than photographs — photographic content is exempt
from the palette, and the script's output says so.

If a script is missing a dependency, its error message names what to install. If nothing
can be installed in your environment, continue without that check and list it as not run
under "Checks run" in the report.

## Step 3 — Check brand compliance

Read `references/brand-checks.md` and work through it. It covers colour, typography, logo
usage, the pattern, accessibility, and voice as numbered checks with pass conditions. Each
check is tagged with its source — `DESIGN.md`, WCAG, or house practice — and only the first
two can make a finding Must fix.

**If the project contains its own `DESIGN.md`, that file is the source of truth.** Read it
and re-derive any value that disagrees with the reference. The reference exists so the
skill still works outside this repository.

## Step 4 — Check the four principles

Read `references/design-principles.md`. This is Robin Williams' framework from *The
Non-Designer's Design Book* — proximity, alignment, repetition, contrast — written against
the kinds of mistakes that show up in GW OSPO work.

Brand compliance and design principles are independent. A piece can be perfectly on-palette
and still unreadable, and a beautifully composed layout can still break the logo rules.
Check both.

## Step 5 — Write the report

Read `references/report-format.md` for the structure, the severity levels, and the tone.
Deliver the report as a Markdown file unless the user asks for something else; if your
client can publish shareable pages, offer that when the report is going to be shared.

## Ground rules

- **Lead with what works, and mean it.** Name two or three specific things that are
  genuinely good and say why they work. A student who only receives corrections learns to
  fear the review instead of using it.
- **Every finding names the element, the location, the rule, and the fix.** "Feels
  cluttered" is not a finding. "The four bullets on page 3 sit at the same 12 pt spacing as
  the gap between sections, so the groups do not read as groups — tighten the bullets to
  5 pt and open the section gap to 18 pt" is a finding.
- **Rank and cap the list.** Three strengths, then findings ordered by severity. Ten
  findings that get acted on beat forty that get ignored.
- **Keep brand rules and judgment apart.** If `DESIGN.md` does not cover something, say so
  and label it house practice or a judgment call rather than a violation — students learn
  to discount a reviewer who presents taste as rules.
- **Describe the change; leave the rebuilding to them.** The report says what to change
  and why. Rebuilding the file is a separate request, and doing it uninvited takes away the
  learning.
- **Quote the rule.** When you cite a brand requirement, name it (`DESIGN.md` §3, clear
  space) so the student can go read the source.
