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
$ pip install numpy
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
        "Principal": {
            "Service": [
                "lambda.amazonaws.com",
                "states.us-west-2.amazonaws.com",
                "events.amazonaws.com"
            ]
        },
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
                        "Service": [
                            "lambda.amazonaws.com",
                            "states.us-west-2.amazonaws.com",
                            "events.amazonaws.com"
                        ]
                    }
                }
            ]
        },
        "RoleId": "AROAICMHVR5XIORT3EM66",
        "CreateDate": "2017-03-30T13:52:09.397Z",
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
$ aws iam put-role-policy \
--role-name visit-someone-role \
--policy-name VisitSomeoneLambdaFullAccess \
--policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:*"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}'
```

### Add Step Function Permission

```
$ aws iam put-role-policy \
--role-name visit-someone-role \
--policy-name VisitSomeoneStepFunctionFullAccess \
--policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
             "Action": [ "states:StartExecution" ],
            "Resource": [ "arn:aws:states:*:*:stateMachine:*" ]
        }
     ]
}'
```

### Add Rekognition Permission

```
$ aws iam attach-role-policy \
--policy-arn arn:aws:iam::aws:policy/AmazonRekognitionFullAccess \
--role-name visit-someone-role
```

# Elastic Search

### Create Domain

```
$ aws es create-elasticsearch-domain \
    --domain-name visit-someone \
    --elasticsearch-version 5.1 \
    --elasticsearch-cluster-config InstanceType=t2.small.elasticsearch,InstanceCount=1 \
    --ebs-options EBSEnabled=true,VolumeType=gp2,VolumeSize=10

# output
{
    "DomainStatus": {
        "ElasticsearchClusterConfig": {
            "DedicatedMasterEnabled": false,
            "InstanceCount": 1,
            "ZoneAwarenessEnabled": false,
            "InstanceType": "t2.small.elasticsearch"
        },
        "DomainId": "550931752661/visit-someone",
        "Created": true,
        "Deleted": false,
        "EBSOptions": {
            "VolumeSize": 10,
            "VolumeType": "gp2",
            "EBSEnabled": true
        },
        "Processing": true,
        "DomainName": "visit-someone",
        "SnapshotOptions": {
            "AutomatedSnapshotStartHour": 0
        },
        "ElasticsearchVersion": "5.1",
        "AccessPolicies": "",
        "AdvancedOptions": {
            "rest.action.multi.allow_explicit_index": "true"
        },
        "ARN": "arn:aws:es:us-west-2:550931752661:domain/visit-someone"
    }
}


$ aws es update-elasticsearch-domain-config \
    --domain-name visit-someone \
    --access-policies '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "AWS": ["*"]
            },
            "Action": ["es:*"],
            "Resource": "arn:aws:es:us-west-2:550931752661:domain/visit-someone/*"
        }]
    }'

# output
{
    "DomainConfig": {
        "ElasticsearchClusterConfig": {
            "Status": {
                "PendingDeletion": false,
                "State": "Active",
                "CreationDate": 1491650436.646,
                "UpdateVersion": 6,
                "UpdateDate": 1491650928.492
            },
            "Options": {
                "DedicatedMasterEnabled": false,
                "InstanceCount": 1,
                "ZoneAwarenessEnabled": false,
                "InstanceType": "t2.small.elasticsearch"
            }
        },
        "ElasticsearchVersion": {
            "Status": {
                "PendingDeletion": false,
                "State": "Active",
                "CreationDate": 1491650436.646,
                "UpdateVersion": 6,
                "UpdateDate": 1491650928.492
            },
            "Options": "5.1"
        },
        "EBSOptions": {
            "Status": {
                "PendingDeletion": false,
                "State": "Active",
                "CreationDate": 1491650436.646,
                "UpdateVersion": 6,
                "UpdateDate": 1491650928.492
            },
            "Options": {
                "VolumeSize": 10,
                "VolumeType": "gp2",
                "EBSEnabled": true
            }
        },
        "SnapshotOptions": {
            "Status": {
                "PendingDeletion": false,
                "State": "Active",
                "CreationDate": 1491650436.646,
                "UpdateVersion": 6,
                "UpdateDate": 1491650928.492
            },
            "Options": {
                "AutomatedSnapshotStartHour": 0
            }
        },
        "AdvancedOptions": {
            "Status": {
                "PendingDeletion": false,
                "State": "Active",
                "CreationDate": 1491651611.845,
                "UpdateVersion": 9,
                "UpdateDate": 1491651611.845
            },
            "Options": {
                "rest.action.multi.allow_explicit_index": "true"
            }
        },
        "AccessPolicies": {
            "Status": {
                "PendingDeletion": false,
                "State": "Processing",
                "CreationDate": 1491651611.643,
                "UpdateVersion": 9,
                "UpdateDate": 1491651611.643
            },
            "Options": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"es:*\",\"Resource\":\"arn:aws:es:us-west-2:550931752661:domain/visit-someone/*\"}]}"
        }
    }
}
```

### Get Endpoint

```
$ aws es describe-elasticsearch-domain \
    --domain-name visit-someone \
    --query 'DomainStatus.Endpoint'

