from urllib.request import Request
from urllib.request import urlopen

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
                  'Safari/537.36'
}

url = "https://en.wikipedia.org/wiki/2.0_(film)"

try:
    req = Request(url, headers=headers)
    resp = urlopen(req)
    # print(resp)
    # print(type(resp))
    html_bytes_page = resp.read()
    # print(html_bytes_page)
    html_page = html_bytes_page.decode("utf-8")
    # print(html_page)
except Exception as e:
    html_page = ""
    print(e.__str__())

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_page, "html.parser")

noise_tags = ["script", "style", "noscript", "link", "meta", "nav", "footer", "form", "input", "button", "label"]

# risky tags to remove but okay in our case
# noise_tags.extend(["header", "head"])  # are keeping the title tag

# removing media and wrappers
noise_tags.extend(["img", "picture", "source", "figure", "figcaption"])

for tag in soup(noise_tags):
    tag.decompose()

"""
        <div class="noprint" id="siteSub">
         From Wikipedia, the free encyclopedia
        </div>
"""

for other_noise in soup.select('div.noprint'):
    other_noise.decompose()

for citation_sup in soup.select('sup.reference, sup.mw-ref, sup[typeof="mw:Extension/ref"]'):
    citation_sup.decompose()

tags_to_unwrap = ["span", "b", "i", "sup", "abbr", "cite", "q", "a"]

for tag in soup(tags_to_unwrap):
    tag.unwrap()

# 1. Locate the References section (or heading)
cutoff = soup.select_one('section[aria-labelledby="References"], h2#References')

if cutoff:
    # 2. If it matched the inner <h2>, step up to the outer <section> wrapper
    #    so we don't leave an empty <section><div class="mw-heading"> behind
    if cutoff.name != "section" and cutoff.find_parent("section"):
        cutoff = cutoff.find_parent("section")

    # 3. Destroy every tag that appears after this <section> in the HTML
    for next_tag in list(cutoff.find_all_next()):
        next_tag.decompose()

    # 4. Destroy the References <section> itself
    cutoff.decompose()

for no_name in soup.select('div.infobox-caption'):
    no_name.decompose()


for text in soup.find_all(string=lambda t: t and t.strip() == "Jump to content"):
    text.extract()


for the_tag in soup.select("div.vector-dropdown-content"):
    the_tag.decompose()

for the_tag in soup.select("div.vector-search-box-vue"):
    the_tag.decompose()

# SMOOTH: Merge adjacent text strings created by unwrapping
soup.smooth()

with open("cleaned_page.html", "w", encoding="utf-8") as page:
    page.write(soup.prettify())