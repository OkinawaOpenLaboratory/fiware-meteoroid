# Slack Notification

A sample function to notify the slack by updating the status.

## Setup

### Create Action

Create a function with the name slack_notification.
You can specify a slack_url and channel using the param option.

```
wsk action create slack_notification ./main.py --param slack_url https://hooks.slack.com/services/XXXXX/XXXXX --param channel "#CHANNEL_NAME" --web true -i
```

### Create API

Create an API with the name /slack_notification.

```
wsk api create /slack_notificaiton post slack_notification -i
```

***response***

```
http://<openwhisk_host>:<openwhisk_port>/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/slack_notificaiton
```

### Create Entity

Create a Switch entity.

```bash
curl -H "Content-Type: application/json" http://<orion_host>:1026/v2/entities -X POST -d @- <<__EOS__
{
  "id": "Switch01",
  "type": "Switch",
  "status": {
    "type": "string",
    "value": "OFF"
  }
}
__EOS__
```


### Create Subscription

Create a subscription.

```bash
curl -H "Content-Type: application/json" http://<orion_host>:1026/v2/subscriptions -X POST -d @- <<__EOS__
{
  "description": "A subscription to get status about Switch01",
  "subject": {
    "entities": [
      {
        "id": "Switch01",
        "type": "Switch"
      }
    ],
    "condition": {
      "attrs": [
        "status"
      ]
    }
  },
  "notification": {
    "http": {
      "url": "http://<openwhisk_host>:<openwhisk_port>/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/slack_notificaiton"
    },
    "attrs": [
      "status"
    ]
  },
  "throttling": 5
}
__EOS__
```

### update Status

Notify the slack by updating the status.

```bash
curl http://<orion_host>:1026/v2/entities/Switch01/attrs -H 'Content-Type: application/json' -d @- <<__EOS__
{
    "status": {
        "value": "ON"
    }
}
__EOS__
```