# output
"search-visit-someone-it3nww4z465kzd73e6nhixvocy.us-west-2.es.amazonaws.com"
```

### Mapping Elasticsearch

```
$ curl -XPUT "https://search-visit-someone-it3nww4z465kzd73e6nhixvocy.us-west-2.es.amazonaws.com/aws-submit" -d'
{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings" : {
        "faces" : {
            "properties" : {
                "Age": { "type": "integer"},
                "BoundingBox": {
                    "type" : "object",
                    "properties": {
                        "Height": { "type": "float" },
                        "Left": { "type": "float" },
                        "Right": { "type": "float" },
                        "Width": { "type": "float" }
                    }
                },
                "Emotions": {
                    "properties": {
                        "Confidence": { "type": "float" },
                        "Type": { "type": "keyword" }
                    }
                },
                "Eyeglasses": { "type": "boolean" },
                "Gender": { "type": "keyword" },
                "Smile": { "type": "float" },
                "created_at" : {
                       "type" : "date",
                       "format": "yyyy-MM-dd HH:mm:ss.SSS"
                },
                "s3": {
                    "type" : "object",
                    "properties": {
                        "bucket": { "type": "string" },
                        "key": { "type": "string" },
                        "region": { "type": "string" }
                    }
                }
            }
        }
    }
}'
```

# Lambda

### AWS Credential

### Install emulambda

```
$ pip install emulambda
```

### [`lambda_face_analysis.py`](https://raw.githubusercontent.com/harryoh/visit-someone/master/lambda/lambda_visit_someone.py)


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

### `sample_clouewatch_event.json`

```
{
    "version":"0",
    "id":"4afaa0d9-8032-4e76-bdd6-e7d7ef2e6898",
    "detail-type":"AWS API Call via CloudTrail",
    "source":"aws.s3",
    "account":"550931752661",
    "time":"2017-04-03T13:28:41Z",
    "region":"us-west-2",
    "resources":[

    ],
    "detail":{
        "eventVersion":"1.05",
        "userIdentity":{
            "type":"Root",
            "principalId":"550931752661",
            "arn":"arn:aws:iam::550931752661:root",
            "accountId":"550931752661",
            "accessKeyId":"AKIAJU2CPEZ6UCROQYAA"
        },
        "eventTime":"2017-04-03T13:28:41Z",
        "eventSource":"s3.amazonaws.com",
        "eventName":"PutObject",
        "awsRegion":"us-west-2",
        "sourceIPAddress":"218.39.65.100",
        "userAgent":"[Boto3/1.4.4 Python/2.7.12 Darwin/16.5.0 Botocore/1.5.12]",
        "requestParameters":{
            "bucketName":"visit.someone",
            "key":"test.jpg"
        },
        "responseElements":{
            "x-amz-expiration":"expiry-date=\"Wed, 05 Apr 2017 00:00:00 GMT\", rule-id=\"MTg1MjU2YTktYTIzOC00NjkyLTlkMWItYWVjMzYxNzY3NTE0\""
        },
        "additionalEventData":{
            "x-amz-id-2":"03yyq14v92iM11Rs5KQhGjqNEWOfatBPkw/eykoZwtRBFa6H0lbm0q+EacVEAWLIFRcTXsxL31E="
        },
        "requestID":"7409E93EA244D867",
        "eventID":"9b079fa1-7531-457e-9468-a9338d32434f",
        "readOnly":false,
        "resources":[
            {
                "type":"AWS::S3::Object",
                "ARN":"arn:aws:s3:::visit.someone/test.jpg"
            },
            {
                "accountId":"550931752661",
                "type":"AWS::S3::Bucket",
                "ARN":"arn:aws:s3:::visit.someone"
            }
        ],
        "eventType":"AwsApiCall",
        "recipientAccountId":"550931752661"
    }
}
```

### [`lambda_normalize.py`](https://raw.githubusercontent.com/harryoh/visit-someone/master/lambda/lambda_normalize.py)

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

### `sample_face_analysis_event.json`

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

### [`lambda_post_elasticsearch.py`](https://raw.githubusercontent.com/harryoh/visit-someone/master/lambda/lambda_post_elasticsearch.py)

```
from __future__ import print_function

