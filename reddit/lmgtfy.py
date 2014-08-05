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

filter_empty = partial(filter, None)

raw_data = open("../data.json")
data = json.load(raw_data)
raw_data.close()

def main():
  reddit = praw.Reddit(user_agent = bot.USERAGENT)
  reddit.login(bot.USERNAME, bot.PASSWORD)

  url = 'https?://(?:www\.)?(?:(?:(?:(?:en|ru|de|pt-br|fr|pl|zh-tw|nl|es|images|maps|video|news|shopping|photos|plus|profiles|books|finance|scholar|bing|snopes|wikipedia)\.)?lmgtfy|lm(?:b|sp|s)tfy)\.com|lmddgtfy\.net)/?\??[^\s\]]*'
  links = re.compile('(?:\[([^]]+)\]\((' + url + ')\))|((' + url + '))')
  cache = deque(maxlen = 2000)

  running = True
  while running:
    comments = reddit.get_comments('all', limit = 1000)
    for comment in comments:
      if comment.id in cache:
        continue

      cache.append(comment.id)
      print comment.body

      found_links = map(filter_empty, re.findall(links, comment.body))
      if found_links:
        try:
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

              to_url = data["uris"][hostname].format(scheme = parsed_link.scheme, com = suffix, query = query["q"][0], ext = urllib.urlencode(ext))
              print to_url
              exit(100)

        except praw.errors.APIException, e:
          print "[ERROR]:", e
          print "sleeping for 30 sec..."
          sleep(30)

    sleep(2)

if __name__ == '__main__':
  main()
