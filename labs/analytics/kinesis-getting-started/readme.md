# Writing to an Amazon S3 Bucket from Kinesis data analytics

[See instructions in this getting started](https://docs.aws.amazon.com/kinesisanalytics/latest/java/examples-s3.html)

* Create Data Streams app and S3 bucket + upload jar

```sh
# Create Data Streams
./createDataStream.sh
# Send records
python3 stock.py
# Add S3 bucket ... it uploads S3 streaming jar to code folder
./createS3bucket.sh
```

* Create Kinesis Analytics app

```
 aws kinesisanalyticsv2 create-application --cli-input-json file://create_request.json
```

* modify the policy attached to the kinesis role.