<!--
  Template from p-suite (templates/README.md), following SUITE.md § 6. Replace every {{…}},
  delete the sections marked optional that do not apply, and delete this comment.
-->
<div align="center">

<img src="{{path/to/icon-256.png}}" width="112" alt="{{Name}}">

# {{Name}}

**{{One sentence: what it does, and for whom.}}**

![macOS](https://img.shields.io/badge/macOS-black?logo=apple&logoColor=white)
![{{Stack}}](https://img.shields.io/badge/{{Stack}}-{{colour}}?logo={{logo}}&logoColor=white)
![License: MIT OR Apache-2.0](https://img.shields.io/badge/License-MIT_OR_Apache--2.0-f5b82e)

</div>

![{{What the screenshot shows, in one sentence}}](docs/screenshots/{{main}}.png)

{{The problem, in one paragraph, from the user's side: what their day looks like without
{{Name}}, and what {{Name}} changes.}}

- **{{Bold phrase.}}** {{One or two sentences.}}
- **{{Bold phrase.}}** {{One or two sentences.}}
- **{{Bold phrase.}}** {{One or two sentences.}}

## What's inside

### {{Feature}}

{{What it does for the user. A screenshot when it shows more than words.}}

### {{Feature}}

{{…}}

## Getting started

### Download the app

{{Where the releases are, which file to take on which system, and what the system says the
first time (an unsigned app, a permission to grant).}}

### Build it

You need {{the toolchain}}. Then:

```bash
just doctor   # what this machine is missing
just install
just dev      # {{what it runs}}
```

`just` lists every other command; `just ci` runs every check.

## Privacy

<!-- Optional: when the app touches anything personal. -->

{{What {{Name}} reads, what leaves the machine and where to, and that nothing else does.}}

## Documentation

- [Developing {{Name}}](docs/dev/README.md) — how the code is built: architecture, patterns
- [Decisions](docs/adrs/README.md) — every technical choice, and what it was chosen against
- {{[A user guide](docs/guide.md) — what it covers; or delete this line}}

## How it was made

{{Name}} was designed, tested and used every day by its author, with the help of an AI coding
agent ([Claude Code](https://claude.com/claude-code)). The agent wrote most of the code and the
tests under the author's direction; the design decisions, the testing on real machines and the
choice of what ships remain the author's. It is part of the
[P suite](https://github.com/Srynetix/p-suite), apps made this way.

## Contributing

Bug reports, ideas and pull requests are welcome: [CONTRIBUTING.md](CONTRIBUTING.md) says how,
and [SECURITY.md](SECURITY.md) how to report a security problem privately.

## License

Dual-licensed under either of [MIT](LICENSE-MIT) or [Apache 2.0](LICENSE-APACHE), at your
option. Unless you state otherwise, any contribution you submit for inclusion is dual-licensed
the same way, with no additional terms.
