from __future__ import print_function
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    faces = list()
    for face in event['faces']:
        if face['Confidence'] < 90:
            continue

        normalized_face = {
            'Eyeglasses': False,
            'Gender': 'Male',
            'Emotions': face['Emotions'],
            'Age': (face['AgeRange']['High'] + face['AgeRange']['Low']) / 2,
            'Smile': 0,
            'BoundingBox': face['BoundingBox']
        }

        if (face['Eyeglasses']['Value'] is True and face['Eyeglasses']['Confidence'] > 90):
            normalized_face['Eyeglasses'] = True

        if face['Smile']['Value'] is True:
            normalized_face['Smile'] = face['Smile']['Confidence']

        faces.append(normalized_face)

    return {
        'faces': faces,
        's3': event['s3'],
        'created_at': event['created_at']
    }
