#! /bin/bash

FILE=/tmp/test_tweet.bin

rm -rf $FILE
python code/app.py --scrape --file $FILE --max_tweets 3
python code/app.py --dump --file $FILE
rm -rf $FILE