---
authors:
- "Lincoln Mullen"
categories:
- News
date: '2021-03-09T17:40:26Z'
draft: false
slug: releasing-a-web-monetization-module-for-omeka-s
tags:
- web monetization
title: Releasing a Web Monetization module for Omeka S
featured_image: Screen-Shot-2021-03-09-at-5.19.15-PM-2-1024x129.png
---

Today RRCHNM is announcing the release of a [module for Omeka S](https://github.com/chnm/WebMonetization-module) that will allow cultural heritage institutions to enable Web Monetization on their digital collections, so that users can stream micropayments for their support.

That was a lot of jargon. Let's back up a few steps.

First, a principle: We believe that cultural heritage institutions (like RRCHNM!) should align their mission with the users that they serve. It would be ideal, in other words, if what was financially good for an institution aligned with what was best for its constituents. It is very rarely the case, however, that providers of digital content are supported by their users. More often they have a different revenue stream. While this is not all bad, it can lead institutions to be funder-driven rather than mission-driven. And it does leave institutions vulnerable to the ebbs and flows of their funding.

Second, an opportunity: the economy around "content creators" in the past several years has changed rather dramatically. Where once it was the expectation that services or content would be provided for free, it is now understood that those services come with a cost (usually your privacy). But users and subscribers are now more willing now to support the people who provide the content they use: witness the growth of podcast memberships, Patreons, and the like.

Finally, a technology. [Web Monetization](https://webmonetization.org) is a JavaScript API that allows users to stream small payments to the websites that they visit. For example, if a user visits a museum website or an educational resource, then small amounts of money are paid to the website, if it has Web Monetization enabled. We see this as a potential way to connect cultural heritage institutions to their users, and allow users to automatically donate to the institutions they frequent.

Many cultural heritage institutions, including RRCHNM, use [Omeka S](https://omeka.org/s/) to host their collections. Our Web Monetization module allows them to enable these donations on their websites.

For example, an institution could add an unobtrusive banner at the top of the page, requesting that users support the site by enabling web monetization and providing a link with an explanation. Users can sign up for a [Coil account](https://coil.com/) to enable streaming payments.

{{< figure src="Screen-Shot-2021-03-09-at-5.19.15-PM-2.png" >}}

Users who already had Web Monetization enabled would then be able start sending automatic payments to the site whenever they browsed it. It is also possible to configure the module so that users with Web Monetization enabled will start donating automatically.

{{< figure src="Screen-Shot-2021-03-09-at-5.21.04-PM-1.png" >}}

The module offers a number of customization options, and it has been integrated into commonly used Omeka S themes.

We hope that this module will be of use to cultural heritage institutions. You can find it on both [GitHub](https://github.com/chnm/WebMonetization-module) and the [Omeka module repository](https://omeka.org/s/modules/WebMonetization/). The module was created by Jim Safley and Kim Nguyen, with an assist in testing from God's Will Katchoua. The module was created thanks to [Grant for the Web](https://www.grantfortheweb.org), which funded its development.

It is still early days for this technology, but we think it offers a great deal of promise for connecting cultural heritage institutions to their users, and for users to become supporters. In a future post, we will explain how we are rolling it out to RRCHNM websites, and how we are encouraging our users to support us in this way.
