#! /bin/bash

FILE=../data/data.json

if [ ! -f $FILE ]; then
	echo '=== MAKE SURE data.json EXISTS in the data DIRECTORY! ==='
	exit 1
fi

echo '=== Installing dependencies ==='
pip install TwitterAPI nltk
python -c "import nltk; nltk.download('stopwords')"
python -c "import nltk; nltk.download('punkt')"

echo '=== RUNNING CLUSTER DETECTOR ON ../data/data.json ==='
python get_events.py --file $FILE

echo '=== RESULTS FROM CLUSTER DETECTOR ==='
sleep 2

cat events.json | python -m json.tool
