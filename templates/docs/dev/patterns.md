<!--
  Template from p-suite (templates/docs/dev/patterns.md, SUITE.md § 13). Replace every {{…}}
  and delete this comment. One section per pattern the code actually uses; delete the example.
-->

# Patterns

The patterns {{Name}}'s code relies on. Each section says what problem the pattern solves
here, where it lives, and how to add one more case without breaking it. When a new pattern
enters the code, it gets a section in the same commit.

## {{Pattern name, e.g. Ports and adapters}}

**The problem.** {{What would go wrong without it, in this app.}}

**Where.** [`{{Type}}`]({{path}}) defines it; {{the implementations, with links}}.

**How it works.** {{A few sentences, and a short excerpt or a diagram if it helps.}}

**Adding a case.** {{The steps: the file to create, the type to implement, where to register
it, the test to write.}}

**Avoid.** {{The ways it has been, or could be, misused here.}}

**Decided in.** {{The ADR, or —.}}
