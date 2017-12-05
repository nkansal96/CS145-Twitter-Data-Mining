import argparse, json, math
from random import shuffle

class geoCluster:
	def __init__(self, file_path):
		file = open(file_path)
		self.tweets = json.load(file)
		shuffle(self.tweets)

	def createClusters(self, clusterSize=500, numClusters=10, neighborDistance=0):
		n = len(self.tweets)
		clusters = []
		for i in range(0, n):
			candidate = self.tweets[i]

			if "timestamp_ms" not in candidate:
				continue

			if "place" not in candidate or candidate["place"] == None:
				continue

			if candidate["place"]["bounding_box"]["type"] != "Polygon":
			 	continue

			icoords = candidate["place"]["bounding_box"]["coordinates"]
			itime = int(candidate["timestamp_ms"])

			neighbors = [i]
			for k in range(0, n):
				if i == k:
					continue

				neighbor = self.tweets[k]

				if "timestamp_ms" not in neighbor:
					continue

				if "place" not in neighbor or neighbor["place"] == None:
					continue

				if neighbor["place"]["bounding_box"]["type"] != "Polygon":
					continue

				kcoords = neighbor["place"]["bounding_box"]["coordinates"]
				ktime = int(neighbor["timestamp_ms"])
				
				# 5 minutes apart
				if itime > ktime:
					td = itime - ktime
				else:
					td = ktime - itime

				if td > 150000:
					continue

				neighbors.append(k)

			if len(neighbors) > clusterSize:

				clusters.append(neighbors)
				print "cluster center:", i, "cluster size:" , len(neighbors)
				if len(clusters) > numClusters:
					return clusters

		return clusters

	def coordinateDistance(self, a, b):
		ax = [a[0][0][0], a[0][1][0], a[0][2][0], a[0][3][0]]
		ay = [a[0][0][1], a[0][1][1], a[0][2][1], a[0][3][1]]

		bx = [b[0][0][0], b[0][1][0], b[0][2][0], b[0][3][0]]
		by = [b[0][0][1], b[0][1][1], b[0][2][1], b[0][3][1]]

		closestX = min(abs(i - k) for i in ax for k in bx)
		closestY = min(abs(i - k) for i in ay for k in by)

		return math.sqrt(math.pow(closestX, 2) + math.pow(closestY, 2))

	def analyzeCluster(self, cluster):
		stop = set(stopwords.words('english'))

		tweet_dict = {};

		stemmer = PorterStemmer()

		for i in cluster:
			tweet = self.tweets[i]
			text = tweet['text'].lower();
			text = re.sub(r'http\S+', '', text)
			keywords = word_tokenize(text)
			keywords = [word for word in keywords if word not in stop]
			keywords = [stemmer.stem(word) for word in keywords]
			letters = re.compile('^[a-z0-9]+$')
			keywords = [word for word in keywords if letters.match(word)]
			tweet_dict[text] = set(keywords)
		
		return tweet_dict



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='CS 145 Twitter Data Mining Project')
	parser.add_argument('--file', help='Location to retrieve tweets for analysis (default ./data.json)', default='data.json')

	args = parser.parse_args()

	g = geoCluster(args.file)
	g.createClusters(clusterSize=400, numClusters=2000, neighborDistance=0)
	