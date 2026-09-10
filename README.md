# gwospo-design

Graphic design materials for the George Washington University Open Source Program Office.

| What | It is |
|---|---|
| [`DESIGN.md`](DESIGN.md) | Our design specification — the GW brand colours and typefaces, plus the OSCON palette, logo, and pattern rules. If you make anything for OSPO or OSCON, this is the rulebook. |
| [`.claude/skills/gw-design-review/`](.claude/skills/gw-design-review/) | A design reviewer you can run on your own work before anyone else sees it. |

---

## Get your design reviewed

Made a poster, flyer, slide deck, social graphic, one-pager, or web page? You can have it
reviewed against our brand guidelines in a few minutes, by yourself, as many times as you
like. Nobody is watching, and there's no wrong answer — that's the point of using it early.

**You'll get back a written report with:**

- Two or three things that are genuinely working, and why
- What reads first, second, and third when someone glances at your page — and whether
  that's the order you wanted
- A ranked list of things to change, each one saying where the problem is, which rule it
  relates to, and exactly what to do about it

Findings come in three flavours, so you know what's urgent:

| | |
|---|---|
| **Must fix** | Breaks a brand rule or an accessibility requirement. Not a matter of taste. |
| **Should fix** | Makes the piece harder to read than it needs to be. |
| **Consider** | A suggestion. Take it or leave it. |

### Before you ask, have three answers ready

The reviewer will ask you these, because the advice genuinely changes depending on them:

1. **What is it, and where will it end up?** A printed 11×17 poster, a 16:9 slide, an
   Instagram post, a web page. Type that's fine on a poster is illegible on a phone.
2. **Who is it for, and what should they do after seeing it?** Submit a talk, sponsor the
   conference, show up on a date.
3. **Is this OSCON, or general OSPO?** OSCON has three extra accent colours that aren't
   allowed on other GW work.

### Then just ask

Attach your file — a PDF, a PNG or JPG, or a link to your Canva design — and say something
like:

> Review this poster against our brand guidelines. It's a printed 11×17 for the OSCON call
> for papers.

> Is this deck on brand? It's a 16:9 slide deck for an OSPO talk to university leadership.

> Here's my Instagram graphic for OSCON — what would you change?

---

## Setting it up

This reviewer is an **Agent Skill** — an open format that most AI tools now understand. You
can use it in Claude, ChatGPT/Codex, Cursor, VS Code with Copilot, and around forty other
tools. The only thing that differs between them is which folder they look in.

**Step one, whichever tool you use:** download this repository. Click the green **Code**
button at the top of the GitHub page, then **Download ZIP**, and unzip it somewhere you'll
find again — your Documents folder is fine.

Then find your tool below.

| If you use… | What to do |
|---|---|
| **Claude Cowork**, the **Claude desktop app**, or **Claude Code** | Nothing. Point Claude at the unzipped folder and the reviewer is already there. |
| **Cursor**, or **VS Code with Copilot** | Nothing. Both read the same folder Claude uses. Open the unzipped folder and it's available. |
| **ChatGPT or Codex** | One extra step — see just below. |
| **claude.ai in a browser** | Upload it to your account — see below. |
| **Anything else** | Use the no-setup method at the bottom. It works everywhere. |

### ChatGPT and Codex

Codex looks in a folder called `.agents/skills` instead. Copy the reviewer there once:

1. In the unzipped folder, open `.claude/skills` and copy the `gw-design-review` folder.
2. Make a folder called `.agents` at the top level of the unzipped folder, and a folder
   called `skills` inside it.
3. Paste `gw-design-review` into `.agents/skills`.

Folders starting with a dot are hidden on a Mac — press
<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> in Finder to show them.

If you'd rather have it available in every project, put the folder in `.agents/skills`
inside your home folder instead.

### claude.ai in a browser

Skills can be added to your account, and then they work in any conversation.

1. In the unzipped folder, find `.claude/skills/gw-design-review`.
2. Compress **that folder** into its own ZIP file — right-click it and choose *Compress*.
3. In Claude's **Settings**, find **Capabilities → Skills** and upload that ZIP.

The menu wording moves around from time to time — look for anything called **Skills**.

### No setup at all — works in any AI tool

You don't have to install anything. The instructions are just text files, so you can hand
them over directly.

