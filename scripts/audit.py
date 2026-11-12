#!/usr/bin/env python3
# SPDX-License-Identifier: MIT OR Apache-2.0
"""Checks an app of the P suite against SUITE.md, and lists what departs from it.

    scripts/audit.py <app> [--markdown] [--commits N] [--no-fetch]

- <app>: a path to a checkout, or a slug (`pave`): then github.com/Srynetix/<slug> is cloned,
  or fetched again, into ~/.cache/p-suite/<slug> (P_SUITE_CACHE overrides the folder).
- Every check is a *must* (✗, fails the audit: exit 1) or a *should* (!, reported only), as
  SUITE.md words them; each names the section of SUITE.md it comes from.
- --markdown prints the departures as a checklist, to hand to an agent as a task.
- --commits: how many of the latest commits must be Conventional (30 by default).

Only reads: never changes the app.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

OWNER = "Srynetix"
LICENCE = "MIT OR Apache-2.0"

REQUIRED_FILES = [
    "README.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "SECURITY.md",
    "LICENSE-MIT", "LICENSE-APACHE", "justfile", ".editorconfig",
    "docs/adrs/README.md", "scripts/release.sh", "scripts/changelog.sh",
    "scripts/check-commits.sh",
]
DEV_DOCS = ["docs/dev/README.md", "docs/dev/architecture.md", "docs/dev/patterns.md"]
REQUIRED_RECIPES = [
    "default", "doctor", "install", "dev", "fmt", "check", "test", "ci",
    "build", "changelog", "release",
]
README_SECTIONS = [  # in this order (SUITE.md § 6); Privacy is optional
    "## What's inside", "## Getting started", "### Build it", "## Documentation",
    "## How it was made",
    "## Contributing", "## License",
]
AGENTS_SECTIONS = ["## Commands", "## Done means", "## Rules", "## Ask before"]
CONVENTIONAL = re.compile(
    r"^(feat|fix|perf|docs|refactor|test|chore|build|ci|style|revert)(\([^)]+\))?!?: \S"
)
SOURCE_EXT = {".rs", ".ts", ".js", ".mjs", ".cjs", ".svelte", ".swift", ".sh", ".py", ".css"}
NOT_SOURCE = re.compile(
    r"(^|/)(node_modules|dist|dist-[^/]*|build|target|vendor|\.svelte-kit|gen|generated)/"
    r"|\.d\.ts$|\.min\.(js|css)$"
)
GENERATED = re.compile(r"@generated|DO NOT EDIT|auto-generated|automatically generated", re.I)


# ------------------------------------------------------------------------------------ results


@dataclass
class Check:
    section: str
    level: str  # "must" | "should"
    title: str
    ok: bool
    details: list[str] = field(default_factory=list)


class Audit:
    def __init__(self, root: Path, slug: str):
        self.root = root
        self.slug = slug
        self.checks: list[Check] = []
        self.tracked = self._tracked()

    def add(self, section, level, title, ok, details=None):
        self.checks.append(Check(section, level, title, bool(ok), details or []))

    def must(self, section, title, ok, details=None):
        self.add(section, "must", title, ok, details)

    def should(self, section, title, ok, details=None):
        self.add(section, "should", title, ok, details)

    # helpers

    def git(self, *args) -> str | None:
        r = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None

    def _tracked(self) -> list[str]:
        out = self.git("ls-files")
        if out is not None:
            return out.splitlines()
        return [str(p.relative_to(self.root)) for p in self.root.rglob("*") if p.is_file()]

    def exists(self, rel: str) -> bool:
        # Case-sensitive, whatever the file system: `Justfile` is not `justfile`.
        path = self.root / rel
        return rel in self.tracked or (path.is_file() and path.name in os.listdir(path.parent))

    def read(self, rel: str) -> str:
        try:
            return (self.root / rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return ""


def short(items, n=5):
    items = list(items)
    return items[:n] + ([f"… and {len(items) - n} more"] if len(items) > n else [])


# ------------------------------------------------------------------------------------- checks


def check_names(a: Audit, name: str | None):
    s = "§ 1 Names"
    a.should(s, "The name starts with a P", bool(name) and name[0] == "P",
             [f"README title: {name!r}"] if name else ["no title found in README.md"])
    a.should(s, "The slug is the name in lowercase ASCII",
             bool(name) and ascii_slug(name) == a.slug,
             [f"name {name!r}, slug {a.slug!r}"])
    remote = (a.git("remote", "get-url", "origin") or "").strip()
    a.should(s, f"The repository is github.com/{OWNER}/{a.slug}",
             re.search(rf"github\.com[:/]{OWNER}/{re.escape(a.slug)}(\.git)?$", remote),
             [f"origin: {remote or 'none'}"])


def check_repository(a: Audit):
    s = "§ 2 Repository"
    missing = [f for f in REQUIRED_FILES if not a.exists(f)]
    if "justfile" in missing and a.exists("Justfile"):
        missing[missing.index("justfile")] = "justfile (found `Justfile`: rename it)"
    a.must(s, "Every required file is there", not missing, missing)
    keys = [f for f in a.tracked if f.endswith("update-key.pub")]
    a.must(s, "The release key's public half, update-key.pub, is committed (ADR 0003)", keys,
           [] if keys else ["no update-key.pub anywhere in the repository"])
    a.should(s, "Screenshots live in docs/screenshots/",
             any(f.startswith("docs/screenshots/") for f in a.tracked))

    claude = a.read("CLAUDE.md").strip()
    a.must(s, "CLAUDE.md only imports AGENTS.md", claude == "@AGENTS.md",
           [] if claude == "@AGENTS.md" else
           ["missing" if not claude else f"{len(claude.splitlines())} lines, expected `@AGENTS.md`"])

    ignore = [l.strip() for l in a.read(".gitignore").splitlines()]
    whole = [l for l in ignore if l.rstrip("/*") in (".claude", "/.claude")]
    a.must(s, "`.claude/` is not ignored as a whole (only its local files)", not whole, whole)

    leftovers = []
    for f in ["README.md", "AGENTS.md", "CONTRIBUTING.md", "SECURITY.md", *DEV_DOCS]:
        for i, line in enumerate(a.read(f).splitlines(), 1):
            if re.search(r"\{\{[^}]*\}\}", line):
                leftovers.append(f"{f}:{i}: {line.strip()[:80]}")
    for f in [justfile_name(a) or "justfile", "scripts/check-commits.sh"]:
        for i, line in enumerate(a.read(f).splitlines(), 1):
            if re.search(r"<<[^>]*>>", line):
                leftovers.append(f"{f}:{i}: {line.strip()[:80]}")
    a.must(s, "No template placeholder is left", not leftovers, short(leftovers))


def check_agents(a: Audit):
    s = "§ 3 Agents"
    text = a.read("AGENTS.md")
    if not text:
        return  # already reported as a missing file
    missing = [h for h in AGENTS_SECTIONS if not re.search(rf"^{re.escape(h)}\b", text, re.M)]
    a.should(s, "AGENTS.md has the template's sections", not missing, missing)
    lines = len(text.splitlines())
    a.should(s, "AGENTS.md is short (under 150 lines)", lines < 150, [f"{lines} lines"])


def justfile_name(a: Audit) -> str | None:
    """The justfile, as spelled: a `Justfile` is reported in § 2, and read all the same."""
    return next((f for f in ("justfile", "Justfile", ".justfile") if f in a.tracked
                 or (a.root / f).is_file() and f in os.listdir(a.root)), None)


def just_dump(a: Audit) -> dict | None:
    name = justfile_name(a)
    if not name or not shutil.which("just"):
        return None
    r = subprocess.run(
        ["just", "--justfile", str(a.root / name), "--working-directory", str(a.root),
         "--dump", "--dump-format", "json"],
        capture_output=True, text=True,
    )
    return json.loads(r.stdout).get("recipes", {}) if r.returncode == 0 else None


def check_commands(a: Audit):
    s = "§ 4 Commands"
    if not justfile_name(a):
        return  # already reported as a missing file
    recipes = just_dump(a)
    if recipes is None:
        a.must(s, "The recipes can be read", False,
               ["`just` is not installed" if not shutil.which("just") else "`just --dump` failed"])
        return
    missing = [r for r in REQUIRED_RECIPES if r not in recipes]
    a.must(s, "Every required recipe exists", not missing, missing)

    ci = recipes.get("ci")
    if ci:
        deps = {d["recipe"] for d in ci.get("dependencies", [])}
        body = json.dumps(ci.get("body", []))
        runs = lambda r: r in deps or re.search(rf"just {r}\b", body)
        absent = [r for r in ("check", "test") if not runs(r)]
        a.should(s, "`just ci` runs `check` and `test`", not absent,
                 [f"does not run: {', '.join(absent)}"] if absent else [])

    undocumented = sorted(n for n, r in recipes.items() if not r.get("doc") and not r.get("private"))
    a.should(s, "Every recipe has a doc comment (shown by `just --list`)", not undocumented,
             short(undocumented, 8))


def check_decisions(a: Audit):
    s = "§ 5 Decisions"
    records = sorted(f for f in a.tracked if re.match(r"docs/adrs/[^/]+\.md$", f)
                     and not f.endswith("/README.md"))
    a.should(s, "At least one decision is recorded", records)
    bad = [f for f in records if not re.match(r"docs/adrs/\d{4}-[a-z0-9-]+\.md$", f)
           and not f.endswith("0000-template.md")]
    a.should(s, "Records are named NNNN-kebab-title.md", not bad, short(bad))
    index = a.read("docs/adrs/README.md")
    if index:
        unlisted = [f for f in records if Path(f).name not in index
                    and not f.endswith("0000-template.md")]
        a.should(s, "Every record is listed in docs/adrs/README.md", not unlisted, short(unlisted))
    nostatus = [f for f in records if not re.search(r"\*\*Status:\*\*", a.read(f))
                and not f.endswith("0000-template.md")]
    a.should(s, "Every record has a status line", not nostatus, short(nostatus))


def check_readme(a: Audit) -> str | None:
    s = "§ 6 README"
    text = a.read("README.md")
    if not text:
        return None
    m = re.search(r"^# (.+)$", text, re.M) or re.search(r"<h1[^>]*>(.+?)</h1>", text)
    name = m.group(1).strip() if m else None

    head = "\n".join(text.splitlines()[:40])
    a.should(s, "The header has one bold sentence under the name",
             re.search(r"^\s*(<b>|\*\*).+", head, re.M))
    a.should(s, "The header has shields.io badges", "img.shields.io" in head)
    a.should(s, "The header's licence badge says MIT OR Apache-2.0",
             re.search(r"img\.shields\.io/badge/[Ll]icen[sc]e[^)\"]*MIT[_ %20]*OR[_ %20]*Apache", head))
    a.should(s, "A screenshot follows the header",
             re.search(r"!\[[^\]]+\]\(docs/screenshots/|<img[^>]+src=\"docs/screenshots/", text))

    positions, missing = [], []
    for h in README_SECTIONS:
        m = re.search(rf"^{re.escape(h)}\s*$", text, re.M)
        (positions.append(m.start()) if m else missing.append(h))
    a.must(s, "Every required section is there", not missing, missing)
    a.should(s, "The sections are in the suite's order", positions == sorted(positions))

    made = section_body(text, "## How it was made")
    flat = " ".join(made.split())
    a.must(s, "“How it was made” is the suite's paragraph, with its link",
           f"[P suite](https://github.com/{OWNER}/p-suite)" in flat
           and "remain the author's" in flat,
           [] if made else ["section missing"])
    return name


def check_gate(a: Audit):
    s = "§ 7 Gate"
    text = a.read(justfile_name(a) or "justfile")
    m = re.search(r"^ci\b[^\n]*\n((?:[ \t]+.*\n?|\n)*)", text, re.M)
    a.should(s, "`just ci` ends by printing “✓ all checks passed”",
             m and "all checks passed" in m.group(1))
    recipes = just_dump(a) or {}
    ci = recipes.get("ci", {})
    ci_deps = {d["recipe"] for d in ci.get("dependencies", [])}
    a.must(s, "`just ci` checks the commits (scripts/check-commits.sh)",
           (m and "check-commits" in m.group(1)) or "check-commits" in ci_deps)
    workflows = [f for f in a.tracked if f.startswith(".github/workflows/")]
    a.should(s, "No hosted CI duplicates the gate (ADR 0002)", not workflows, workflows)


def check_commits(a: Audit, n: int):
    s = "§ 8 Commits and releases"
    log = a.git("log", f"-{n}", "--no-merges", "--format=%h %s")
    if log is None:
        a.must(s, "The history can be read", False, ["not a git checkout"])
    else:
        roots = set((a.git("rev-list", "--max-parents=0", "--abbrev-commit", "HEAD") or "").split())
        commits = [c for c in log.splitlines() if not any(c.startswith(r[:7]) for r in roots)]
        bad = [c for c in commits if not CONVENTIONAL.match(c.split(" ", 1)[1])]
        a.must(s, f"The latest commits are Conventional ({len(commits) - len(bad)}/{len(commits)})",
               not bad, short(bad))

        tags = (a.git("tag", "-l") or "").split()
        tag_re = re.compile(rf"^{re.escape(a.slug)}-v\d+\.\d+\.\d+(-[\w.]+)?$")
        bad_tags = [t for t in tags if not tag_re.match(t)]
        a.must(s, f"Every tag is {a.slug}-v<semver>", not bad_tags, short(bad_tags))

    release = a.read("scripts/release.sh")
    if release:
        a.should(s, f"release.sh tags {a.slug}-v<version>", f"{a.slug}-v" in release)
        a.should(s, "release.sh has --dry-run", "--dry-run" in release)
        a.should(s, "release.sh refuses uncommitted changes",
                 re.search(r"git (status --porcelain|diff --quiet|diff-index)", release))
        a.should(s, "release.sh publishes a .sha256 of every file", "sha256" in release)
        a.must(s, "release.sh signs every file with minisign (ADR 0003)", "minisign" in release)
        a.should(s, "release.sh checks the commits first", "check-commits" in release)


def check_licence(a: Audit):
    s = "§ 9 Licence and signing"
    if a.exists("LICENSE"):
        a.must(s, "No single LICENSE file (LICENSE-MIT and LICENSE-APACHE instead)", False,
               ["LICENSE"])
    wrong = []
    for f in a.tracked:
        if f.endswith("Cargo.toml"):
            text = a.read(f)
            pkg = re.search(r"^\[(workspace\.)?package\]\s*\n(.*?)(?=^\[|\Z)", text, re.M | re.S)
            if not pkg:
                continue
            m = re.search(r'^license\s*=\s*"([^"]*)"', pkg.group(2), re.M)
            inherited = re.search(r"^license\.workspace\s*=\s*true", pkg.group(2), re.M)
            if inherited:
                continue
            if not m or m.group(1) != LICENCE:
                wrong.append(f"{f}: license = {m.group(1)!r}" if m else f"{f}: no license field")
        elif f.endswith("package.json") and "node_modules" not in f:
            try:
                lic = json.loads(a.read(f)).get("license")
            except ValueError:
                continue
            if lic is not None and lic != LICENCE:
                wrong.append(f"{f}: \"license\": {lic!r}")
    a.must(s, f"Manifests say license = \"{LICENCE}\"", not wrong, short(wrong))

    lic = section_body(a.read("README.md"), "## License")
    a.must(s, "The README's License section names MIT and Apache 2.0",
           "MIT" in lic and "Apache" in lic, [] if lic else ["section missing"])

    security = a.read("SECURITY.md")
    if security:
        a.should(s, "SECURITY.md says how to report privately", "advisories/new" in security)
        a.should(s, "SECURITY.md says how to check a signature (ADR 0003)",
                 "minisign" in security and "update-key.pub" in security)


def check_style(a: Audit):
    s = "§ 11 Style"
    missing, total = [], 0
    for f in a.tracked:
        p = Path(f)
        if p.suffix not in SOURCE_EXT or NOT_SOURCE.search(f):
            continue
        try:
            with open(a.root / f, encoding="utf-8", errors="replace") as fh:
                head = "".join(fh.readline() for _ in range(3))
        except OSError:
            continue
        if GENERATED.search(head):
            continue
        total += 1
        if f"SPDX-License-Identifier: {LICENCE}" not in head:
            missing.append(f)
    a.must(s, f"Source files start with the SPDX header ({total - len(missing)}/{total})",
           not missing, short(missing))


def check_dev_docs(a: Audit):
    s = "§ 13 Developer documentation"
    missing = [f for f in DEV_DOCS if not a.exists(f)]
    a.must(s, "docs/dev/ has its README, architecture and patterns", not missing, missing)
    if a.exists("docs/dev/architecture.md"):
        a.should(s, "architecture.md says where the app departs from § 12",
                 re.search(r"^## Departures", a.read("docs/dev/architecture.md"), re.M))
    docs = section_body(a.read("README.md"), "## Documentation")
    a.should(s, "The README's Documentation links docs/dev/", "docs/dev/" in docs)
    a.should(s, "AGENTS.md points to docs/dev/", "docs/dev/" in a.read("AGENTS.md"))


# ------------------------------------------------------------------------------------ helpers


def section_body(text: str, heading: str) -> str:
    m = re.search(rf"^{re.escape(heading)}\s*$(.*?)(?=^#{{1,{heading.count('#')}}} |\Z)",
                  text, re.M | re.S)
    return m.group(1) if m else ""


def ascii_slug(name: str) -> str:
    import unicodedata
    return unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()


def resolve(app: str, fetch: bool) -> tuple[Path, str]:
    path = Path(app).expanduser()
    if path.is_dir():
        root = path.resolve()
        remote = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"],
                                capture_output=True, text=True).stdout.strip()
        m = re.search(r"/([^/]+?)(\.git)?$", remote)
        return root, (m.group(1) if m else root.name).lower()

    if not re.fullmatch(r"[a-z][a-z0-9-]*", app):
        sys.exit(f"audit: {app!r} is neither a folder nor a slug")
    cache = Path(os.environ.get("P_SUITE_CACHE", "~/.cache/p-suite")).expanduser()
    root = cache / app
    url = f"https://github.com/{OWNER}/{app}.git"
    quiet = {"stdout": subprocess.DEVNULL}
    if not (root / ".git").is_dir():
        cache.mkdir(parents=True, exist_ok=True)
        print(f"  cloning {url} …", file=sys.stderr)
        r = subprocess.run(["git", "clone", "-q", "--filter=blob:none", url, str(root)], **quiet)
        if r.returncode:
            sys.exit(f"audit: could not clone {url}")
    elif fetch:
        subprocess.run(["git", "-C", str(root), "fetch", "-q", "--tags", "--force",
                        "--prune", "--prune-tags", "origin"], **quiet)
        subprocess.run(["git", "-C", str(root), "reset", "-q", "--hard", "origin/HEAD"], **quiet)
    return root, app


# ------------------------------------------------------------------------------------- output


def print_text(a: Audit, name: str | None):
    tty = sys.stdout.isatty()
    c = (lambda code, t: f"\033[{code}m{t}\033[0m") if tty else (lambda code, t: t)
    print(f"\n  {c('1', name or a.slug)}  {c('2', str(a.root))}\n")
    section = None
    for ch in a.checks:
        if ch.section != section:
            section = ch.section
            print(f"  {c('1', section)}")
        mark = c("32", "✓") if ch.ok else (c("31", "✗") if ch.level == "must" else c("33", "!"))
        print(f"    {mark} {ch.title}")
        if not ch.ok:
            for d in ch.details:
                print(f"        {c('2', d)}")
    must = sum(1 for ch in a.checks if not ch.ok and ch.level == "must")
    should = sum(1 for ch in a.checks if not ch.ok and ch.level == "should")
    ok = sum(1 for ch in a.checks if ch.ok)
    print()
    if must or should:
        print(f"  {ok}/{len(a.checks)} in line · {c('31', f'{must} must')} · "
              f"{c('33', f'{should} should')} to fix (SUITE.md)\n")
    else:
        print(f"  {c('32', '✓ in line with the suite')}\n")


def print_markdown(a: Audit, name: str | None):
    title = name or a.slug
    print(f"# Bring {title} in line with the P suite\n")
    print("Each item departs from p-suite's SUITE.md, in the section named. "
          "*Must* items first; a *should* left as is gets an ADR saying why.\n")
    for level in ("must", "should"):
        items = [ch for ch in a.checks if not ch.ok and ch.level == level]
        if not items:
            continue
        print(f"## {level.capitalize()}\n")
        for ch in items:
            print(f"- [ ] **{ch.title}** ({ch.section})")
            for d in ch.details:
                print(f"  - `{d}`")
        print()
    if all(ch.ok for ch in a.checks):
        print("Nothing to do: the app is in line with the suite.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("app", help="a path to a checkout, or a slug (prism, pave, pastille…)")
    ap.add_argument("--markdown", action="store_true", help="print a checklist for an agent")
    ap.add_argument("--commits", type=int, default=30, help="how many commits to check")
    ap.add_argument("--no-fetch", action="store_true", help="use the cached clone as it is")
    args = ap.parse_args()

    root, slug = resolve(args.app, fetch=not args.no_fetch)
    a = Audit(root, slug)
    name = check_readme(a)  # first: it finds the name the other checks use
    readme_checks, a.checks = a.checks, []
    check_names(a, name)
    check_repository(a)
    check_agents(a)
    check_commands(a)
    check_decisions(a)
    a.checks += readme_checks
    check_gate(a)
    check_commits(a, args.commits)
    check_licence(a)
    check_style(a)
    check_dev_docs(a)

    (print_markdown if args.markdown else print_text)(a, name)
    sys.exit(1 if any(not ch.ok and ch.level == "must" for ch in a.checks) else 0)


if __name__ == "__main__":
    main()
