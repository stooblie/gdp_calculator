import json
from collections import defaultdict
from api import Request

#

class Output():
    '''
    Collects the results of the API call results and puts the data into a usable format.
    '''
    def __init__(self, type, data):
        if type == 'bea':
            self.handle = 'BEAAPI'
        else self.handle = None
        self.parameters = data[self.handle]['Request']['RequestParam']
        self.results = data[self.type]['Request']['Results']

        self.table = None
        self.time = None
        self.frequency = None

    def parse(self):
        for entry in self.parameters:
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
        pass

    def display(self):
        pass

if __name__ == '__main__':
    pass
