import json

def parse_bh(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    print(data['meta']['type'])
