# 1. Every app is dual-licensed MIT OR Apache-2.0

- **Status:** accepted
- **Date:** 2026-11-11
- **Deciders:** Denis Bourge

## Context and problem statement

The suite's three apps had two licences: Prism and Pavé under MIT, Pastille under MIT OR
Apache-2.0 ([its ADR 0001](https://github.com/Srynetix/pastille/blob/main/docs/adrs/0001-permissive-dual-licence.md)).
A suite whose apps are made the same way should not differ on what a reader may do with them,
and the templates need one licence to carry. Which one?

## Decision

Every app of the suite is licensed under **MIT OR Apache-2.0**, at the user's option:
`LICENSE-MIT` and `LICENSE-APACHE` at the root, `license = "MIT OR Apache-2.0"` in every
manifest that has the field, `SPDX-License-Identifier: MIT OR Apache-2.0` at the top of every
source file. Dependencies stay under permissive licences only.

## Options considered

### MIT OR Apache-2.0 — chosen

The Rust ecosystem's default, which two of the three apps are built on. Apache 2.0 adds an
explicit patent grant and a contribution clause; MIT keeps compatibility with GPLv2 code that
would take ours. Offering both costs a second file.

### MIT everywhere — rejected

The simplest, and already Prism's and Pavé's. Rejected because it gives no patent grant, and
because moving Pastille back to it would revise a decision taken for a reason that still holds.

### Apache-2.0 alone — rejected

Rejected because it is incompatible with GPLv2, which closes a door MIT leaves open, for no
gain over offering both.

## Consequences

1. **Prism and Pavé change licence.** Both have one author, so the change needs no one
   else's consent: their next release is under MIT OR Apache-2.0, and earlier releases stay
   under MIT.
2. **`just audit` checks it:** the two licence files, the manifests' `license` field, and the
   SPDX header of every source file.
3. **SPDX headers arrive in Prism and Pavé** as part of their move, file by file being a
   mechanical change an agent can make in one commit.
