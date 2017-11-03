from TwitterAPI import TwitterAPI
from twitter_data import TwitterData
from passwords import *
import argparse, pprint

def scrape_tweets(file_loc):
	""" Scrape tweets and store into a file """
	td = TwitterData(file_loc)
	api = TwitterAPI(apiKey, apiSecret, accessToken, accessTokenSecret)

	stream = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
	for tweet in stream:
		td.add_data(tweet)

def dump_data(file_loc, pretty):
	""" Dumps the data stored in the file """
	td = TwitterData(file_loc)
	if pretty:
		pprint.pprint(td.get_data())
	else:
		print(td.get_data())


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='CS 145 Twitter Data Mining Project')
	parser.add_argument('--file', help='Location to store/retrieve tweets (default ./data.bin)', default='data.bin')
	parser.add_argument('--scrape', help='Start scraping tweets from twitter', action='store_true')
	parser.add_argument('--raw_dump', help='Dump the raw data from the given file to stdout', action='store_true')
	parser.add_argument('--pretty_dump', help='Dump the data prettified from the given file to stdout', action='store_true')

	args = parser.parse_args()
	if args.scrape:
		scrape_tweets(args.file)
	if args.raw_dump or args.pretty_dump:
		dump_data(args.file, args.pretty_dump)
