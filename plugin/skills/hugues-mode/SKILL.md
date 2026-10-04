---
name: hugues-mode
description: "Run the read-only huguesStack WP1 loader probe. Mobile routing follows in WP2."
disable-model-invocation: true
---

# hugues-mode loader probe

Return exactly these two lines, then stop:

```text
HUGUESSTACK_WP1_LOADER_PROBE_7F3A91C2
WP2 routing is unimplemented.
```

Treat every invocation as a loader probe, including requests for mobile work.
Use no tools and make no changes. Implementation, delegation, routing and
consumer proof belong to WP2 and later packages.
