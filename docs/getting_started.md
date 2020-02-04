# Getting started
## Download

```bash
git clone https://github.com/OkinawaOpenLaboratory/fiware-meteoroid.git --recursive && cd fiware-meteoroid/
```

## Install

OpenWhisk must be running to build Meteoroid.

### Install OpenWhisk

```bash
cd fiware-meteoroid/docker/openwhisk-devtools/docker-compose
make quick-start

```

### Install [Meteoroid CLI](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid-cli)

```bash
pip install meteoroid-cli
```

### Install Meteoroid

You can install Meteoroid in two ways:

- [Automatic installation](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid/tree/master#automatic-installation) using Docker (Docker Compose)
- [Manual installation](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid/tree/master#manual-installation) using pipenv and Django manage.py

---

## Automatic installation
using Docker (Docker Compose)

```bash
cd fiware-meteoroid/docker/
docker-compose up -d
```

### Export METEOROID_SCHEMA_ENDPOINT for CLI (Option)
Defualt endpoint (http://localhost:3000/schema/?format=corejson)

```
export METEOROID_SCHEMA_ENDPOINT=http://host:port/schema/?format=corejson
```

---

## Manual installation
using pipenv and Django manage.py

```
pipenv shell
pipenv install
```

### Migrate database

```bash
python manage.py migrate
```

### Run meteoroid

```bash
python manage.py runserver
```

### Export METEOROID_SCHEMA_ENDPOINT (Option) for CLI
Defualt endpoint (http://localhost:3000/schema/?format=corejson)

```bash
export METEOROID_SCHEMA_ENDPOINT=http://host:port/schema/?format=corejson
```

---

## Usage

#### Create a Python script

Create a Python script to register as Function.
```python
def main(arg):
    return {"test": "test"}
```

### Create Function

Create a function with the name function1.
You can pass parameters to Function with the param option.

```bash
meteoroid function create function1 function1.py --language python:3 --param orion_endpoint orion
```

### Create Endpoint

Create a endpoint with the name endpoint1.
For [FUNCTION_ID], specify the ID of the Function created in the previous step.

```bash
meteoroid endpoint create endpoint1 /hello post [FUNCTION_ID]
```

### Create Subscription

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

### Call Function by Orion Subscription

#### Create Entity

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

### Check result

If you can get the execution result of Function1, it is successful.

```bash
meteoroid result list
```

### Create Schedule

Schedule is a function that executes a function periodically.
Schedule can be defined by Cron-like description.

Create a schedule named schedule1.

```bash
curl -X POST http://localhost:3000/api/v1/schedules \
    -H 'Content-Type: application/json' \
    -d '{"function": FUNCTION_ID, "name": "schedule1", "schedule": "*/20 * * * * *"}'
```

### List Schedules

List schedules.

```bash
curl http://localhost:3000/api/v1/schedules
```

### Delete Schedule

Delete schedules.

```bash
curl -X DELETE http://localhost:3000/api/v1/schedules/SCHEDULE_ID
```
