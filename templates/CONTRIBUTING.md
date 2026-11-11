<!--
  Template from p-suite (templates/CONTRIBUTING.md). Replace every {{…}} and delete this
  comment.
-->

# Contributing to {{Name}}

Thank you for wanting to help. {{Name}} is a small project kept by one person, so a short
issue first saves you work: say what you would like to change and why, and we can agree on
the shape before you write it.

## Reporting a bug

Open an issue with:

- what you did, what you expected, and what happened instead;
- {{the file or setting that reproduces it, e.g. "your config file, without its tokens"}};
- where you ran it: which system, and which release (or which commit, built from source).

A security problem goes through [SECURITY.md](SECURITY.md), not an issue.

## Ideas

Ideas are welcome as issues. {{What fits best, and who {{Name}} stays aimed at, which is why
some good ideas will not be taken.}}

## Changing the code

### Setting up

Install what the README's [*Build it*](README.md#build-it) section lists, then:

```bash
just doctor   # what this machine is missing
just install
just dev
```

### Before you open a pull request

**Run `just ci`, and say in the pull request that it passed.** There is no hosted pipeline:
nothing checks a pull request but this command. `just fmt` fixes formatting; `just test` runs
the tests alone while you work.

### Conventions

- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org):
  `feat({{scope}}): …`, `fix: …`, `docs: …`. The release notes are built from them, so the
  subject is written for someone reading what changed. A pull request's title follows the same
  rule: it becomes the commit.
- **Every source file** starts with `SPDX-License-Identifier: MIT OR Apache-2.0` in its first three
  lines; the gate checks it.
- **Tests come with the change.** A fixed bug gets a test that fails without the fix.
- **Dependencies** are few on purpose, and only under permissive licences. Ask before adding
  one.

### Where things are decided

Every technical decision is recorded in [`docs/adrs`](docs/adrs/README.md), with what was
considered and why it lost. Much of what looks odd here was chosen: read the record behind a
part of the code before proposing to change it. A change that goes against a record comes
with a new one.

{{Optional: "Some common changes", one bullet each, saying which folders a typical change
touches.}}

## Licence

Unless you state otherwise, any contribution you submit for inclusion is dual-licensed
under MIT or Apache 2.0, as the project is, with no additional terms.
