<p align="center"><img src="docs/logo.svg" width="128" alt="The P suite's logo"></p>

# p-suite

The conventions shared by the apps of the P suite, and the files that carry them:
[Prism](https://github.com/Srynetix/prism), [Pavé](https://github.com/Srynetix/pave) and
[Pastille](https://github.com/Srynetix/pastille), apps built almost entirely by AI coding agents
under one author's direction.

- [**SUITE.md**](SUITE.md) — the conventions: names, commands, the gate, decisions, the README,
  commits and releases.
- [**templates/**](templates) — the files an app starts from, or is brought in line with:
  `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `justfile`,
  `.editorconfig`, `docs/adrs/`. Every `{{…}}` is to be replaced (`<<…>>` in the justfile and in scripts, where `{{…}}` is
  the language's own).
- [**docs/adrs/**](docs/adrs) — the decisions that hold for the whole suite.
- [**scripts/audit.py**](scripts/audit.py) — checks an app against SUITE.md, and lists what
  departs from it.

```bash
just audit pave              # a slug (cloned into ~/.cache/p-suite) or a path to a checkout
just audit pave --markdown   # the same, as a checklist to hand to an agent
just audit-all               # every app of the suite
```

A *must* that fails (✗) fails the audit; a *should* (!) is reported only, and an app that
keeps it gets an ADR saying why.

Nothing here runs inside an app: the apps share a way of being made, not code.
