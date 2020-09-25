# Validation

A sample validation function

## Setup

### Create Action

Create a virtualenv as follows:

```
docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash   -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
```

Create a zip file containing the virtualenv directory, schema.json and *__main__.py*.

```
zip -r custom.zip virtualenv __main__.py schema.json
```

Create a function with the name validation.

```
wsk action create validation custom.zip --kind python:3 --web true -i
```

### Create API

Create an API with the name /validation.

```
wsk api create /validation post validation -i
```

***response***

```
http://<openwhisk_host>:<openwhisk_port>/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/validation
```

### Apply validation

```bash
curl http://<openwhisk_host>:<openwhisk_port>/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/validation -H 'Content-Type: application/json' -d @- <<__EOS__
{
    "name": "Eggs",
    "price": 34.99
}
__EOS__
```

#### Success Response:

```
{'validaiton': 'success'}
```

#### Failed Response:

```
{'validation': 'failed', 'reason': "1 is not of type 'string'"}
```
