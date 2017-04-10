from __future__ import print_function
import urllib
import logging
import boto3
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    bucket = event['detail']['requestParameters']['bucketName']
    region = event['detail']['awsRegion']
    key = urllib.unquote_plus(event['detail']['requestParameters']['key'].encode('utf8'))
    client = boto3.client('rekognition', region)

    response = client.detect_faces(
        Attributes=['ALL'],
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        }
    )

    faces = response['FaceDetails']

    if not len(response['FaceDetails']):
        faces = False

    return {
        'faces': faces,
        's3': {
            'region': region,
            'bucket': bucket,
            'key': key
        },
        'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    }
