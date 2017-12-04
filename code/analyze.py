import argparse, json, math

class geoCluster:
	def __init__(self, file_path):
		file = open(file_path)
		self.tweets = json.load(file)


	def createClusters(self, clusterSize=2500, numClusters=500, neighborDistance=0):
		n = len(self.tweets)
		clusters = []
		for i in range(0, n):
			candidate = self.tweets[i]

			if "place" not in candidate or candidate["place"] == None:
				continue

			if candidate["place"]["bounding_box"]["type"] != "Polygon":
			 	continue

			icoords = candidate["place"]["bounding_box"]["coordinates"]
			neighbors = [i]

			for k in range(0, n):
				if i == k:
					continue

				neighbor = self.tweets[k]
				if "place" not in neighbor or neighbor["place"] == None:
					continue

				if neighbor["place"]["bounding_box"]["type"] != "Polygon":
					continue

				kcoords = neighbor["place"]["bounding_box"]["coordinates"]

				d = self.coordinateDistance(icoords, kcoords)
				
				if d <= neighborDistance:
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

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='CS 145 Twitter Data Mining Project')
	parser.add_argument('--file', help='Location to retrieve tweets for analysis (default ./data.json)', default='data.json')

	args = parser.parse_args()

	g = geoCluster(args.file)
	g.createClusters()
	