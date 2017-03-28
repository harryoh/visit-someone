# 라즈베리파이
### python 설치
### opencv 설치

```
sudo apt-get update
sudo apt-get -y upgrade
sudo rpi-update

sudo apt-get install build-essential git cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libgtk2.0-dev libatlas-base-dev gfortran
```

```
$ sudo apt-get install -y python2.7-dev
$ pip install --upgrade pip
```

```
$ mkdir ~/work;cd $_
$ git clone https://github.com/Itseez/opencv.git
$ cd opencv
$ git checkout 3.1.0
```

```
$ cd ~/work
$ git clone https://github.com/Itseez/opencv_contrib.git
$ cd opencv_contrib
$ git checkout 3.1.0
```

```
$ cd ~/work/opencv
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/work/opencv_contrib/modules \
	-D BUILD_EXAMPLES=ON ..
```

```
$ nohup make &
$ tail -f nohup.out
```

```
$ sudo make install
$ sudo ldocnfig
```

```
$ python
>>> import cv2
>>> 
```

### S3 Credential
### Config
### RUN


# Role

### Create Role

```
$ aws iam create-role --role-name visit-someone-role \
--assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": { "Service": "lambda.amazonaws.com" },
        "Action": "sts:AssumeRole"
    }]
}'

# output

{
    "Role": {
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    }
                }
            ]
        },
        "RoleId": "AROAILLL665OMCWWVYXFA",
        "CreateDate": "2017-03-21T14:13:06.616Z",
        "RoleName": "visit-someone-role",
        "Path": "/",
        "Arn": "arn:aws:iam::550931752661:role/visit-someone-role"
    }
}
```

### Add S3 Permission

```
$ aws iam put-role-policy \
--role-name visit-someone-role \
--policy-name VisitSomeoneS3FullAccess \
--policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "s3:*",
        "Resource": "arn:aws:s3:::visit.someone/*"
    }]
}'
```

### Add Lambda Permission

```
$ aws iam attach-role-policy \
--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
--role-name visit-someone-role
```

### Add Rekognition Permission

```
$ aws iam attach-role-policy \
--policy-arn arn:aws:iam::aws:policy/AmazonRekognitionFullAccess \
--role-name visit-someone-role
```



# Lambda

### AWS Credential

### Install emulambda

```
$ pip install emulambda
```

### lambda_face_analysis.py

```
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
```

### s3put_event.json

```
{
  "Records": [
    {
      "eventVersion": "2.0",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "s3": {
        "configurationId": "testConfigRule",
        "object": {
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901",
          "key": "test.jpg",
          "size": 84278
        },
        "bucket": {
          "arn": "arn:aws:s3:::funnyfaces",
          "name": "funnyfaces",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          }
        },
        "s3SchemaVersion": "1.0"
      },
      "responseElements": {
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
        "x-amz-request-id": "EXAMPLE123456789"
      },
      "awsRegion": "ap-northeast-2",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "eventSource": "aws:s3"
    }
  ]
}
```

### lambda_normalize.py

```
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
            'Smile': 0
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
```

### face_analysis_event.json

