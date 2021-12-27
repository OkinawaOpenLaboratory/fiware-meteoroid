import json
import requests
import hashlib

def main(params):

    forwarding_orion_host="http://<forwarding_orion_host>:1026"

    id = params['data'][0]['id']
    type = params['data'][0]['type']
    age = params['data'][0]['age']['value']
    address = params['data'][0]['address']['value']
    name = params['data'][0]['name']['value']
    anonymous_name = hashlib.sha256(name.encode("utf-8")).hexdigest()
    gender = params['data'][0]['gender']['value']

    data = {
            "actionType": "append",
            "entities": [{
                "id": id,
                "type": type,
                "address": {"type": "Text", "value": address.split("県")[0]},
                "name": {"type": "Text", "value": anonymous_name},
                "age": {"type": "Integer", "value":age},
                "gender": {"type": "Integer", "value":gender}
            }]
    }
    resp = requests.post(f'{forwarding_orion_host}/v2/op/update',
                         data=json.dumps(data),
                         headers={"Content-Type": "application/json"})
