# OOH specifica

**What is genuinely different about Out of Home**, expressed as requirements an
agentic advertising protocol has to satisfy.

This directory is descriptive. It says what OOH is and what it needs. It does not
say where in AdCP or AAMP that belongs — that is [`../mapping/`](../mapping/) — and
it does not contain proposed schema text — that is [`../proposals/`](../proposals/).

## Documents

| # | Document | Core question |
| --- | --- | --- |
| 01 | [Inventory & supply model](01-inventory-and-supply-model.md) | How do you describe a network of screens, frames and loops? |
| 02 | [Trading & pricing models](02-trading-and-pricing-models.md) | How do you price a play, a share of voice, or a panel-week? |
| 03 | [Audience & measurement](03-audience-and-measurement.md) | Whose impression number is it, and how is it derived? |
| 04 | [Targeting dimensions](04-targeting-dimensions.md) | Geospatial, venue and temporal targeting as first-class citizens |
| 05 | [Creative & formats](05-creative-and-formats.md) | Format specs, silence, multi-frame, dynamic triggers, print |
| 06 | [Delivery & proof of play](06-delivery-and-proof-of-play.md) | What does "delivered" mean without an ad server impression? |
| 07 | [Availability & booking lifecycle](07-availability-and-booking-lifecycle.md) | Reservations, calendars, lead times, cancellation terms |
| 08 | [Compliance & content restrictions](08-compliance-and-content-restrictions.md) | Landlord rules, municipal law, category separation |
| 09 | [Privacy & identity](09-privacy-and-identity.md) | A channel with no user identity — and what that simplifies |
| 10 | [Sustainability](10-sustainability.md) | Energy and emissions per play as a buying criterion |

## Document shape

Each document follows the same structure so it can be reviewed and mapped
mechanically:

1. **Question this document answers**
2. **How OOH works** — the observable reality
3. **Why the digital-first assumption breaks** — the specific mismatch
4. **Requirements** — numbered `R-<area>-<n>`, each one testable
5. **Open questions**
6. **Related** — links to the mapping documents that carry these requirements

Requirement IDs are stable once published. `mapping/` and `proposals/` cite them,
so renumbering breaks references.