import os
import logging
import requests

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
```

### `sample_normalize.json`

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
            "Eyeglasses":false,
            "Gender":"Male",
            "Age":34,
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
            "BoundingBox":{  
                "Width":0.39423078298568726,
                "Top":0.12980769574642181,
                "Height":0.5256410241127014,
                "Left":0.19591346383094788
            },
            "Smile":94.11669921875
        }
    ]
}
```

### Test

```
$ emulambda -v lambda_face_analysis.lambda_handler sample_cloudwatch_event.json

$ emulambda -v lambda_normalize.lambda_handler sample_face_analysis_event.json

$ ES_ENDPOINT='search-visit-someone-it3nww4z465kzd73e6nhixvocy.us-west-2.es.amazonaws.com' emulambda -v lambda_post_elasticsearch.lambda_handler sample_normalize.json
```

### Packing

```
$ rm -f face_analysis.zip normalize.zip post_elasticsearch.zip
# Once
$ pip install slacker -t packages
$ pushd packages;zip -r ../post_elasticsearch.zip *;popd

$ zip face_analysis.zip lambda_face_analysis.py
$ zip normalize.zip lambda_normalize.py
$ zip post_elasticsearch.zip lambda_post_elasticsearch.py
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
    "CodeSha256": "aJbGchlenI2IIHQ1V6ZUCPf223jMNLRhpFfEEBgyZS0=",
    "FunctionName": "GetFacesByReko",
    "CodeSize": 636,
    "MemorySize": 128,
    "FunctionArn": "arn:aws:lambda:us-west-2:550931752661:function:GetFacesByReko",
    "Version": "$LATEST",
    "Role": "arn:aws:iam::550931752661:role/visit-someone-role",
    "Timeout": 10,
    "LastModified": "2017-03-30T12:19:28.523+0000",
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
    "CodeSha256": "MOfxtbSd6vE3lZjWKA7Si6Kh/R3GTDiCdwyNQUcGces=",
    "FunctionName": "NormalizeFaces",
    "CodeSize": 576,
    "MemorySize": 128,
    "FunctionArn": "arn:aws:lambda:us-west-2:550931752661:function:NormalizeFaces",
    "Version": "$LATEST",
    "Role": "arn:aws:iam::550931752661:role/visit-someone-role",
    "Timeout": 10,
    "LastModified": "2017-03-30T13:26:32.490+0000",
    "Handler": "lambda_normalize.lambda_handler",
    "Runtime": "python2.7",
    "Description": "Normalize anlysis of faces"
}

$ aws lambda create-function \
    --region us-west-2 \
    --runtime python2.7 \
    --role arn:aws:iam::550931752661:role/visit-someone-role \
    --descript 'Insert faces to elasticsearch' \
    --timeout 10 \
    --memory-size 128 \
    --handler lambda_post_elasticsearch.lambda_handler \
    --zip-file fileb://post_elasticsearch.zip  \
    --function-name PostElasticSearch \
    --environment Variables='{
        ES_ENDPOINT=search-visit-someone-it3nww4z465kzd73e6nhixvocy.us-west-2.es.amazonaws.com,
        ES_INDEX=aws-submit,
        ES_TYPE=faces,
        SLACK_TOKEN='xxxxxx',
        SLACK_CHANNEL='xxx'
    }'

# output
{
    "CodeSha256": "DbxOVgxH4jJK0bJERCmdA6FVlEBf1xZw+F5vw8Q3hoA=",
    "FunctionName": "PostElasticSearch",
    "CodeSize": 663,
    "MemorySize": 128,
    "FunctionArn": "arn:aws:lambda:us-west-2:550931752661:function:PostElasticSearch",
    "Environment": {
        "Variables": {
            "ES_ENDPOINT": "search-visit-someone-it3nww4z465kzd73e6nhixvocy.us-west-2.es.amazonaws.com"
        }
    },
    "Version": "$LATEST",
    "Role": "arn:aws:iam::550931752661:role/visit-someone-role",
    "Timeout": 10,
    "LastModified": "2017-04-08T12:19:46.519+0000",
    "Handler": "lambda_post_elasticsearch.lambda_handler",
    "Runtime": "python2.7",
    "Description": "Insert faces to elasticsearch"
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

$ aws lambda update-function-code \
    --region=us-west-2 \
    --function-name PostElasticSearch \
    --zip-file fileb://post_elasticsearch.zip

# output
{
    "CodeSha256": "fUa1tB6TsUH1xsEsqcNJifd8zCN+ARCTmIy7dd63t1c=",
    "FunctionName": "PostElasticSearch",
    "CodeSize": 663,
    "MemorySize": 128,
    "FunctionArn": "arn:aws:lambda:us-west-2:550931752661:function:PostElasticSearch",
    "Environment": {
        "Variables": {
            "ES_ENDPOINT": "search-visit-someone-it3nww4z465kzd73e6nhixvocy.us-west-2.es.amazonaws.com"
        }
    },
    "Version": "$LATEST",
    "Role": "arn:aws:iam::550931752661:role/visit-someone-role",
    "Timeout": 10,
    "LastModified": "2017-04-08T12:21:56.358+0000",
    "Handler": "lambda_post_elasticsearch.lambda_handler",
    "Runtime": "python2.7",
    "Description": "Insert faces to elasticsearch"
}
```

