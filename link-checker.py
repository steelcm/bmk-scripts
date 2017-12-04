import httplib
import json
import urllib2
import urlparse
import pprint

def pingUrl(url):
	try:
		urllib2.urlopen(url)
		return True         # URL Exist
	except ValueError, ex:
		print ex
		return False        # URL not well formatted
	except urllib2.URLError, ex:
		print ex
		return False        # URL don't seem to be alive

with open("scrape.json") as data_file:
    data = json.load(data_file)

for trader in data:
	if trader["social"]:
		pops = []
		for index, social in enumerate(trader["social"]):
			url = social["url"]
			url_parts = urlparse.urlparse(url)
			if not url_parts[0]:
				print "no scheme yo!"
				social["url"] = "https://"+url
				url = social["url"]
			# ping URL
			if not pingUrl(url):
				print "-- " + url
				pops.append(index)
				# trader["social"].pop(social)
		if len(pops) > 0:
			print(pops)
			for i in reversed(pops):
				trader["social"].pop(i)

with open('link-scrape.json', 'w') as outfile:
    outfile.write(json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8"))
