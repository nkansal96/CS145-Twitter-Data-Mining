import pickle, sys, json, os, datetime
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *

stop = list(set(stopwords.words('english')))
stemmer = PorterStemmer()

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
		with open(self.file_loc, 'w') as f:
			os.fsync(f.fileno())
			f.write(json.dumps(self.tweets))

class Tweet(object):
	""" One actual tweet object -- we can methods to transform data here """
	def __init__(self, tweet):
		if type(tweet) == dict:
			self.tweet = tweet
		if type(tweet) == str:
			self.tweet = json.loads(tweet)

	def coordinates(self):
		if "coordinates" in self.tweet:
			if "coordinates" in self.tweet["coordinates"]:
				return (self.tweet["coordinates"]["coordinates"][0], self.tweet["coordinates"]["coordinates"][1])
		if "geo" in self.tweet:
			if "coordinates" in self.tweet["coordinates"]:
				return (self.tweet["geo"]["coordinates"][1], self.tweet["geo"]["coordinates"][0])
		return None

	def timestamp(self):
		if "timestamp_ms" in self.tweet:
			return int(self.tweet["timestamp_ms"])
		return None

	def words(self):
		if "text" in self.tweet:
			text = self.tweet['text'].lower();
			text = re.sub(r'http\S+', '', text)
			keywords = word_tokenize(text)
			keywords = [word for word in keywords if word not in stop]
			keywords = [stemmer.stem(word) for word in keywords]
			letters = re.compile(r'^[a-z0-9]+$')
			keywords = [word for word in keywords if letters.match(word)]
			return keywords
		return []

	def hashtags(self):
		if "entities" in self.tweet:
			if "hashtags" in self.tweet["entities"]:
				return map(lambda x: x["text"], self.tweet["entities"]["hashtags"])
		return []

	def text(self):
		if "text" in self.tweet:
			return self.tweet["text"]

	def __repr__(self):
		return json.dumps(self.tweet, sort_keys=True, indent=2)
