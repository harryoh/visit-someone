# 라즈베리파이
### python 설치
### opencv 설치
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

# Lambda

### AWS Credential

### Install emulambda

```
$ pip install emulambda
```

### lambda_visit_someone.py

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

### Run

```
$ emulambda -v lambda_visit_someone.lambda_handler s3put_event.json
```

