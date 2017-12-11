# Install dependencies
$ pip install TwitterAPI nltk

# Download nltk language processing data
$ python -c "import nltk; nltk.download('stopwords')"
$ python -c "import nltk; nltk.download('punkt')"

# Run the cluster script
./run.sh             # this actually installs dependencies for you

- analyze.py has the data crawler
- get_events.py is the implementation of the bigram/unigram model (see report)
- passwords.py has API key and various other secrets
- twitter_data.py is a convenience script that serializes and loads tweets