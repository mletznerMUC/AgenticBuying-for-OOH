# Contributing

This repository is a working space for turning OOH domain knowledge into protocol
extensions. Two kinds of contribution are equally valuable:

- **Domain input** — "here is how OOH actually trades in my market, and here is
  why the current protocol shape breaks it".
- **Protocol input** — "here is the right place in AdCP/AAMP for that, and here is
  what the schema should look like".

## Where to put things

| You want to... | Put it in |
| --- | --- |
| Describe an OOH characteristic or requirement | `ooh-specifics/` |
| Say where a requirement belongs in AdCP or AAMP | `mapping/adcp/` or `mapping/aamp/` |
| Propose a concrete, reviewable extension | `proposals/` (copy `proposals/TEMPLATE.md`) |
| Draft a schema for an accepted proposal | `schemas/` |
| Explain background or define a term | `docs/` |

## Ground rules

1. **Separate observation from proposal.** `ooh-specifics/` describes reality.
   `mapping/` and `proposals/` propose changes. Do not mix them in one document.
2. **Cite the protocol revision.** AdCP and AAMP both change quickly. When you
   reference a task, field or version, name the revision and the date you checked
   it.
3. **Cite the market.** OOH conventions and audience currencies are national.
   State which market(s) a statement applies to; flag it explicitly when you
   believe something is universal.
4. **Prefer extension over invention.** Reuse an existing field or enum wherever
   one fits. A new object or task needs a stated reason why nothing existing works.
5. **Mark uncertainty.** `> Status: stub`, `TODO`, and open-questions sections are
   good. Confident-sounding guesses are not.

## Workflow

Branch, commit, open a pull request. Substantive protocol proposals should land as
an OEP in `proposals/` so there is one reviewable document to discuss and, later,
to hand to a working group.

## Open questions on the repo itself

- [ ] **Licence.** A standards repository needs one before it can be contributed
  upstream. Candidates: CC BY 4.0 for the documents, Apache-2.0 or MIT for the
  schemas; check what AdCP and AAMP require for incoming contributions.
- [ ] **Governance.** Who decides an OEP is ready to submit upstream?
- [ ] **Relationship to the upstream projects.** Do we file issues/PRs directly
  against `adcontextprotocol/adcp` and the AAMP repositories, or engage through a
  working group first?
- [ ] **Scope of "OOH".** DOOH only, or classic/printed OOH as well? This
  repository currently assumes **both**, because both are bought from the same
  budget and increasingly in the same plan.
