# 2. The gate stays on the author's machine, for every app

- **Status:** accepted
- **Date:** 2026-11-11
- **Deciders:** Denis Bourge

## Context and problem statement

Pastille decided that its gate, `just ci`, runs on the author's Mac and nowhere else
([its ADR 0014](https://github.com/Srynetix/pastille/blob/main/docs/adrs/0014-the-gate-stays-local.md)),
and SUITE.md leaned on that record for the whole suite. Prism and Pavé have no hosted CI
either, but by default rather than by decision. A rule every app follows should be the
suite's own: does any app of the suite get a hosted pipeline?

## Decision

No. **`just ci`, run on the author's machine before every commit meant to stay, is the
gate of every app.** No app adds a workflow that runs it, or part of it, on a hosted runner.
`just audit` reports a `.github/workflows/` as a departure.

## Options considered

### GitHub Actions running `just ci` on every push — rejected for now

Every push checked, by a machine nobody has to remember. Rejected because the apps' gates
hold checks a hosted runner cannot run honestly: Pastille's benchmark calibrated to one Mac,
Pavé's tests that need the Accessibility permission, Prism's and Pastille's macOS universal
builds. A runner would run a weaker gate, a second definition to keep in step with the first.

### A hosted pipeline for what it can run, the rest local — rejected for now

Rejected while one person pushes: the failure it guards against, a push nobody checked, is
the same person forgetting either way. It is the starting point the day a second person
pushes, as Pastille's record already says.

### Keep it local, everywhere, and say why — chosen

## Consequences

1. **Nothing enforces the gate on a push.** A commit message that says `just ci` could not
   run, and why, is the convention when it could not.
2. **The checks a pipeline would enforce move into the gate instead.** Conventional Commits
   are checked by `scripts/check-commits.sh`, which `just ci` and `release.sh` both run.
3. **Revisit when a second person pushes** to any app: then for that app first.
