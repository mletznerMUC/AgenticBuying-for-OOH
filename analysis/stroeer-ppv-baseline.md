# Ströer Public Video — baseline inventory of proprietary additions

Everything in the analysed documents that is **not** plain OpenRTB 2.5 / VAST, or
that is plain OpenRTB used to mean something the standard did not intend.

Ströer SSP declares itself OpenRTB 2.5 compliant and states the explicit design
goal of leveraging "as much of the existing OpenRTB 2.5 specification, with as
little extensions or modifications as possible" (v6 §1). The list below is what
that minimum turned out to be.

Each row names the addition in [`../additions/`](../additions/) that carries it.

---

## 1. Audience and billing basis

| Concept | Encoding | Source |
| --- | --- | --- |
| Forecast audience per opportunity | `imp[].ext.totalaud` — float, "the total number of viewers in the audience" | v6 §4 |
| Confirmed audience at play time | `${TOTAL_IMP}` macro — "replaced with a rational number of the actual Total Audience Impressions when the creative is played, thus confirming the billing impression" | v6 §4 |
| Play chain identity | `1 DSP Impression = 1 Master Play * n Screens Plays * n Total Audience Impressions` | v6 §3 |
| Billing formula, computed by the DSP | `(${TOTAL_IMP} * ${AUCTION_PRICE}) / 1000` | v6 §4 |
| Reporting obligation | DSP must report Total Audience Impressions "on all user facing reports and dashboards"; buyer sets CPM on the one-to-many basis in the DSP UI | v6 §4 (CPM/Impressions) |

Notable properties: the audience figure is a **float**, not an integer (`118.63105`,
`119.4702`, `35.1624`), and it is a **forecast at bid time that is restated at play
time** — the number the buyer is billed on does not exist when the bid is made.

→ **ADD-001** (Total Audience Impressions), **ADD-002** (play chain)

## 2. Delivery timing

| Concept | Encoding | Source |
| --- | --- | --- |
| Play confirmation delay | Up to **10 minutes** between bid response and impression URL call; "80% of all the plays are confirmed < 3 minutes" | v6 §4 (Pacing & ooH Latency) |
| Cause | Creatives pre-loaded by players with slow, unreliable, restricted or absent internet access; players may be unable to report impressions directly | v6 §4 |
| Pacing consequence | "Do not use asap pacing"; even pacing required; PG pacing is done by the SSP | v6 §4, §9 |
| Aggregation model | Ströer SSP aggregates play confirmations from slave players (v6 Fig. 1) | v6 §4.1 |

→ **ADD-003** (delayed play confirmation and settlement)

## 3. Venue, network and location

| Concept | Encoding | Source |
| --- | --- | --- |
| Ströer network taxonomy | `networkid` two/three-letter codes: `inf` Infoscreen, `sv` Station, `mv` Mall, `cc` Cinema, `cs` City, `ct` City Tower, `elv` Elevator, `ret` Retail, `rss` Roadside, `gou` Giant Outdoor, `gin` Giant Indoor, `sce` Scene | v6 §6 table |
| Standard venue taxonomy | `device.ext.dooh.venuetypeid` (e.g. `106`) | Static Creatives, pp. 4–5 |
| Location as a synthetic domain | `site.domain` / `site.page` = `{sitename.cleaned}-{city.cleaned}-{networkid}.de`, e.g. `duesseldorfhbf-duesseldorf-sv.de`, `stuttgarthbf-stuttgart-sv.de`, `ekzalstertaleinkaufszentrumhamburg-hamburg-mv.de` | v6 §4, code examples |
| Transparency tiers | `transparent` → full site-city-network domain **plus** lat/lon and other geo fields; `semi-transparent` → `{city.cleaned}-{networkid}.de`; `intransparent` → `{networkname.cleaned}.de` | v6 §4 (Location Targeting) |
| Geo object | `lat`, `lon`, `type` (required, defaults to 3 "user provided"), `country` ISO-3166-1-alpha-3, `region` ISO-3166-2, `city` as UN/LOCODE (`DESTR`, `DEHAM`), `utcoffset` | v6 §5 table |
| Time zone caveat | Germany is CET/CEST; DSP account time zone must match to avoid serving at the wrong local time | v6 §9 |

Notable: the transparency tier is a **commercial** decision that changes the
**schema fidelity** of the request. Location is not a field, it is a string to be
parsed, and its parseability depends on what the buyer paid for.

