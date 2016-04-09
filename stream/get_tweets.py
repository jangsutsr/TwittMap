'''
This script is supposed to run continuously along the app lifespan to catch
desired tweets from stream and push them into the elastic search engine.
'''
from requests_oauthlib import OAuth1
import requests
import os.path
import json

# Meta data for elastic search
host = 'http://40.114.93.37:9200'
index = 'twitter'
mapping_type = 'tweet'
file_path = os.path.dirname(__file__)

# Metadata including authentication info for twitter api and desired keywords.
twitt_auth = OAuth1('p32FdQyWOR7XvikqGrk1WmjD9',
                client_secret='Ywi4Mq4Hae3LvIHlsU9TBO1L1Tn9mjpUMHkfpHoqdzfjmv9gkt',
                resource_owner_key='1646649835-hz23yaCiq16uanq3qghkG9k7SuAO2L3UkqM3IkH',
                resource_owner_secret='pWLADxamvVS5eq3IZ3VjM24ZSqUC3b7UillWMKP76CRyL')
kws = ["music","python", "sports", "technology", "zombie", "jordan", "gravity", "amazon"]

def init_index():
    '''Initiates elastic search engine.

    This function creats index 'twitter' along with mapping type 'tweet' which
    is defined in file 'type_config.json'. Note if ES finds a same index
    previously exists, this function deletes the original one to prevent
    incontinuity of timestamps.

    Args: None

    Returns: None
    '''
    path = '/'.join([host, index])
    is_exist = requests.head(path)
    if is_exist.status_code == 200:
        requests.delete(path).json()
    with open('type_config.json') as f:
        mapping = json.dumps(json.load(f))
    requests.put('/'.join([host, index]), data=mapping)

def _generate(pattern):
    '''Table generating phase of KMP.
    '''
    table = [0 for i in range(len(pattern))]
    table[0] = -1
    pos, cnd = 2, 0
    while pos < len(pattern):
        if pattern[pos-1] == pattern[cnd]:
            table[pos] = cnd + 1
            cnd += 1; pos += 1
        elif cnd > 0:
            cnd = table[cnd]
        else:
            table[pos] = 0; pos += 1
    return table

def _search(pattern, string):
    '''searching phase of KMP.
    '''
    table = _generate(pattern)
    i = 0; j = 0
    while i + j < len(string):
        if pattern[j] == string[i+j]:
            if j == len(pattern)-1: return True
            j += 1
        else:
            if table[j] > -1:
                i = i + j - table[j]; j = table[j]
            else:
                j = 0; i += 1
    return False

def categorize(string, table):
    '''categorize catched tweet to its supposed category(keyword).

    KMP algorithm is used here for reliable and efficient search process.

    Args:
        string: the text field of tweet to be checked.
        table: A set (hash table) of all keywords for lookup.

    Returns:
        The desired pattern or 'NA' shorthanding for 'Not Applicable'.
    '''
    string = string.lower()
    for pattern in table:
        if _search(pattern, string):
            return pattern
    return 'NA'

def jsonify(response, category):
    '''Form json to be stored as document.

    This function checks relevant fields of response json to populate the json
    to be stored. A series of check procedules gurarantees the validness of json.

    Args:
        response: the original tweet json.
        category: the keyword of response.

    Returns:
        Serialized json to be stored.
    '''
    result = {'keyword': category}
    result['coordinates'] = response['coordinates']['coordinates']
    result['text'] = response['text']
    if 'created_at' in response and response['created_at']:
        result['timestamp'] = response['created_at']
    else: result['timestamp'] = None
    if 'user' in response and response['user']:
        result['author'] = response['user']['name']
    else: result['author'] = None
    return json.dumps(result)

def insert(string):
    '''Insert tweets into twitter index.

    This function takes dumped jsonized tweet and stores it into search engine.
    It would check response to make sure the tweet is successfully stored at
    last.

    Args:
        string: dumped jsonized tweet

    Returns: None
    '''
    print(string)
    path = '/'.join([host, index, mapping_type])
    res = requests.post(path, data=string)
    while res.status_code != 201 or not res.json()['created']:
        res = requests.post(path, data=string)

if __name__ == '__main__':
    # Prepossessing
    table = set(kws)
    #init_index()
    res = requests.get('https://stream.twitter.com/1.1/statuses/filter.json',
                    stream=True,
                    auth=twitt_auth,
                    params={'track': ','.join(kws)})
    # Main fetch-n-store procedule
    for line in res.iter_lines():
        if line:
            tweet = json.loads(line)
            if 'coordinates' in tweet \
               and 'text' in tweet \
               and tweet['coordinates']:
                category = categorize(tweet['text'], table)
                if category != 'NA':
                    insert(jsonify(tweet, category))
