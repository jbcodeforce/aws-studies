# Monitoring and Audit

## [CloudWatch](https://docs.aws.amazon.com/cloudwatch/)

CloudWatch collects monitoring and operational data in the form of logs, metrics, and events, and visualizes it using automated dashboards so you can get a unified view of your AWS resources, applications, and services that run in AWS and on-premises. The basic features set:

* correlate your metrics and logs to better understand the health and performance of your resources.
* create alarms based on metric value thresholds or anomalous metric behavior based on machine learning algorithms. 

### [CloudWatch Metrics](https://docs.aws.amazon.com/cloudwatch/)

CloudWatch provides metrics for every services in AWS. Metric represents a variable to measure like CPU utilization, Network inbound traffic... 

Metrics are within a VPC so belong to namespaces. They have timestamps and heve up to 10 attributes or dimensions.

![](./images/cloudwatch-1.png)

* To monitor our EC2 instance memory usage, we need to use a Unified CloudWatch Agent to push memory usage as a custom metric to CW.
* Alarm is associated with one metric. So, we need one alarm per metric. You can also combine outcome of two alarms using the CloudWatch Composite Alarm.

### CloudWatch Logs

Concepts:

* Log groups to groups logs, representing an application.

    ![](./images/cw-log-groups.png)

* Log streams: instances within an application / log files or containers.

    ![](./images/cw-log-streams.png)


Priced for retention period, so expiration policies can be defined. 

CloudWatch can send logs to S3, Kinesis Firehose, Kinesis Data Streams, Lambda,... 

Can define filters to reduce logs or trigger CloudWatch alarms, or add insights to query logs and for Dashboards. Here are simple filter:

![](./images/cw-filter.png)

Use Subscription Filter to get near real-time logs to targeted sink:

![](./images/cw-subscription.png)


Logs Insights helps to define query to search within the logs. 

### CloudWatch Agent

By default EC2 instances do not send logs to CloudWatch. We need to run agent on EC2 to push log files we want. We need to use an IAM role that let the EC2 instance be able to send logs to CW.

The new Unified Agent send logs and system-level metrics. 

### CloudWatch Alarms

Alarms are used to trigger notification from any metrics. The states of an alarm are: OK, INSUFFICIENT_DATA, ALARM. A period specifies the lenght of time in seconds to evaluate the metric.

The target of the alarm may be to stop, reboot, terminate, recover of an EC2 instance, trigger an Auto Scaling Action for EC2, or send notification to SNS.

You can use the stop or terminate actions to help you save money when you no longer need an instance to be running. You can create an Amazon CloudWatch alarm that monitors an Amazon EC2 instance and automatically reboots the instance. The reboot alarm action is recommended for Instance Health Check failures.

## CloudWatch Event 

Is now [EventBridge](../serverless/eventbridge.md), a more generic event-driven, serverless managed service.


## CloudWatch Insight

CloudWatch Container Insights collects, aggregates, and summarizes metrics and logs from your containerized applications and microservices. Available for ECS, EKS, K8S on EC2s. 

CloudWatch Lambda Insights simplifies the collection, visualization, and investigation of detailed compute performance metrics, errors, and logs to isolate performance problems and optimize your Lambda environment.

Application Insight is to set up monitoring and gain insights to your application health so you can quickly detect and diagnose problems and reduce the mean time to resolution

Contributor Insights allows you to create realtime Top N time series reports by analyzing CloudWatch Logs based on rules you define. The rule matches log events and reports the top Contributors, where a "Contributor" is a unique combination of the fields defined in the rule. It can be used to identify the heaviest network users, find the URLs that generate the most erroes.

* [EKS workshop with CloudWatch container insight](https://www.eksworkshop.com/intermediate/250_cloudwatch_container_insights/)

## [CloudTrail](https://aws.amazon.com/cloudtrail/)

A managed service to provides governance, audit capabilities for all activities (API calls) and events within an Account. Can be across regions and accounts on a single, centrally controlled platform. We can use CloudTrail to detect unusual activity in our AWS accounts.

![](./images/cloudtrail-home.png)

By default, trails are configured to log management events (operations performed on AWS resources). Data events are not logged.

This is a usage-based paid service.

CloudTrail Insight is used to detect unusual activity in AWS account.

## [Config](https://docs.aws.amazon.com/config/index.html#lang/en_us)

Record and evaluate configurations against compliance rules of your AWS resources. For example can be used to continuously monitor our EC2 instances to assess if they have a specific port exposed.

AWS Config allows you to remediate noncompliant resources that are evaluated by AWS Config Rules. AWS Config applies remediation using AWS Systems Manager Automation documents. This is done at the Action level of a config rule.

## Putting them together

If we define an Elastic Load Balancer then, 

* **CloudWatch** will help us to monitor incoming connections metric, visualize error codes as % over time, and supports dashbaord to get performance monitoring.
* **Config** will help us to track security group rules, configuration changes done on the load balancer, as well as defining compliance rules to ensure SSL certificates are always assigned to LB.
* **CloudTrail** tracks who made any changes to the configuration with API calls.

## Deeper Dive

* [CDK sample: CDK Python Backup & Cloudwatch event](https://github.com/aws-samples/aws-cdk-examples/tree/master/python/ec2-cloudwatch) to illustrate a cloudwatch event rule to stop instances at UTC 15pm everyday
* [CloudWatch Container Insights for EKS cluster workshop](https://www.eksworkshop.com/intermediate/250_cloudwatch_container_insights/)