→ **ADD-004** (venue & network taxonomy), **ADD-005** (location disclosure tiers)

## 4. Creative formats and landlord restrictions

| Concept | Encoding | Source |
| --- | --- | --- |
| Static-only inventory | Bid request carries **only** `image/jpeg`, `image/png` (`image/bmp` in examples) in `video.mimes`; image+video inventory carries both sets | Static Creatives pp. 1, 3 |
| Reason for the restriction | "Based on the rules set by the publisher landlords some time only static creatives (jpeg/png) are allowed — especially when the screens are next to the road" | Static Creatives p. 1 |
| Affected networks | As of August 2022: PV Roadside, PV City, PV City Tower, PV Giant | Static Creatives p. 1 |
| Never restricted | Infoscreen, Station Video, Mall Video show standard video mimes only | Static Creatives pp. 1, 3 |
| Cinemagraph | Some Roadside screens allow "Cinemagraph" animation only — technically MP4 but with animation limits | Static Creatives pp. 1, 3 |
| Static option 1 — image in video object | `video` object always present; VAST response with ImageURL in `MediaFile`, **exactly one** ImageURL per VAST, explicit duration, w/h, full tracking events, VAST mimeType matching the file | Static Creatives p. 1 |
| Static option 2 — banner object | `banner` **and** `video` objects present; response uses `iurl`; file type conveyed via the `iurl` link's `Content-Type` metadata; **duration agreed at deal creation and inserted manually by Ströer**; trackers in `bid.ext.imptrackers` with both `${TOTAL_IMP}` and `${AUCTION_PRICE}` | Static Creatives p. 3, p. 6 |
| Resolution pairs | 1080×1920 (9:16 portrait) and 1920×1080 (16:9 landscape) | code examples |
| Duration bounds | `minduration` / `maxduration` per request; observed `1`/`3600` on Mall sync, `10`/`30` and `10`/`10` on static examples | code examples |

Notable: a **legal/contractual restriction imposed by a landlord** is communicated
to the buyer as a mime-type list. Nothing in the request says *why*, or that the
restriction is stable, or which network it belongs to.

→ **ADD-006** (creative format constraints and media-type restriction)

## 5. Synchronised multi-screen delivery

| Concept | Encoding | Source |
| --- | --- | --- |
| Sync group | One bid request with **two** `imp` entries, same `tagid` (`84288`), one 1080×1920 and one 1920×1080, both `sequence: 1` | v6 §7.1 |
| Response obligation | Both impressions answered in one response, each with its own creative (`A2-9-16_...`, `A1-16-9_...`), same `cid`, same `dealid` | v6 §7.2 |
| Test case | "Two items on one request and response compliance; one 16:9 and one 9:16 in sync group" | DSP Integration, PG Deal Test |
| Buyer-side note | "Mall Video dual creative setup" listed as a DOOH specific to check with the DSP rep | v6 §9 |

Notable: the coupling between the two impressions — that they are one physical
moment on adjacent screens and must both be won — is expressed only by shared
`tagid` and `sequence`, which OpenRTB does not define as a synchronisation contract.

→ **ADD-007** (synchronised multi-screen delivery)

## 6. Creative approval

| Concept | Encoding | Source |
| --- | --- | --- |
| Mandatory pre-broadcast review | Manual **and** automatic review of all creatives; "Only approved creatives can broadcast in public" | Creative Approval |
| Legal basis | Legal and regulatory requirements; "special safety standards" for public display | Creative Approval |
| Approval key | Approval is bound to the **DSP creative ID**; every creative must be tied to exactly one | Creative Approval, v6 §8 |
| SLA | "can take up to 48 hours" (Creative Approval one-pager) / "may take up to 24 hours" (v6 §9) — see [open-gaps.md](open-gaps.md) | both |
| Status channels | Creative Pre-Approval API, or auction win- and loss-notifications | Creative Approval |
| Pre-approval API | Submission and status calls, single or bulk; access token required from Ströer SSP rep | v6 §8 |
| Approval buckets | `Standard Creative with Caching` (default) or `Dynamic Creative for DCO` | Creative Approval |

→ **ADD-008** (creative approval lifecycle and SLA)

## 7. Creative integrity and caching