```
{
    "s3":{
        "region":"us-west-2",
        "bucket":"visit.someone",
        "name":"test.jpg"
    },
    "created_at":"2017-03-28 22:48:21.784109",
    "faces":[
        {
            "Confidence":99.97056579589844,
            "Eyeglasses":{
                "Confidence":99.95707702636719,
                "Value": false
            },
            "Sunglasses":{
                "Confidence":98.92345428466797,
                "Value": false
            },
            "Gender":{
                "Confidence":99.92604064941406,
                "Value":"Male"
            },
            "Landmarks":[
                {
                    "Y":0.30275556445121765,
                    "X":0.347167432308197,
                    "Type":"eyeLeft"
                },
                {
                    "Y":0.36305585503578186,
                    "X":0.48134320974349976,
                    "Type":"eyeRight"
                },
                {
                    "Y":0.42722126841545105,
                    "X":0.41235440969467163,
                    "Type":"nose"
                },
                {
                    "Y":0.5120241045951843,
                    "X":0.3270901143550873,
                    "Type":"mouthLeft"
                },
                {
                    "Y":0.5528923869132996,
                    "X":0.4303555488586426,
                    "Type":"mouthRight"
                },
                {
                    "Y":0.3059152364730835,
                    "X":0.3448222279548645,
                    "Type":"leftPupil"
                },
                {
                    "Y":0.3625945746898651,
                    "X":0.48040908575057983,
                    "Type":"rightPupil"
                },
                {
                    "Y":0.21726252138614655,
                    "X":0.3077225685119629,
                    "Type":"leftEyeBrowLeft"
                },
                {
                    "Y":0.20653237402439117,
                    "X":0.35335808992385864,
                    "Type":"leftEyeBrowRight"
                },
                {
                    "Y":0.2363770306110382,
                    "X":0.3961260914802551,
                    "Type":"leftEyeBrowUp"
                },
                {
                    "Y":0.27234551310539246,
                    "X":0.4717646539211273,
                    "Type":"rightEyeBrowLeft"
                },
                {
                    "Y":0.2787947356700897,
                    "X":0.5092535614967346,
                    "Type":"rightEyeBrowRight"
                },
                {
                    "Y":0.3084357678890228,
                    "X":0.535347580909729,
                    "Type":"rightEyeBrowUp"
                },
                {
                    "Y":0.29425984621047974,
                    "X":0.3234119117259979,
                    "Type":"leftEyeLeft"
                },
                {
                    "Y":0.31245723366737366,
                    "X":0.371552437543869,
                    "Type":"leftEyeRight"
                },
                {
                    "Y":0.29424184560775757,
                    "X":0.34868162870407104,
                    "Type":"leftEyeUp"
                },
                {
                    "Y":0.3106662929058075,
                    "X":0.34533846378326416,
                    "Type":"leftEyeDown"
                },
                {
                    "Y":0.35337427258491516,
                    "X":0.45938533544540405,
                    "Type":"rightEyeLeft"
                },
                {
                    "Y":0.37366944551467896,
                    "X":0.5035064816474915,
                    "Type":"rightEyeRight"
                },
                {
                    "Y":0.35477784276008606,
                    "X":0.4827948212623596,
                    "Type":"rightEyeUp"
                },
                {
                    "Y":0.37086790800094604,
                    "X":0.47978901863098145,
                    "Type":"rightEyeDown"
                },
                {
                    "Y":0.44320812821388245,
                    "X":0.3692103922367096,
                    "Type":"noseLeft"
                },
                {
                    "Y":0.4658723473548889,
                    "X":0.4281693994998932,
                    "Type":"noseRight"
                },
                {
                    "Y":0.49883031845092773,
                    "X":0.3936365246772766,
                    "Type":"mouthUp"
                },
                {
                    "Y":0.5755541324615479,
                    "X":0.3751201033592224,
                    "Type":"mouthDown"
                }
            ],
            "Pose":{
                "Yaw":9.099959373474121,
                "Roll":17.926361083984375,
                "Pitch":10.884692192077637
            },
            "Emotions":[
                {
                    "Confidence":24.25369644165039,
                    "Type":"CALM"
                },
                {
                    "Confidence":10.527027130126953,
                    "Type":"CONFUSED"
                },
                {
                    "Confidence":8.463282585144043,
                    "Type":"HAPPY"
                }
            ],
            "AgeRange":{
                "High":43,
                "Low":26
            },
            "EyesOpen":{
                "Confidence":63.61029052734375,
                "Value": true
            },
            "BoundingBox":{
                "Width":0.39423078298568726,
                "Top":0.12980769574642181,
                "Left":0.19591346383094788,
                "Height":0.5256410241127014
            },
            "Smile":{
                "Confidence":94.11669921875,
                "Value": true
            },
            "MouthOpen":{
                "Confidence":97.92354583740234,
                "Value": false
            },
            "Quality":{
                "Sharpness":99.98487854003906,
                "Brightness":46.21891403198242
            },
            "Mustache":{
                "Confidence":98.9549789428711,
                "Value": false
            },
            "Beard":{
                "Confidence":93.79923248291016,
                "Value":false
            }
        }
    ]
}
```

### Test

```
$ emulambda -v lambda_face_analysis.lambda_handler s3put_event.json

$ emulambda -v lambda_normalize.lambda_handler face_analysis_event.json
```

### Packing

```
$ rm -f face_analysis.zip normalize.zip
$ zip face_analysis.zip lambda_face_analysis.py
$ zip normalize.zip lambda_normalize.py
```

### Create Function

