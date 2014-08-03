import praw
import sys
# from collections import deque

try:
  import lmgtfy_bot as bot
except ImportError, e:
  print "No username and password found!"
  sys.exit(10)

# cache = deque(maxlen = 200)

def main():
  reddit = praw.Reddit(user_agent = bot.USERAGENT)
  reddit.login(bot.USERNAME, bot.PASSWORD)

  print bot.USERNAME

if __name__ == '__main__':
  main()
