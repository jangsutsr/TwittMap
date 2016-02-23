import requests
import json
'''
This module provides elastic search api for other parts of
the app to use.
'''
# meta data
host = 'http://localhost:9200'
index = 'twitter'
mapping_type = 'tweet'

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

def insert(string):
    '''Insert tweets into twitter index.

    This function takes dumped jsonized tweet and stores it into search engine.
    It would check response to make sure the tweet is successfully stored at
    last.

    Args:
        string: dumped jsonized tweet

    Returns: None
    '''
    path = '/'.join([host, index, mapping_type])
    res = requests.post(path, data=string)
    while res.status_code != 201 or not res.json()['created']:
        res = requests.post(path, data=string)

def temporal_search(keyword, start, end):
    '''Fetch categorized tweet in the given time span.

    This function extracts tweets under the specified keyword posted from a
    start timestamp to an end timestamp. The query is defined in file
    temporal_query.json. After the query is loaded, arguments are passed to
    their specific fields to make a complete search body.

    Args:
        keyword: string representing keyword of expected tweets.
        start: start time represented by twitter-styled timestamp.
        end: end time represented by twitter-styled timestamp.

    Returns:
        Jsonized elastic search result.
D
    '''
    path = '/'.join([host, index, mapping_type, '_search'])
    with open('stream/temporal_query.json') as f:
        query = json.load(f)
    query['query']['bool']['filter'][0]['match']['keyword'] = keyword
    query['query']['bool']['filter'][1]['range']['timestamp']['gte']\
            = start
    query['query']['bool']['filter'][1]['range']['timestamp']['lte']\
            = end
    res = requests.get(path, data=json.dumps(query))
    return json.loads(res.text)

def proximity_search(keyword, start, end, lat, lon, distance):
    '''Fetch categorized tweet in the given time span and area.

    This function extracts tweets under the specified keyword posted from a
    start timestamp to an end timestamp in the given geographical cycle defined
    by center latitute and longitute and radius. The query is defined in file
    proximity_query.json. After the query is loaded, arguments are passed to
    their specific fields to make a complete search body.

    Args:
        keyword: string representing keyword of expected tweets.
        start: start time represented by twitter-styled timestamp.
        end: end time represented by twitter-styled timestamp.
        lat: (real) number representing latitute.
        lon: (real) number representing longitute.
        distance: string measuring radius which should be in the correct format.

    Returns:
        Jsonized elastic search result.
    '''
    path = '/'.join([host, index, mapping_type, '_search'])
    with open('stream/proximity_query.json') as f:
        query = json.load(f)
    query['query']['bool']['filter'][0]['match']['keyword'] = keyword
    query['query']['bool']['filter'][1]['range']['timestamp']['gte']\
            = start
    query['query']['bool']['filter'][1]['range']['timestamp']['lte']\
            = end
    query['query']['bool']['filter'][2]['geo_distance']['distance']\
            = distance
    query['query']['bool']['filter'][2]['geo_distance']['coordinates']\
            = [lat, lon]
    res = requests.get(path, data=json.dumps(query))
    return json.loads(res.text)
