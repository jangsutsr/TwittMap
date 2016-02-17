from requests import *
from json import *

host = 'http://localhost:9200'
index = 'twitter'

def init_index():
    path = '/'.join([host, index])
    is_exist = requests.head(path)
    if is_exist.status_code == 200:
        requests.delete(path).json()
    mapping = json.dumps(json.load('type_config.json'))
    requests.put('/'.join([host, index]), data=mapping)

def insert(keyword, string):
    path = '/'.join([host, index, keyword])
    res = requests.post(path, data=string)
    print res.status_code
    while res.status_code != 201 or not res.json()['created']:
        print('Failed')
        res = requests.post(path, data=string)
    print("Success in {}.".format(keyword))

