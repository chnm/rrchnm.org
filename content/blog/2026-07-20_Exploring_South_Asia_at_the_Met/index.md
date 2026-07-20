---
title: "South Asia Collections at The Met: A Preliminary Computational Look"
authors:
  - "Deepthi Murali"
date: 2026-06-14
publishDate: 2026-07-20
draft: false
slug: exploring-south-asia-at-the-met-through-data
categories:
  - post
tags:
  - digital humanities
  - museums
  - data
  - metadata
  - south asia
  - art history
lede: "A preliminary computational analysis of 5,000+ MET objects reveals how South Asian art entered the collection — who donated it, when, and what happens to it now."
featured_image: met-south-asia-timeline.png
---

Originally published at https://www.deepthimurali.com/art-history-and-data/south-asia-at-the-met

---

Museum metadata is messy metadata (and sometimes, also, just messy in non-computational ways.) But museum metadata is also historical archive that scholars and the public alike ignore.

Every object in a museum collection arrives with a story attached — a donor's name, a date, a department assignment, a classification. Individually, these are administrative details: the bureaucratic residue of how an object got from somewhere else to a vitrine, a storage shelf, or a database entry. But at scale, across thousands of objects and more than a century of acquisitions, these details become historical data. They become a record of *how* an institution decided what South Asia was, who got to decide that, and when those decisions were made.

This post shares three preliminary visualizations from an ongoing project analyzing The Metropolitan Museum of Art's open-access metadata for objects associated with India — 5,291 records in total, spanning accessions from 1881 to 2023. The goal isn't to evaluate individual objects (that's a separate, object-by-object art-historical task) but to ask a different kind of question: what patterns emerge when you treat the *collection itself* as a primary source? Who built it, in what proportions, through what mechanisms, and what happened to the objects once they arrived?

Some of the digital artifacts below are "clickable" and you can interact with them.

**Please do not reproduce text or image from this post without explicit written permission.**

## 1. The Timeline: Who Was Collecting, and When?

{{< observable notebook="5a641adc46e15e8c" version="19" cell="container" height="676" apikey="85122c689efca86d4bf014327ce1064f0d52c02e" title="Met South Asia accessions timeline, 1881–2023, by collector" >}}

The visualization above is an interactive stacked bar chart showing every accession year from 1881 to 2023, with eight named collectors highlighted against the broad category of "all other objects." Clicking any collector's button isolates their contribution against the timeline and opens a detail panel with further information about that collection.

What this view makes immediately visible is something that's easy to lose when reading object records one at a time: collecting at the MET happens in *pulses*, not a steady drip. Most years see a handful of objects entering from a long tail of individual donors, bequests, and small purchases — this is the gray "all other objects" layer, which itself represents roughly 300 distinct sources. But periodically, a single source delivers a large block of objects in one or two years, and these blocks are where most of the collection's defining character actually comes from.

## 2. The Detail View: How Objects Enter, and What They Bring

{{< observable notebook="5a641adc46e15e8c" version="77" cell="collectorViz" height="474" apikey="85122c689efca86d4bf014327ce1064f0d52c02e" title="Acquisition mechanism and object classification by collector" >}}

The detail panel that appears when you click a collector on the visualization above does two things side by side: it shows the *mechanism* by which that collection's objects entered (gift, bequest, museum-fund purchase, direct purchase), and it shows the *classification profile* of what they brought (sculpture, paintings, codices, jewelry, textiles, and so on).

This pairing turns out to be more revealing than either piece of information alone, because acquisition mechanism and object type are not independent — they're entangled with each other and with the historical moment in ways that map onto recognizable collecting cultures.

The Eilenberg collection, for instance, is overwhelmingly Gift (231 objects) and Bequest (111), with only 17 objects purchased — and overwhelmingly Sculpture (237) and Metalwork (99). This is the profile of a *connoisseur*: someone who built a personal collection over decades through the market, then transferred it to an institution as an act of philanthropy rather than the institution acquiring it directly.

## 3. The Visibility Gap: What Happens After an Object Arrives

{{< observable notebook="5a641adc46e15e8c" version="85" cell="southAsiaSankey" height="587" apikey="85122c689efca86d4bf014327ce1064f0d52c02e" title="Flow of 4,521 objects across departments and display vs. storage" >}}

The third visualization above steps back from *how objects entered* to ask a different question: *where are they now?* It's a flow diagram tracing all 4,521 objects from their departmental homes — Asian Art, Islamic Art, Musical Instruments, European Sculpture and Decorative Arts, Arms and Armor, Costume Institute, and a residual "other departments" category — into one of two destinations: on display in a gallery, or in storage.

The numbers here are stark. Of 4,521 objects, only 581 — about 13% — are currently on display. The remaining 3,940, or roughly 87%, exist for the visiting public only as database records (to the extent that they're searchable at all).

## What This Adds Up To

None of these three visualizations, on its own, makes a complete argument. But together, they sketch the outline of a much larger claim: that a museum's collection metadata is an accumulated record of decisions about what to accept, from whom, through what channel, classified under what name, and ultimately shown to whom. Together, further analysis of this metadata provides both a history of collecting South Asia at The Met and contributes to the institutional history of The MET across time at a granular level.

This is a preliminary post, and these are preliminary visualizations. The next steps for this project involve digging into the donor data further. There's also the question of how representative The MET is of North American collecting patterns more broadly, which would require bringing comparable open-access datasets from other institutions into the same framework. More on both of those soon.

*This post is part of an ongoing project using open-access museum metadata to study the history of South Asian object collecting in North American museums. Data: Metropolitan Museum of Art Open Access initiative, filtered for objects associated with South Asia.*

> ***Please do not use any material, text or image, from this blog post without explicit written permission.***
