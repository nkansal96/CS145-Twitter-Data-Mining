from TwitterAPI import TwitterAPI
from passwords import *


api = TwitterAPI(apiKey, apiSecret, accessToken, accessTokenSecret)

# get statuses from LA
r = api.request('statuses/filter', {'locations':'-118.6,33.7,-118.2,34.4'})
for item in r:
        print(item['text'])
        print('\n')