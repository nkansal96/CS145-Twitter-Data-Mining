from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
import argparse, json, pprint, re, random

def analyze(file_loc):
  f = open(file_loc)
  tweets = json.load(f)

  tweet_dict = get_keywords(tweets)
  clusters = cluster(list(tweet_dict.keys()), list(tweet_dict.values()), 10)
  pprint.pprint(clusters)

def areEquivalentClusters(clusters1, clusters2):
  for i in range(len(clusters1)):
    if clusters1[i].issubset(clusters2[i]) and clusters2[i].issubset(clusters1[i]):
      continue
    else:
      return False
  return True


def cluster(tweets, keywords, num_clusters):
  clusters = []
  clusterKeywords = []
  for i in range(num_clusters):
    clusters.append(set())
    clusterKeywords.append(set())

  for i in range(len(tweets)):
    index = random.randint(1, num_clusters) - 1
    clusters[index].add(i)
    clusterKeywords[index] = clusterKeywords[index].union(keywords[i])

  while True:
    distances = [[] for tweet in tweets]

    for i in range(len(tweets)):
      for j in range(num_clusters):
        distance = get_distance(keywords[i], clusterKeywords[j])
        distances[i].append(distance)

    newClusters = []
    newClusterKeywords = []
    for i in range(num_clusters):
      newClusters.append(set())
      newClusterKeywords.append(set())

    for i in range(len(tweets)):
      i_distances = distances[i]
      index = i_distances.index(min(i_distances))
      newClusters[index].add(i)
      newClusterKeywords[index] = newClusterKeywords[index].union(keywords[i])

    if areEquivalentClusters(newClusters, clusters):
      return replaceIndicesWithTweets(clusters, tweets)
    else:
      clusters = newClusters
      clusterKeywords = newClusterKeywords

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
  return len(s1.intersection(s2)) * -1

def replaceIndicesWithTweets(clusters, tweets):
  for i in range(len(clusters)):
    cluster = clusters[i]
    tweetSet = set()
    for index in cluster:
      tweetSet.add(tweets[index])
    clusters[i] = tweetSet
  return clusters


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='CS 145 Twitter Data Mining Project')
  parser.add_argument('--file', help='Location to retrieve tweets for analysis (default ./data.json)', default='data.json')

  args = parser.parse_args()
  analyze(args.file)
