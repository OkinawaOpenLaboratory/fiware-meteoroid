# Getting started

This getting started realizes a scenario such as the following image.

1. The user updates the temperature attribute of the Room entity using curl.
2. Orion notifies to the thermometer.py as a function in OpenWhisk. (HTTP POST)
3. The function writes messages according to the value of temperature to result.
4. User can confirm results using wsk.



## Install

### Install [OpenWhisk](https://github.com/apache/openwhisk)

```
cd fiware-meteoroid/docker/openwhisk-devtools/docker-compose
make quick-start
```



## Set API Host

```
wsk property set --apihost <OPENWHISK API HOST>
```

Output:

```
ok: whisk API host set to <OPENWHISK API HOST>
```



## Usage

### Create a Python script

Create a Python script named **thermometer.py**. The first argument of the main function is provided POST parameter and function param option.

#### Parameters

- **temperature**: The temperature is given an attribute of Entity as the HTTP request parameter(POST) assumed structures of Orion notification.
- **threshold**: The threshold is given parameters when creating or updating function as a command line option.

[Support Language](https://openwhisk.apache.org/documentation.html#actions-creating-and-invoking)

```
def main(params):
    temperature = params['data'][0]['temperature']['value']
    threshold = int(params['threshold'])
    message = "No problem."
    if temperature > threshold:
        message = "Dangerous because it’s too hot!"
    print(temperature, message)
    return {"temperature": temperature, "message": message}
```

------

### Create Function

Create a function with the name **Thermometer**. You can pass parameters to Function with the **param** option.

```
wsk action create Thermometer thermometer.py --param threshold 35 --web true -i
```

Output:

```
ok: created action Thermometer
```

------

### Create API

Create an api with the name hello. For function ID, specify the ID of the Function created in the previous step.

```
wsk api create room /thermometer post Thermometer -i
```

Output:

```
ok: created API room/thermometer POST for action /_/Thermometer
http://192.168.128.100:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/room/thermometer
```

------

### Invoke the function using curl

Invoke the function with the URL obtained when created endpoint. Request parameter is specified as JSON assuming structures of Orion notification.

```
curl -X POST http://192.168.128.100:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/room/thermometer -H 'Content-Type: application/json' -d @- <<__EOS__
{
    "data": [{
        "temperature": {
            "value": 30
        }
    }]
}
__EOS__
```

Output:

```
{
  "message": "No problem.",
  "temperature": 30
}
```

------

### Create Entity

Subscription is notified to OpenWhisk by creating an entity. The function is called by Orion subscription.

```
curl http://localhost:1026/v2/entities -X POST -H 'Content-Type: application/json' -d @- <<__EOS__
{
    "id": "Room1",
    "type": "Room",
    "temperature": {
        "type": "Number",
        "value": 25
    }
}
__EOS__
```

------

### Create Subscription

Create a subscription.

```
curl -H "Content-Type: application/json" http://localhost:1026/v2/subscriptions -X POST -d @- <<__EOS__
{
  "description": "A subscription to get status about Room1",
  "subject": {
    "entities": [
      {
        "id": "Room1",
        "type": "Room"
      }
    ],
    "condition": {
      "attrs": [
        "temperature"
      ]
    }
  },
  "notification": {
    "http": {
      "url": "http://192.168.128.100:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/room/thermometer"
    },
    "attrs": [
      "status"
    ]
  },
  "throttling": 5
}
__EOS__
```



### Invoke the function using Orion subscription

Update the temperature attribute using curl.

```
curl http://localhost:1026/v2/entities/Room1/attrs -H 'Content-Type: application/json' -d @- <<__EOS__
{
    "temperature": {
        "value": 40
    }
}
__EOS__
```

------

### Confirm result list

Obtain results of function using wsk. You cannot obtain the latest results unless You execute the following command twice.

```
wsk activation list -i
wsk activation list -i
```

Output:

```
Datetime            Activation ID                    Kind                 Start Duration   Status            Entity
2020-07-14 17:57:41 fecb0e4e498046ce8b0e4e4980d6ced7 python:3             cold  975ms      success           guest/Thermometer:0.0.1
2020-07-14 17:28:52 e4956fd59cfb401c956fd59cfb901c73 nodejs:10            cold  157ms      success           guest/hello:0.0.2
2020-07-14 17:28:42 67af88bf6ec04039af88bf6ec0103962 nodejs:10            cold  102ms      success           guest/hello:0.0.1
```

------

### Confirm message of function

Show a result using the activation ID.

```
wsk activation result fecb0e4e498046ce8b0e4e4980d6ced7 -i
```

Output:

```
{
    "message": "No problem.",
    "temperature": 30
}
```
