from flask import Flask, request, render_template
import json
from stream.elastic_search import temporal_search, proximity_search
from datetime import datetime

application = Flask(__name__)

def convert(original_time):
    timestamp = datetime.strptime(original_time, '%m-%d-%Y %I:%M %p')
    return timestamp.strftime('%a %b %d %H:%M:%S +0000 %Y')

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/global', methods=['POST'])
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

@application.route('/local', methods=['POST'])
def get_local():
    '''View function for sending local tweets

    Args:
        None

    Returns:
        Dumped json file containing desired tweets.
    '''
    keyword = request.args['kw']
    start = convert(request.args['start'])
    end = convert(request.args['end'])
    lat = request.args['lat']
    lon = request.args['lon']
    distance = '500km'
    search_res = proximity_search(keyword, start, end, float(lat), float(lon), distance)
    response = {'tweets': [], 'count': 0, 'pattern': 'local'}
    for item in search_res['hits']['hits']:
        response['tweets'].append("@"+item['_source']['author']+": "+item['_source']['text']+" Sentiment: "+item['_source'].get('sentiment', 'N/A'))
        response['count'] += 1
    return json.dumps(response, indent=2)

if __name__=='__main__':
    application.run(debug=True)
