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
    '''
    This class handles performing a web request for information from a specified government economic database.

    :param type:
    :param method:
    :param parameters: A list of tuples containing parameter and value pairs.
    '''
    def __init__(self, type, method, parameters=None, format='json'):
        #Base parameters
        self.type = type
        self.uri = api_dict[type]['uri']
        self.method = method
        self.key = '&UserID=' + os.environ[api_dict[type]['key']]
        self.format = api_dict[type]['format'][format]

        self.parameters = dict(parameters)
        self.required = api_dict[type]['method'][method]['parameters']['required']
        self.optional = api_dict[type]['method'][method]['parameters']['optional']

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
        url = self.uri + self.key + self.format + self.method
        for param, value in self.parameters:
            url += '&{}={}'.format(param, value)

        response = http.request('GET',)
        return response

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

    def check_parameters(self):
        for req in self.required:
            if req not in self.parameters:
                print('Missing required parameter {}. Please supply this parameter and retry.'.format(req))
            else: continue

    def display_data(self):
        data = self.get_data()
        for i in data['BEAAPI']['Results']['Dataset']:
            print(i['DatasetName'] + '\n' + i['DatasetDescription'] + '\n\n')
        #print(json.dumps(data, indent=4, sort_keys=True))

# Sysarg format: Type, Method, Dataset_Name, Table_Name, Frequency, Year
# Example: DataSet = NIPA, TableName = T10101, Frequency = Q, Year = 2018
# Table Results: BEAAPI > Results > Data/Notes
if __name__ == '__main__':
    # Database/type specified by command ine argument.
    type = sys.argv[1]
    print('Type: {}'.format(type))
    # Method is a command line argument.
    method = sys.argv[2]
    print('Method: {}'.format(method))
    print('Example Parameters for Get Data: DataSet = NIPA, TableName = T10101, Frequency = Q, Year = 2018')
    # Parameters defined by prompting for user keyboard input (for now).
    parameters = list()
    required_parameters = api_dict[type]['method'][method]['parameters']['required']
    optional_parameters = api_dict[type]['method'][method]['parameters']['optional']
    for param in required_parameters:
        value = input('{} (required):'.format(param))
        parameters.append( (param, value) )
    for i in optional_parameters:
        value = input('{} (optional):'.format(param))
        parameters.append( (param, value) )

    #print('kwargs: {}'.format(kwargs))
    obj = Request(type, method, parameters)
    data = obj.get_data()
    data_dict = ast.literal_eval(json.dumps(data))
    #print(data_dict['BEAAPI']['Results'])
    print(json.dumps(data, indent=4, sort_keys=True))
    #print('Required Parameteres:\n{}'.format([dict['ParameterName'] if dict['ParameterIsRequiredFlag'] == '1' else continue
    #                                            for dict in data[obj.title]['Results']['Parameter'] ]))
