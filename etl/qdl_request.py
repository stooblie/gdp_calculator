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
    def __init__(self, type='data', dataset_format='ts', format='json',
                datatable_code=None, parameters=None):
        self.uri = quandl_dict['base_uri'][type]
        self.datatable_code = datatable_code
        self.format = format
        self.req_type = type
        self.parameters = parameters
        self.dataset_format = dataset_format

        #print('URI: ', self.uri)

    def get_table_data(self):
        '''Make a data request'''
        data = quandl.get_table(self.datatable_code, **self.parameters)
        return data

    def get_ts_data(self):
        '''Make a data request'''
        data = quandl.get(self.datatable_code, **self.parameters)
        return data

    def get_table_metadata(self):
        '''Make a metadata requestfor a specific table'''
        metadata = quandl.Datatable(self.datatable_code).data().meta
        return metadata

    def get_ts_metadata(self):
        '''Make a metadata requestfor a specific dataset'''
        metadata = quandl.Dataset(self.datatable_code).data().meta
        return metadata

if __name__ == '__main__':
    code = 'MER/F1'
    params = {'start_date': "2003-12-31", 'end_date': "2005-12-31"}

    test = Request(datatable_code=code, parameters=params, type='data')

    #data = test.get_table_data()
    #print(data)
    metadata = test.get_table_metadata()
    print(metadata)
