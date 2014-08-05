import praw
import re
import sys

from collections import deque
from functools import partial
from time import sleep

try:
  import lmgtfy_bot as bot
except ImportError, e:
  print "No username and password found!"
  sys.exit(10)

filter_empty = partial(filter, None)

def main():
  reddit = praw.Reddit(user_agent = bot.USERAGENT)
  reddit.login(bot.USERNAME, bot.PASSWORD)

  url = 'https?://(?:www\.)?(?:(?:(?:(?:en|ru|de|pt-br|fr|pl|zh-tw|nl|es|images|maps|video|news|shopping|photos|plus|profiles|books|finance|scholar|bing|snopes|wikipedia)\.)?lmgtfy|lm(?:b|sp|s)tfy)\.com|lmddgtfy\.net)/?\??[^\s\]]*'
  links = re.compile('(?:\(([^)]+)\)\[(' + url + ')\])|((' + url + '))')
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
          for text, query in found_links:
            print "FOUND:", text, query
            exit(100)

        except praw.errors.APIException, e:
          print "[ERROR]:", e
          print "sleeping for 30 sec..."
          sleep(30)

    sleep(2)

if __name__ == '__main__':
  main()
