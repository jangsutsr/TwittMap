from requests_oauthlib import OAuth1
import requests
from json import loads

twitt_auth = OAuth1('p32FdQyWOR7XvikqGrk1WmjD9',
                client_secret='Ywi4Mq4Hae3LvIHlsU9TBO1L1Tn9mjpUMHkfpHoqdzfjmv9gkt',
                resource_owner_key='1646649835-hz23yaCiq16uanq3qghkG9k7SuAO2L3UkqM3IkH',
                resource_owner_secret='pWLADxamvVS5eq3IZ3VjM24ZSqUC3b7UillWMKP76CRyL')
kws = ','.join(["music","python", "sports", "technology", "prototype", "kobe", "gravity", "amazon"])
res = requests.get('https://stream.twitter.com/1.1/statuses/filter.json',
                stream=True,
                auth=twitt_auth,
                params={'track': kws})

for line in res.iter_lines():
    if line:
        tweet = loads(line)
        if 'text' in tweet \
           and 'coordinates' in tweet \
           and 'created_at' in tweet \
           and tweet['coordinates']:
            print(tweet['created_at'])
            print(tweet['coordinates']['coordinates'])
            print(tweet['text'])
