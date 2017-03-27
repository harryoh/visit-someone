# 라즈베리파이
### python 설치
### opencv 설치

```
sudo apt-get update
sudo apt-get -y upgrade
sudo rpi-update

sudo apt-get install build-essential git cmake pkg-config libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libgtk2.0-dev libatlas-base-dev gfortran
```

```
$ mkdir ~/work
$ cd ~/work
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

### lambda_visit_someone.py

```
from __future__ import print_function
import urllib
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    region = event['Records'][0]['awsRegion']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    client = boto3.client('rekognition', region)

    response = client.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        }
    )

    if not len(response['FaceDetails']):
        return False

    return response
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

### Test

```
$ emulambda -v lambda_visit_someone.lambda_handler s3put_event.json
```

### Packing

```
$ zip packages.zip lambda_visit_someone.py
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
    --handler lambda_visit_someone.lambda_handler \
    --zip-file fileb://packages.zip  \
    --function-name GetFacesByReko

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
    "LastModified": "2017-03-23T00:53:53.007+0000",
    "Handler": "lambda_visit_someone.lambda_handler",
    "Runtime": "python2.7",
    "Description": "Get faces from a image on s3 using rekognition"
}
```


### Update Function

```
$ aws lambda update-function-code \
    --region=us-west-2 \
    --function-name GetFacesByReko \
    --zip-file fileb://packages.zip

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
