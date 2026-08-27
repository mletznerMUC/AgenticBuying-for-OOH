# Open gaps and inconsistencies in the source documents

Recorded so that nothing in [`../additions/`](../additions/) rests on an assumption
without saying so.

## 1. Sources that could not be retrieved

Both live specification URLs were unreachable from the environment this analysis ran
in — the network egress policy refused the connection (`403 CONNECT tunnel failed`)
for both hosts. They were not fetched, and nothing in this repository is derived
from them.

### `https://creative.api.adscale.de/v1/docs` — Creative Pre-Approval API

Needed to complete **ADD-008** (creative approval lifecycle). Specifically:

- [ ] Endpoints and HTTP methods for submission, bulk submission and status polling
- [ ] Request and response schemas, field names and types
- [ ] Authentication mechanism (the guide says an access token from a Ströer SSP rep)
- [ ] The **approval status enum** — the exact set of states a creative can be in
- [ ] **Rejection reason codes**, if any exist, and whether they are machine-readable
- [ ] Whether approval is queried per creative ID, per batch, or by campaign
- [ ] Rate limits and recommended polling interval
- [ ] Whether the API exposes the approval bucket (`Standard Creative with Caching`
      vs `Dynamic Creative for DCO`) and the DCO-ID lifecycle
- [ ] Whether the API is per-market or global, and whether it is versioned

The rejection reason codes matter most: an agentic protocol needs a machine-readable
rejection taxonomy for a buyer agent to act on a rejection without a human reading
prose.

### `https://specs.myadscale.de/dsp-adapter/external/1.0.html` — DSP adapter spec

Needed to confirm the transport bindings recorded across all additions:

- [ ] Whether `imp.ext.totalaud` is documented there with the same name and type
- [ ] The full set of Ströer `ext` objects beyond `totalaud`, `dooh.venuetypeid`,
      `deals[].ext.guaranteed`, `bid.ext.imptrackers`, `bid.ext.avn`, `bid.ext.agn`
- [ ] The complete substitution-macro list (only `${TOTAL_IMP}` and
      `${AUCTION_PRICE}` appear in the PDFs)
- [ ] The win-notification schema — the PDF example shows `uuid`, `p`, `tpid`, `id`,
      `iid`, `impid`, `userid`, `buyeruid`, `bidid`, `dealid`, `seat`, `crid`, `t`,
      `win`, none of which are defined anywhere in the analysed documents
- [ ] Loss-notification codes, and whether creative-approval status is conveyed
      through them as the Creative Approval document implies
- [ ] Whether the adapter is OpenRTB 2.5 only, or whether a 2.6 / AdCOM path exists
      (this decides whether **ADD-004** and **ADD-005** should target the OpenRTB 2.6
      `dooh` object rather than the `site` workaround)

**To fill these in:** paste the content, attach an export, or run the analysis from a
network where those hosts are reachable. Until then, every affected addition carries
`status: draft` and an explicit note.

## 2. Internal inconsistencies

| # | Inconsistency | Sources | Impact |
| --- | --- | --- | --- |
| 1 | **Creative approval SLA**: "can take up to 48 hours" vs "may take up to 24 hours" | Creative Approval one-pager and v6 Appendix B say 48h; v6 §9 Best Practice says 24h | Directly affects **ADD-008**. A buyer agent planning a campaign start needs one number. Recorded as "up to 48 h" with the discrepancy flagged, because the 48 h figure appears twice and in the normative document rather than the best-practice list. **Needs confirmation.** |
| 2 | **DCO lead time vs approval SLA**: DCO enrolment requires "at least three weekdays prior to campaign start", which is longer than either approval SLA | Creative Approval | Two different lead times govern the same campaign start. **ADD-008** and **ADD-010** must both express lead time, and an agent needs to know they compose (take the maximum), not that one supersedes the other. |
| 3 | **`maxduration` values**: `3600` on the Mall Video sync-group example vs `10`–`30` on the static-creative examples | v6 §7.1 vs Static Creatives pp. 4–5 | A 3600-second maximum duration is almost certainly a placeholder or an unconstrained default rather than a real slot length. If slot duration is genuinely not communicated in the request, **ADD-006** has to say so — it changes what a buyer agent can validate before bidding. |
| 4 | **Static creative duration**: option 1 (video object) requires the DSP to declare duration in the VAST; option 2 (banner object) has the duration "agreed at the time of creating the deal/campaign and inserted manually later by us" | Static Creatives pp. 1, 3 | The same physical play has its duration set by the buyer in one binding and by the seller out-of-band in the other. **ADD-006** must model duration as a negotiated property of the offer, not a property of the creative. |
| 5 | **Page-count mismatch**: the v6 guide's internal footers read "Page n/9" while the file has 11 pages | v6 | Cosmetic, but it suggests the appendices were bolted on and may be maintained separately from the core guide. Worth confirming there is no missing section. |
| 6 | **`image/bmp`** appears in the code examples' mime lists but never in the prose, which consistently says "jpeg/png" | Static Creatives pp. 1, 3 vs 4–5 | Minor, but **ADD-006** should not enumerate supported types from the examples alone. |
| 7 | **Affected-networks list is dated** "In August 2022" | Static Creatives p. 1 | Four years stale at the time of analysis. The static-only network set in **ADD-006** must be treated as an example, not a fact, and the addition should require the restriction to be discoverable per screen rather than hard-coded per network. |
| 8 | **Geo `type` default**: the geo table says `type` defaults to `3` ("User provided (e.g. registration data)") and the examples confirm `"type": 3` | v6 §5, code examples | For a fixed physical screen the location is surveyed, not user-provided. There is no OpenRTB `type` value that means "fixed installation", which is itself a finding for **ADD-005**. |

## 3. Questions for Ströer

Answers to these would change the shape of the additions, not just their detail:

1. **Is `totalaud` a forecast for the specific play, or an average for the screen/daypart?**
   This decides whether **ADD-001** models it as a prediction with a confidence
   interval or as a published rate card figure.
2. **What is the audience methodology behind `totalaud`?** The guide says "based on
   geospatial datasets". Which currency, which version, and is it comparable to the
   German market currency? **ADD-001** cannot specify provenance fields without this.
3. **Is the ±variance between `totalaud` and `${TOTAL_IMP}` bounded?** The DSP
   integration plan has a "DOOH Impressions Variance Check" test but names no
   tolerance. A buyer agent needs to know the expected variance to pace and to
   validate settlement.
4. **Can a sync group be partially won?** If a DSP answers only one of the two
   impressions, what plays? **ADD-007** needs the failure semantics.
5. **Is the transparency tier discoverable before a deal exists?** If the tier is set
   in the IO, a buyer agent cannot know at brief time what location fidelity it will
   receive — which is precisely what **ADD-005** has to fix.
6. **Are there OOH-specific loss-notification codes?** In particular, does a bid lost
   to advertiser loop separation (**ADD-012**) look different from a bid lost on
   price?
7. **What is the IO's machine-readable form, if any?** **ADD-014** assumes there is
   none today. If a structured order or deal object exists, the IO binding should
   target it rather than inventing one.
8. **Which OpenOOH venue taxonomy version** does `device.ext.dooh.venuetypeid`
   follow, and is the mapping from Ströer `networkid` to venue type published
   anywhere? **ADD-004** needs it.
