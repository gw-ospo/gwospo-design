---
name: gw-design-review
description: Review a graphic design — poster, flyer, slide deck, prospectus, report, social graphic, banner, or web page — against the GW brand guidelines, the OSCON extended palette, and the four design principles (proximity, alignment, repetition, contrast), then issue a structured report with prioritized fixes. Use whenever someone asks to review, critique, check, audit, or give feedback on a design, layout, poster, flyer, deck, or asks whether something is on brand for GW OSPO or GW OSCON.
compatibility: Works in any Agent Skills client. The two Python 3 helper scripts are optional; palette_audit.py needs Pillow. The review still works without them.
metadata:
  author: GW Open Source Program Office
  version: "1.0"
---

# GW design review

Produce a written review of a piece of graphic design: what works, what breaks a brand
rule, what breaks a design principle, and exactly what to change. The reader is usually a
student worker who is learning, so the report has to teach, not just grade.

## Before you start

Establish three things. If the user has not said, ask — the answers change almost every
judgment that follows.

1. **What is it and where does it live?** Print (what trim size? bleed?), slide deck
   (16:9 at 1920×1080?), web page, Instagram post, roll-up banner. Minimum type sizes,
   contrast tolerances, and margin advice all depend on this.
2. **Who is it for and what is the one action?** A sponsorship prospectus, a call for
   papers, and a schedule poster fail in different ways.
3. **Is this OSCON or general GW OSPO work?** The OSCON extended accents (Gold, Green,
   Orchid) are OSCON-only and must never be presented as university colours.

## Step 1 — Look at it properly

You cannot review what you have not seen at full size.

- **PDF** — `Read` with the `pages` parameter. For finer detail, rasterize into the
  scratchpad first: `gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r150 -sOutputFile=p%d.png in.pdf`
  (or `pdftoppm -r 150 -png in.pdf p`).
- **Image** — `Read` it directly.
- **Web page or HTML** — open it in the browser pane, screenshot at a real desktop width,
  then again at mobile width. Check both themes if the page is theme-aware.
- **Canva, Figma, Google Slides link** — open in the browser pane, page through it, and
  pull the copy with `get_page_text` so you can quote it accurately.

Then do the **squint test**: view the whole page small, as a thumbnail. Write down what
reads first, second, third. If that order is not the order the message needs, that is your
headline finding and everything else is detail.

## Step 2 — Run the objective checks

Do not eyeball these. Report numbers.

Paths below are relative to **this skill's own directory**, not the user's working
directory. If a bare `scripts/contrast.py` is not found, locate the skill first:

```bash
SKILL=$(dirname "$(find . ~/.claude/skills ~/.agents/skills -name SKILL.md -path '*gw-design-review*' 2>/dev/null | head -1)")
python3 "$SKILL/scripts/contrast.py" --palette
```

```bash
# WCAG contrast for a specific pair, plus the whole brand palette as a matrix
python3 scripts/contrast.py "#FFD34D" "#FFFFFF"
python3 scripts/contrast.py --palette

# Colours actually present in a graphic, matched against the brand palette
python3 scripts/palette_audit.py path/to/design.png
```

`palette_audit.py` needs Pillow (`pip install Pillow`). Run it on graphics, not on
photographs — photographic content is exempt from the palette, and the script says so.

## Step 3 — Check brand compliance

Read `references/brand-checks.md` and work through it. It covers colour, typography, logo
usage, the pattern, accessibility, and voice as numbered checks with pass conditions.

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

Read `references/report-format.md` for the exact structure, the severity levels, and the
tone. Deliver the report as a Markdown file in the working directory unless the user asks
for something else; offer to publish it as an artifact if it is going to be shared.

## Ground rules

- **Lead with what works, and mean it.** Name two or three specific things that are
  genuinely good and say why they work. A student who only receives corrections learns to
  fear the review instead of using it.
- **Every finding names the element, the location, the rule, and the fix.** "Feels
  cluttered" is not a finding. "The four bullets on page 3 sit at the same 12 pt spacing as
  the gap between sections, so the groups do not read as groups — tighten the bullets to
  5 pt and open the section gap to 18 pt" is a finding.
- **Rank ruthlessly and cap the list.** Three strengths, then findings ordered by severity.
  Ten findings that get acted on beat forty that get ignored.
- **Never invent a brand rule.** If `DESIGN.md` does not cover something, say so and label
  it a judgment call, not a violation.
- **Do not redesign it for them.** The report tells them what to change and why. Rebuilding
  the file is a separate request — and doing it uninvited takes away the learning.
- **Quote the rule.** When you cite a brand requirement, name it (`DESIGN.md` §3, clear
  space) so the student can go read the source.
