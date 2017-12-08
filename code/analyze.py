import nltk
nltk.download('punkt')
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
import argparse, json, pprint, re, random
dictMonth = {'Jan': [1, 31], 'Feb': [2, 28.25], 'March': [3, 31], 'April': [4, 30], 'May': [5, 31], 'June': [6, 30], 'July': [7, 31], 'Aug': [8, 31], 'Sept': [9, 30], 'Oct': [10, 31], 'Nov': [11, 30], 'Dec': [12, 31]}

def analyze(file_loc):
    f = open(file_loc)
    tweets = json.load(f)

    tweet_dict = get_values(tweets)
    clusters = cluster(list(tweet_dict.keys()), list(tweet_dict.values()), 10)
    pprint.pprint(clusters)

def areEquivalentClusters(clusters1, clusters2):
    for i in range(len(clusters1)):
        if clusters1[i].issubset(clusters2[i]) and clusters2[i].issubset(clusters1[i]):
            continue
        else:
            return False
    return True


def cluster(tweets, values, num_clusters):
    clusters = []
    clusterValues = []
    for i in range(num_clusters):
        clusters.append(set())
        clusterValues.append([set(), 0, 0])

    for i in range(len(tweets)):
        index = random.randint(1, num_clusters) - 1
        clusters[index].add(i)
        clusterValues[index][0] = clusterValues[index][0].union(values[i][0])
        clusterValues[index][1] = clusterValues[index][1]+(values[i][1]-clusterValues[index][1])/(clusterValues[index][2] + 1)
        clusterValues[index][2] += 1

    while True:
        distances = [[] for tweet in tweets]

    for i in range(len(tweets)):
        for j in range(num_clusters):
            distance = get_distance(values[i][0], clusterValues[j][0])
            print(distance)
            distance = distance - get_time_distance(values[i][1], clusterValues[j][1])
            distances[i].append(distance)

    newClusters = []
    newClusterValues = []
    for i in range(num_clusters):
        newClusters.append(set())
        newClusterValues.append([set(), 0, 0])

    for i in range(len(tweets)):
        i_distances = distances[i]
        index = i_distances.index(min(i_distances))
        newClusters[index].add(i)
        newClusterValues[index][0] = newClusterValues[index][0].union(values[i][0])
        newClusterValues[index][1] = newClusterValues[index][1]+(values[i][1]-newClusterValues[index][1])/(newClusterValues[index][2] + 1)
        newClusterValues[index][2] += 1

    if areEquivalentClusters(newClusters, clusters):
        return replaceIndicesWithTweets(clusters, tweets)
    else:
      clusters = newClusters
      clusterKeywords = newClusterValues

def get_values(tweets):
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
        tweet_time_info = tweet['created_at'].split()
        tweet_time=0
        if len(tweet_time_info) > 0:
            tweet_time += float(tweet_time_info[3][6:8])
            tweet_time += float(tweet_time_info[3][3:5])*60
            tweet_time += float(tweet_time_info[3][0:2])*60*60
            tweet_time += float(tweet_time_info[2])*60*60*24
            tweet_time += dictMonth[tweet_time_info[1]][0]*60*60*24*dictMonth[tweet_time_info[1]][1]
            tweet_time += (float(tweet_time_info[5])-2000)*60*60*24*365
        if len(keywords) > 0:
            tweet_dict[text] = [set(keywords), tweet_time]

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

def get_time_distance(tweet1_time, tweet2_time):
    difference = abs(tweet1_time - tweet2_time)
    print(difference)
    return difference

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CS 145 Twitter Data Mining Project')
    parser.add_argument('--file', help='Location to retrieve tweets for analysis (default ./data.json)', default='data.json')

    args = parser.parse_args()
    analyze(args.file)
