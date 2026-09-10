# Report format

The review is a teaching document, not a scorecard. A student should finish it knowing what
to change, in what order, and *why* — well enough to avoid the same mistake unprompted next
time.

## Severity levels

Use exactly these three, and label every finding with one.

| Level | Meaning |
|---|---|
| **Must fix** | Breaks a stated brand rule in `DESIGN.md`, or fails WCAG AA. Not a matter of taste — the piece cannot ship this way. |
| **Should fix** | Breaks a design principle in a way that measurably costs the reader: hierarchy, grouping, or legibility. |
| **Consider** | A judgment call that would improve the piece. Say plainly that it is an opinion. |

Never label a personal preference "Must fix". Credibility is the whole currency of a review.

## Structure

```markdown
# Design review — <piece name>
<Medium and final size> · Reviewed <date> · Against DESIGN.md + the four design principles

## The one-line read
<What the piece is doing well and the single biggest thing holding it back. Two sentences.>

## Reading order
<The squint test result: what reads first, second, third — and whether that is right.
Two or three sentences. This frames everything below.>

## What's working
<Two or three specific things, each with WHY it works. Name the element. Generic praise
is worse than none — it reads as padding before the criticism.>

## Findings

### Must fix
**1. <Short imperative title>**
*Where:* <page / element>
*Rule:* <DESIGN.md §x, or WCAG AA, or the principle by name>
*What's happening:* <one or two sentences of diagnosis>
*Fix:* <concrete, specific, actionable — a value, not a direction>

### Should fix
...same shape, numbering continues...

### Consider
...same shape...

## If you only do three things
<The three highest-leverage changes, as a checklist. Many students will act on this
section and nothing else, so choose it carefully.>

## Checks run
<Which objective checks were run and their results — contrast pairs tested, palette audit
output. Include the numbers so the student can re-run them.>
```

## Writing the findings

**Name the element and its location.** "Page 3", "the tier table header", "the four bullets
under Who Attends". A student cannot act on a finding they cannot locate.

**Give a value, not a direction.** "More spacing" is not actionable. "Cut the space between
the bullets to 5 pt and open the gap between blocks to 18 pt" is.

**Cite the rule.** `DESIGN.md` §3 (clear space), WCAG AA, or the principle by name. This
teaches the student where to look next time, and it separates rules from your opinion.

**One finding per problem.** If the same misalignment repeats on six pages, that is one
finding that says "on every page", not six findings.

**Rank across the whole piece, not per page.** The reader wants the most important thing
first, wherever it is.

### Worked example

> **3. Section headings fail contrast on white**
> *Where:* "Who Attends?", "Why Sponsor?" and "Conference Highlights" — pages 3, 4, 5
> *Rule:* `DESIGN.md` §1.5 — never set text in OSCON Gold, Green, or Orchid on white
> *What's happening:* the headings are set in OSCON Green `#33A56E` on white, which measures
> 3.11:1. That clears WCAG only for large text, and the brand rule reserves the extended
> accents for shapes and fills regardless of size. Three different accent colours across
> three headings also breaks the repetition the section headings should be building.
> *Fix:* set all section headings in GW Blue `#033C5A` (11.68:1). If you want the accent
> colour present, put it in a small square or rule above the heading — that is a shape, which
> the accents are for, and repeating one motif across all sections is stronger than three
> different coloured headings.

Note what that example does: locates it, cites the rule, gives the measured number, explains
*two* problems (contrast and repetition), and offers a fix that keeps what the student was
reaching for.

## Length

- **What's working:** 2–3 items.
- **Findings:** 12 at the absolute maximum, and fewer is usually better. Ten findings acted
  on beat forty ignored. If you have more, the extras are symptoms of the ones you kept —
  fold them in.
- **Whole report:** should be readable in under ten minutes.

## Tone

- Address the designer, not the artefact: "you've got the hierarchy right on the cover", not
  "the cover exhibits correct hierarchy".
- Describe the effect on the reader, not your feelings: "the eye lands on the photo before
  the headline", not "I don't like the photo placement".
- No sarcasm, no sighing, no "obviously". The person reading this is learning.
- Where the draft already got something right that is genuinely hard, say so explicitly.
  Correct instincts deserve to be named so they get repeated.
- Do not soften a Must fix. Kindness is in the tone and the explanation, not in hedging
  about whether a rule was broken.

## Delivery

Write the report to a Markdown file in the working directory
(`design-review-<piece>-<YYYY-MM-DD>.md`) and send it to the user. If it is going to be
shared with a team or discussed in a meeting, offer to publish it as an artifact — but do
not publish without asking, since a review names someone's work.
