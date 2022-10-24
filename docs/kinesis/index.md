# Kinesis services

Designed to process real-time data. 

 ![kin](./images/kinesis.png)

Three main different components are: 

* **Kinesis Streams**: low latency streaming ingest at scale. They offer patterns for data stream processing. It looks similar to Kafka, but MKS is the Kafka deployment.
* **Kinesis Analytics**: perform real-time analytics on streams using SQL. This Apache Flink as managed service.
* **Kinesis Firehose**: load streams into S3, Redshift, ElasticSearch. No administration, auto scaling, serverless.

## Data Streams

Distributed data stream into Shards for parallel processing. Producer sends message with `Partition Key` and a throughput of 1 Mb/s or 1000 msg /s per Shard. A sequence number is added to the message to note where the message was in the Shard. 

* Retention from 1 to 365 days
* Replay the messages
* Immutable records, not deleted by applications.
* Message in a shard, can share partition key, and keep ordering.
* Producer can use SDK, or Kinesis Producer Library (KPL) or being a Kinesis agent.
* Consumer may use SDK and Kinesis Client Library (KCL), or being one of the managed services like: Lambda, Kinesis Data Firehose, Kinesis Data Analytics
* For consuming side, each Shard gets 2MB/s out
* Pricing is per Shard provisioned per hour
* The capacity limits of a Kinesis data stream are defined by the number of shards within the data stream. The limits can be exceeded by either data throughput or the number of reading data calls. Each shard allows for 1 MB/s incoming data and 2 MB/s outgoing data. You should increase the number of shards within your data stream to provide enough capacity.

There is an On-demand mode, pay as you go, with a default capacity of 4MB/s or 4000mg/s. Pricing per stream, per hour and data in/out per GB. 

captured Metrics are: # of incoming/outgoing bytes, # incoming/outgoing records, Write / read provisioned throughput exceeded, and iterator age ms.

### Producer

#### AWS CLI

Produce:

```sh
aws kinesis put-record --stream-name test --partition-key user1 --data "user signup" --cli-binary-format raw-in-base64-out
```

### Consumer

#### AWS CLI

Consume:

```sh
# Describe the stream
aws kinesis describe-stream --stream-name test
# Get some data
aws kinesis get-shard-iterator --stream-name test --shard-id shardId--00000000 --shard-iterator-type TRIM_HORIZON
# The returned message gave the next message iterator that should be used in the next call.
aws kinesis get-records --shard-iterator <the-iterator-id>
```
## Kinesis Data Firehose

Firehose is a fully managed service for delivering real-time streaming data to various supported destinations.

![](./diagrams/firehose.drawio.svg)

It can delegates the record transformation processing to a custom Lambda function, but it supports different format already. It outputs batch files to the target destinations. Batch is based on 60s (or more) window or 1 MB of data. Therefore it is a near real-time service. Failed records can go to a S3 bucket.

As a managed services it also support auto scaling.

IAM role need to be referenced to write to S3.

## Stream analytics

