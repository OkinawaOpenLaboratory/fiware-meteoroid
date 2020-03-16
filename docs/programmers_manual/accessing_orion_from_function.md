# Accessing Orion from Function

You can access context data of Orion Context Broker from within the Meteoroid Function.

- [Python](#python)

## Python

### Create new entity

You can creates new entity to Orion as follows:

```python
import json
import requests

def main(params):
    url = 'http://orion:1026/v2/entities'
    headers = {'content-type': 'application/json'}
    payload = {
        'id': 'Room1',
        'type': 'Room',
        'temperature': {
            'value': 23,
            'type': 'Float'
        }
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    status_code = response.status_code
    return {'status_code': status_code}
```

### Read entity

You can get the temperature attribute of Room1 entity from Orion as follows:

```python
import requests

def main(params):
    url = 'http://orion:1026/v2/entities/Room1'
    response = requests.get(url)
    data = response.json()

    return {'temperature': data['temperature']}
```

### Update Entity

You can update the temperature attribute of Room1 entity as follows:

```python
import requests

def main(params):
    url = 'http://orion:1026/v2/entities/Room1/attrs/temperature/value'
    headers = {'content-type': 'text/plain'}
    update_value = 20
    response = requests.put(url, data=str(update_value), headers=headers)

    return {"status_code": response.status_code}
```
