# 3. Every file a release publishes is signed with minisign

- **Status:** accepted
- **Date:** 2026-11-11
- **Deciders:** Denis Bourge

## Context and problem statement

Prism and Pavé sign every file they publish with minisign, because they update themselves: an
installed copy installs only a file signed with the key whose public half it ships. Pastille,
which does not update itself, publishes its files with a `.sha256` alone. A `.sha256` published
beside a file proves the download is whole, not that the author made it: whoever can replace
one can replace the other. Should every app sign, or only those that update themselves?

## Decision

**Every app signs every file a release publishes**, with minisign:

- one key per app, `~/.minisign/<slug>.key` (or `<SLUG>_SIGN_KEY`);
- its public half committed in the repository as `update-key.pub` (where the app bundles it,
  when it updates itself), and shown in
  `SECURITY.md`, so a user can check a download without the app;
- every file published with its `.sha256` and its `.minisig`; `release.sh` refuses to
  publish when it cannot sign.

This is about the release's files. Signing with an Apple or Microsoft certificate is a
separate question, not decided here.

## Options considered

### Every app signs — chosen

One way to publish across the suite, one paragraph in every `SECURITY.md`, and an app that
starts updating itself later already has its key. The cost is a key to keep per app and
`minisign` on the release machine, which Prism and Pavé already need.

### Only the apps that update themselves sign — rejected

What the suite did by default. Rejected because it makes the release steps differ between
apps for a saving of one command, and leaves the apps without an updater with a weaker
promise to their users.

## Consequences

1. **Pastille gets a key and signs from its next release.** Its ADR on how it is published
   gains a record revising it; releases already made stay as they are.
2. **`just audit` checks it:** `update-key.pub` present, `release.sh` signing with minisign,
   `SECURITY.md` saying how to check a signature.
3. **A lost key is a new key, announced** in the release notes and in `SECURITY.md`; for an app
   that updates itself, the last release signed with the old key ships the new one.
