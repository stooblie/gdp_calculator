import json
from collections import defaultdict

class Output():
    ''''''
    def __init__(self, output):
        self.output = None

    def parse(self):
        results = self.output['Results']

        pass

    def data_by_columns(self, data):
        dict = defaultdict(list)
        for entry in data:
            dict[entry['LineDescription']].append(entry['DataValue'])
        pass

    def display(self):
        pass
