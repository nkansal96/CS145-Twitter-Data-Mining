from TwitterAPI import TwitterAPI
from twitter_data import TwitterData, Tweet
from passwords import *
import argparse, pprint, math, json

def scrape_tweets(file_loc, max_tweets):
	""" Scrape tweets and store into a file """
	td = TwitterData(file_loc)
	api = TwitterAPI(apiKey, apiSecret, accessToken, accessTokenSecret)
	count = 0

	stream = api.request('statuses/filter', {'locations':'-118.6,33.7,-118.2,34.4'})
	for tweet in stream:
		td.add_tweet(tweet)
		count += 1
		if count >= max_tweets:
			break;

def dump_data(file_loc):
	""" Dumps the data stored in the file """
	td = TwitterData(file_loc)
	print(json.dumps(td.get_tweets(), sort_keys=True, indent=2))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='CS 145 Twitter Data Mining Project')
	parser.add_argument('--file', help='Location to store/retrieve tweets (default ./data.bin)', default='data.bin')
	parser.add_argument('--max_tweets', help='The maximum number of tweets to crawl (default is 2 ** 63 - 1)', type=int, default=(2 ** 63 - 1))
	parser.add_argument('--scrape', help='Start scraping tweets from twitter', action='store_true')
	parser.add_argument('--dump', help='Dump the data from the given file to stdout in JSON format', action='store_true')

	args = parser.parse_args()
	if args.scrape:
		scrape_tweets(args.file, args.max_tweets)
	if args.dump:
		dump_data(args.file)
