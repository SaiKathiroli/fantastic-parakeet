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

# --- OPTION A: Uncomment these 2 lines ONLY if you want to REMOVE the Infobox table ---
# for infobox in soup.select("table.infobox"):
#     infobox.decompose()

# 1. Remove citation superscripts ([1], [a], etc.) and hidden spans BEFORE unwrapping
for noisy_el in soup.select('sup.reference, sup.mw-ref, [style*="display:none"], [style*="display: none"]'):
    noisy_el.decompose()

# 2. Remove noisy tags (Removed "head" so <title> is actually kept!)
noise_tags = [
    "script", "style", "noscript", "link", "meta",
    "nav", "footer", "form", "input", "button", "label",
    "header", "img", "picture", "source", "figure", "figcaption"
]

for tag in soup(noise_tags):
    tag.decompose()

# 3. Unwrap inline formatting tags (kept "sup" for real superscripts like km²)
tags_to_unwrap = ["span", "b", "i", "sup", "abbr", "cite", "q", "a"]

for tag in soup(tags_to_unwrap):
    tag.unwrap()

# 4. Merge adjacent text strings created by unwrapping
soup.smooth()

with open("cleaned_page.html", "w", encoding="utf-8") as page:
    page.write(soup.prettify())