| Concept | Encoding | Source |
| --- | --- | --- |
| Cache-once model | Ströer downloads the mp4/jpg/png from the advertiser's file host **once**, then serves it from Ströer cache on winning bids; all other trackers preserved | Creative Approval |
| Anti-swap enforcement | Any swap of the MediaFile or MediaFileURL is "detected and treated as fraudulent behavior", causing immediate rejection of the DSP creative | Creative Approval |
| Permutation rule | Every permutation must be a separate DSP creative, with a **new DSP creative ID** and a **unique MediaFile filename** | Creative Approval |
| Buyer guidance | "Do not override existing creatives. Set up new creatives always (new name & creative ID) to avoid caching related issues" | v6 §9 |

→ **ADD-009** (creative integrity and caching)

## 8. Dynamic creative authorisation

| Concept | Encoding | Source |
| --- | --- | --- |
| The conflict | DCO rotates the MediaFileURL in the VAST, which the anti-swap rule classifies as fraud | Creative Approval |
| Authorisation token | A `DCO-ID` issued by Ströer, applied by the buyer **to the file name** of every DOOH creative file; Ströer reads it from the file name and serves from the ad server file host instead of cache | Creative Approval |
| Process | (1) enrolment and compliance declaration at least **three weekdays** before campaign start; (2) hand over mockups and concept; (3) Ströer approves and issues the DCO-ID **by e-mail**; (4) buyer applies it to file names | Creative Approval |
| Also gated | "Swapping creative files on the VAST creatives commonly used for Dynamic Creative Rendering (DCR) requires prior case by case approval ... plus an issued valid access token" | v6 §8 |

Notable: an authorisation grant is transported as a substring of a file name, and
issued over e-mail. This is the single clearest example of a concept with no home in
the protocol.

→ **ADD-010** (dynamic creative authorisation)

## 9. Compliance declarations

| Concept | Encoding | Source |
| --- | --- | --- |
| Creative compliance declaration | Buyer declares compliance with "provisions of trade and industry law, the regulatory authorities and the requirements of the laws for the protection of youths" | v6 Appendix (Accreditation), Creative Approval (DCO enrolment) |
| When | At accreditation, and again at DCO enrolment | both |
| Form | Out of band — part of accreditation paperwork and e-mail | both |

→ **ADD-011** (compliance declaration and youth protection)

## 10. Advertiser separation

| Concept | Encoding | Source |
| --- | --- | --- |
| Loop separation | "Ströer SSP prevents advertiser from looping on public video screens" | v6 §4 |
| Signalling | Standard `badv` (advertiser domains) and `bcat` (IAB content categories); "DSP bidder may listen to the badv or bcat attribute to refrain from sending bids who can't win" | v6 §4 |

Notable: an OOH-specific competitive-separation rule is enforced server-side and
communicated through generic block lists. The buyer cannot see the rule, only its
effect on which bids lose.

→ **ADD-012** (advertiser loop separation)

## 11. Deal access model

| Concept | Encoding | Source |
| --- | --- | --- |
| No open auction | `pmp.private_auction: 1`; "Bids on PPV are only considered for deals as indicated in the bid request, ie., no open auction bids are considered" | v6 §4 |
| Guaranteed flag | `pmp.deals[].ext.guaranteed: 1` | Static Creatives pp. 4–5 |
| Fixed price | `deals[].at: 3` (fixed price), `bidfloor` + `bidfloorcur: EUR` | code examples |
| PG obligation | "Programmatic Guaranteed buyer must answer every bid request with a valid response"; DSP must "bid on every bid request with valid bid" | v6 §9, DSP Integration |
| Access tiering | "Fix price deal and private auction only" | v6 §9 |
| Request identification | UA always `Mozilla/5.0 (PPV; X11; Linux armv7l) AppleWebKit/537.42 ... Safari/537.42`; `publisher.id` `17409` production / `17387` sandbox; `imp.ext.totalaud` present only on PPV traffic | v6 §5 |

→ **ADD-013** (deal access and guaranteed response obligation)

## 12. Accreditation, insertion order and settlement

