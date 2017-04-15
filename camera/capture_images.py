# -*- coding: utf-8 -*-

import os
import sys
import time
from collections import deque
from datetime import datetime, timedelta
from importlib import import_module
from threading import Thread
from Queue import Queue

import cv2
import boto3
from botocore.exceptions import ClientError

try:
    CONFIG = import_module('config')
except ImportError as e:
    sys.exit('Error: {}\n'
             'Copy config.sample.py to config.py and modify it.'
             .format(str(e)))

SENSITIVITY = 2000
WAIT_SECONDS = 3

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', CONFIG.AWS_ACCESS_KEY_ID)
AWS_ACCESS_KEY_SECRET = os.getenv('AWS_ACCESS_KEY_SECRET', CONFIG.AWS_ACCESS_KEY_SECRET)
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', CONFIG.AWS_BUCKET_NAME)
AWS_REGION = os.getenv('AWS_REGION', CONFIG.AWS_REGION)
CAMERA_NAME = os.getenv('CAMERA_NAME', CONFIG.CAMERA_NAME)
DISPLAY = os.getenv('DISPLAY', CONFIG.DISPLAY)
IMG_WIDTH = os.getenv('IMG_WIDTH', CONFIG.IMG_WIDTH)
IMG_HEIGHT = os.getenv('IMG_HEIGHT', CONFIG.IMG_HEIGHT)


def initial_camera(width, height):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print 'Can\'t open a camera'
        return False

    cam.set(3, width)
    cam.set(4, height)

    # Wait a moment while the camera adjusts to light levels
    time.sleep(1)

    return cam


def initial_s3():
    s3 = boto3.client('s3',
                      AWS_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_ACCESS_KEY_SECRET)
    bucket = None
    try:
        bucket = s3.create_bucket(
            Bucket=AWS_BUCKET_NAME,
            CreateBucketConfiguration={
                'LocationConstraint': AWS_REGION
            })
    except ClientError:
        # print str(e)
        print '{} bucket is exist.'.format(AWS_BUCKET_NAME)

    if bucket:
        s3.put_bucket_lifecycle_configuration(
            Bucket=AWS_BUCKET_NAME,
            LifecycleConfiguration={
                'Rules': [{
                    'Status': 'Enabled',
                    'Prefix': '',
                    'Expiration': {
                        'Days': 1
                    }
                }]
            })

    return s3


def get_image(cam):
    return cam.read()[1]


def motion_event(cam, cv_images):
    event_time = datetime.now()
    while 1:
        delta = cv2.absdiff(cv_images[0], cv_images[2])
        __, delta_diff = cv2.threshold(delta, 16, 255, 3)
        cv2.normalize(delta_diff, delta_diff, 0, 255, cv2.NORM_MINMAX)
        diff_gray = cv2.cvtColor(delta_diff, cv2.COLOR_RGB2GRAY)
        diff_count = cv2.countNonZero(diff_gray)
        delta_diff = cv2.flip(delta_diff, 1)

        # Event
        if datetime.now() > event_time and diff_count >= SENSITIVITY:
            event_time = datetime.now() + timedelta(seconds=WAIT_SECONDS)
            image = get_image(cam)
            print 'Catch a motion.'
            yield image

        cv_images.rotate()
        cv_images[0] = get_image(cam)
        cv_images[0] = cv2.blur(cv_images[0], (8, 8))


def get_faces(faceCascade, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        return faces


def _upload_to_s3(s3, queue):
    while True:
        file_path = queue.get()
        try:
            s3.upload_file(file_path, AWS_BUCKET_NAME,
                           CAMERA_NAME + '/' + file_path.split('/')[-1],
                           ExtraArgs={
                               'ContentType': 'image/jpeg',
                               'Metadata': {
                                   'x-amz-meta-width': str(IMG_WIDTH),
                                   'x-amz-meta-height': str(IMG_HEIGHT)
                               }
                           })
        except Exception as e:
            print str(e)
        finally:
            os.unlink(file_path)
            queue.task_done()

        time.sleep(0.1)


def main():
    cam = initial_camera(IMG_WIDTH, IMG_HEIGHT)
    s3 = initial_s3()
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface.xml')
    cv_images = deque()

    queue = Queue()
    t = Thread(target=_upload_to_s3, args=(s3, queue))
    t.start()

    for idx in xrange(0, 3):
        cv_images.append(get_image(cam))
        cv_images[idx] = cv2.resize(cv_images[idx], (IMG_WIDTH, IMG_HEIGHT))

    motion_images = motion_event(cam, cv_images)
    for image in motion_images:
        faces = get_faces(faceCascade, image)
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if len(faces):
            filename = ('{}.jpg'
                        .format(datetime.now().strftime("%Y%m%d_%H%M%S")))
            file_path = os.path.join('/tmp', filename)
            cv2.imwrite(file_path, image)

            print '[{}] Find face({})'.format(datetime.now(), len(faces))

            queue.put(file_path)
            if DISPLAY is True:
                cv2.imshow('viewer', image)
                cv2.waitKey(1)

        time.sleep(0.1)

    cam.release()
    t.join()
    if DISPLAY is True:
        cv2.destoryAllWindows()

if __name__ == "__main__":
    main()
