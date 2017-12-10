from datetime import date as d
from pprint import pprint
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.util import ngrams
import argparse, json, re, random

def get_events(file_loc):
  f = open(file_loc)
  tweets = json.load(f)

  tweetsByDate = {}
  statsByDate = {}

  for tweet in tweets:
  	tweetDate = d.fromtimestamp(int(tweet['timestamp_ms']) / 1000.0)
  	if tweetDate in tweetsByDate:
  		tweetsByDate[tweetDate].append(tweet['text'])
  	else:
  		tweetsByDate[tweetDate] = [tweet['text']]

  totalTweetCount = 0.0

  for date in tweetsByDate.keys():
    if len(tweetsByDate[date]) < 1000:
      continue
    totalTweetCount += len(tweetsByDate)
    statsByDate[date] = get_stats_for_day(tweetsByDate[date])

  bigWordDict = {}
  for wordList in statsByDate.values():
    for word in wordList.keys():
      if word in bigWordDict:
        bigWordDict[word] += wordList[word]
      else:
        bigWordDict[word] = wordList[word]

  # convert counts to frequencies
  for word in bigWordDict.keys():
    bigWordDict[word] /= totalTweetCount

  eventsByDate = {}
  for date in statsByDate.keys():
    eventsByDate[date] = set()

  # individual days
  for date in statsByDate.keys():
    print()
    numTweets = len(tweetsByDate[date]) * 1.0
    for word in statsByDate[date].keys():
      statsByDate[date][word] = statsByDate[date][word] / numTweets
      if statsByDate[date][word] < 0.0007 or bigWordDict[word] > 0.4:
        continue
      if statsByDate[date][word] - bigWordDict[word] > -0.5:
        eventsByDate[date].add(word)

  results = open('events.json', 'w')
  results.write(json.dumps(eventsByDate))

  return eventsByDate



def get_stats_for_day(tweets):
  wordDict = {}

  # count how many tweets each word appears in
  for tweet in tweets:
    words = get_words(tweet)
    seen = set()
    for word in words:
      if word in wordDict and word not in seen:
        wordDict[word] += 1
      else:
        wordDict[word] = 1
      seen.add(word)

  return wordDict

def get_words(tweet):
  # do some initialization
  letters = re.compile('^[a-z]+$')
  stop = set(stopwords.words('english'))

  # user lower case text
  tweet = tweet.lower();

  # remove URLs
  tweet = re.sub(r'http\S+', '', tweet)

  # break into unigrams and bigrams
  keywords = word_tokenize(tweet)
  bigrams = []
  for bigram in ngrams(keywords, 2):
    # don't consider bigrams where one of the words contains non-letters
    if len([word for word in bigram if letters.match(word)]) < 2:
      continue

    # don't consider bigrams where both words are stop words
    if bigram[0] in stop and bigram[1] in stop:
      continue

    bigrams.append(' '.join(str(i) for i in bigram))

  # remove stop words from unigrams
  keywords = [word for word in keywords if word not in stop]

  # remove unigrams that contain non-letters
  keywords = [word for word in keywords if letters.match(word)]

  # return both unigrams and bigrams
  return keywords + bigrams


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='CS 145 Twitter Data Mining Project')
  parser.add_argument('--file', help='Location to retrieve tweets for analysis (default ./data.json)', default='data.json')

  args = parser.parse_args()
  get_events(args.file)