aws s3api create-bucket \
    --bucket kda-app-code-boyerje \
    --region eu-west-2 \
    --create-bucket-configuration LocationConstraint=eu-west-2

sleep 20
aws s3api put-object --bucket  kda-app-code-boyerje --key data/
aws s3 cp /Users/boyerje/Code/Studies/amazon-kinesis-data-analytics-java-examples/S3Sink/target/aws-kinesis-analytics-java-apps-1.0.jar s3://kda-app-code-boyerje/code/aws-kinesis-analytics-java-apps-1.0.jar