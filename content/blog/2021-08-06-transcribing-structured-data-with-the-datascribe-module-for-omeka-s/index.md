---
authors:
- Janet Hammond
categories:
- Post
date: '2021-08-06T10:10:56Z'
description: DataScribe is an Omeka S module that helps ease laboriously detailed
  transcription work. Created at RRCHNM and funded by the NEH, this module allows
  users to complete…
draft: false
lastmod: '2022-03-25T21:59:46Z'
slug: transcribing-structured-data-with-the-datascribe-module-for-omeka-s
title: Transcribing Structured Data with the DataScribe Module for Omeka S
featured_image: image-1.jpeg
---

by Janet Hammond

DataScribe is an Omeka S module that helps ease laboriously detailed transcription work. Created at RRCHNM and funded by the [NEH](https://www.neh.gov/), this module allows users to complete a two-step process. The **first**is to craft transcription forms for structured data, which is particularly useful when transcribing historical forms and other highly structured documents. ([Greta Swain’s write up](https://religiousecologies.org/blog/deploying-datascribe-to-create-a-new-dataset-for-american-religious-history/) on *American Religious Ecologies*’ bloggoes into detail about this process.) **Then**, professionals can use these forms to transcribe data into a format amenable to computational analysis, combining the data creation and data cleaning steps of a project into a single process. This blog post focuses on the second step.

As a Digital History Fellow at the Center, I transcribed the Bills of Mortality for the project, [*Death by Numbers*](https://deathbynumbers.org/). The bills were weekly London publications that accounted for where individuals died and why (Figure 1).  Other information includes the price of bread and the number of christenings. Focusing on the years 1603 to 1752, this project aims “to transcribe and publish the information in these bills in a dataset suitable for computational analysis.”

{{< figure src="image.jpeg" alt="Bill of mortality listing number of deaths in each London parish" >}}

{{< figure src="image-1.jpeg" alt="Bill of mortality listing all causes of death in a week and number of people who died of each cause" >}}

Figure 1. [These images](https://luna.folger.edu/luna/servlet/detail/FOLGERCM1~6~6~632260~142055?qvq=q%3Amortality%3Bsort%3Acall_number%2Cauthor%2Ccd_title%2Cimprint%3Blc%3AFOLGERCM1~6~6&mi=1&trs=12) are examples of how the Bills of Mortality usually appear. On the left is the front that states the city, the week number, the dates, the year, and the parishes. On the right is the back of a bill that, among other things, shows causes of death and the number of people attributed with each type. Image sources: Folger Shakespeare Library under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).

To ensure the sources’ presence in DataScribe, I first made items in Omeka S, employing [CSV](https://omeka.org/s/docs/user-manual/modules/csvimport/)imports. This plugin transfers spreadsheets filled with the primary source images’ metadata to the suitable format for individual items in this online platform. According to identifying information, I uploaded the corresponding photos to each item. (If images are public online, you can include URLs in the spreadsheet, foregoing the last measure.) With the sources present, Dr. Jessica Otis created the DataScribe form that I could use for transcription.

The DataScribe transcription webpage can appear in a variety of manners. Users can choose the arrangement that best suits their screens, data, sources, and more. Figure 2 displays the automated perspective with the image on the left, entry field in the middle, and a column for notes or other special notations on the far right. Figure 3 shows it in “focus mode,” which eliminates the far-right column. Pictured a bit further down, Figure 4 reflects one of my personal preferences where the image is on the top with data entry below. In the latter option, I felt that, for this project, I could zoom in closer and pan across the page with greater ease.

{{< figure src="image-5.png" alt="screenshot of datascribe interface showing image to be transcribed and data entry boxes" >}}

Figure 2. Screenshot of DataScribe with the primary resource on the left, the entry field boxes in the middle, and a special actions column on the far right. Bill of Mortality Image Rights: CC-BY Wellcome Collection.

{{< figure src="image-4.png" alt="image of datascribe screen interface in focus mode showing just image and entry boxes" >}}

Figure 3. Screenshot of DataScribe with “focus mode” enabled, which eliminates the far-right column seen in Figure 2. Bill of Mortality Image Rights: CC-BY Wellcome Collection.

Historians—particularly digital historians—discuss the frustration of web applications that lack flexibility, as these scholars infrequently possess readily clean data. As seen in Figure 4, the primary historical sources need not contain strict consistency. The bills possessed a number of causes of death but usually limited the list to those relevant. For instance, there were no canker deaths January 19-26, 1668. As a result, I used the “is missing” feature to indicate that it was inapplicable that week. When information is present but difficult to understand—whether the handwriting turns too sloppy or water damage occurred—people can provide their best guess and mark “is illegible” to signal that reviewers need to especially look over this section.

{{< figure src="image-3.png" alt="screenshot of datascribe interface showing extreme zoom on image" >}}

Figure 4. Screenshot of DataScribe with the primary resource listed above and boxes below to indicate whether a cause of death is listed or legible. It also depicts navigation features like “Guidelines.” Bill of Mortality Image Rights: CC-BY Wellcome Collection.

When the data is unclean, it might seem unrealistic to invite a wide variety of transcribers. With DataScribe, project managers (or the like) can avoid confusion with the “Guidelines” tool (Figure 5). This feature is editable and permits the project lead to add instructions as needed.

{{< figure src="image-2.png" alt="screenshot of transcription guidelines, showing text detailing transcription process" >}}

Figure 5. This screenshot displays the portal that appears when individuals click on “Guidelines” in the*Death by Numbers* project.

If the Guidelines lacks necessary instructions, transcribers can make personalized notes to the reviewer (Figure 6).  This feature avoids the need to toggle back and forth between messages over email, Slack, or other systems and the transcription page. People can also “flag” the record by checking the box next to “Needs review.”

{{< figure src="image-1.png" alt="screenshot of DataScribe interface showing where to insert transcriber notes"  caption="Figure 6. This screenshot shows where transcribers can add notes or check the box, 'Needs review.'" >}}

Successful organization of historical data not only benefits from a tailor-made transcription form but continued flexibility for transcribers to uniquely respond. DataScribe offers “flexible structure” for the project leads to craft the model and for the participants to fill it out.

When complete, people can download a CSV version of the data. Users can export a file of all validated data, which allows anyone to computationally analyze it. This tool encourages shared data as well as a method for others to readily take advantage of such opportunities.
