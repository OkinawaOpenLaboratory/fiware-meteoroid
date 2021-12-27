# Anonymous Attribute

A sample function to anonymous Attribute by Orion subscription.

Register anonymized context information from Orion including personal information to the forwarding Orion.

## Setup

### Create Action

Create a function with the name anonymousAttribute.

```
meteoroid function create anonymousAttribute main.py --language python:3
+---------------------+-------------------------------------------------------------------------------+
| Field               | Value                                                                         |
+---------------------+-------------------------------------------------------------------------------+
| id                  | 1                                                                             |
| code                | import json                                                                   |
|                     | import requests                                                               |
|                     | import hashlib                                                                |
|                     |                                                                               |
|                     | def main(params):                                                             |
|                     |                                                                               |
|                     |     orion_host="http://<orion_host>:<orion_port>"                             |
|                     |                                                                               |
|                     |     id = params['data'][0]['id']                                              |
|                     |     type = params['data'][0]['type']                                          |
|                     |     age = params['data'][0]['age']['value']                                   |
|                     |     address = params['data'][0]['address']['value']                           |
|                     |     name = params['data'][0]['name']['value']                                 |
|                     |     anonymous_name = hashlib.sha256(name.encode("utf-8")).hexdigest()         |
|                     |     gender = params['data'][0]['gender']['value']                             |
|                     |                                                                               |
|                     |     data = {                                                                  |
|                     |             "actionType": "append",                                           |
|                     |             "entities": [{                                                    |
|                     |                 "id": id,                                                     |
|                     |                 "type": type,                                                 |
|                     |                 "address": {"type": "Text", "value": address.split("県")[0]}, |
|                     |                 "name": {"type": "Text", "value": anonymous_name},            |
|                     |                 "age": {"type": "Integer", "value":age},                      |
|                     |                 "gender": {"type": "Integer", "value":gender}                 |
|                     |             }]                                                                |
|                     |     }                                                                         |
|                     |     resp = requests.post(f'{orion_host}/v2/op/update',                        |
|                     |                          data=json.dumps(data),                               |
|                     |                          headers={"Content-Type": "application/json"})        |
|                     |                                                                               |
| language            | python:3                                                                      |
| binary              | False                                                                         |
| main                |                                                                               |
| version             | 0.0.1                                                                         |
| parameters          | []                                                                            |
| fiware_service      |                                                                               |
| fiware_service_path | /                                                                             |
| name                | anonymousAttribute                                                            |
+---------------------+-------------------------------------------------------------------------------+
```
### Create API

Create an API with the name /anonymous.

```
meteoroid endpoint create anonymous /attribute post 1
+---------------------+----------------------------------------------------------------------------------------------+
| Field               | Value                                                                                        |
+---------------------+----------------------------------------------------------------------------------------------+
| id                  | 1                                                                                            |
| url                 | http://<meteoroid_Host>:<meteoroid_port>/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/test1/test |
| fiware_service      |                                                                                              |
| fiware_service_path | /                                                                                            |
| name                | anonymous                                                                                    |
| path                | /attribute                                                                                   |
| method              | post                                                                                         |
| function            | 1                                                                                            |
+---------------------+----------------------------------------------------------------------------------------------+
```

### Create Entity

Create a Person Entity with person1.json.

```
curl -X POST http://<orion_host>:1026/v2/entities -H "Content-Type: application/json" -d @person1.json
```

### Create Subscription

Create a subscription with subscription.json.

```
curl -X POST http://<orion_host>:1026/v2/subscriptions -H "Content-Type: application/json" -d @subscription.json
```

## Execute

### update Entity

Register anonymized context information in the forwarding Orion.

```
curl -X PUT http://<orion_host>:1026/v2/entities/person1/attrs/age -H "Content-Type: text/plain" -d 25
```

```
curl http://<forwarding_orion_host>:1026/v2/entities
```

***response***

```
[
  {
    "id": "Person1",
    "type": "Person",
    "age": {
      "type": "Integer",
      "value": 25,
      "metadata": {}
    },
    "gender": {
      "type": "Integer",
      "value": "man",
      "metadata": {}
    }
  }
]
```