### Step Functions

```
$ aws stepfunctions create-state-machine \
    --name visit-someone \
    --role-arn arn:aws:iam::550931752661:role/visit-someone-role \
    --definition '{
    "Comment": "Analysis Faces",
    "StartAt": "FaceAnalysis",
    "States": {
        "FaceAnalysis": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-west-2:550931752661:function:GetFacesByReko",
            "Next": "IsExistFaces"
        },
        "IsExistFaces": {
            "Type": "Choice",
            "Choices": [{
                "Variable": "$.faces",
                "BooleanEquals": false,
                "Next": "NoFaces"
            }],
            "Default": "Normalize"
        },
        "Normalize": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-west-2:550931752661:function:NormalizeFaces",
            "Next": "PostElasticSearch"
        },
        "NoFaces": {
            "Type": "Pass",
            "End": true
        },
        "PostElasticSearch": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-west-2:550931752661:function:PostElasticSearch",
            "End": true
        }
    }
}'

#output
{
    "creationDate": 1490880724.993,
    "stateMachineArn": "arn:aws:states:us-west-2:550931752661:stateMachine:visit-someone"
}
```

```
$ aws stepfunctions start-execution \
    --state-machine-arn arn:aws:states:us-west-2:550931752661:stateMachine:visit-someone \
    --input file://s3put_event.json

#output
{
    "startDate": 1490712189.964,
    "executionArn": "arn:aws:states:us-west-2:550931752661:execution:test:38a70381-0e74-4e49-92b0-7b1945eb0681"
}
```


# S3 Event via cloudwatch

### CloudTrail

```
$ aws cloudtrail create-trail \
    --name visit-someone-trail \
    --s3-bucket-name 'visit.someone.log' \
    --no-is-multi-region-trail \
    --enable-log-file-validation

# output
    {
        "IncludeGlobalServiceEvents": true,
        "Name": "visit-someone-trail",
        "TrailARN": "arn:aws:cloudtrail:us-west-2:550931752661:trail/visit-someone-trail",
        "LogFileValidationEnabled": true,
        "IsMultiRegionTrail": false,
        "S3BucketName": "visit.someone.log"
    }
```

```
$ aws cloudtrail put-event-selectors \
    --trail-name visit-someone-trail \
    --event-selectors '[{
        "ReadWriteType": "WriteOnly",
        "IncludeManagementEvents":true,
        "DataResources": [{
            "Type": "AWS::S3::Object",
            "Values": ["arn:aws:s3:::visit.someone/"] 
        }]
    }]'

# output
{
    "EventSelectors": [
        {
            "IncludeManagementEvents": false,
            "DataResources": [
                {
                    "Values": [
                        "arn:aws:s3:::visit.someone/"
                    ],
                    "Type": "AWS::S3::Object"
                }
            ],
            "ReadWriteType": "WriteOnly"
        }
    ],
    "TrailARN": "arn:aws:cloudtrail:us-west-2:550931752661:trail/visit-someone-trail"
}
```

### CloudWatch


### Event Rule
```
$ aws events put-rule \
    --name visit-someone-event \
    --event-pattern '{
        "source": ["aws.s3"],
        "detail": {
            "eventSource": ["s3.amazonaws.com"],
            "eventName": ["PutObject"],
            "requestParameters": {
                "bucketName": ["visit.someone"]
            }
        }
    }'

# output
{
    "RuleArn": "arn:aws:events:us-west-2:550931752661:rule/visit-someone-event"
}
```

### Event Target
```
$ aws events put-targets --rule visit-someone-event \
    --targets '[{
        "Id": "visit-some-event",
        "RoleArn": "arn:aws:iam::550931752661:role/visit-someone-role",
        "Arn": "arn:aws:states:us-west-2:550931752661:stateMachine:visit-someone"
    }]'
    
# output
{
    "FailedEntries": [],
    "FailedEntryCount": 0
}
```


