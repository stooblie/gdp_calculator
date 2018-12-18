import urllib3
import tempfile
import os
import sys
import argparse
import json
import certifi
import ast

api_dict = json.load(open("./api_dict.json", 'r'))

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

class Request():

    def __init__(self, type, method, parameters=None, format='json'):
        #Base parameters
        self.type = type
        self.uri = api_dict[type]['uri']
        self.method = api_dict[type]['params']['method'][method]
        self.key = '&UserID=' + os.environ[api_dict[type]['key']]
        self.format = api_dict[type]['format'][format]

        #Additional parameters
        #self.params = ''
        #for key, value in kwargs.items():
            #if value == None: continue
            #else:
                #self.params += api_dict[type]['params'][key] + value

        #self.url = self.uri + self.key + self.method + self.format
    def execute_method(self):
        if self.method in ["list_datasets", "get_parameters", "get_parameter_values", "get_parameter_values_filtered"]:
            get_metadata(self.method)
        if self.method = 'get_data':
            get_data()
        else: pass

    def get_metadata(self):
        if self.method == "list_datasets":
        if self.method ==:
        if self.method ==:

    def get_data(self):
        print('URL: {}'.format(self.url))
        response = http.request('GET', self.url)
        #print(response.data)
        data = json.loads(response.data)
        self.title = list(data.keys())[0]
        return data
        #for i in data['BEAAPI']['Results']['Dataset']:
            #print(i['DatasetName'] + '\n' + i['DatasetDescription'] + '\n\n')
        #output = json.loads(data)
        #return output

    def display_data(self):
        data = self.get_data()
        for i in data['BEAAPI']['Results']['Dataset']:
            print(i['DatasetName'] + '\n' + i['DatasetDescription'] + '\n\n')
        #print(json.dumps(data, indent=4, sort_keys=True))

# Sysarg format: Type, Method, Dataset_Name, Table_Name, Frequency, Year
# Example: DataSet = NIPA, TableName = T10101, Frequency = Q, Year = 2018
# Table Results: BEAAPI > Results > Data/Notes
if __name__ == '__main__':
    type = sys.argv[1]
    print('Type: {}'.format(type))
    method = sys.argv[2]
    print('Method: {}'.format(method))
    if method == 'list_datasets': kwargs = {}
    else: kwargs = {'dataset_name': sys.argv[3], 'table_name': sys.argv[4], 'frequency': sys.argv[5], 'year': sys.argv[6]}
    print('Parameters: {}'.format(kwargs))
    #print('kwargs: {}'.format(kwargs))
    obj = Request(type, method, **kwargs)
    data = obj.get_data()
    data_dict = ast.literal_eval(json.dumps(data))
    #print(data_dict['BEAAPI']['Results'])
    print(json.dumps(data, indent=4, sort_keys=True))
    #print('Required Parameteres:\n{}'.format([dict['ParameterName'] if dict['ParameterIsRequiredFlag'] == '1' else continue
    #                                            for dict in data[obj.title]['Results']['Parameter'] ]))
