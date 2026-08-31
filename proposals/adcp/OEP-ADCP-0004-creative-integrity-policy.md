# OEP-ADCP-0004: Creative integrity policy

| | |
| --- | --- |
| **Status** | `draft` |
| **Target protocol** | AdCP |
| **Target surface** | Creative; `enums/creative-event-reason-code.json` |
| **Target revision** | 3.2.0-beta.8, checked 2026-08-27 |
| **Additions** | [`ADD-009@0.2.0`](../../additions/adcp/ADD-009-creative-integrity-and-caching.md) |
| **Requirements** | `R-CRE-*` (pending) |
| **Placement** | **Core** — applies to any human-reviewed, cached creative |
| **Created** | 2026-08-27 |
| **Upstream issue/PR** | — |

## Summary

Where a seller reviews a creative before it may run, it must guarantee that the asset
which played is the asset that was approved. Sellers do this by caching the file and
treating any later swap as fraud. AdCP has a full approval lifecycle but **no concept of
asset integrity**: no declared caching authority, no creative identity rule, no
mutability policy, and no way to report an integrity violation distinguishably from a
content rejection.

This proposal adds a `creative_integrity` policy declaration, an optional
`asset_digest` on submitted assets, and one new reason-code value.

## Motivation

Ströer's model, in production:

- On first submission Ströer downloads the media file from the advertiser's host
  **once** and thereafter serves it from Ströer's own cache when the creative wins. All
  other trackers are preserved.
- Any swap of the MediaFile or MediaFileURL is *"detected and treated as fraudulent
  behavior"*, causing immediate rejection of the DSP creative.
- Every permutation must be a separate creative with a **new creative ID** and a
  **unique media file name**.

This is a sound integrity model and it is entirely invisible in the protocol. It
survives as folklore: *"Do not override existing creatives. Set up new creatives always
(new name & creative ID) to avoid caching related issues."*

Two things make this urgent for agentic buying rather than merely untidy:

1. **It inverts the digital default.** Rotating a creative URL behind a stable ID is
   routine and expected in digital. An agent reasoning from digital defaults will
   violate the rule *by doing the normal thing*.
2. **The failure is a fraud flag, not a validation error.** The creative is rejected as
   fraudulent, mid-campaign, and the buyer's remedy — resubmit under a new identity —
   is completely different from the remedy for a content rejection. An agent cannot
   choose the right remedy because it cannot tell the two apart.

The concern is not OOH-specific. It applies wherever an asset is human-reviewed then
cached: cinema, broadcast, and any regulated placement.

## Current behaviour

AdCP 3.2 has a mature approval lifecycle and nothing underneath it about the bytes.

| What exists | Where | Why insufficient |
| --- | --- | --- |
| `creative-approval-status`: `pending_review`, `approved`, `partially_approved`, `rejected`, with `approval_scopes` and `rejection_reason` | `enums/creative-approval-status.json` | Models the *decision* well. Says nothing about what the decision is bound to, or what invalidates it |
| `creative-status`: `processing`, `pending_review`, `approved`, `suspended`, `rejected`, `archived` | `enums/creative-status.json` | Lifecycle states; no integrity concept |
| 17 `creative-event-reason-code` values, incl. `review_failure`, `policy_revocation`, **`content_drift`**, `takedown_request`, `processing_failure` | `enums/creative-event-reason-code.json` | `content_drift` is the nearest — but it is defined as the *landing page or referenced content* changing after approval, **not the media asset itself**. There is no value for "the approved bytes were replaced" |
| `sync_creatives`, `list_creatives`, `creative-status-changed-webhook`, `creative-purged-webhook` | `creative/` | Submission and notification exist and are the right carriers for this |
| `audit-observation.json` | `creative/` | Non-blocking governance observations — explicitly "not rejection grounds by themselves", so not a fit for a hard integrity failure |
| `identity_authorization_revoked` / `_expired` | reason codes | Proves an authorisation-with-expiry pattern exists (relevant to ADD-010, not to integrity) |

