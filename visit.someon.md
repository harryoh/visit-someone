# Create Bucket

```
aws s3 mb --region ap-northeast-2 s3://visit.someone
make_bucket: visit.someone
```

# lifecycle

```
$ aws s3api put-bucket-lifecycle --bucket funnyfaces \
--lifecycle-configuration '{
    "Rules": [{
        "Status": "Enabled",
        "Prefix": "",
        "Expiration": {
            "Days": 1
        }
    }]
}'
```
