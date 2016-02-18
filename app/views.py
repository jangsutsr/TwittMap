from app import app
from flask import request
from stream.elastic_search import temporal_search, proximity_search

@app.route('/')
def index():
    pass

@app.route('/global', methods=['POST'])
def get_global():
    keyword = request.form['kw']
    start = request.form['start']
    end = request.form['end']
    response = temporal_search(keyword, start, end)
    return response

@app.route('/local', methods=['POST'])
def get_local():
    keyword = request.form['kw']
    start = request.form['start']
    end = request.form['end']
    lat = request.form['lat']
    lon = request.form['lon']
    distance = request.form['distance']
    response = proximity_search(keyword, start, end, lat, lon, distance)
    return response
