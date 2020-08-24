from jsonschema import validate, ValidationError

# Define the schema for the validation
schema = {
    "type": "object",
    "properties": {
        "price": {"type": "number"},
        "name": {"type": "string"},
    },
}


def main(args):
    try:
        validate(instance=args, schema=schema)
        return {"validaiton": "success"}
    except ValidationError as e:
        return {"validation": "failed", "reason": e.message}
