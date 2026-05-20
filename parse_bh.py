import json

def read_bh(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
        meta = data.get('meta', {})
        if meta.get('type') == 'users':
            print("USERS")
            for user in data.get('data', []):
                props = user.get('Properties', {})
                print(f"Name: {props.get('name')}, domain: {props.get('domain')}, hasspn: {props.get('hasspn')}, dontreqpreauth: {props.get('dontreqpreauth')}")
        elif meta.get('type') == 'groups':
            print("GROUPS")
            for group in data.get('data', []):
                props = group.get('Properties', {})
                print(f"Name: {props.get('name')}, domain: {props.get('domain')}")
