# History

How the `gw-design-review` skill came to exist, and what we learned building it. The work was
done by Lorena A. Barba with Claude, working in the Claude Code desktop app, between August and
September 2026.

## 1. It started with a prospectus (August 2026)

A student worker produced a first-pass **Sponsorship Prospectus for GW OSCON 2027** in Canva.
The content was solid — the overview, attendance figures, testimonials, tier structure, and
travel information were all there. The design was not: six crowded pages, a dark-blue
background on most of them, heavy horizontal rules chopping the layout into strips, and the
conference logo repeated on five pages.

Claude was asked to redesign it using the design specification (`DESIGN.md`) and the supplied
2027 assets: the revised logo, the modular pattern, the OSPO lockup, and a folder of event
photographs.

- **Extracting the content.** Claude read the Canva design through the in-app browser. Most text
  came from the page's text layer; the cover, the sponsorship-tier table, and the exact chart
  values were not in that layer and had to be read visually from zoomed screenshots.
- **Building the redesign.** The new prospectus was built as an HTML/CSS print document at US
  Letter size, using the brand typefaces (Gazzetta, Avenir Next, Source Serif), rendered to PDF
  with headless Chrome, and rasterized page by page for review. Photographs were cropped and
  resized for each placement.
- **The structural moves.** Six pages became eight so the density could come down. White became
  the ground, with GW Blue reserved for four deliberate bands. Thick rules were replaced by
  hairlines and a three-square motif borrowed from the logo grid. The logo appeared twice —
  cover and back cover. The charts were redrawn in the brand palette, and the pattern was
  cropped on its 210 px module so tiles break cleanly at page edges.
- **Iterating on renders.** Each round was checked against the rendered pages, which caught
  overlaps and dead space the source code did not reveal. Later rounds added the keynote
  speaker's portrait (a high-resolution black-and-white frame was chosen over a low-resolution
  colour one with an off-palette background), enlarged the body text, and reflowed every page
  to absorb the larger type.

## 2. From a fix to a lesson

Rather than simply hand back a corrected file, we wrote a short note for the student explaining
*why* the new version works, organised around the four principles in Robin Williams'
*The Non-Designer's Design Book*: **proximity, alignment, repetition, and contrast**. Each
principle was illustrated with a concrete before-and-after from the student's own document.

That note made the next step obvious: the same review, applied to any future piece of work,
would teach more students than one corrected prospectus.

## 3. Turning it into a skill (September 2026)

`DESIGN.md` was moved into this repository so it could be version-controlled, and Claude built
the `gw-design-review` skill alongside it:

- `SKILL.md` — the review procedure: establish the medium and audience, look at the piece at
  full size, run the objective checks, review brand compliance and design principles
  separately, then write the report.
- `references/` — brand checks derived from `DESIGN.md`, the four principles written against
  real failure modes, and a report format with severity levels and tone guidance aimed at
  students.
- `scripts/` — a WCAG contrast checker and a palette audit that compares the colours in a
  graphic against the brand palette.

Writing the contrast script immediately paid for itself: it showed that several contrast ratios
Claude had first computed by hand were wrong. The reference tables now carry measured values,
and they flag the two cases where `DESIGN.md` is stricter than WCAG — OSCON Green and Orchid
pass some contrast thresholds on white, but the brand rule still reserves them for shapes and
fills.

## 4. Making it usable by students

The first README assumed a command line. It was rewritten for students who use Claude Cowork,
the Claude web app, or other assistants: what the review produces, the three questions to have
answered before asking, copy-ready example prompts, and setup instructions per tool, with a
no-setup fallback that works anywhere.

## 5. Corrections along the way

Several of Claude's claims turned out to be wrong, and each was caught by a person or by
checking the evidence. They are recorded here because they shaped the final design.

- **Skills are not Claude-only.** Claude initially told students that Codex could not use the
  skill. Lorena questioned this; the documentation showed that Agent Skills is an open standard
  ([agentskills.io](https://agentskills.io)) supported by about forty tools. The skill's folder
  layout already matched the specification exactly. What differs between tools is only the
  discovery folder — Claude reads `.claude/skills/`, Codex reads `.agents/skills/`, Cursor and
  VS Code read both — so the README now gives per-tool instructions. A symlink between the two
  folders was rejected because GitHub's *Download ZIP* breaks symlinks.
- **The first student test failed.** A student uploading the skill to claude.ai got "the MD file
  must be in the top-level folder." The README had told students to download the repository
  ZIP, which nests `SKILL.md` four folders deep. The fix, committed on 11 September 2026, was a
  ready-made `gw-design-review.zip` with the correct structure, a build script that verifies
  that structure, and README instructions that no longer ask anyone to create a ZIP by hand.

## What we learned

- **Content and container are separate problems.** The student's draft did the hard part; the
  redesign changed none of the facts, only how they were arranged.
- **Crowding is usually solved with room, not graphics.** Adding pages unlocked all four design
  principles at once.
- **Measure what can be measured.** Contrast ratios and palette matches belong in scripts, not
  in judgment.
- **Check rendered output, not just source.** Most layout problems only appeared in the PDF.
- **Test with the real audience.** The most consequential bug was found by the first student who
  tried the instructions, not by any of our checks.
- **Keep a person in the loop.** The most useful corrections came from  prompts to verify rather than assert on assumptions the user did not trust.
