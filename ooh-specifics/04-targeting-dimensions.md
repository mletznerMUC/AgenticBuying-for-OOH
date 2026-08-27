# 04 — Targeting dimensions

> Status: **stub** — outline only.

**Question this document answers:** what does an OOH agent need to express when it
targets, given there is no user to target?

## What this document will cover

- [ ] Geospatial: point plus radius, polygon, isochrone/drive-time, catchment area
- [ ] Administrative geography: country, region, city, district, postcode
- [ ] Proximity: distance to a POI set (stores, competitors, stadiums, clinics)
- [ ] Venue-type targeting and exclusion using a shared taxonomy
- [ ] Temporal: dayparts, days of week, calendar periods, campaign flighting
- [ ] Contextual and trigger-based: weather, temperature, air quality, transit
      status, event schedules, sports results, stock or price feeds, countdowns
- [ ] Screen and network inclusion/exclusion lists
- [ ] Environmental constraints: indoor/outdoor, operating hours, illumination
- [ ] Combining targeting with capacity: a targeting expression that resolves to
      fewer screens than the budget requires

## Why the digital-first assumption breaks

Digital targeting models treat geography as a coarse filter and have no vocabulary
for drive-time catchments, venue taxonomies or weather triggers. In OOH these are
the primary targeting levers, not extras.

## Requirements

`R-TGT-1` … *to be written.*

## Open questions

- How precise should geospatial targeting be allowed to get before it becomes a
  privacy or a competitive-disclosure concern?
- Do trigger conditions belong in targeting, in creative selection, or both?
- Should targeting be expressible as a query the seller resolves, an explicit screen
  list, or either?

## Related

- [`../mapping/adcp/media-buy.md`](../mapping/adcp/media-buy.md)
- [`../mapping/adcp/signals.md`](../mapping/adcp/signals.md)
- [`../mapping/aamp/artf.md`](../mapping/aamp/artf.md)