| Concept | Encoding | Source |
| --- | --- | --- |
| Accreditation prerequisite | Required in advance; covers billing registration, creative compliance declaration, DCR instruction | v6 Appendix |
| Framework IO | "Buying Ströer Public Video pDOOH requires a framework insertion order", issued by Ströer sales | v6 Appendix |
| Contracting | Ströer SSP contract, amendment, or registration as Nautilus debtor if DOOH only | DSP Integration |
| **Any deal contingent on an IO** | "Any deal is contingent upon the issuance of an initial IO (Insertion Order) by Ströer Digital Media (SDM) through Ströer sales" | DSP Integration |
| Floor price derivation | Based on the Public Video price list plus upgrades; customisable by **transparency level, audience pre-filtering and estimated budget** | v6 Appendix |
| Deal setup | Seat setup and test, deal setup (private auction or fixed price), creative approval, deal monitoring | v6 Appendix |
| Invoicing | Issued from Ströer SSP transactional data within **three business days** of month end; recipient is the client/agency directly, or the DSP on request (must be requested before deal start) | v6 Appendix, DSP Integration |
| Advanced reporting | Loss notification reports, ad play reports, in-depth location reports, available on request from operations | v6 Appendix |

Notable: **programmatic execution sits inside a paper contract.** The IO is the
gate, and the floor price is a function of the transparency tier. Any agentic model
that treats pDOOH as self-serve is wrong about this market.

→ **ADD-014** (accreditation, insertion order and settlement)

## 13. Planning vocabulary

| Concept | Source |
| --- | --- |
| "Apply ooH planning tactics in order to generate a meaningful advertising pressure (**Share of Voice, OTP, GRP, Dwell time**)"; with small budgets, focus on location targeting | v6 §9 |
| Whitelist planning: read the bid stream or request a domain list; set up a fallback line item to catch new stations/malls added to the portfolio | v6 §9 |

Notable: the seller tells buyers to plan on SOV/GRP/OTP/dwell — none of which any
programmatic field expresses. The planning vocabulary and the transaction
vocabulary are disjoint.

→ **ADD-015** (OOH planning metrics in briefs and offers)

## 14. Onboarding and conformance testing

The DSP Integration document is effectively a **conformance suite**, phased
Discovery → Negotiation → PG deal test (on PV Mall) → PA deal test (on PV Roadside):

| Phase | Test |
| --- | --- |
| Discovery | Spec review and Q&A; billing instructions and forms |
| Negotiation | Framework contract / implementation media order / Nautilus debtor registration |
| PG on PV Mall | Creative pre-approval round trip: rejection → resubmit → approval (token needed) |
| PG on PV Mall | Creative approval: VAST inspection, pDOOH creative specs, caching & DCO approval |
| PG on PV Mall | Multi-format bidding: two items on one request/response, 16:9 + 9:16 in sync group |
| PG on PV Mall | DOOH impression variance check: impressions from the VAST substitution macro |
| PG on PV Mall | Pacing: PG pacing by SSP; DSP bids on every request with a valid bid |
| PG on PV Mall | Creative targeting A/B: creative set A on Mall A, set B on Mall B |
| PA on PV Roadside | Static creative compliance: bid image when request is image-only, video when either is allowed |
| PA on PV Roadside | DSP pacing: no overspend on the UAT test private auction |

A sandbox environment exists (`publisher.id 17387`) and is used for this.

→ **ADD-016** (seller conformance profile and test plan)

## 15. Fields used against their standard meaning

Worth calling out separately, because these are the strongest argument for a
product-layer representation rather than more transport extensions:

| Field | Standard meaning | Used here for |
| --- | --- | --- |
| `site.domain` / `site.page` | The web page the ad appears on | A physical screen's identity, city and network, encoded as a fake hostname |
| `site` object at all | A website | A digital screen in a public place |
| `user.id` | A user identifier | Populated with a hash (`f39e2f3a...`) in a channel with no identifiable user |
| `device.devicetype: 6` | Connected device | A DOOH player |
| `device.ua` | Browser user agent | A signal that this is PPV inventory |
| `video` object | A video ad slot | Always present, even for image-only inventory |
| `imp.instl: 1` | Interstitial | A full-screen public display |
| MediaFile **file name** | A file name | A DCO authorisation token (`DCO-ID`) |
| `badv` / `bcat` | Buyer-side block lists | Seller-side loop-separation rules the buyer cannot read |

→ argues the case in **ADD-001**, **ADD-004**, **ADD-005**, **ADD-010**; see also
[`../ooh-specifics/09-privacy-and-identity.md`](../ooh-specifics/09-privacy-and-identity.md)
for the `user.id` point.
