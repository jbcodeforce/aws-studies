# Integration and middleware: SQS, SNS

## SQS: Standard queue

* Oldest queueing service on AWS. Full managed service. 
* Unlimited throughput and unlimited number of message in queue
* The default retention is 4 days up to 14 days. low latency < 10ms. 
* Max mesage size is 256KB. 
* Duplicate messages is possible (at least once delivery) and out of order too (best effort). 
* Consumer deletes the message. It is auto scaling.

Specific SDK to integrate to `SendMessage`, GetMessage...

Consumers receive, process and then delete the messages. Parallelism is possible. The consumers can be in an auto scaling group (ASG) and with CloudWatch, it is possible to monitor the queue size / # of instances and in the CloudWatch alarm action, trigger EC2 scaling. 

![](./images/SQS-ASG.png)

Message has metadata out of the box. After a message is polled by a consumer, it becomes invisible to other consumers. 

 ![Metadata](./images/sqs-msg.png)

### Visibility timeout

By default, the “message visibility timeout” is 30 seconds, which means the message has 30 seconds to be processed (Amazon SQS prevents other consumers from receiving and processing the message). If a consumer fails to process a message within the Visibility Timeout, the message goes back to the queue.

![](./images/visibility-to.png)

After the message visibility timeout is over, the message is “visible” in SQS, so it may be processed twice. But a consumer could call the `ChangeMessageVisibility` API to get more time. When the visibility timeout is high (hours), and the consumer crashes then the re-processing of all the messages will take time. If it is set too low (seconds), we may get duplicates

To reduce the number of API call to request message (improve latency and app performance), consumer can use the `long polling` API and wait for message arrival. 

### Dead Letter Queue

We can set a threshold for how many times a message can go back to the queue. 

After the `MaximumReceives` threshold is exceeded, the message goes into a dead letter queue (DLQ) (which has a limit of 14 days to process).

 ![DLQ](./images/sqs-dlq.png)

Delay queues let you postpone the delivery of new messages to a queue for a number of seconds. If you create a delay queue, any messages that you send to the queue remain invisible to consumers for the duration of the delay period. The default (minimum) delay for a queue is 0 seconds. The maximum is 15 minutes.

For security, there is encryption in fight via HTTPS, and at rest with KMS keys. SQL API access control via IAM policies, and SQS Access Policies for cross-account access and for other AWS services to access SQS. 

It comes with monitoring.

### FIFO Queue

Queue can be set as FIFO to guaranty the order: limited to throughput at 300 msg/s without batching or 3000 msg/s with batching. It can also support exactly once delivery. While configuring the FIFO queue a paramter can be set to remove duplicate by looking at the content.
*The name of the queue has to end with `.fifo`*.

### Sample Code

* [Python boto3 SQS](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html)
* [See Python aws folder](https://github.com/jbcodeforce/python-code)

## SNS - Simple Notification Service

Used for pub/sub communication. Producer sends message to one SNS Topic. SNS supports up to 12,500,000 subscriptions per topic, 100,000 topics limit. 

Each subscriber to the topic will get all the messages.

The producers can publish to topic via SDK and can use different protocols like: HTTP / HTTPS (with delivery retries – how many times), SMTP,  SMS, ... 

The subscribers can be a SQS, a Lambda, Kinesis Firehose, Emails...

Many AWS services can send data directly to SNS for notifications: CloudWatch (for alarms), AWS budget, Lambda, Auto Scaling Groups notifications, Amazon S3 (on bucket events), DynamoDB, CloudFormation, AWS DMS, RDS Event.

SNS can be combined with SQS: Producers push once in SNS, receive in all SQS queues that they subscribed to. It is fully decoupled without any data loss. SQS allows for data persistence, delayed processing and retries. SNS cannot send messages to SQS FIFO queues.

For security it supports HTTPS, and encryption at REST with KSM keys. For access control, IAM policies can be defined for the SNS API (looks like S# policies). Same as SQS, used for cross account access and with other services. 

### Combining with SQS - Fan Out pattern

* An application puch once in a SNS Service, and the SQS queues are subscribers to the topic and then get the messages. Fan Out.
* Fully decoupled with no data loss
* SQS adds data persistence, delayed processing and retries of work
* Increase the number of subscriber over time.
* Using SNS FIFO and SQS FIFO it will keep ordering.
* Can use Message Filtering using a JSON policy 

## Kinesis

See [dedicated note](../kinesis/index.md)