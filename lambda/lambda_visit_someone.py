from __future__ import print_function
import urllib
import logging
import boto3
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def normalize(faces):
    result = []
    for face in faces:
        if face['Confidence'] < 90:
            continue

        normalized_face = {
            'Eyeglasses': False,
            'Gender': 'Male',
            'Emotions': face['Emotions'],
            'Age': (face['AgeRange']['High'] + face['AgeRange']['Low']) / 2,
            'Smile': 0,
            'Created_At': str(datetime.now())
        }

        if (face['Eyeglasses']['Value'] is True and face['Eyeglasses']['Confidence'] > 90):
            normalized_face['Eyeglasses'] = True

        if face['Smile']['Value'] is True:
            normalized_face['Smile'] = face['Smile']['Confidence']

        result.append(normalized_face)

    return result


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

    return normalize(faces)