**There is no content hash, checksum, digest or fingerprint anywhere in the creative
schemas.** Grepped across `static/schemas/source/` — hashing appears only in
governance, compliance, protocol and registry contexts, never on a creative asset.
Verified absent from AAMP as well.

## Proposal

**Change type:** `new-object`, `add-field`, `extend-enum`.

### Part A — integrity policy on the product or creative agent

```json
{
  "$id": "/schemas/core/creative-integrity.json",
  "title": "Creative Integrity Policy",
  "description": "How the seller guarantees that the asset which serves is the asset that was approved. Declared where creative approval is required.",
  "type": "object",
  "properties": {
    "asset_authority": {
      "type": "string",
      "enum": ["seller_cached", "buyer_hosted", "either"],
      "description": "seller_cached: the seller fetches once and serves its own copy, which is authoritative at play time. buyer_hosted: the asset is fetched from the buyer's host at play time."
    },
    "identity": {
      "type": "array",
      "description": "The properties which together identify an approved creative. Changing any of them creates a new creative requiring new approval.",
      "items": {
        "type": "string",
        "enum": ["creative_id", "asset_url", "asset_file_name", "asset_digest"]
      }
    },
    "immutable_after_approval": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Fields that MUST NOT change once approved. Changing one is an integrity violation, not an update."
    },
    "mutable_after_approval": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Fields that may change without re-approval, e.g. impression trackers."
    },
    "violation_outcome": {
      "type": "string",
      "enum": ["reject", "suspend", "reject_and_flag"],
      "description": "reject_and_flag indicates the seller records the event against the buyer, not merely the creative."
    },
    "mutation_authorisation_available": {
      "type": "boolean",
      "description": "Whether an authorisation exists permitting asset rotation (e.g. for dynamic creative). See ADD-010."
    }
  },
  "required": ["asset_authority"],
  "additionalProperties": false
}
```

### Part B — asset digest

Add an optional `asset_digest` to submitted creative assets:

```json
{
  "asset_digest": {
    "type": "object",
    "properties": {
      "algorithm": { "type": "string", "enum": ["sha256"] },
      "value": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
    },
    "required": ["algorithm", "value"]
  }
}
```

A content digest is a **better creative identity than a file name.** Ströer's
unique-filename requirement is a workaround for not having one: it makes identity
depend on a convention the buyer must remember rather than on the bytes themselves. A
digest lets a seller detect a swap deterministically, lets a buyer prove it did not
swap, and removes the need for filename discipline entirely.

### Part C — reason code

Add to `enums/creative-event-reason-code.json`:

```
"asset_integrity_violation": "The approved media asset was replaced or its
  content changed after approval. Distinct from content_drift, which concerns a
  landing page or referenced content rather than the asset itself. Recovery:
  submit as a new creative with a new identity; the existing creative cannot be
  restored by reverting the asset."
```

The recovery sentence is the point. A buyer agent receiving `review_failure` should
alter the artwork; receiving `asset_integrity_violation` it must instead resubmit under
a new identity. Same status, different remedy — and today indistinguishable.

### Normative rules

1. A seller declaring `asset_authority: seller_cached` MUST declare `identity`.
2. A seller MUST NOT report an integrity violation as a generic rejection once
   `asset_integrity_violation` is available.
3. Where `asset_digest` is supplied on submission and the seller declares
   `identity` including `asset_digest`, the seller SHOULD verify it at fetch time and
   fail the submission — not the campaign — on mismatch.
4. A buyer agent MUST NOT assume that replacing an asset behind a stable creative ID is
   permitted. Absent a declared policy it SHOULD treat assets as immutable after
   approval.

Rule 4 makes the safe assumption the default, which is the inverse of today's digital
convention and the entire reason this proposal exists.

## Examples

A seller that caches and keys identity on ID plus content:

```json
{
  "creative_integrity": {
    "asset_authority": "seller_cached",
    "identity": ["creative_id", "asset_digest"],
    "immutable_after_approval": ["asset_url", "asset_digest", "duration", "dimensions"],
    "mutable_after_approval": ["impression_trackers", "click_trackers"],
    "violation_outcome": "reject_and_flag",
    "mutation_authorisation_available": true
  }
}
```

Submission:

