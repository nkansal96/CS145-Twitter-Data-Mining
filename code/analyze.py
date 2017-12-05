import argparse, json, math
from twitter_data import TwitterData, Tweet
from random import shuffle
from collections import Counter

class geoCluster:
	def __init__(self, file_path):
		self.tweets = [Tweet(t) for t in TwitterData(file_path).get_tweets()]
		shuffle(self.tweets)

	def createClusters(self, clusterSize=500, numClusters=10, neighborDistance=0):
		n = len(self.tweets)
		clusters = []
		for i in range(0, n):
			candidate = self.tweets[i]
			neighbors = [i]

			itime = candidate.timestamp()
			if not itime:
				continue

			for k in range(0, n):
				if i == k:
					continue

				neighbor = self.tweets[k]
				ktime = neighbor.timestamp()
				# 2.5 minutes
				if ktime and abs(ktime - itime) < 150000:
						neighbors.append(k)

			if len(neighbors) > clusterSize:
				clusters.append(neighbors)
				print "cluster center:", i, "cluster size:" , len(neighbors)
				if len(clusters) > numClusters:
					return clusters
		return clusters

	def clusterCommonTheme(self, cluster):
		score = 0.0
		for tweet in cluster:
			c = Counter(tweet.words())
			score += sum(0 if v == 1 else v for (k, v) in c.items()) / (3.0 * len(cluster))
		return score

	def coordinateDistance(self, a, b):
		ax = [a[0][0][0], a[0][1][0], a[0][2][0], a[0][3][0]]
		ay = [a[0][0][1], a[0][1][1], a[0][2][1], a[0][3][1]]

		bx = [b[0][0][0], b[0][1][0], b[0][2][0], b[0][3][0]]
		by = [b[0][0][1], b[0][1][1], b[0][2][1], b[0][3][1]]

		closestX = min(abs(i - k) for i in ax for k in bx)
		closestY = min(abs(i - k) for i in ay for k in by)

		return math.sqrt(math.pow(closestX, 2) + math.pow(closestY, 2))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='CS 145 Twitter Data Mining Project')
	parser.add_argument('--file', help='Location to retrieve tweets for analysis (default ./data.json)', default='data.json')

	args = parser.parse_args()

	g = geoCluster(args.file)
	g.createClusters(clusterSize=400, numClusters=2000, neighborDistance=0)
