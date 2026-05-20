import urllib.request
import json
import zipfile
import io

url = "https://github.com/BloodHoundAD/BloodHound/raw/master/examples/Sample%20Data/BloodHoundExampleData.zip"
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        with zipfile.ZipFile(io.BytesIO(response.read())) as z:
            for filename in z.namelist():
                if filename.endswith('users.json') or filename.endswith('groups.json'):
                    with z.open(filename) as f:
                        data = json.load(f)
                        print(filename)
                        print(json.dumps(data['data'][0], indent=2))
                        print("-------------")
except Exception as e:
    print("Failed:", e)
