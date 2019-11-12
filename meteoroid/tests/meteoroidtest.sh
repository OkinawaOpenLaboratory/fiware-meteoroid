#!/bin/bash

if !(type "jq" > /dev/null 2>&1); then
    echo "This script requires jq."
    echo "    Install: apt install jq"
    exit
fi

FUNCTION_ID=`curl -sS -X POST http://localhost:8000/api/v1/functions -H 'Content-Type: application/json' -d '{
    "code": "def main(arg): return {\"test\": \"test\"}",
    "language": "python:3",
    "parameters": [{"key": "orion_endpoint", "value": "xxxxxxxxx"}],
    "fiware_service": "",
    "fiware_service_path": "/",
    "name": "function1"
}' | jq .id` && echo 'Create Function '${FUNCTION_ID}'... OK' || echo "Create Function... NG"

ENDPOINT_ID=`curl -sS -X POST http://localhost:8000/api/v1/endpoints -H 'Content-Type: application/json' -d '{
    "name": "endpoint1",
    "path": "/hello",
    "method": "post",
    "function": '${FUNCTION_ID}',
    "fiware_service": "",
    "fiware_service_path": "/"
}' | jq .id` && echo 'Create Endpoint '${ENDPOINT_ID}'... OK' || echo "Create Function... NG"

SUB_ID=`curl -sS -X POST http://localhost:8000/api/v1/subscriptions -H 'Content-Type: application/json' -d '{
    "fiware_service": "",
    "fiware_service_path": "/",
    "endpoint_id": '${ENDPOINT_ID}',
    "orion_subscription": {
        "description": "test subscription",
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
    }
}' | jq .id` && echo 'Create Subscription '${SUB_ID}'... OK' || echo "Create Subscription... NG"

curl -sS http://localhost:1026/v2/entities -H 'Content-Type: application/json' -d '{
    "id": "Room1",
    "type": "Room",
    "temperature": {
        "value": 23,
        "type": "Float"
    }
}' && echo 'Create Entity... OK'

sleep 10

RESULT_ID=`curl -sS http://localhost:8000/api/v1/results | jq .[0].activationId` && echo 'Get Result '${RESULT_ID}'... OK' || echo "Get Result... NG"

curl -sS -X DELETE http://localhost:1026/v2/entities/Room1 && echo "Delete Entity... OK" || echo "Delete Entity... NG"

curl -sS -X DELETE http://localhost:8000/api/v1/subscriptions/${SUB_ID} && echo "Delete Subscription ${SUB_ID}... OK" || echo "Delete Subscription... NG"

curl -sS -X DELETE http://localhost:8000/api/v1/endpoints/${ENDPOINT_ID} && echo "Delete Endpoint ${ENDPOINT_ID}... OK" || echo "Delete Endpoint... NG"

curl -sS -X DELETE http://localhost:8000/api/v1/functions/${FUNCTION_ID} && echo "Delete Function ${FUNCTION_ID}... OK" || echo "Delete Function... NG"
