# Report format

The review is a teaching document, not a scorecard. A student should finish it knowing what
to change, in what order, and *why* — well enough to avoid the same mistake unprompted next
time.

## Severity levels

Use exactly these three, and label every finding with one.

| Level | Meaning |
|---|---|
| **Must fix** | Breaks a stated brand rule in `DESIGN.md`, or fails WCAG AA — a check tagged `[DESIGN.md §x]` or `[WCAG x.x.x]` in `brand-checks.md`. Not a matter of taste — the piece cannot ship this way. |
| **Should fix** | Breaks a design principle in a way that measurably costs the reader (hierarchy, grouping, or legibility), or fails a `[House practice]` check. |
| **Consider** | A judgment call that would improve the piece. Say plainly that it is an opinion. |

A house-practice check never makes a finding Must fix, however confident you are. If
something feels like it should be a rule and `DESIGN.md` is silent, say so in the finding;
the fix for that is adding it to `DESIGN.md`, not stretching an existing rule. Credibility is
the whole currency of a review.

## Structure

```markdown
# Design review — <piece name>
<Medium and final size> · Reviewed <date> · Against DESIGN.md + the four design principles
<Anything you inferred rather than were told — medium, audience, OSCON vs general OSPO —
in one line, e.g. "Assumed: US Letter print, sponsor audience, OSCON." Omit if all stated.>

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
output. Include the numbers so the student can re-run them. List any check that could not
run, and why (for example, Pillow unavailable), so its absence is not read as a pass.>
```

## Writing the findings

**Name the element and its location.** "Page 3", "the tier table header", "the four bullets
under Who Attends". A student cannot act on a finding they cannot locate.

**Give a value, not a direction.** "More spacing" is not actionable. "Cut the space between
the bullets to 5 pt and open the gap between blocks to 18 pt" is.

**Cite the rule.** `DESIGN.md` §3 (clear space), WCAG AA (1.4.3), the principle by name,
or "house practice" with the check ID. Quote the rule as `DESIGN.md` actually words it, not
a stronger paraphrase. This teaches the student where to look next time, and it separates
rules from your opinion.

**One finding per problem.** If the same misalignment repeats on six pages, that is one
finding that says "on every page", not six findings.

**Rank across the whole piece, not per page.** The reader wants the most important thing
first, wherever it is.

### Worked examples

The same pages produce two findings at different severities, because one breaks a
requirement and the other is house practice.

> **2. Section heading on page 3 is unreadable**
> *Where:* the "Who Attends?" heading, page 3
> *Rule:* WCAG AA contrast (1.4.3) — required for digital assets by `DESIGN.md` §1.5
> *What's happening:* the heading is set in OSCON Gold `#FFD34D` on white, which measures
> 1.43:1. That is far below 3:1, the minimum even for large text, so on most screens the
> heading barely shows.
> *Fix:* set it in GW Blue `#033C5A` (11.68:1), and see finding 6 for the other headings.

> **6. Section headings change colour from page to page**
> *Where:* "Why Sponsor?" (OSCON Green, page 4) and "Conference Highlights" (OSCON Orchid,
> page 5), alongside the Gold heading in finding 2
> *Rule:* Repetition, plus house practice (brand-checks A3) — not a `DESIGN.md` rule
> *What's happening:* both pass WCAG at this size (Green 3.11:1 as large text, Orchid
> 4.97:1), so neither breaks a rule. But three accent colours across three headings break the
> repetition the headings should be building: the reader cannot learn "this colour means a
> new section".
> *Fix:* set all section headings in GW Blue. If you want the accent colour present, put it
> in a small square above each heading — a shape, which is where `DESIGN.md` §1.5 points the
> accents — and use the same square in every section.

Note what these do: each locates the problem and cites its source. The Must fix rests on a
measured number against a stated requirement. The Should fix says outright that it is
house practice. And the fix keeps what the student was reaching for.

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

Write the report as a Markdown file named `design-review-<piece>-<YYYY-MM-DD>.md` — in
the working directory if you have one, otherwise as a downloadable file — and give it to
the user. If it is going to be shared with a team or discussed in a meeting and your client
can publish shareable pages, offer that, but ask first: a review names someone's work.