```
$ aws lambda create-function \
    --region us-west-2 \
    --runtime python2.7 \
    --role arn:aws:iam::550931752661:role/visit-someone-role \
    --descript 'Get faces from a image on s3 using rekognition' \
    --timeout 10 \
    --memory-size 128 \
    --handler lambda_face_analysis.lambda_handler \
    --zip-file fileb://face_analysis.zip  \
    --function-name GetFacesByReko

# output
{
    "CodeSha256": "xpaU90w0zB4IIoZdH4JTW0hE6cw3JI5WyeeB8b/m7aE=",
    "FunctionName": "GetFacesByReko",
    "CodeSize": 824,
    "MemorySize": 128,
    "FunctionArn": "arn:aws:lambda:us-west-2:550931752661:function:GetFacesByReko",
    "Version": "$LATEST",
    "Role": "arn:aws:iam::550931752661:role/visit-someone-role",
    "Timeout": 10,
    "LastModified": "2017-03-28T14:01:56.187+0000",
    "Handler": "lambda_face_analysis.lambda_handler",
    "Runtime": "python2.7",
    "Description": "Get faces from a image on s3 using rekognition"
}

$ aws lambda create-function \
    --region us-west-2 \
    --runtime python2.7 \
    --role arn:aws:iam::550931752661:role/visit-someone-role \
    --descript 'Normalize anlysis of faces' \
    --timeout 10 \
    --memory-size 128 \
    --handler lambda_normalize.lambda_handler \
    --zip-file fileb://normalize.zip  \
    --function-name NormalizeFaces

#output
{
    "CodeSha256": "PgfVw7bgph8Ot2VDHExdG85NCGfeEP/YE1wdso84+i0=",
    "FunctionName": "NormalizeFaces",
    "CodeSize": 576,
    "MemorySize": 128,
    "FunctionArn": "arn:aws:lambda:us-west-2:550931752661:function:NormalizeFaces",
    "Version": "$LATEST",
    "Role": "arn:aws:iam::550931752661:role/visit-someone-role",
    "Timeout": 10,
    "LastModified": "2017-03-28T14:04:15.276+0000",
    "Handler": "lambda_normalize.lambda_handler",
    "Runtime": "python2.7",
    "Description": "Normalize anlysis of faces"
}
```


### Update Function

```
$ aws lambda update-function-code \
    --region=us-west-2 \
    --function-name GetFacesByReko \
    --zip-file fileb://face_analysis.zip

# output
{
    "CodeSha256": "uzeCEJjqt9ElC79+y3CX8+nvI2iZhnfKtXQubIiWH0A=",
    "FunctionName": "GetFacesByReko",
    "CodeSize": 543,
    "MemorySize": 128,
    "FunctionArn": "arn:aws:lambda:us-west-2:550931752661:function:GetFacesByReko",
    "Version": "$LATEST",
    "Role": "arn:aws:iam::550931752661:role/visit-someone-role",
    "Timeout": 10,
    "LastModified": "2017-03-23T00:54:28.176+0000",
    "Handler": "lambda_visit_someone.lambda_handler",
    "Runtime": "python2.7",
    "Description": "Get faces from a image on s3 using rekognition"
}

$ aws lambda update-function-code \
    --region=us-west-2 \
    --function-name NormalizeFaces \
    --zip-file fileb://normalize.zip

#output
{
    "CodeSha256": "PgfVw7bgph8Ot2VDHExdG85NCGfeEP/YE1wdso84+i0=",
    "FunctionName": "NormalizeFaces",
    "CodeSize": 576,
    "MemorySize": 128,
    "FunctionArn": "arn:aws:lambda:us-west-2:550931752661:function:NormalizeFaces",
    "Version": "$LATEST",
    "Role": "arn:aws:iam::550931752661:role/visit-someone-role",
    "Timeout": 10,
    "LastModified": "2017-03-28T14:04:15.276+0000",
    "Handler": "lambda_normalize.lambda_handler",
    "Runtime": "python2.7",
    "Description": "Normalize anlysis of faces"
}
```

### Permission

```
$ aws lambda add-permission \
    --region=us-west-2 \
    --function-name GetFacesByReko \
    --statement-id 1 \
    --action "lambda:InvokeFunction" \
    --principal s3.amazonaws.com \
    --source-arn arn:aws:s3:::visit.someone

# output
{
    "Statement": "{\"Sid\":\"1\",\"Resource\":\"arn:aws:lambda:us-west-2:550931752661:function:GetFacesByReko\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"s3.amazonaws.com\"},\"Action\":[\"lambda:InvokeFunction\"],\"Condition\":{\"ArnLike\":{\"AWS:SourceArn\":\"arn:aws:s3:::visit.someone\"}}}"
}

$ aws lambda add-permission \
    --region=us-west-2 \
    --function-name NormalizeFaces \
    --statement-id 1 \
    --action "lambda:InvokeFunction" \
    --principal s3.amazonaws.com \
    --source-arn arn:aws:s3:::visit.someone

#output
{
    "Statement": "{\"Sid\":\"1\",\"Resource\":\"arn:aws:lambda:us-west-2:550931752661:function:NormalizeFaces\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"s3.amazonaws.com\"},\"Action\":[\"lambda:InvokeFunction\"],\"Condition\":{\"ArnLike\":{\"AWS:SourceArn\":\"arn:aws:s3:::visit.someone\"}}}"
}
```

### Triger Event

```
$ aws s3api put-bucket-notification-configuration \
--bucket visit.someone \
--notification-configuration '{
    "LambdaFunctionConfigurations": [{
        "Id": "visit-someone-lambda",
        "Events": [ "s3:ObjectCreated:*" ],
        "LambdaFunctionArn": "arn:aws:lambda:us-west-2:550931752661:function:GetFacesByReko"
    }]
}'
```
