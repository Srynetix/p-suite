# 4. Code a person can take over

- **Status:** accepted
- **Date:** 2026-11-12
- **Deciders:** Denis Bourge

## Context and problem statement

The apps of the suite are written almost entirely by AI coding agents. Nothing so far said
what the code itself should look like: the gate checks that it builds, is formatted, passes
its lints and its tests, but not that a person could read it. Code an agent writes for the
next agent drifts in its own ways: rules that end up in views, layers that leak, comments
that narrate each change or repeat the line below them, choices explained nowhere but in a
conversation that is gone.

The author wants each app to stay one that a person could take over and develop by hand. What
does the code have to be for that, and where is the knowledge a person needs kept?

## Decision

**The code follows Clean Code and Clean Architecture as far as the app allows, keeps only the
comments that say why, and every app documents how it is built in `docs/dev/`.**
SUITE.md §12 states the rules, §13 the documentation.

1. **Clean Architecture**: a core that holds the domain and knows nothing of the platform;
   dependencies that point inward, enforced by the compiler where the language allows; a UI
   that holds no rule; platform code confined behind interfaces; a core tested without the
   platform. Layers are earned: a small app may have only a core and a shell.
2. **Clean Code**: names in the domain's words, functions that do one thing, visible effects,
   no swallowed error, no magic value, no dead code, tests that read like specifications.
3. **Comments say why** a reader could not guess: a constraint, a surprising choice, a
   workaround, the ADR behind it. None repeats the code or narrates its history. Doc comments
   document contracts across module boundaries.
4. **`docs/dev/`** holds, in every app, a starting point (`README.md`), the architecture
   (`architecture.md`) and the patterns used (`patterns.md`), kept true in the same commit as
   the code. Where an app departs from §12, `architecture.md` says where and why.

`just audit` checks that the documents exist and that the README links them. Whether the code
follows the rules is a matter for review: the author's, and the agent's own before it calls a
change done (SUITE.md §7).

## Options considered

### Clean Code and Clean Architecture, with developer docs — chosen

Well-known references, so a person taking an app over shares the vocabulary, and so do the
agents: both books are part of what they were trained on. The direction of the dependencies
is what makes a core testable and a platform replaceable, which the apps need anyway (Pavé's
`PaveCore`, Pastille's Rust core under three front ends). The cost is review: most of these
rules cannot be checked by a machine.

### Leave the code to the gate — rejected

Formatting, lints and tests are checked already. Rejected: they say nothing of where a rule
lives or why a choice was made, which is what a person taking over needs first.

### Document in comments rather than in `docs/dev/` — rejected

The explanation would sit next to the code it explains. Rejected: comments explain a line,
not how modules fit together; long comments rot unseen, and agents tend to write too many of
them. A short comment pointing to a document keeps both readable.

### A stricter rule set, checked by a tool — rejected for now

Architecture linters and complexity thresholds exist for some of the languages. Rejected for
now: the apps use Rust, Swift and TypeScript, and a threshold right for one is wrong for
another. An app adds such a check to its `just ci` when it pays, as Pastille does for its
boundary.

## Consequences

1. **Every app gains a `docs/dev/`**, from the templates, and `just audit` reports the apps
   without one. Writing it for an existing app is a task of its own, per app.
2. **Pavé's README** holds a long *Development* section: it moves to `docs/dev/`, and the
   README keeps a link.
3. **Existing code is brought in line as it is touched**, not in one rewrite. A change to a
   part of the code leaves that part following §12.
4. **Reviews have more to look at**, and `AGENTS.md` points an agent to §12 and `docs/dev/`
   before it writes code.
