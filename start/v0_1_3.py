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

all_tags = soup.find_all(True)

all_tag_names = [tag.name for tag in all_tags]
print(all_tag_names)

all_unique_tag_names = {tag.name for tag in all_tags}
print(all_unique_tag_names)

