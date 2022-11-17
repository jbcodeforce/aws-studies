# [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)

AWS proprietary NoSQL database, Serverless, provisioned capacity, auto scaling, on demand capacity. Fully managed,  Highly Available with replication across multiple AZs in one AWS Region by default, Read and Writes are decoupled, and DAX can be used for read cache. 

Single digit ms latency, even with increased number of requests. Can support millions of requests per second, trillions of row, 100s of TB storage. Data is stored on solid-state disks (SSDs) and may be encrypted at rest.

The maximum size for an item in a table is 400k.

It is integrated with IAM for authentication and authorization.

A table is a collection of items, and each item is a collection of attributes. DynamoDB uses primary keys to uniquely identify each item in a table and secondary indexes to provide more querying flexibility.
Useful when the solution does not want to design a data schema upfront and which may change overtime. 

The read operations can be eventually consistent or strongly consistent.

DynamoDB Streams to integrate with AWS Lambda.

There is two capacities modes: 

* **provisioned**: where you specify and pay for read capacity units and write capacity units. Need to plan beforehand. Less expensive
* **on-demand**: read and writes automatically scale up/down with your workloads. Better for unpredictable workloads. More expensive.

## Coding

With the aws CLI:

```sh
aws dynamodb create-table --table-name Orders \
                          --attribute-definitions AttributeName=orderID,AttributeType=S \
                          --key-schema AttributeName=orderID,KeyType=HASH \
                          --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

```

### CDK 
Before you can use the AWS SDKs with DynamoDB, you must get an AWS access key ID and secret access key.

Create a dynamodb instance with CDK:

```python
class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # create dynamo table
        order_table = aws_dynamodb.Table(
            self, "orders",
            partition_key=aws_dynamodb.Attribute(
                name="orderID",
                type=aws_dynamodb.AttributeType.STRING,
            ),
            table_class= aws_dynamodb.TableClass.STANDARD_INFREQUENT_ACCESS,
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            # make it global
            #replicationRegions= ['us-west-1', 'us-east-1', 'us-west-2'],
        )
```

Or using the SDK like `boto3`

```python
import boto3

```

### Other coding pattern

* [Using quarkus, docker image for dynamodb, ](https://quarkus.pro/guides/dynamodb.html): Add dynamodb extension, and do data transformation between item and the business entity managed by the resource.

## DynamoDB Accelerator - DAX

To address read congestion of the read operation, DAX is a managed service of a distributed cache cluster in front of DynamoDB. It brings microsecond latency. The API is the same as DynamoDB. 

It caches the most frequently used data, thus offloading the heavy reads on hot keys off your DynamoDB table, hence preventing the "ProvisionedThroughputExceededException" exception.

## DynamoDB Stream processing

It is possible to get ordered stream of item-level modification such as Create, Update, Delete in a DynamoDB table. It is relevant for:

* React on changes in real-time.
* Real-time usage analytics
* Insert into derivative tables
* Implement cross-region replication
* Invoke Lambda on changes 

![](./diagrams/dynamodb-stream.drawio.png)

## DynamoDB global table

The goal is to make a table accessible with low latency in different regions. It uses two-way replication, active-active so application can read and write to the table in any region. We need to enable streaming to get the replication activated.

## DynamoDB Time to live

This feature helps to remove records after a specified timestamp. It is used to clean old records, like older than 2 years, or for session data, to be removed after 2 hours.

## Backup

DynamoDB supports continuous backup using point-in-time recovery (PITR). It can go up to the last 35 days. Recovery creates new table.