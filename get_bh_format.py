import urllib.request
import json
url = "https://raw.githubusercontent.com/BloodHoundAD/BloodHound/master/examples/Sample%20Data/users.json"
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        print(json.dumps(data['data'][0], indent=2))
except Exception as e:
    print(e)
