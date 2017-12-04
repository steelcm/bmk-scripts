import json
import re
import requests
import StringIO
from PIL import Image
from urllib2 import urlopen, URLError, HTTPError
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

def dlfile(url, filename):
    # Open the url
    try:
        r = requests.get(url)
        i = Image.open(StringIO.StringIO(r.content))
        rgb_im = i.convert('RGB')
        rgb_im.save(filename)
        print "Downloaded {0}...".format(url.encode('utf-8'))
        return True
    #handle errors
    except:
        print "Failed to download {0} to {1}".format(url.encode('utf-8'), filename)
        pass
    return False
        

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

with open("scrape.json") as data_file:
    data = json.load(data_file)

for trader in data:
# https://twitter.com/[screen_name]/profile_image?size=original

# trader = data[8]
    if not trader["social"]:
        print "-- " + trader["name"].encode('utf-8')
    else:
        hasInstagram = hasFacebook = hasTwitter = False
        instagramURL = facebookURL = twitterURL = ""
        regexp = '^https?://(www\.)?{0}\.com/(#!/)?([^/?]+)'
        for social in trader["social"]:
            try:
                if social["type"] == "twitter":
                    m = re.search(regexp.format("twitter"), social["url"])
                    twitterURL = "https://avatars.io/twitter/{0}".format(m.group(3))
                    hasTwitter = True
                if social["type"] == "facebook":
                    m = re.search(regexp.format("facebook"), social["url"])
                    facebookURL = "https://avatars.io/facebook/{0}".format(m.group(3))
                    hasFacebook = True
                if social["type"] == "instagram":
                    m = re.search(regexp.format("instagram"), social["url"])
                    instagramURL = "https://avatars.io/instagram/{0}".format(m.group(3))
                    hasInstagram = True
            except:
                pass

        avatarurl = ""
        if hasInstagram:
            avatarurl = instagramURL
        elif hasTwitter:
            avatarurl = twitterURL
        elif hasFacebook:
            avatarurl = facebookURL

        if dlfile(avatarurl, "images/{0}.jpeg".format(trader["id"])):
            trader['avatarUrl'] = "assets/imgs/avatars/{0}.jpeg".format(trader["id"])

with open('avatar-scrape.json', 'w') as outfile:
    outfile.write(json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8"))
        # print avatarurl.encode('utf-8')

    # if hastwitter:
    #     pagerequest = urllib2.Request(lookupurl, headers=headers)
    #     print lookupurl
    #     page = urllib2.urlopen(pagerequest)
    #     soup = BeautifulSoup(page, "html.parser")
    #     print soup
    #     # coverImage = soup.select("div.ProfileCanopy-headerBg > img")[0]["src"]
    #     avatarImage = soup.select("img.ProfileAvatar-image")[0]["src"]
    #     print avatarImage
    #     imgRequest = urllib2.Request(avatarImage, headers=headers)
    #     imgData = urllib2.urlopen(imgRequest).read()
    #     with open('images/' + slugify(trader["name"]) + '.jpg', 'w') as outfile:
    #         outfile.write(imgData)

    #     print avatarImage
