import requests
import json


def main(args):
    status = args['data'][0]['status']['value']
    slack_url = args['slack_url']
    channel = args['channel']
    slack_params = {
        'channel': channel,
        'text': 'ステータスが{}になりました'.format(status),
    }
    requests.post(slack_url, data=json.dumps(slack_params))
    return {'result': 'success'}
