# Readability Scraper

**Purpose**: Scrape bookmark links out of
[Readability](https://www.readability.com) via web interface.

**Warning**: I have closed my Readability account. I am therefore unable
to help with any issues you might have. I nonetheless hope you find this
project helpful.

Table of Contents

1. [Background](#background)
2. [Installation](#installation)
3. [Using the Scraper](#using-the-scraper)

## Background

I'm a big fan of Readability, and have been using the service for years.
Unfortunately, Readability announced on August 31st of 2016 that they
would be closing down their bookmarking service on September 30.

To ease transitioning away from the service, Readability advertised
their export tool. Despite multiple attempts to use it before September
30th, I was unable to export my bookmarks. 

Once October came around, things were looking bleak: I couldn't export,
the API had shutdown, and support wasn't responding to my emails.

Luckily, the web interface still lists my bookmarks! My final resort
was thus to write this scraper.

If you too had trouble exporting your bookmarks, or simply didn't have a
chance to do so in September, this project should be able to help you.

## Installation

Requirements:

- Python 3.5
- Pip

Create a virtual environment, and install the depencies defined by the
project with `pip`.

    $ pip install -r requirements.txt

## Using the Scraper

The scraper uses the [Scrapy](https://scrapy.org/) project, and may be
invoked from the command line. You will need your Readability username
and password.

    $ # replace USERNAME and PASSWORD in command below
    $ scrapy crawl readability -a username="USERNAME" -a password="PASSWORD" -o links.json

The output of the scraper is JSON, and it maintains the structure it
finds the links in: 20 links per page. It also notes whether the page
was a standard page or an archived page.

While this may be desirable to have this format, it is probably more
desirable to have a flat list of all of the links available. The
`flatten_link_results.py` script will take JSON output found in a file
named `links.json` and will output a flat file with a URL on each line,
named `links.txt`. It assumes the names of these files, and takes no
arguments, as demonstrated in the code below.

    $ python flatten_link_results.py