Attach these files to your conversation, along with your design:

- `DESIGN.md`
- `.claude/skills/gw-design-review/references/brand-checks.md`
- `.claude/skills/gw-design-review/references/design-principles.md`
- `.claude/skills/gw-design-review/references/report-format.md` — optional, but it's what
  keeps the report useful and specific rather than a list of complaints

Then ask:

> Review my design against the brand checks and design principles in these files. Give me a
> report with what's working, then a ranked list of fixes labelled Must fix / Should fix /
> Consider.

The one thing you lose this way is the automatic colour-contrast measurement, so if a colour
looks borderline, check it yourself at
[WebAIM's contrast checker](https://webaim.org/resources/contrastchecker/).

---

## A few things worth knowing

**Ask early, not at the end.** A review is most useful while things are still easy to move.
Running it on a half-finished draft is a completely normal thing to do.

**It won't redesign your work.** It tells you what to change and why, and then stops. That's
deliberate — you learn more fixing it yourself, and it's your design.

**If it's wrong, say so.** It can misread a layout, especially in a screenshot. Push back
and ask it to look again.

**Two separate things get checked.** Whether you followed the brand rules, and whether the
layout communicates. You can pass one and fail the other — a page can be perfectly on-palette
and still impossible to read.

**The four principles** it checks against — proximity, alignment, repetition, contrast — come
from Robin Williams' *The Non-Designer's Design Book*. It's short and non-technical, and
reading it is the best few hours you can spend if you'd like to stop needing the reviewer.

---

## For maintainers

`DESIGN.md` is the source of truth. The skill keeps a working copy of the brand values in
`references/brand-checks.md` so reviews still work in a folder that has no `DESIGN.md`, and
it is instructed to prefer a project's own `DESIGN.md` wherever the two disagree.

When `DESIGN.md` changes, check `references/brand-checks.md` for values that need to follow
— and if a *rule* changes rather than a value, update the check, not just the number.

### Why the skill lives in `.claude/skills/`

The skill follows the [Agent Skills specification](https://agentskills.io/specification) —
`SKILL.md` with `name`/`description` frontmatter, plus `scripts/`, `references/`, and
`assets/` — so it is portable across clients. What is *not* standardised is the discovery
directory, and as of September 2026 the clients differ:

| Client | Reads |
|---|---|
| Claude Code / desktop / Cowork | `.claude/skills/` only |
| ChatGPT / Codex | `.agents/skills/` (repo and `~/.agents/skills`) |
| Cursor | `.agents/skills/`, `.cursor/skills/`, and `.claude/skills/` |
| VS Code / Copilot | `.agents/skills/`, `.github/skills/`, and `.claude/skills/` |

There is no single folder every client reads, so the canonical copy sits in
`.claude/skills/` — the primary audience here is Claude Cowork — and the README tells Codex
users to copy it into `.agents/skills/`.

Do **not** solve this with a symlink. GitHub's *Download ZIP* converts symlinks into plain
text files containing the target path, and downloading the ZIP is the route this README
sends non-technical users down. If `.agents/skills/` ever needs to work out of the box,
commit a second real copy and add a check that the two stay identical.

<details>
<summary>Using it from the command line</summary>

Claude Code discovers the skill automatically when started inside the repository:

```bash
git clone https://github.com/gw-ospo/gwospo-design.git
cd gwospo-design
claude
```

To make it available in any folder, link it into your personal skills directory:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/.claude/skills/gw-design-review" ~/.claude/skills/gw-design-review
```

A symlink stays current as this repository is updated; use `cp -R` to pin a copy instead.

The two checkers are plain Python and are useful on their own. Claude runs them for you
during a review, so you only need these if you want a number quickly:

```bash
cd .claude/skills/gw-design-review

# WCAG contrast for one pair, or the whole palette against the usual backgrounds
python3 scripts/contrast.py "#FFD34D" "#033C5A"
python3 scripts/contrast.py --palette

# Which colours are actually in a graphic, matched against the brand palette
python3 scripts/palette_audit.py ~/Desktop/poster.png
```

`contrast.py` has no dependencies. `palette_audit.py` needs Pillow (`pip install Pillow`)
and should be run on graphics rather than photographs — photographic content is exempt from
the palette, and the script says so in its output.

</details>
