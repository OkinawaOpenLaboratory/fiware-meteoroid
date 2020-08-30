import json
import requests
from jsonschema import validate, ValidationError

schema = {}

# Define the schema to schema.json for the validation
with open('./schema.json') as f:
    schema = json.load(f)


def main(args):
    try:
        validate(instance=args, schema=schema)
        return {'validation': 'success'}
    except ValidationError as e:
        return {'validation': 'failed', 'reason': e.message}
