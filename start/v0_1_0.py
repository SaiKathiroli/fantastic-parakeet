from urllib.request import urlopen

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
                  'Safari/537.36'
}

page = urlopen("https://en.wikipedia.org/wiki/2.0_(film)")

print(page)
print(type(page))