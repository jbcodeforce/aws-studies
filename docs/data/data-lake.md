# Data Lake with AWS

Here is a mapping with AWS services to support your data strategy:

![](./diagrams/datalake-aws.drawio.png)

* [Amazon Redshift](./redshift.md)
* [S3](../../infra/storage/#s3-simple-storage-service)

## Big Data

The 3 V's of big data are 

* Volume: we are at the terabytes and petabytes level. 
* Variety: includes data from a wide range of sources and formats
* Velocity: data needs to be collected, stored, processed and analyzed withn a short period of time.

## [EMR]()

Created in 2009, it is a managed service to run Spark, Haddop, Hive, Presto, HBase... Per-second prcing and save 50%-80% with Amazon EC2 Spot and reserved instances.


## [OpenSearch]()

Fully managed service

## [Glue](https://aws.amazon.com/glue/)

Serverless data integration and data pipeline to do ETL jobs. You can discover and connect to over 70 diverse data sources, manage your data in a centralized data catalog, and visually create, run, and monitor ETL pipelines to load data into your data lakes. Pay only for resources used while running.

* [Product documentation](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
* [AWS Glue samples repository](https://github.com/aws-samples/aws-glue-samples)

## Lake Formation

AWS Lake Formation is a service that makes it easy to set up a secure data lake in days. A data lake is a centralized, curated, and secured repository that stores all your data, both in its original form and prepared for analysis. 

Amazon S3 forms the storage layer for Lake Formation. 

AWS Lake Formation is integrated with AWS Glue which you can use to create a data catalog that describes available datasets and their appropriate business applications. Lake Formation lets you define policies and control data access with simple “grant and revoke permissions to data” sets at granular levels

### Deeper Dive

* [How it works](https://docs.aws.amazon.com/lake-formation/latest/dg/how-it-works.html)
* [Building secured data lakes on AWS](https://aws.amazon.com/blogs/big-data/building-securing-and-managing-data-lakes-with-aws-lake-formation/)