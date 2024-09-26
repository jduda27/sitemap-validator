import requests
import xml.etree.ElementTree as ET
import config

def loadSitemap():
    resp = requests.get(SITEMAPURL)
    with open('sitemap.xml','wb') as f:
        f.write(resp.content)

def binSearch(unsorted,key):
    middle = int(len(unsorted)/2)
    if len(unsorted) == 0:
        result = -1
    elif unsorted[middle] > key:
        result = binSearch(unsorted[:middle],key)
    elif unsorted[middle] < key:
        result = binSearch(unsorted[middle+1:],key)
        if result >= 0:
            result += middle+1
    else:
            result = middle

    return result

loadSitemap()

root = ET.parse("sitemap.xml").getroot()

sitemapURLs = []
for urlset in root:
    url = urlset[0].text
    sitemapURLs.append(url)


with open(COMPAREFILE) as f:
    lines = f.read().splitlines()

lines.sort()

noMatch = []
matched = []
for url in sitemapURLs:
    matching = binSearch(lines,url)
    if matching == -1:
        noMatch.append(url)
        print(url)
    else:
        matched.append(lines[matching])
