import json
from collections import defaultdict
from api import Request
import yaml

#with open("./src_bea/generic.table.yaml", 'r') as stream:
    #try:
        #print(yaml.load(stream)['columns'])
    #except yaml.YAMLError as exc:
        #print(exc)

class Output():
    '''
    Collects the results of the API call results and puts the data into a usable format.
    '''
    def __init__(self, type, data):
        if type == 'bea':
            self.handle = "BEAAPI"
        else: self.handle = None
        self.parameters = data[self.handle]['Request']['RequestParam']
        self.results = data[self.handle]['Results']['Data']

        self.table = None
        self.time = None
        self.frequency = None

        # Keeping this here for future use. Define fields to look for depending on table.
        #self.table_schema = None

    def parse(self):
        for entry in self.parameters:
            column = lower(entry['ParameterName'])
            if entry['ParameterName'] == 'TABLENAME':
                self.table = self.type + '_' + lower(entry['ParameterValue'])
            if entry['ParameterName'] == 'FREQUENCY':
                self.frequency = self.type + '_' + lower(entry['ParameterValue'])
        pass

    def data_by_columns(self, data):
        dict = defaultdict(list)
        for entry in data:
            column = lower(entry['LineDescription'].replace(' ', '_'))
            dict[column].append(entry['DataValue'])

    def display(self):
        pass

if __name__ == '__main__':
    # Example response web API.
    data = json.load(open("./example_data.json", 'r'))

    obj = Output('bea', data)
    print(obj.results[0])
