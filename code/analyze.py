import argparse, json

def analyze(file_loc):
  f = open(file_loc)
  tweets = json.load(f)

  tweet_dict = {};

  for tweet in tweets:
    for hashtag in tweet['entities']['hashtags']:
      if hashtag['text'] in tweet_dict:
        tweet_dict[hashtag['text']].append(tweet['text'])
      else:
        tweet_dict[hashtag['text']] = [tweet['text']]

  print(tweet_dict.keys())





if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='CS 145 Twitter Data Mining Project')
	parser.add_argument('--file', help='Location to retrieve tweets for analysis (default ./data.json)', default='data.json')

	args = parser.parse_args()
	analyze(args.file)
