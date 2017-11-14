import re
import json
import urllib2
from bs4 import BeautifulSoup

def cleanstring(mystring):
    mystring = mystring.strip()
    mystring = mystring.replace("\n", "")
    return re.sub(" +", " ", mystring)

domain = "http://boroughmarket.org.uk"
directoryurls = [domain + "/traders?p={}".format(i) for i in range(1,29)]
traderurls = []
jsondata = []

for url in directoryurls:
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    for article in soup.find_all("article"):
        traderurls.append(domain + article.find_all("a")[1]["href"])


for url in traderurls:
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser", from_encoding="utf-8")
    data = {}
    # print url
    data['url'] = url
    data['name'] = cleanstring(soup.select("h1.article-header__heading")[0].text)
    data['summary'] = cleanstring(soup.select("p.article-header__profile")[0].text)
    data['description'] = cleanstring(soup.select("article > p")[0].text)
    openingtimes = []
    for item in soup.select("ol.trader-meta__open-days li"):
        openingtimes.append(cleanstring(item.text))
    data['openingtimes'] = openingtimes 
    socialmedia = []
    socialtype  = re.compile("meta__social__link--(.*)")
    for item in soup.select("ul.trader-meta__social a"):
        socialmediaitem = {}
        socialmediaitem["url"] = item["href"]
        classstring = " ".join(item["class"])
        m = socialtype.search(classstring)
        socialmediaitem["type"] = m.group(1)
        socialmedia.append(socialmediaitem)
    data["social"] = socialmedia
    jsondata.append(data)

with open('scrape.json', 'w') as outfile:
    outfile.write(json.dumps(jsondata, ensure_ascii=False, indent=4).encode("utf-8"))
