# SPDX-License-Identifier: MIT OR Apache-2.0
#
# What p-suite can be asked to do. It is not an app: it holds the suite's conventions
# (SUITE.md), the files that carry them (templates/), and the audit that checks them.

APPS := "prism pave pastille"

# List the recipes.
default:
    @just --list --unsorted

# Check an app against SUITE.md: a slug (`pave`) or a path to a checkout. `--markdown` for a
# checklist to hand to an agent.
audit app *args:
    @python3 scripts/audit.py {{app}} {{args}}

# Audit every app of the suite, one after the other, whatever each one's result.
audit-all *args:
    #!/usr/bin/env bash
    status=0
    for app in {{APPS}}; do
        python3 scripts/audit.py "$app" {{args}} || status=1
    done
    exit $status
