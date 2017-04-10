from __future__ import print_function

import os
import logging

from botocore.vendored import requests


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ES_ENDPOINT = os.getenv('ES_ENDPOINT')
ES_INDEX = os.getenv('ES_INDEX', 'aws-submit')
ES_TYPE = os.getenv('ES_TYPE', 'faces')


def post_elasticsearch(data):
    request_url = 'https://{}/{}/{}'.format(ES_ENDPOINT, ES_INDEX, ES_TYPE)
    response = requests.post(request_url, json=data)
    return any([response.status_code == 200, response.status_code == 201])


def lambda_handler(event, context):
    result = {
        'total': len(event['faces']),
        'success': 0,
        'error': 0
    }

    for face in event['faces']:
        face.update({
            's3': event['s3'],
            'created_at': event['created_at']
        })

        res = post_elasticsearch(face)
        if not res:
            result['error'] += 1
        else:
            result['success'] += 1

    return result
