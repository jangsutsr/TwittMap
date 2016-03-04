from app import server
from flask import request, render_template
import json
from stream.elastic_search import temporal_search, proximity_search
from datetime import datetime

def convert(original_time):
    timestamp = datetime.strptime(original_time, '%m-%d-%Y %I:%M %p')
    return timestamp.strftime('%a %b %d %H:%M:%S +0000 %Y')

@server.route('/')
def index():
    return render_template('index.html')

@server.route('/global', methods=['POST'])
def get_global():
    '''View function for sending tweet points

    Args:
        None

    Returns:
        Dumped json file containing desired twitter points.
    '''
    keyword = request.args['kw']
    start = convert(request.args['start'])
    end = convert(request.args['end'])
    search_res = temporal_search(keyword, start, end)
    response = {'tweets': [], 'count': 0, 'pattern': 'global'}
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
    distance = '500km'
    search_res = proximity_search(keyword, start, end, float(lat), float(lon), distance)
    response = {'tweets': [], 'count': 0, 'pattern': 'local'}
    for item in search_res['hits']['hits']:
        response['tweets'].append(item['_source']['text'])
        response['count'] += 1
    return json.dumps(response, indent=2)


