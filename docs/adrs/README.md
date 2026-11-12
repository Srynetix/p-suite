# Decisions of the suite

Decisions that hold for every app of the P suite. An app's own decisions live in its own
`docs/adrs/`, and can cite these. The format is [the template](../../templates/docs/adrs/0000-template.md).

The questions still open are listed at the end of [SUITE.md](../../SUITE.md#open-decisions);
each becomes a record here once it is settled.

| # | Decided | In force |
|---|---|---|
| [1](0001-dual-licence.md) | Every app is dual-licensed MIT OR Apache-2.0. | Yes |
| [2](0002-the-gate-stays-local.md) | The gate, `just ci`, runs on the author's machine; no app has a hosted CI. | Yes |
| [3](0003-every-release-signed.md) | Every file a release publishes is signed with minisign, by every app. | Yes |
| [4](0004-code-a-person-can-take-over.md) | The code follows Clean Code and Clean Architecture, keeps only the comments that say why, and every app documents how it is built in `docs/dev/`. | Yes |
