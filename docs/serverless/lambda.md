# [Lambda]()

## Introduction

With AWS Lambda, we can run code without provisioning or managing servers or containers.

Upload the source code, and Lambda takes care of everything required to run and scale the code with high availability.

* [Getting started tutorial with free tier](https://aws.amazon.com/getting-started/hands-on/run-serverless-code/)

A  Lambda function has three primary components – trigger, code, and configuration.

![](./images/lambda-fct-0.png)

* Triggers describe when a Lambda function should run. A trigger integrates the Lambda function with other AWS services, enabling us to run our Lambda function in response to certain API calls that occur in our AWS account.
* Configuration includes compute resources, execution timeout, IAM roles (lambda_basic_execution)...
* Code: Java, Node.js, C#, Go, or Python
* Pay only for what we use: # of requests and CPU time.
* Lambda functions always operate from an AWS-owned VPC. By default, the function has the full ability to make network requests to any public internet address — this includes access to any of the public AWS APIs. Only enable our functions to run inside the context of a private subnet in our VPC, when we need to interact with a private resource located in a private subnet.
* AWS Lambda automatically monitors Lambda functions and reports metrics through Amazon CloudWatch. To help us monitoring the code as it executes, Lambda automatically tracks the number of requests, the latency per request, and the number of requests resulting in an error and publishes the associated metrics.  We can leverage these metrics to set custom alarms.
* To reuse code in more than one function, consider creating a Layer and deploying it there. A layer is a ZIP archive that contains libraries, a custom runtime, or other dependencies.
* Lambda support versioning and we can maintain one or more versions of our lambda function. 
* Each lambda function has a unique ARN. 
* Lambda also supports Alias for each of the functions. Lambda alias is a pointer to a specific lambda function version. Alias enables you to promote new lambda function versions to production and if you need to rollback a function, you can simply update the alias to point to the desired version. Event source needs to use Alias ARN for invoking the lambda function.

## Criteria to use lambda.

* Per region deployment.
* Must run under 15 min.
* Memory from 128MB to 10GB.
* 100 concurrent calls.
* Code in compressed zip should be under 50MB and 250MB uncompressed.
* Disk capacity for /tmp is limited to 10GB.

## Security control

AWS Lambda supports resource-based permissions policies for Lambda functions and layers, for example to allow granting usage permission to other AWS accounts on per-resource basis.

Resource-based policies let you grant usage permission to other AWS accounts on a per-resource basis.

## Hands-on

* Can start from a blueprint

    ![](./images/lambda-fct-1.png)

* To get the function to upload logs to cloudWatch, select an existing role, or create a new one
    
    ![](./images/lambda-fct-2.png)

    Here the example of role created

    ![](./images/iam-role-for-lambda.png)

* Add the code as an implementation of an handler function:

    ![](./images/lambda-fct-3.png)

* Create a test event (a request) and run the test and get the resources and logs output.

    ![](./images/lambda-fct-4.png)

* Verify configuration and monitoring.

### Python function with dependencies

It is common to have a function that needs libraries not in the standard python 3.x environment. So the approach is to use a zip file as source of the function with all the dependencies inside it. The process to build such zip can be summarized as:

* `lambda` is the folder with code and future dependencies. It has a `requirements.txt` file to define dependencies.
* do a `pip install --target ./package -r requirements.txt`
* zip the content of the package directory in a zip in the lambda folder

    ```sh
    cd package
    zip -r ../lambda-layer.zip .
    ```

* The zip can be used as a layer, so reusable between different lambda function. For that upload the zip to a s3 bucket and create a layer in the Lambda console, referencing the zip in s3 bucket.
* A layer can be added to any lambda function, then the libraries included in the layer can be imported in the code. Example is the XRay tracing capability in Python.
* We can also add the lambda-function code in the zip and modify the existing function, something like:

    ```sh
    zip lambda-layer.zip lambda-handler.py
    aws lambda update-function-code --function-name  ApigwLambdaCdkStack-SageMakerMapperLambda2EFF1AC9-bERmXFWzvWSC --zip-file fileb://lambda-layer.zip
    ```

### Other personal implementations

* [S3 to Lambda to S3 for data transformation](https://github.com/jbcodeforce/aws-studies/tree/main/labs/s3-lambda)
* [Big data SaaS: lambda to call SageMaker](https://github.com/jbcodeforce/big-data-tenant-analytics/tree/main/setup/saas-solution-cdk/lambda)

## Edge Function

When we need to customize the CDN content, we can use Edge Function to run close to the end users. 

CloudFront provides two types: CloudFront functions or Lambda@Edge.

Can be used for:

* Website security and privacy.
* Dynamic web application at the Edge.
* Search engine optimization (SEO).
* Intelligently route across origins and data centers.
* Bot mitigation at the Edge.
* Real-time image transformation.
* User authentication and authorization.

## Layers

Layer helps to define reusable elements to run a function.

## More reading

* [Using an Amazon S3 trigger to invoke a Lambda function](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html).
* [Tutorial: Resize Images on the Fly with Amazon S3, AWS Lambda, and Amazon API Gateway](https://aws.amazon.com/blogs/compute/resize-images-on-the-fly-with-amazon-s3-aws-lambda-and-amazon-api-gateway/).
* [Best Practices for Developing on AWS Lambda](https://aws.amazon.com/blogs/architecture/best-practices-for-developing-on-aws-lambda/).