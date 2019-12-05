# Meteoroid

## Overview

Meteoroid realizes integrating Function as a Service(FaaS) capabilities in FIWARE.
It provides a management interface specialized for FaaS and FIWARE.


## Getting started
### Download

```bash
git clone https://github.com/OkinawaOpenLaboratory/fiware-meteoroid.git && cd fiware-meteoroid/
```

### Install

You can install Meteoroid in two ways:

- Manual installation using pipenv and Django manage.py
- Automatic installation using Docker (Docker Compose)

#### Manual installation using pipenv and Django manage.py

```
pipenv shell
pipenv install
```

##### Migrate database

```
python manage.py migrate
```

##### Run meteoroid

```
python manage.py runserver
```

#### Automatic installation using Docker

```bash
cd docker

docker-compose up -d
```

#### Install Meteoroid CLI

```bash
git clone https://github.com/OkinawaOpenLaboratory/fiware-meteoroid-cli.git && cd fiware-meteoroid-cli/
```

```bash
pip install .
```

### Usage

#### Create a Python script

Create a Python script to register as Function.

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