```json
{
  "creative_id": "brand-q4-10s-1080x1920-v1",
  "assets": [{
    "url": "https://cdn.example.com/brand-q4-10s-portrait-v1.mp4",
    "asset_digest": { "algorithm": "sha256", "value": "e3b0c44298fc1c149afbf4c8996fb924…" }
  }]
}
```

A buyer agent reading the policy knows before submitting that it must register one
creative per permutation, that rotation needs authorisation, and that a swap will be
flagged against it — rather than learning this from a fraud rejection mid-flight.

## Why core and not an OOH extension

The trigger is any **human review followed by caching**, which is not an OOH property.
Cinema, broadcast and regulated categories share it. And the mechanism has to sit
alongside `creative-approval-status` and the reason-code enum in core — Part C is
literally an enum value in a core file, which an extension cannot provide.

## Alternatives considered

| Alternative | Why not |
| --- | --- |
| **Do nothing** | Agents will keep doing the normal digital thing and keep getting fraud-flagged. The cost lands on the buyer's reputation with the seller, not just on one creative. |
| Reuse `content_drift` | Defined as landing-page or referenced-content change. Overloading it would merge two failures with different remedies — the exact ambiguity this proposal removes. |
| Reuse `audit-observation` | Explicitly non-blocking and "not rejection grounds by themselves". An integrity violation is blocking. |
| Digest only, no policy object | The digest detects swaps but does not tell a buyer the rules *before* submitting — which is where the value is. |
| Policy only, no digest | Workable, and leaves identity resting on filename conventions. The digest is the part that makes identity portable across sellers. |
| Make `asset_digest` required | Too strong for a first step; some buyers cannot compute it at submission. Optional, with sellers free to require it via `identity`. |

## Compatibility

- **Fully backwards compatible.** All three parts optional; absent means today's
  undeclared behaviour.
- Adding an enum value is additive; consumers not recognising it fall back to a generic
  rejection reason, which is the status quo.
- Rule 4 changes recommended *buyer* behaviour, not wire format. It is stricter than
  today's convention, deliberately — the current default is unsafe on this inventory.
- Sellers already enforcing anti-swap start describing existing behaviour.

## Market applicability

Evidenced in **Germany** (Ströer, DOOH). The cache-and-verify model is asserted to be
general wherever creative is human-reviewed before public display, **not verified
against a second seller**. Whether Ströer additionally fingerprints content, or relies
solely on `(creative_id, file name)`, is unresolved
([`../../analysis/open-gaps.md`](../../analysis/open-gaps.md)) — Part B proposes the
digest as the better identity regardless.

## Privacy and compliance

None. A content digest of an advertising asset carries no personal data. It has a mild
integrity benefit for regulators: a seller can demonstrate that the asset which ran in
public is the asset that was cleared.

## Open questions

- [ ] Should `asset_digest` support algorithms beyond SHA-256? One algorithm is simpler
      and avoids downgrade ambiguity; a second may be needed for very large files.
- [ ] Does the policy apply per asset or per creative when a creative has several
      assets (a sync group, a multi-part manifest)?
- [ ] How long is a cached asset retained, and does resubmitting the same identity
      trigger a re-fetch? Seller-specific, but may deserve a field.
- [ ] Should `violation_outcome: reject_and_flag` be visible to the buyer at all? It
      discloses that the seller keeps a record — arguably it should, so the buyer knows
      the stakes.
- [x] ~~Does AdCP's C2PA / provenance machinery already cover this?~~ **Checked — no
      overlap.** `c2pa-watermark-action`, `embedded-provenance-method` and
      `digital-source-type` classify **how content was produced** (AI involvement,
      aligned with the IPTC `digitalsourcetype` vocabulary) and whether a watermark is
      cryptographically bound to a C2PA manifest. That is authorship provenance, not
      identity binding between an approved asset and a served one. The two are
      complementary: a C2PA manifest says *who made this and how*, `asset_digest` says
      *this is the exact artefact that was approved*. Worth noting in the proposal that
      a seller already consuming C2PA manifests may be able to derive a digest from
      one — but the manifest is optional and removable, so it cannot replace the field.
