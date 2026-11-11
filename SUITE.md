# The P suite

Apps whose name starts with a P, built almost entirely by AI coding agents under one author's
direction: [Prism](https://github.com/Srynetix/prism), [Pavé](https://github.com/Srynetix/pave)
and [Pastille](https://github.com/Srynetix/pastille) so far.

The apps share nothing at runtime and need not share a language. What they share is **the way
they are made**: the same commands, the same gate, the same kind of README, the same release.
An agent that has worked on one finds its way in the next without being told, and that is the
point: every convention here is written so an agent can follow it, and checked so nobody has
to remember it.

This file says **what** the conventions are. [`templates/`](templates) holds the files that
carry them into an app. When an app and this file disagree, the app is the one to change, or
this file, on purpose, with a word on why.

Words used below: **must** is checked or expected of every app; **should** is the default,
and an app departing from it says why in an ADR.

---

## 1. Names

- The app's **name** starts with a P and is a word, often French: Prism, Pavé, Pastille. It
  keeps its accents wherever a person reads it: the README, the window, the release title.
- Its **slug** is the name in lowercase ASCII: `prism`, `pave`, `pastille`. It names the
  repository, the binary, the bundle, the release tag, and the prefix of every environment
  variable the app reads (`PAVE_SIGN_KEY`, `PASTILLE_RELEASE_TO`).
- The repository is `github.com/Srynetix/<slug>`.

## 2. The repository

Every app **must** have, at its root:

| File | What it is | Template |
|---|---|---|
| `README.md` | What the app is, for someone who has never heard of it (§6) | [README.md](templates/README.md) |
| `AGENTS.md` | The contract an agent works under (§3) | [AGENTS.md](templates/AGENTS.md) |
| `CLAUDE.md` | One line: `@AGENTS.md` | [CLAUDE.md](templates/CLAUDE.md) |
| `CONTRIBUTING.md` | How to report, propose and change | [CONTRIBUTING.md](templates/CONTRIBUTING.md) |
| `SECURITY.md` | How to report privately, what is supported, what the app does with data | [SECURITY.md](templates/SECURITY.md) |
| `LICENSE-MIT`, `LICENSE-APACHE` | The licence (§9) | [LICENSE-MIT](templates/LICENSE-MIT), [LICENSE-APACHE](templates/LICENSE-APACHE) |
| `justfile` | Every command (§4) | [justfile](templates/justfile) |
| `.editorconfig` | What every editor does to every file | [.editorconfig](templates/.editorconfig) |
| `docs/adrs/` | Every technical decision (§5) | [docs/adrs/](templates/docs/adrs) |
| `docs/screenshots/` | What the README shows | — |
| `scripts/release.sh`, `scripts/changelog.sh` | The release (§8) | — |
| `scripts/check-commits.sh` | Conventional Commits, checked (§8) | [check-commits.sh](templates/scripts/check-commits.sh) |

The justfile is spelled `justfile`, in lowercase, like the slug.

Files of an agent's **local** state are git-ignored: `.claude/settings.local.json`,
`.claude/launch.json`, worktrees. What every agent should share (`AGENTS.md`, shared skills in
`.claude/skills/`, a shared `.claude/settings.json`) is committed. Never ignore `.claude/` as a
whole.

## 3. Agents

The code is written by agents; the contract they work under is versioned with it.

- **`AGENTS.md` is the contract**, tool-neutral, committed. `CLAUDE.md` imports it and adds
  nothing, so every agent reads the same rules.
- It says, in this order: what the app is in two lines, where things are, the commands, the
  definition of done (§7), the rules, and what an agent must ask before doing.
- **It is short.** What a reader of the code would need anyway goes in the README, the ADRs or a
  comment; `AGENTS.md` points to it rather than repeating it.
- **A mistake an agent made twice becomes a rule** in `AGENTS.md`, or better a check in
  `just ci`. A rule a check can enforce belongs in the check.
- The author directs, reviews, tests on real machines and decides what ships. An agent never
  publishes a release, pushes a tag, or adds a dependency without being asked.

## 4. Commands

Every app is driven through `just`, and these recipes **must** exist with these names and these
meanings, whatever the language behind them:

| Recipe | Does | Fails when |
|---|---|---|
| `just` | Lists the recipes (`@just --list --unsorted`) | — |
| `just doctor` | Lists the tools this machine needs, with their versions | One is missing |
| `just install` | Installs the dependencies | — |
| `just dev` | Runs the app from source, rebuilding what it needs | — |
| `just fmt` | Formats everything in place | — |
| `just check` | The fast static checks: format, lint, types | Any of them |
| `just test` | Every test | One fails |
| `just ci` | **The gate** (§7): `check`, `test`, and every slower check | Anything does |
| `just build` | A release build of the app for this machine | — |
| `just changelog` | Prints the notes of the next release | — |
| `just release` | Publishes a release (§8) | Its checks fail |

An app adds what it needs beside them (`dmg`, `linux`, `windows`, `pages`, `bench`…). An
existing recipe whose meaning is one of the above is renamed: Pavé's `run` becomes `dev`. The
old name may stay a while as a private alias (`[private]`, `alias run := dev`), so it does not
show in `just --list`, then goes.

The justfile starts with a comment that says what the app's gate holds, and groups recipes under
`# ---- development`, `# ---- checks`, `# ---- packaging`, `# ---- release` rules.

## 5. Decisions

Every technical decision **must** be recorded in `docs/adrs/`, Pastille's way:

- one file per decision, `NNNN-kebab-title.md`, numbered in the order they were taken;
- the shape of [the template](templates/docs/adrs/0000-template.md): status, date, context,
  decision, the options considered and why each lost, the consequences;
- `docs/adrs/README.md` lists them by theme, one sentence each, with whether it is in force;
- a record is never rewritten: a later one revises it and says so in both status lines.

A change that goes against a record comes with a new record. An agent proposing to change
something odd reads the record behind it first.

Decisions that hold for the whole suite are recorded here, in [`docs/adrs/`](docs/adrs), and an
app's record can cite them.

## 6. The README

Every README follows [the template](templates/README.md):

1. A centred header: the icon at 112 px, the name, **one bold sentence** that says what the app
   does and for whom, then the badges: platforms, stack, licence, all in `img.shields.io`'s
   flat style.
2. The screenshot that best shows the app, with an alt text that describes what it shows.
3. The problem, in one paragraph, from the user's side. Then three to five bullets, each
   opening with a bold phrase.
4. `## What's inside`: one `###` per feature, each with what it does for the user. The
   feature titles are the app's own voice (Pavé's *Snap like you mean it*); only the level
   above them is shared.
5. `## Getting started`: download first, then `### Build it` with `just doctor`, `just install`,
   `just dev`.
6. `## Privacy`, when the app touches anything personal: what it reads, what leaves the
   machine, and that nothing else does.
7. `## Documentation`, when there is more than the README.
8. `## How it was made`: the suite's paragraph, word for word (§10).
9. `## Contributing`: two lines pointing at `CONTRIBUTING.md` and `SECURITY.md`.
10. `## License`.

The README is written for a user, not for a developer: it sells nothing it cannot show, and
it is updated in the same commit as the feature it describes.

## 7. The gate

**`just ci` is what says a change is good.** It runs on the author's machine, before every
commit that is meant to stay. There is no hosted CI
([ADR 0002](docs/adrs/0002-the-gate-stays-local.md)), until a second person pushes.

`just ci` is ordered so the fastest thing that can fail fails first, and ends by printing
`✓ all checks passed`. It holds at least `check` and `test`, and should hold everything else
a machine can verify: licence checks on dependencies, SPDX headers, a build, a smoke run of
the built app.

**Done** means, for every change:

- `just ci` passed, and the commit message says so if it could not be run, and why;
- the change comes with its tests; a fixed bug with a test that fails without the fix;
- a decision taken on the way has its ADR;
- the README and the docs say what is now true;
- the commit subject is one a user can read in the release notes (§8).

## 8. Commits and releases

**Commits** **must** follow [Conventional Commits](https://www.conventionalcommits.org):
`feat(scope): …`, `fix: …`, `perf: …`, `docs: …`, `refactor: …`, `test: …`, `chore: …`; a `!`
or a `BREAKING CHANGE:` footer for what a user must read first. The release notes are built
from them, so the subject is written for someone reading what changed. A pull request merged
by squash takes its title as the subject: the title follows the same rule.

The rule is checked, not remembered: [`scripts/check-commits.sh`](templates/scripts/check-commits.sh)
checks every commit since the previous release tag. `just ci` runs it, so a commit that breaks
the rule fails the gate on the next run, and `release.sh` runs it again before publishing.
It also works as a `commit-msg` hook (`ln -s ../../scripts/check-commits.sh .git/hooks/commit-msg`),
to stop such a commit before it is made.

**Versions** follow [SemVer](https://semver.org). An app has **one file** that holds its
version; every other file that repeats it must agree, and `release.sh` refuses when one does
not.

**A release** is made by `just release`, from the author's machine:

- it is a commit: nothing uncommitted, the commit already pushed;
- it runs `just ci` first, unless `--skip-checks` says it just passed on this commit;
- it is tagged **`<slug>-v<version>`** and titled **`<Name> <version>`**; a version already
  released is refused;
- its notes are `just changelog`'s: Features, Fixes and Performance since the previous tag, the
  rest only counted, then how to install;
- its files are named **`<Name>_<version>_<platform>.<ext>`** (`Pave_0.6.0.dmg`,
  `Prism_0.12.0_macos-universal.dmg`, `Pastille_0.1.0_amd64.deb`), each with its `.sha256`
  and its `.minisig` (§9);
- `--dry-run` builds and prints what would be published, and publishes nothing.

Platforms are written `macos-universal`, `amd64`, `windows-x64`, `windows-arm64`.

The suite publishes on GitHub. An app that also publishes elsewhere (Prism's team builds, to a
GitLab project) records why in an ADR of its own; the GitHub release follows this section.

## 9. Updates, signing, licence

- **Every file a release publishes is signed** with [minisign](https://jedisct1.github.io/minisign/)
  ([ADR 0003](docs/adrs/0003-every-release-signed.md)): the key is `~/.minisign/<slug>.key` (or
  `<SLUG>_SIGN_KEY`), its public half is committed as `update-key.pub` (where the app bundles
  it), and every file gets
  its `.minisig` beside its `.sha256`. `SECURITY.md` says how to check one.
- An app that **updates itself** reads its releases from GitHub, and installs only a file
  signed with that key, whose public half it ships.
- A macOS app that needs a permission which survives updates (Accessibility…) is signed with
  the same certificate every version. Apple's notarization is not required: an app that is not
  notarized says, in its README's *Download the app*, what macOS shows the first time.
- The **licence** is **MIT OR Apache-2.0** ([ADR 0001](docs/adrs/0001-dual-licence.md)):
  `LICENSE-MIT` and `LICENSE-APACHE` at the root, the same in every manifest's `license` field.
  Dependencies are under permissive licences only, checked by `just ci` where the ecosystem
  allows it.

## 10. How it was made

Every README ends its presentation with this paragraph, the name replaced:

> ## How it was made
>
> <Name> was designed, tested and used every day by its author, with the help of an AI coding
> agent ([Claude Code](https://claude.com/claude-code)). The agent wrote most of the code and
> the tests under the author's direction; the design decisions, the testing on real machines
> and the choice of what ships remain the author's. It is part of the
> [P suite](https://github.com/Srynetix/p-suite), apps made this way.

## 11. Style

- Everything in a repository is written in **English**: code, comments, docs, commits.
- Prose is plain: short sentences, the user's words, what and why before how. A comment says
  why the code is the way it is, not what it does.
- Source files start with `SPDX-License-Identifier: MIT OR Apache-2.0` in their first three
  lines, checked by `just ci`.
- Each language keeps its own formatter's defaults (`cargo fmt`, Prettier, `swift-format`);
  `.editorconfig` covers the rest.

---

## Open decisions

Questions the suite has not settled. Each becomes an ADR in [`docs/adrs/`](docs/adrs) once it
is.

1. **Shared scripts.** `changelog.sh` and most of `release.sh` are three copies of one idea.
   Whether they move here, and how an app takes them (copied by a sync script, or called from
   a checkout of this repository), is to be decided once `just audit` shows how far they have
   drifted.
