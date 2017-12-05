# from nltk import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem.porter import *
from twitter_data import TwitterData, Tweet
import argparse, json, pprint, re

def analyze(file_loc):
  tweets = map(Tweet, TwitterData(file_loc).tweets)
  print(tweets[0:10000])
  return
  # f = open(file_loc)
  # tweets = json.load(f)

  tweet_dict = get_keywords(tweets)
  cluster(list(tweet_dict.keys()), list(tweet_dict.values()))

def cluster(tweets, keywords):
  return tweets

def get_keywords(tweets):
  stop = set(stopwords.words('english'))

  tweet_dict = {};

  stemmer = PorterStemmer()

  for tweet in tweets:
    text = tweet['text'].lower();
    text = re.sub(r'http\S+', '', text)
    keywords = word_tokenize(text)
    keywords = [word for word in keywords if word not in stop]
    keywords = [stemmer.stem(word) for word in keywords]
    letters = re.compile('^[a-z0-9]+$')
    keywords = [word for word in keywords if letters.match(word)]
    tweet_dict[text] = set(keywords)

  return tweet_dict

def get_distance(s1, s2):
  distance = 0
  for word in s1:
    if word in s2:
      distance += 1
  return distance