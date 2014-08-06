import json
import praw
import re
import sys
import urllib

from collections import deque
from functools import partial
from time import sleep
from urlparse import urlparse, parse_qs

try:
  import lmgtfy_bot as bot
except ImportError, e:
  print "No username and password found!"
  sys.exit(10)

reddit = praw.Reddit(user_agent = bot.USERAGENT)
reddit.login(bot.USERNAME, bot.PASSWORD)

url_re = 'https?://(?:www\.)?(?:(?:(?:(?:en|ru|de|pt-br|fr|pl|zh-tw|nl|es|images|maps|video|news|shopping|photos|plus|profiles|books|finance|scholar|bing|snopes|wikipedia)\.)?lmgtfy|lm(?:b|sp|s)tfy)\.com|lmddgtfy\.net)/?\??[^\s\]]*'
links_re = re.compile('(?:\[([^]]+)\]\((' + url_re + ')\))|((' + url_re + '))')
cache = deque(maxlen = 2000)

filter_empty = partial(filter, None)

raw_data = open("../data.json")
data = json.load(raw_data)
raw_data.close()

comment = """**WAIT!**  You're about to walk into a trap...

-----

The following {link} were found in the above comment:

{lmgtfy_links}

Skip the pretension and annoying animation and use these {link} to go straight to the results you were looking for:

{fixed_links}

-----
^I ^am ^the **[^lmgtfy-redirect ^bot](http://github.com/samkellett/lmgtfy-redirect)**^. ^I ^also ^come ^as **[^an ^extension](https://chrome.google.com/webstore/detail/lmgtfy-redirect/aokibefgjhbpnfaalkikepfjckdligek)**^, ^install ^me ^and ^never ^be ^caught ^out ^again!

^Did ^I ^do ^something ^wrong? ^Please **[^report ^an ^issue](https://github.com/samkellett/lmgtfy-redirect/issues)** ^so ^that ^I ^can ^be ^fixed!"""

def extract_links(comment):
  links = []

  found_links = map(filter_empty, re.findall(links_re, comment))
  if found_links:
    for text, link in found_links:
      parsed_link = urlparse(link)

      hostname = parsed_link.netloc
      subdomain = hostname.split('.', 1)[0]

      suffix = data["languages"]["en"]
      if subdomain == "www":
        hostname = hostname[4:]
      elif subdomain in data["languages"]:
        suffix = data["languages"][subdomain]
        hostname = hostname[len(subdomain) + 1:]

      if hostname in data["uris"]:
        query = parse_qs(parsed_link.query)

        if 'q' not in query:
          continue

        ext = {}
        if "l" in query and query["l"] == "1":
          if hostname == "lmgtfy.com":
            ext = {"btnI": "I"}
          elif hostname == "scholar.lmgtfy.com":
            ext = {"as_sdt": "2,47"}

        new_url = data["uris"][hostname].format(
          scheme = parsed_link.scheme,
          com = suffix,
          query = query["q"][0],
          ext = urllib.urlencode(ext))

        links.append((text, link, new_url))
  return links

def main():
  running = True
  while running:
    try:
      comments = reddit.get_comments('all', limit = 1000)
      for comment in comments:
        if comment.id in cache:
          continue

        cache.append(comment.id)
        print comment.body

        urls = extract_links(comment.body)
        if urls:
          print(urls)
          exit(100)

    except praw.errors.APIException, e:
      print "[ERROR]:", e
      print "sleeping for 30 sec..."
      sleep(30)

    sleep(2)

if __name__ == '__main__':
  main()
