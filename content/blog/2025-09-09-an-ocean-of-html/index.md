---
title: "An Ocean of HTML"
date: 2026-09-09T15:00:00Z
draft: false
slug: an-ocean-of-html
author_name: "Alexandra Miller"
authors:
  - "Alexandra Miller"
categories:
  - post
featured_image: image4.webp
lede: "Graduate Research Assistant Alexandra Miller reflects on building a Twine game to teach students about the cosmopolitan world of ports and ships in the age of sail."
tags:
  - games
  - teaching + learning
  - research + tools
---

My job is worldbuilding. Well, that's not quite accurate. My job is recovering the world as it was in the age of sail.

For the past year my job at RRCHNM has been to write my own game, ["Learning the Ropes"](https://1812shipping.rrchnm.org/), using a free, open-source program called [Twine](https://twinery.org/). The platform allows users to write create-your-own-adventure-style text-based games using HTML, CSS, and JavaScript. Before pitching my own game, I spent a year revising another Twine game: ["Gaming the Great Plague"](https://jmotis.github.io/GamingtheGreatPlague). These are a part of the [RRCHNM Games](https://games.rrchnm.org/) project.

## Writing a Game from the Archives

Writing a game like "Learning the Ropes" means constructing a playable game world from the archives.

The game is set around the year 1812. In the game, players build a character, enter the merchant marine, sail the world encountering the waves of good and bad fortune, and spend time in port. The game's intended educational outcome is to teach students about the cosmopolitan world of ports and ships in an era of globalization.

What this means on the practical level is that to write an introduction to a character and get them on a ship going somewhere, I had to do a lot of reading. I needed to identify the major ports in this period for British merchant traders, plot the sailing distance between each of them, identify what the most popular merchant vessels were, find the names of every British merchant vessel sailing in the period of this game (fortunately there is a [website featuring every merchant ship ever embarked](https://threedecks.org/index.php?display_type=ships_search)), calculate the standard merchant marine wages for sailors with varying ethnicities and levels of experience and trade knowledge, and, most time consuming of all, research what names would be most common for male and male-presenting people of every ethnicity/national origin combination possible in the game.

![](/media/blog/an-ocean-of-html/image1.webp)

![](/media/blog/an-ocean-of-html/image2.webp)

*In these screenshots, the player has created a character who is a young adult Black man from Canton, China who knows no trade and has no experience as a sailor. Players start by building a character, choosing their national origin, age, gender, city of origin, dependents, knowledge of a trade, experience on a ship, ethnicity, motivation for joining a sailing crew, and objective in first speaking to a captain (passage, work, lodging).*

When players first open the game, they are greeted by a landing page welcoming them to the game world and guiding them through creating a character.

![](/media/blog/an-ocean-of-html/image3.webp)

*This is the landing page of Learning the Ropes. Players begin by creating a character before commissioning with a ship and sailing.*

## Building the World at Sea

But the game is not limited to creating a character, and leaving port to sail entailed much more research. To write the at sea portion of the narrative, I first investigated shipboard conditions and sailor experiences. I read several sailing memoirs, most notably Richard Henry Dana's *Two Years Before the Mast*, and I curated a description of what sailing life and work looked like. From there, I wrote a narrative across six months of a sea voyage. In the first month players embark on their voyage and settle into tasks depending on their level of experience and knowledge of a trade. The rest of the months proceed with brief descriptions of what kind of work they have been doing, what kind of recreation they found, and, in a few passages, instances of discord between other sailors or between the crew and captain. Each passage varies in language depending on player role and experience, as well as choices.

I also compiled a list of random events which might befall a sailor at sea or in town and wrote four versions of each. For example, characters have a 1 in 20 chance of encountering another ship. If that chance triggers, then players have a 1 in 5 chance of seeing another ship at a great distance, seeing another ship within hailing distance, being flagged by a British naval ship for impressment, being visited by a small whaling ship for medical assistance, and being pursued by American privateers.

For each variation in every random event, I conducted research into how the event would have felt and been treated by sailors. I also did some research for color. For example, if a privateer ship or navy ship pursues your vessel, you learn the name of that ship. I found a [list of every British naval vessel at work in this period](https://sites.rootsweb.com/~pbtyc/18-1900/Index.html) and used that for the navy ship's name, and I found a [list of every American vessel licensed for privateering](https://www.1812privateers.org/United_States/index.html) and used that to generate the navy and privateer ship names. As an easter egg, because there was a naval vessel sailing a few decades after the game period named the Alexandra (that's me!), I included a painting of that ship which would appear if its name were randomly generated.

![](/media/blog/an-ocean-of-html/image4.webp)

*H.M.S. Alexandra, Flag ship of Vice Admiral G.T.P. Hornby, Mediterranean. 1874. National Maritime Museum, Greenwich, London.*

## Probability, Testing, and Continuous Improvement

These events in the game are triggered randomly. I assigned probabilities for the events based on my judgement of how often they might actually have occurred and an effort to not let these random occurrences distract too much from the main storyline. For example, I wanted to know the frequency of mutiny attempts (and successes). I discovered that in the revolutionary period immediately preceding the setting of this game there was a rash of mutinies. Historians estimated that as many as [1 in 3](https://www.cambridge.org/core/journals/international-review-of-social-history/article/mutiny-and-maritime-radicalism-in-the-age-of-revolution-an-introduction/185D39851961E731B92A0CE80F759892) ships had an attempted mutiny. Assuming that the unrest would have abated by the early nineteenth century and yet not have faded entirely amid ongoing Atlantic revolutions, I initially set the mutiny random chance at 1 in 10. This was later decreased to 1 in 15 based on feedback from game testing. Many of the random chances were initially set at 1 in 10 and have subsequently been decreased. Death, for example, has now been set at 1 in 20 based on gameplay feedback in which players complained that they were dying too often.

## Growing the Game

The game continues to grow and change. As I read more about the age of sail and conducted my own dissertation research on city spaces, I added random details. I learned for example that the first [sidewalks](https://granta.com/products/wanderlust/) in the modern era appeared in London in 1665–1666, during the setting of "Gaming the Great Plague." I added sidewalks to a passage in which a character avoids being run over in the street. In "Learning the Ropes" I added [elixir of vitriol](https://www.routledge.com/Rough-Medicine-Surgeons-at-Sea-in-the-Age-of-Sail/Druett/p/book/9780415924528) as a failed cure for scurvy after becoming curious about the origins of carbonated water.

## Reflections on Historical Games

Doing this work has made me more conscious of how little of a world we can represent in words alone. As much as I strive to recreate a holistic playable world, I remain very aware of all the aspects of historical experience which can never be conveyed here. But I have also grown convinced that historical games are significant (and fun!) tools for thinking historically. Games are an effective way to explore the past as lived and a tool for finding the limits of historical interpretation.
