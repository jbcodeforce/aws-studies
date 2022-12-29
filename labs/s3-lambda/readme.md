# A simple lab to do S3 to lambda processing

For example a client send a txt file to S3 and then S3 invokes a lambda that transform to a json. This is bases on Chandra Lingam's (Udemy) work.

* Create two buckets one for source and one for results
* Create permission policy for R/W on S3 bucket, named: `s3-rw-permission `
* Create IAM role to grant lambda to access cloudwatch and XRay

    * Select New Service -> Lambda
    * Add policies: `AWSXRayDaemonWriteAccess`, `AWSLambdaBasicExecutionRole` and ``

![](./s3-role.png)

* Add Lambda function using blueprint named `s3-get-object-python`.

To get S3 to call Lambda function: