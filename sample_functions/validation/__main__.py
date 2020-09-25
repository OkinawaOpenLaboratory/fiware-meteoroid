import json
import uuid
from jsonschema import validate, ValidationError

schema = {}

# Define the schema to schema.json for the validation
with open('./schema.json') as f:
    schema = json.load(f)


def convert_to_ngsi_entity(data, schema):
    entity_id = str(uuid.uuid4())
    entity_type = schema['type']
    result = {}
    if 'id' in data:
        entity_id = data['id']
    if 'type' in data:
        entity_type = data['type']
    result['id'] = entity_id
    result['type'] = entity_type
    attrs = {k: v for k, v in data.items() if k not in ['id', 'type']}
    for k, v in attrs.items():
        if k in schema['properties']:
            attr_type = schema['properties'][k]['type']
            result[k] = {
                'value': data[k],
                'type': attr_type
            }
    return result


def main(args):
    try:
        validate(instance=args, schema=schema)
        entity = convert_to_ngsi_entity(args, schema)
        return {'validation': 'success', 'entity': entity}
    except ValidationError as e:
        return {'validation': 'failed', 'reason': e.message}


if __name__ == '__main__':
    args = {
        "id": "Grocery1",
        "name": "Eggs",
        "price": 34.99
    }
    print(main(args))
