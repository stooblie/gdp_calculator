import quandl
import os
import json
import certifi
import urllib3

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

quandl_dict = json.load(open("./quandl/quandl_dict.json", 'r'))

quandl.ApiConfig.api_key = os.environ['QUANDL_KEY']

class Request():
    '''Handles making an API request through Quandl.'''
    def __init__(self, type='data', datatable_code=None, parameters=None, format='json'):
        self.data_uri = quandl_dict['base_uri']['data']
        self.metadata_uri = quandl_dict['base_uri']['metadata']
        self.datatable_code = datatable_code
        self.format = format
        self.type = type

    def get_data(self, **kwargs):
        quandl.get(self.datatable_code, )
        pass

    def get_metadata(self):
        pass

if __name__ == '__main__':
    code = 'FRED/GDP'
    params = {start_date: "2001-12-31", end_date: "2005-12-31"}

    test = Request(datatable_code='FRED/')
    print(test)

    data = test.get_data()
    print(base_uri)
