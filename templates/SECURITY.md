<!--
  Template from p-suite (templates/SECURITY.md). Replace every {{…}} and delete this
  comment.
-->

# Security

## Reporting a problem

Please do not open a public issue for a security problem. Report it privately instead, through
GitHub's [private vulnerability reporting](https://github.com/Srynetix/{{slug}}/security/advisories/new)
(the *Report a vulnerability* button under the repository's *Security* tab).

Say what the problem is, how to reproduce it, and what someone could do with it. You will get
an answer within a week. Once it is fixed and released, you are credited in the advisory
unless you prefer not to be.

## What is supported

Only the latest release: fixes go into a new release, not into old ones.

## What {{Name}} does with your data

{{What it reads, where it keeps it, what leaves the machine and where to. Then: "A way to make
{{Name}} do otherwise is the kind of problem worth reporting."}}

## Checking what you download

Every file of a release is published with its `.sha256` and its `.minisig`, signed with
[minisign](https://jedisct1.github.io/minisign/) by the key whose public half is
[`update-key.pub`]({{path/to/update-key.pub}}):

```
{{the public key, as update-key.pub holds it}}
```

To check a download: `minisign -Vm <file> -p update-key.pub`. Download the apps only from this
repository's releases.

{{If the app updates itself, keep this sentence; otherwise delete it.}} {{Name}} itself installs
an update only if it is signed with this key.
