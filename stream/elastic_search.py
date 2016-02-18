import requests
import json

host = 'http://localhost:9200'
index = 'twitter'
mapping_type = 'tweet'

def init_index():
    path = '/'.join([host, index])
    is_exist = requests.head(path)
    if is_exist.status_code == 200:
        requests.delete(path).json()
    with open('type_config.json') as f:
        mapping = json.dumps(json.load(f))
    requests.put('/'.join([host, index]), data=mapping)

def insert(string):
    path = '/'.join([host, index, mapping_type])
    res = requests.post(path, data=string)
    print res.status_code
    while res.status_code != 201 or not res.json()['created']:
        print('Failed')
        res = requests.post(path, data=string)
    print(res.json()['created'])

def temporal_search(keyword, start, end):
    path = '/'.join([host, index, mapping_type, '_search'])
    with open('temporal_query.json') as f:
        query = json.load(f)
    query['query']['bool']['must'][0]['match']['keyword'] = keyword
    query['query']['bool']['must'][1]['range']['timestamp']['gte']\
            = start
    query['query']['bool']['must'][1]['range']['timestamp']['lte']\
            = end
    res = requests.get(path, data=json.dumps(query))
    print json.dumps(json.loads(res.text), indent=2)


if __name__ == '__main__':
    temporal_search('music',
                    "Wed Feb 17 23:13:27 +0000 2016",
                    "Wed Feb 17 23:13:38 +0000 2016")
