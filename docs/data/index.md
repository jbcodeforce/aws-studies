# Data services

## Relational Database Service - RDS

Managed service for SQL based database (MariaDB, MySQL, Postgresql, SQL server, Oracle, Amazon Aurora).  AWS maintains instance AMI, OS patching... 

* Support multi AZs for Reliability Availability with automatic failover to standby, app uses one unique DNS name. Continuous backup and restore to specific point of time restore. 
* It uses gp2 or io1 EBS. 
* Transaction logs are backed-up every 5 minutes. Support user triggered snapshot.
* Supports **Storage Auto Scaling** to increase storage dynamically with automatic detections of running out of free storage and scale it. (Free storage < 10%, low storeage last at least 5 minutes, 6 hours have passed since last notification)
* Installed in private subnet in a VPC. No public IP address. 
* For Oracle and MS SQL it is possible to setup a RDS custom. where you have access to OS and Database.

From a solution architecture point of view:

* **Operations**:  small downtime when failover happens. For maintenance, scaling in read replicas, updating underlying ec2 instance, or restore EBS, there will be manual intervention.
* **Security**: AWS is responsible for OS security, we are responsible for setting up KMS, security groups, IAM policies, authorizing users in DB, enforcing SSL.
* **Reliability**: Multi AZ feature helps to address it, with failover mechanism in case of failures
* **Performance**: depends on EC2 instance type, EBS volume type, ability to add Read Replicas. Doesn’t auto-scale, adapt to workload manually. 

### Multi AZ DB Cluster - Read Replicas

Read replicas helps to scale the read operations. Can create up to 5 read-replicas within a AZ, cross AZ and cross regions. Replication is asynch (eventually consistent). Use cases include, adding reporting, analytics on existing DB, or develop a ML model.
The application which needs to access a read-replica DB needs to change the connection parameters.

AWS charges for network when for example data goes from one AZ to another. Replicas in the same region in RDS managed services are for free, cross regions has a network cost.

### DR - Multi AZ DB instance

RDS supports instance standby with synchronous replication from master to standby. The application talk to one DNS name, and there will be automatic failover, if connection to master RDS fails.

Read-replica DB can be setup as a multi AZ for DR, but RTO is not 0.

It is possible to move from a Single-AZ to a Multi-AZ with zero downtime, by changing the multi-AZ parameter in the RDS.  The internal process is creating a snapshot from master, create a DB via restore operation in target AZ and start synchronous replication from master to standby.

### Security 

* Support at rest Encryption. Master needs to be encrypted to get encrypted replicas. 
* We can create a snapshot from unencrypted DB and then copy it by enabling the encryption for this snapshot. From there we can create an Encrypted DB

Customer's responsibilities:

* Check the ports / IP / security group inbound rules in DB’s SG
* In-database user creation and permissions or manage through IAM
* Creating a database with or without public access
* Ensure parameter groups or DB is configured to only allow SSL connections
* Specify a time window to do maintenance, for version to version migration for example.

## Aurora

Proprietary SQL database storage engine, works using **Postgresql** and **mysql** drivers. It is cloud optimized and claims 5x performance improvement over mySQL on RDS, and 3x for Postgresql. 

The major benefit is the automatic storage scaling: it can grow up by increment of 10GB to 128 TB. Sub 10ms replica lag, up to 15 replicas (MySQL has only 5 replicas). It costs 20% more than RDS.

### HA and Read Scaling

Failover in Aurora is instantaneous. It’s HA (High Availability) native. Use 1 master - 5 readers to create 6 copies of the data over 3 AZs. It supports cross-region replications.

* It needs 4 coies out of 6 to consider write operation as successful.
* And 3 copies out of 6 need for read operations. 
* There is a self-healing capability in case of data corruption with peer-to-peer replication. 
* Storage is done across 100s of volumes. 
* Autoscaling on the read operation from 1 to 15 read-replicas. 

 ![6](./images/aws-aurora.png)

It is CQRS at DB level, and read can be global. Use **writer endpoint** for write operation and **reader endpoint**.

It also supports one write with multiple reader and parallel query, multiple writes and serverless to automate scaling down to zero (No capacity planning needed and pay per second).

With Aurora global database one primary region is used for write and then up to 5 read only regions with replica lag up to 1 s. Promoting another region (for disaster recovery) has an RTO of < 1 minute

* **Operations**:  less operation, auto scaling storage.
* **Security**: AWS responsible for OS security, we are responsible for setting up KMS, security groups, IAM policies, authorizing users in DB, enforcing SSL.
* **Reliability**: Multi AZ, HA
* **Performance**: 5x performance, up to 15 read replicas.

* [Building serverless applications with Amazon Aurora Serverless](https://aws.amazon.com/getting-started/hands-on/building-serverless-applications-with-amazon-aurora-serverless/)

## ElastiCache

Get a managed Redis or Memcached cluster. Applications queries ElastiCache, if not available, get from RDS and store in ElastiCache. Key-Value store.
It can be used for user session store so user interaction can go to different application instances.

**Redis** is a multi AZ with Auto-Failover, supports read replicas to scale and for high availability. It can persist data using AOF persistence, and has backup and restore features.

**Memcached** is a multi-node for partitioning of data (sharding), and no persistence, no backup and restore. It is based on a multi-threaded architecture.

Some patterns for ElastiCache:

* **Lazy Loading**: all the read data is cached, data can become stale in cache
* **Write Through**: Adds or update data in the cache when written to a DB (no stale data)
* **Session Store**: store temporary session data in a cache (using TTL features)

Sub millisecond performance, in memory read replicas for sharding. 

## DynamoDB

AWS proprietary NoSQL database, Serverless, provisioned capacity, auto scaling, on demand capacity. Highly Available, Multi AZ  in an AWS Region by default, Read and Writes are decoupled, and DAX can be used for read cache. 

Single digit ms latency, even with increased number of requests. 

Data is stored on solid-state disks (SSDs).

A table is a collection of items, and each item is a collection of attributes. DynamoDB uses primary keys to uniquely identify each item in a table and secondary indexes to provide more querying flexibility

The read operations can be eventually consistent or strongly consistent.

DynamoDB Streams to integrate with AWS Lambda.

## DocumentDB

## Neptune - GraphDB

## Amazon QLDB
