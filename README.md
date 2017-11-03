# CS145-Twitter-Data-Mining
Data Mining project for CS 145

## Setup

Clone this repository and download the `passwords.py` file and put inside the folder with `app.py`. Then install the requirements:

```bash
$ pip install TwitterAPI
```

## Run

The program supports the following arguments:

```bash
$ python app.py --help
usage: app.py [-h] [--file FILE] [--max_tweets MAX_TWEETS] [--scrape] [--dump]

CS 145 Twitter Data Mining Project

optional arguments:
  -h, --help      show this help message and exit
  --file FILE     Location to store/retrieve tweets (default ./data.bin)
  --max_tweets M  The maximum number of tweets to crawl (default is 2 ** 63 - 1)
  --scrape        Start scraping tweets from twitter
  --dump          Dump the data from the given file to stdout in JSON format
```
