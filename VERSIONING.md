# Versioning

The standards in this repository will expand and change. Three things carry a
version, and they move independently.

| Versioned thing | Identifier | Example |
| --- | --- | --- |
| **Addition** — one normative extension unit | `ADD-NNN` + SemVer | `ADD-001@1.2.0` |
| **Release** — a frozen manifest pinning addition versions | `R<major>.<minor>` | `R1.0` |
| **Protocol target pin** — the upstream revision an addition was written against | date-stamped in the addition | `adcp@2026-08-27` |

## 1. Additions

An **addition** is the unit of normative work: one coherent extension, with a
transport-neutral definition plus its bindings. Additions live in
[`additions/`](additions/), one file each, and are indexed in
[`additions/REGISTRY.md`](additions/REGISTRY.md).

### Identifiers

- `ADD-NNN`, zero-padded, assigned in order of creation.
- **IDs are permanent.** Never renumber, never reuse a retired number. Mapping
  documents, proposals, conformance claims and third-party implementations cite
  them.
- The file name may change (title edits); the ID may not.

### SemVer rules

`MAJOR.MINOR.PATCH`, judged from the perspective of someone who has already
implemented the addition:

| Bump | When | Examples |
| --- | --- | --- |
| **MAJOR** | An existing implementation breaks | field renamed or removed; a field's semantics change; an enum value changes meaning; a previously optional field becomes required; unit or basis of a value changes |
| **MINOR** | Additive, backwards compatible | new optional field; new enum value; a new binding (e.g. adding the IO binding to an addition that only had the programmatic one); a re-pin to a newer upstream revision with no semantic change |
| **PATCH** | No implementation impact | wording, examples, typo fixes, clarifying a rule that was already unambiguous in effect |

Pre-`1.0.0` additions (`0.x.y`) are explicitly unstable: MINOR may break. An
addition reaching `status: stable` must be at `>= 1.0.0`.

### Status lifecycle

```
draft ──> review ──> stable ──> deprecated ──> superseded
   └────────┴──────────┴──> withdrawn
```

| Status | Meaning |
| --- | --- |
| `draft` | Being written. Do not implement. |
| `review` | Complete enough to review here. Shape may still change. |
| `stable` | Agreed in this repository. Safe to implement and to cite upstream. |
| `deprecated` | Still valid but discouraged; a replacement exists or is coming. |
| `superseded` | Replaced. `superseded_by` names the successor. File is kept. |
| `withdrawn` | Abandoned. File is kept with the reason. |

Superseded and withdrawn additions are **never deleted** — a dangling ID is worse
than a tombstone.

### Required front matter

Every addition file starts with YAML front matter so the registry and conformance
manifests can be generated rather than hand-maintained:

```yaml
---
id: ADD-001
title: Total Audience Impressions
version: 1.0.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §3–§4"
targets:
  adcp: [media-buy, signals]
  aamp: [artf, agentic-audiences]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---
```

`applies_to` is load-bearing: it records whether the addition is meaningful for
programmatic transport, for insertion-order/direct buying, or (usually) both. See
[`additions/README.md`](additions/README.md).

### Changelog

Every addition file ends with a `## Changelog` table. One row per version, newest
first, with the date and a one-line reason. The repository-level
[`additions/CHANGELOG.md`](additions/CHANGELOG.md) aggregates across additions per
release.

## 2. Releases

A **release** is a frozen manifest: a list of additions at exact versions,
published so that an implementer can say "we support `R1.0`" and both sides know
precisely what that means.

- Identified `R<major>.<minor>` — `R1.0`, `R1.1`, `R2.0`.
- **MINOR** — additions added, or pinned versions advanced within the same line.
- **MAJOR** — one or more additions in the manifest took a MAJOR bump, or an
  addition was removed from the set.
- **A published release is immutable.** Corrections ship as the next release. A
  published manifest is never edited except to add an erratum note pointing at its
  successor.
- Manifests live in [`additions/releases/`](additions/releases/).

## 3. Protocol target pins

Every addition records which upstream surfaces it targets and the date those
surfaces were last verified (`target_revision_checked`). AdCP and AAMP both move
quickly, so a pin going stale is expected and normal.

- Re-verifying with no semantic change → **MINOR** bump, new date.
- Upstream changed such that the mapping no longer holds → **MAJOR** bump, and the
  mapping document in [`mapping/`](mapping/) is corrected in the same change.
- An addition whose pin is more than ~2 upstream releases old should be treated as
  unverified regardless of its status.

## 4. Conformance claims

So that a seller agent can advertise what it implements, and a buyer agent can
reason about it, support is declared with these strings:

| Form | Meaning |
| --- | --- |
| `oohstd:R1.0` | Implements every addition in release R1.0 at the pinned versions |
| `oohstd:ADD-001@1.0` | Implements ADD-001, minor-compatible with 1.0 |
| `oohstd:ADD-001@1.0/partial` | Partial support — the addition's own "Partial conformance" section defines what may be omitted |

A claim of `oohstd:R1.0` with exceptions is written as the release claim plus
explicit per-addition claims that override it.

This is deliberately the same shape as the seller-capability advertisement in
[`mapping/aamp/agent-sdks-and-registry.md`](mapping/aamp/agent-sdks-and-registry.md):
the versioning scheme and the discovery mechanism should be one thing, not two.

## 4a. Checking consistency

The registry and the release manifests restate what the additions' front matter already
says, so they can drift. [`scripts/validate.py`](scripts/validate.py) checks that they
have not:

```
python3 scripts/validate.py
```

It verifies front matter, ID/file-name agreement, SemVer, the `stable` ≥ 1.0.0 rule,
registry agreement with front matter, release pins, and that every relative link
resolves. Run it before committing any change to an addition.

## 5. Relationship to proposals

| | Addition | Proposal (OEP) |
| --- | --- | --- |
| Answers | "What is the OOH requirement, precisely?" | "What change do we ask AdCP/AAMP to make?" |
| Versioned as | SemVer, ongoing | Status lifecycle, one-shot |
| Lifetime | Long — outlives any single upstream submission | Ends when accepted, rejected or superseded |
| Cites | `R-*` requirement IDs from `ooh-specifics/` | One or more `ADD-NNN@version` |

An addition can be submitted upstream several times, in different forms, as
different OEPs, without changing its own identity. That is the reason for keeping
the two concepts apart.
