---
authors:
- Savannah Scott
categories:
- Post
date: '2025-08-25T15:40:25Z'
draft: false
lastmod: '2025-08-25T15:40:26Z'
slug: graduate-student-reflections-sustainability-summer
title: 'Graduate Student Reflections: Sustainability Summer'
featured_image:
lede: PhD student Savannah Scott reflects on the challenges of flattening the 98,000-item 9/11 Digital Archive into a static site and building search for it.
tags:
- Research + Tools
- Teaching + Learning
- Sustainability
---

<aside>Savannah is a PhD student at George Mason University and a Graduate Research Assistant at RRCHNM.</aside>

This past summer I had the opportunity to work on RRCHNM’s sustainability team. Our work focused on flattening [websites built with content management systems (CMS)](https://sustainabledh.org/blog/scott-static-search/), such as Drupal, Omeka, and WordPress. Flattening refers to the process of simplifying dynamic, database-backed websites to static versions built with only HTML, CSS, and JavaScript. This minimizes server space and reduces security risks. However, flattening comes with trade-offs, such as losing dynamic features like a search function. One of my main roles this summer was creating a [static site search](https://sustainabledh.org/blog/building-static-search/) for these flattened websites.

The process of flattening websites and implementing static site search varies by CMS and size of the website. This summer, one website posed several challenges to our team: the [9/11 Digital Archive](https://911digitalarchive.org/). The 9/11 Archive was built to capture memories, media, and materials related to the September 11 terrorist attacks. The project began in 2002, and crowdsourced materials for nearly two decades before [closing submissions](https://911digitalarchive.org/news/index.html%3Fp=270.html). Since 2014 the digital archive has operated with Omeka and holds over 98,000 items. The sheer size of this website would be a test for our flattening and static site search workflows.

By far, the biggest challenge of working with the 9/11 Digital Archive was creating a static copy of the website. A flattened version of a website can be created using the command line tool wget. Wget can recursively create a mirror of a website on a local machine by crawling through a website’s directories. Due to the size of the 9/11 Digital Archive, our original wget command ran for about a week straight. This was frustrating, as my work had to pause while I waited for the download to finish. My laptop’s storage capacity was also a concern since we did not know how large or how many files would download. Eventually, the download was completed.

Or so we thought. As I was testing the static site search locally, I noticed that my search results were different from the live site for the same term. This was curious, as the page’s content should have been captured by the search index. After looking at the search index and then searching for the files on my computer, I realized that wget had missed an item. Moreover, it had missed multiple items in a collection (though not all). This was troubling. Like a physical archive, digital archives take measures to ensure the preservation and protection of their collections. The personal nature of items in the 9/11 Digital Archive, as well as the national significance, heightened the importance. Because of the size of the archive, it was impossible for me to manually check which files were missing. It could have been the five or so I noticed, or it could have been five hundred or five thousand. We needed to flatten the website again. To add to the problem, we could not figure out why wget missed the file, or how to prevent them from being skipped again. I ran another round of wget with modified flags, and it continued for a week with no end in sight. After no progress, the sustainability team decided to run the wget on RRCHNM’s servers under the guidance of our systems administrator to avoid storage and temporal constraints.

The original wget copy, while incomplete, allowed me to work on the website, specifically the search feature. Deciding which directories to exclude from the search index (to avoid duplicate items in our search results) prompted another question: what to do with Omeka’s alternative formats? Omeka has the option to export an item’s page as a variety of alternative formats, such as json, csv, etc. While this is an asset for users, it also creates thousands of more files to be stored, as each of the 98,000 has seven other copies in different file formats. Did the benefit of these files outweigh the amount of server space they require? Should these alternative formats be included in the search results? Ultimately, we decided to include the option for alternative formats on the webpages but not include them in the search results. This preserves the functionality of the original website but optimizes the search function.

Another issue I tackled was the volume of search results. Because of the number of items in the archive, a query can return hundreds of results. To deal with this, I created a pagination feature to break up the results into subpages for a more manageable experience for the user. MiniSearch returns the search results in an array. To paginate the results, I created subgroups of this array to display based on a set results-per-page and added buttons for navigation. This allowed users to traverse the search results more easily.

The 9/11 Digital Archive tested our sustainability workflow. It exposed the fickleness of wget, and the limitations of out-the-box MiniSearch. After confronting these challenges, our sustainability workflow is more robust and can tackle websites of any size and scale. My sustainability summer exposed me to the importance of prioritizing longevity with website design, and I will carry this to my future digital projects.
