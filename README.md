# Meteoroid

![PyPI](https://img.shields.io/pypi/v/meteoroid-cli)
![GitHub](https://img.shields.io/github/license/OkinawaOpenLaboratory/fiware-meteoroid?color=blue)

## Overview

Meteoroid realizes integrating Function as a Service(FaaS) capabilities in FIWARE.
It provides a management interface specialized for FaaS and FIWARE.


## Getting started
### Download

```bash
git clone https://github.com/OkinawaOpenLaboratory/fiware-meteoroid.git --recursive && cd fiware-meteoroid/
```

### Install

OpenWhisk must be running to build Meteoroid.

#### Install OpenWhisk

```bash
cd fiware-meteoroid/docker/openwhisk-devtools/docker-compose
make quick-start

```

#### Install [Meteoroid CLI](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid-cli)

```bash
pip install meteoroid-cli
```

#### Install Meteoroid

You can install Meteoroid in two ways:

- [Automatic installation](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid/tree/master#automatic-installation) using Docker (Docker Compose)
- [Manual installation](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid/tree/master#manual-installation) using pipenv and Django manage.py

---

### Automatic installation
using Docker (Docker Compose)

```bash
cd fiware-meteoroid/docker/
docker-compose up -d
```

#### Export METEOROID_SCHEMA_ENDPOINT (Option) for CLI
Defualt endpoint (http://localhost:3000/schema/?format=corejson)

```
export METEOROID_SCHEMA_ENDPOINT=http://host:port/schema/?format=corejson
```

---

### Manual installation
using pipenv and Django manage.py

```
pipenv shell
pipenv install
```

#### Migrate database

```
python manage.py migrate
```

#### Run meteoroid

```bash
python manage.py runserver
```

#### Export METEOROID_SCHEMA_ENDPOINT (Option) for CLI
Defualt endpoint (http://localhost:3000/schema/?format=corejson)

```
export METEOROID_SCHEMA_ENDPOINT=http://host:port/schema/?format=corejson
```

---

### Usage

#### Create a Python script

Create a Python script to register as Function.
```python
def main(arg):
    return {"test": "test"}
```

#### Create Function

Create a function with the name function1.
You can pass parameters to Function with the param option.

```bash
meteoroid function create function1 function1.py --language python:3 --param orion_endpoint orion
```

#### Create Endpoint

Create a endpoint with the name endpoint1.
For [FUNCTION_ID], specify the ID of the Function created in the previous step.

```bash
meteoroid endpoint create endpoint1 /hello post [FUNCTION_ID]
```

#### Create Subscription

Create a subscription.

```bash
meteoroid subscription create [ENDPOINT_ID] '{
        "description": "Example subscription",
        "subject": {
            "entities": [
	        {
	            "id": "Room1",
       	            "type": "Room"
	        }
	    ]
        },
        "notification": {
            "attrs": [
	        "temperature"
            ]
        },
        "expires": "2040-01-01T14:00:00.00Z",
        "throttling": 1
    }'
```

#### Call Function by Orion Subscription

##### Create Entity

Subscription is notified to Meteoroid by creating entity.
The function1 is called by orion subscription.

```bash
curl -sS http://localhost:1026/v2/entities -H 'Content-Type: application/json' -d '{
    "id": "Room1",
    "type": "Room",
    "temperature": {
        "value": 23,
        "type": "Float"
    }
}'
```

#### Check result

If you can get the execution result of Function1, it is successful.

```bash
meteoroid result list
```

## Support language

Currently, supported languages depend on [OpenWhisk](https://openwhisk.apache.org/documentation.html#actions-creating-and-invoking).

* [Python3](./docs/function/python.md)
* [Java(JDK8)](./docs/function/java.md)
