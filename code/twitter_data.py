import pickle, sys, json

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
			with open(file_loc, 'rb') as f:
				self.tweets = pickle.load(f)
				sys.stderr.write("Read {} tweets.\n".format(len(self.tweets)))
		except:
			sys.stderr.write("\n --> File not found or file not unpickleable -- using empty dataset\n")

	def add_tweet(self, tweet):
		""" Adds a tweet to the object """
		self.tweets.append(tweet)
		self.serialize()

	def get_tweets(self):
		""" Returns all tweets stored in the object """
		return self.tweets

	def serialize(self):
		""" Serializes the object. Writes its data to a file """
		with open(self.file_loc, 'wb') as f:
			pickle.dump(self.tweets, f)

class Tweet(json.JSONEncoder):
	""" One actual tweet object -- we can methods to transform data here """
	def __init__(self, tweet):
		self.tweet = tweet

	def __repr__(self):
		return json.loads(self.tweet)