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
        self.handle = api_dict[type]['method'][method]['handle']
        self.key = '&UserID=' + os.environ[api_dict[type]['key']]
        self.format = api_dict[type]['format'][format]

        self.parameters = dict(parameters)
        self.required = api_dict[type]['method'][method]['parameters']['required']
        self.optional = api_dict[type]['method'][method]['parameters']['optional']

        #print('In class type is: {}'.format(self.type))
        #print('In class method is: {}'.format(self.method))
        #print('In class handle is: {}'.format(self.handle))
        #print('In class uri is: {}'.format(self.uri))
        #print('In class format is: {}'.format(self.format))
        #print('In class parameters is: {}'.format(self.parameters))

        #self.url = self.uri + self.key + self.method + self.format
    def execute_method(self):
        print('Running execute_method...')
        if self.method in ["list_datasets", "get_parameter_list", "get_parameter_values", "get_parameter_values_filtered"]:
            print('Running get_metadata method...')
            response = self.get_metadata()
            data = json.loads(response.data)
        if self.method == 'get_data':
            print('Running get_data method...')
            data = self.get_data()
        else: pass

        return data

    def get_metadata(self):
        url = self.uri + self.key + self.format + self.handle
        for param, value in self.parameters.items():
            url += '&{}={}'.format(param, value)

        print('Request URL: {}'.format(url))
        response = http.request('GET', url)
        return response

    def get_data(self):
        url = self.uri + self.key + self.format + self.handle
        for param, value in self.parameters.items():
            url += '&{}={}'.format(param, value)

        response = http.request('GET', url)
        #print(response.data)
        data = json.loads(response.data)
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
    # Database/type specified by command line argument.
    type = sys.argv[1]
    print('Type: {}'.format(type))

    # Method is a command line argument.
    method = sys.argv[2]
    print('Method: {}'.format(method))
    print('Example Parameters for Get Data: DataSet = NIPA, TableName = T10101, Frequency = Q, Year = 2018')

    # Parameters defined by prompting for user keyboard input (for now).
    parameters = list()
    dataset = None
    required_parameters = api_dict[type]['method'][method]['parameters']['required']
    optional_parameters = api_dict[type]['method'][method]['parameters']['optional']
    for param in required_parameters:
        # Do not need to input key/UserID, included in configuration. Method is a command line argument.
        if param in ['UserID', 'Method']: continue
        value = input('{} (required):'.format(param))
        # Keep dataset name stored outside for grabbing extra parameters for a get_data method.
        if param == 'DatasetName': dataset = value
        parameters.append( (str(param), value) )
    for param in optional_parameters:
        # Do not need to define result format, already set to json by default.
        if param == 'ResultFormat': continue
        value = input('{} (optional):'.format(param))
        parameters.append( (str(param), value) )

    # If the method is get_data, need to run a second loop to add dataset specific parameters.
    if method == 'get_data':
        required_parameters = api_dict[type]['method'][method]['parameters'][dataset]['required']
        try:
            optional_parameters = api_dict[type]['method'][method]['parameters'][dataset]['optional']
        except:
            optional_parameters = None
        for param in required_parameters:
            value = input('{} (required):'.format(param))
            parameters.append( (param, value) )
        if optional_parameters != None:
            for param in optional_parameters:
                value = input('{} (optional):'.format(param))
                parameters.append( (param, value) )

    print('Complete Parameters list: {}'.format(parameters))

    #print('kwargs: {}'.format(kwargs))
    obj = Request(type, method, parameters)
    data = obj.execute_method()
    print('Data JSON Object: {}'.format(data))
    data_dict = ast.literal_eval(json.dumps(data))
    #print(data_dict['BEAAPI']['Results'])
    print(json.dumps(data, indent=4, sort_keys=True))
