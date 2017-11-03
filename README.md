# CS145-Twitter-Data-Mining
Data Mining project for CS 145

## Setup

Clone this repository and install the requirements:

```bash
$ pip install TwitterAPI
```

## Run

The program supports the following arguments:

```bash
$ python app.py --help
usage: app.py [-h] [--file FILE] [--scrape] [--raw_dump] [--pretty_dump]

CS 145 Twitter Data Mining Project

optional arguments:
  -h, --help     show this help message and exit
  --file FILE    Location to store/retrieve tweets (default ./data.bin)
  --scrape       Start scraping tweets from twitter
  --raw_dump     Dump the raw data from the given file to stdout
  --pretty_dump  Dump the data prettified from the given file to stdout
```
