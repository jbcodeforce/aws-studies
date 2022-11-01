# Amazon RedShift

[Redshift](https://aws.amazon.com/redshift/) is the cloud data warehouse managed services, with no data movement or data transformation. 

Amazon Redshift uses SQL to analyze structured and semi-structured data across data warehouses, operational databases, and data lakes, using AWS-designed hardware and machine learning to deliver the best price performance at any scale.

It is based on Postgresql but is not used for OLTP. It is used for analytical processing and data warehousing, scale to Peta Bytes. It is Columnar storage of data. It uses massively parallel query execution.

Data can be loaded from S3, DynamoDB, DMS and other DBs. It can scale from 1 to 128 nodes, and each node has 160GB per node.

The architecture is based on a leader node to support query planning and aggregate results, and compute nodes to perform the queries and send results back.

Redshift spectrum performs queries directly on top of S3.
