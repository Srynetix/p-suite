<!--
  Template from p-suite (templates/docs/dev/README.md, SUITE.md § 13). Replace every {{…}} and
  delete this comment. Written for a developer who knows the language but not {{Name}}.
-->

# Developing {{Name}}

How {{Name}} is built, for a developer who knows {{the language(s)}} but not this code. The
README says what the app does; [the decisions](../adrs/README.md) say why it was built this way;
these documents say how it is built now.

## Where to start

1. [Architecture](architecture.md): the layers, the modules and how a {{user action}} flows
   through them. Read it first.
2. [Patterns](patterns.md): the patterns the code uses, and how to add a case to each.
3. `just doctor`, then `just dev`: the commands are in the [justfile](../../justfile), listed by
   `just`.

## Vocabulary

<!-- The domain's words, as the code names them. A reader meets them in every file. -->

| Term | Meaning | In the code |
|---|---|---|
| {{term}} | {{what it is, in one sentence}} | [`{{Type}}`]({{path}}) |

## The documents

| Document | Covers |
|---|---|
| [Architecture](architecture.md) | Layers, modules, flows, platform code, departures |
| [Patterns](patterns.md) | The patterns used, where, and how to extend them |
| {{[Testing](testing.md)}} | {{What is tested where, and how to run a part of it}} |
