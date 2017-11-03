#! /bin/bash

FILE=/tmp/test_tweet.bin

rm -rf $FILE

pip install TwitterAPI
python code/app.py --scrape --file $FILE --max_tweets 3

if [ ! $? -eq 0 ]; then
	echo 'Error running the scraper!'
	rm -rf $FILE
	exit 1
fi

python code/app.py --dump --file $FILE

if [ ! $? -eq 0 ]; then
	echo 'Error running the scraper!'
	rm -rf $FILE
	exit 1
fi