import json
import urllib2
from bs4 import BeautifulSoup
from pprint import pprint

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

with open("scrape.json") as data_file:
    data = json.load(data_file)

#for trader in data:
# https://twitter.com/[screen_name]/profile_image?size=original

trader = data[0]
if not trader["social"]:
    print "-- " + trader["name"]
else:
    hastwitter = False
    lookupurl = ""
    for social in trader["social"]:
        if social["type"] == "twitter":
            hastwitter = True
            lookupurl = social["url"]
    if hastwitter:
        pagerequest = urllib2.Request(lookupurl, headers=headers)
        print lookupurl
        page = urllib2.urlopen(pagerequest)
        soup = BeautifulSoup(page, "html.parser")
        print soup
        # coverImage = soup.select("div.ProfileCanopy-headerBg > img")[0]["src"]
        avatarImage = soup.select("img.ProfileAvatar-image")[0]["src"]
        print avatarImage
        imgRequest = urllib2.Request(avatarImage, headers=headers)
        imgData = urllib2.urlopen(imgRequest).read()
        with open('images/' + slugify(trader["name"]) + '.jpg', 'w') as outfile:
            outfile.write(imgData)

        print avatarImage
