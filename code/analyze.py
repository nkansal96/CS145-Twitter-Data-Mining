import argparse, json, math, re
import utils
from twitter_data import TwitterData, Tweet, stop
from random import shuffle
from collections import Counter, defaultdict

class geoCluster:
	def __init__(self, file_path):
		self.tweets = [Tweet(t) for t in TwitterData(file_path).get_tweets()]
		self.lcs_cache = defaultdict(defaultdict)
		shuffle(self.tweets)

	def createClusters(self, clusterSize=500, numClusters=10, neighborDistance=0):
		tweets = self.tweets
		clusters = []
		foundCluster = True

		while foundCluster and len(clusters) < numClusters:
			foundCluster = False
			for i in range(0, len(tweets)):
				candidate = tweets[i]
				neighbors = [candidate]
				indices = [i]

				itime = candidate.timestamp()
				if not itime:
					continue

				for k in range(0, len(tweets)):
					if i == k:
						continue

					neighbor = tweets[k]
					ktime = neighbor.timestamp()

					# 2.5 minutes
					if ktime and abs(ktime - itime) < 150000:
						neighbors.append(neighbor)
						indices.append(k)

				if len(neighbors) > clusterSize:
					foundCluster = True
					clusters.append(neighbors)
					print "cluster center:", i, "cluster size:" , len(neighbors), "tweets remaining", len(tweets) - len(neighbors)

					numRemoved = 0
					for j in indices:
						del tweets[j - numRemoved]
						numRemoved += 1

					print "cluster word counts:"
					wm = self.clusterWordmap(neighbors)
					for word in wm:
						if wm[word] > 15:
							print word, wm[word]

					break
		return clusters

	def clusterCommonTheme(self, cluster):
		score = 0.0
		d = defaultdict(int)
		for tweet in cluster:
			d.update(Counter(list(set(tweet.words()))))
		for tweet in cluster:
			score += sum(0 if d[w] == 1 else d[w] for w in list(set(tweet.words()))) / (3.0 * len(cluster))
		return score

	def clusterNearness(self, cluster):
		d = 0
		c = 0
		for i in range(len(cluster) - 1):
			itw = cluster[i]
			for j in range(len(cluster))[i:]:
				jtw = cluster[j]
				v = None
				for (a, b) in [(itw.id, jtw.id), (jtw.id, itw.id)]:
					if a in self.lcs_cache:
						if b in self.lcs_cache[a]:
							v = self.lcs_cache[a][b]
				if not v:
					a = "".join(itw.words())
					b = "".join(jtw.words())
					m = min(len(a), len(b))
					if m == 0:
						continue
					v = float(utils.lcs(a, b)) / float(m)

				self.lcs_cache[itw.id][jtw.id] = v
				d += v
				c += 1
		return d / float(c)

	def clusterWordmap(self, cluster):
		wordmap = defaultdict(int)
		for tweet in cluster:
			text = tweet.text()
			text = re.sub(r'http\S+', '', text)
			words = text.split()
			for word in words:
				if word not in stop and len(word) > 3:
					wordmap[word] += 1
		return wordmap

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
