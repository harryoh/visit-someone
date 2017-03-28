from __future__ import print_function
import urllib
import logging
import boto3
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    region = event['Records'][0]['awsRegion']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
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
        return False

    return {
        'faces': faces,
        's3': {
            'region': region,
            'bucket': bucket,
            'name': key
        },
        'created_at': str(datetime.now())
    }
