import pickle, sys, json, os

class TwitterData(object):
	""" Keep track of twitter data in a serialized fashion """
	def __init__(self, file_loc):
		""" Construct the object. Reads the given file_loc for
		any existing data. If it exists and is unpickleable, it
		loads it. Otherwise it uses an empty list
		"""
		self.tweets = []
		self.file_loc = file_loc
		try:
			sys.stderr.write("Attempting to read stored tweets from '{}'... ".format(file_loc))
			sys.stderr.flush()
			with open(file_loc, 'r') as f:
				self.tweets = json.loads(f.read())
				sys.stderr.write("Read {} tweets.\n".format(len(self.tweets)))
		except:
			sys.stderr.write("\n --> File not found or file not in json format -- using empty dataset\n")

	def add_tweet(self, tweet):
		""" Adds a tweet to the object """
		self.tweets.append(tweet)
		if len(self.tweets) % 50 == 0:
			self.serialize()

	def get_tweets(self):
		""" Returns all tweets stored in the object """
		return self.tweets

	def serialize(self):
		""" Serializes the object. Writes its data to a file """
		with open(self.file_loc, 'w', 0) as f:
			os.fsync(f.fileno())
			f.write(json.dumps(self.tweets))

class Tweet(json.JSONEncoder):
	""" One actual tweet object -- we can methods to transform data here """
	def __init__(self, tweet):
		self.tweet = tweet

	def __repr__(self):
		return json.loads(self.tweet)
