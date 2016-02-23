from app import server
from flask import request
from stream.elastic_search import temporal_search, proximity_search
import json

@server.route('/')
def index():
    pass

@server.route('/global', methods=['POST'])
def get_global():
    '''View function for sending tweet points

    Args:
        None

    Returns:
        Dumped json file containing desired twitter points.
    '''
    keyword = request.form['kw']
    start = request.form['start']
    end = request.form['end']
    search_res = temporal_search(keyword, start, end)
    response = {'tweets': [], 'count': 0}
    for item in search_res['hits']['hits']:
        response['tweets'].append(item['_source']['coordinates'])
        response['count'] += 1
    return json.dumps(response, indent=2)

@server.route('/local', methods=['POST'])
def get_local():
    '''View function for sending local tweets

    Args:
        None

    Returns:
        Dumped json file containing desired tweets.
    '''
    keyword = request.form['kw']
    start = request.form['start']
    end = request.form['end']
    lat = request.form['lat']
    lon = request.form['lon']
    distance = request.form['distance']
    search_res = proximity_search(keyword, start, end, float(lat), float(lon), distance)
    response = {'tweets': [], 'count': 0}
    for item in search_res['hits']['hits']:
        response['tweets'].append(item['_source'])
        response['count'] += 1
    return json.dumps(response, indent=2)
