import json
from dataclasses import dataclass
from typing import Optional, List

from bs4 import BeautifulSoup
from urllib.request import Request
from urllib.request import urlopen

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
    "Safari/537.36"
}

url = "https://en.wikipedia.org/wiki/2.0_(film)"

# request = Request(url=url, headers=headers)

try:
    request = Request(url=url, headers=headers)
    response = urlopen(request)
    html_bytes = response.read()
    html_page = html_bytes.decode("utf-8")
except Exception as e:
    print(e.__str__())
    raise Exception("Unknown Error as Occurred")


@dataclass
class DocumentMetadata:
    """Strict data contract for every ingested Wikipedia document."""

    wikidata_id: Optional[str]
    title: str
    canonical_url: str
    # headline: Optional[str]
    date_published: Optional[str]
    date_modified: Optional[str]
    categories: List[str]


soup = BeautifulSoup(html_page, "html.parser")

"""
https://docs.google.com/document/d/10jKPeJ36NlUFvQmQUMdFIusOWuyHu5N14swG3euYGxQ/edit?tab=t.0
"""

# script_tag = soup.find('script[type="application/ld+json"]') --> Wrong - returned None

script_tag = soup.find("script", type="application/ld+json")

print(script_tag)

if script_tag and script_tag.string:
    data = json.loads(script_tag.string)
    print(data)
else:
    data = {}

"""
Write a try/except or if/else fallback: if JSON-LD is missing, pull title from <h1 id="firstHeading"> and url from 
<link rel="canonical">.
"""

heading_tag = None
link_tag = None

if script_tag is None:
    heading_tag = soup.find("h1", id="firstHeading")
    link_tag = soup.find("link", rel="canonical")

wikidata_id = data.get("sameAs")
title = data.get("name")
url = data.get("url")
date_published = data.get("datePublished")
date_modified = data.get("dateModified")

if title is None:
    title = heading_tag.string

if url is None:
    url = link_tag.string

# 1. Find the specific div
target_div = soup.find(name="div", id="mw-normal-catlinks")

categories = []

# 2. Check if the div actually exists on the page to avoid errors
if target_div:
    # 3. Loop through and print the specific <a> tags
    for x in target_div.select("ul li a"):
        categories.append(x)

document = DocumentMetadata(
    wikidata_id, title, url, date_published, date_modified, categories
)

print(str(document))
