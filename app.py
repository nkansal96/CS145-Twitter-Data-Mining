from TwitterAPI import TwitterAPI
from passwords import *


api = TwitterAPI(apiKey, apiSecret, accessToken, accessTokenSecret)

# get statuses from NYC
r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
for item in r:
        print(item)
        print('\n')