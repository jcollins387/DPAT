import json
data = {
  "data": [
    {
      "Properties": {
        "domain": "TEST.LOCAL",
        "name": "ADMINISTRATOR@TEST.LOCAL"
      },
      "ObjectIdentifier": "S-1-5-21-1234-500"
    }
  ],
  "meta": {
    "type": "users"
  }
}
print(data['data'][0]['Properties']['name'].split('@')[0])
