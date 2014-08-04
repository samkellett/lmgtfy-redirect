import praw
import regex
import sys

from collections import deque

try:
  import lmgtfy_bot as bot
except ImportError, e:
  print "No username and password found!"
  sys.exit(10)

def main():
  reddit = praw.Reddit(user_agent = bot.USERAGENT)
  reddit.login(bot.USERNAME, bot.PASSWORD)

  links = regex.compile('(?|(?<txt>(?<url>https?://(www\.)?((((en|ru|de|pt-br|fr|pl|zh-tw|nl|es|images|maps|video|news|shopping|photos|plus|profiles|books|finance|scholar|bing|snopes|wikipedia)\.)?lmgtfy|lm(b|sp|s)tfy)\.com|lmddgtfy.net)))|\(([^)]+)\)\[(\g<url>)\])')
  cache = deque(maxlen = 200)

  running = True
  while running:
    comments = reddit.get_comments('all', limit = 100)
    for comment in comments:
      if comment.id in cache:
        break

      cache.append(comment.id)
      print (comment.body)
      running = False

  print bot.USERNAME

if __name__ == '__main__':
  main()
