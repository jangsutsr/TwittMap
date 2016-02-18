from requests_oauthlib import OAuth1
import requests
from json import loads, dumps
from re import search
import elastic_search

twitt_auth = OAuth1('p32FdQyWOR7XvikqGrk1WmjD9',
                client_secret='Ywi4Mq4Hae3LvIHlsU9TBO1L1Tn9mjpUMHkfpHoqdzfjmv9gkt',
                resource_owner_key='1646649835-hz23yaCiq16uanq3qghkG9k7SuAO2L3UkqM3IkH',
                resource_owner_secret='pWLADxamvVS5eq3IZ3VjM24ZSqUC3b7UillWMKP76CRyL')

kws = ["music","python", "sports", "technology", "zombie", "jordan", "gravity", "amazon"]

def categorize(string, table):
    string = string.lower()
    for pattern in table:
        if search('.*'+pattern+'.*', string):
            return pattern
    return 'NA'

def jsonify(response, category):
    result = {'keyword': category}
    result['coordinates'] = response['coordinates']['coordinates']
    result['text'] = response['text']
    if 'created_at' in response and response['created_at']:
        result['timestamp'] = response['created_at']
    else: result['timestamp'] = None
    if 'user' in response and response['user']:
        result['author'] = response['user']['name']
    else: result['author'] = None
    return dumps(result)


if __name__ == '__main__':
    table = set(kws)
    elastic_search.init_index()

    res = requests.get('https://stream.twitter.com/1.1/statuses/filter.json',
                    stream=True,
                    auth=twitt_auth,
                    params={'track': ','.join(kws)})
    for line in res.iter_lines():
        if line:
            tweet = loads(line)
            if 'coordinates' in tweet \
               and 'text' in tweet \
               and tweet['coordinates']:
                category = categorize(tweet['text'], table)
                if category != 'NA':
                    print(category)
                    elastic_search.insert(jsonify(tweet, category))
