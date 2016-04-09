import requests
import json
import os.path
'''
This module provides elastic search api for other parts of
the app to use.
'''

# Meta data for elastic search
host = 'http://40.114.93.37:9200'
ind = 'twitter_again'
mapping_type = 'tweet_sentiment'
file_path = os.path.dirname(__file__)

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
    '''
    path = '/'.join([host, ind, mapping_type, '_search'])
    with open(os.path.join(file_path, 'temporal_query.json')) as f:
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
    path = '/'.join([host, ind, mapping_type, '_search'])
    with open(os.path.join(file_path, 'proximity_query.json')) as f:
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





