# Analytics Services

## AWS Athena

[AWS Athena](https://aws.amazon.com/athena) runs analytics directly on S3 files, using SQL language to query the files (CSV, JSON, Avro, Parquet...). `S3 Access Logs` log all the requests made to buckets, and Athena can then be used to run serverless analytics on top of the logs files. 

* No need to load the data to Athena, the query is executed on top of S3.
* Queries are done on high availability capability so will succeed, and scale based on the data size.
* No need for complex ETL jobs to prepare your data for analytics.
* Athena integrates with Amazon QuickSight for easy data visualization.
* Integrated with AWS **Glue Data Catalog**, allowing you to create a unified metadata repository across various services, crawl data sources to discover schemas and populate your Catalog with new and modified table and partition definitions, and maintain schema versioning.
* Pricing pet TB of data scanned.
* It also includes `Federated Query` to run SQL queries across data stored in relational and non-relational , object, and custom data sources. It uses the Data Source Connectors which executes a Lambda to run the Federated Query.

* Prefer using [Apache Parquet](https://parquet.apache.org/) data format for better performance and optimized cost. It is a columnar file format that provides optimizations to speed up queries and is a far more efficient file format than CSV or JSON
* Partition your data in S3 folder.

???- "CSV to Parquet"
    For Python, Pandas support it by reading the csv file into dataframe using read_csv and writing that dataframe to parquet file using `to_parquet`. [Apache Drill](https://drill.apache.org/) has also such tool. In Spark the data frame has write.parquet API. Finaly AWS Glue can also do such transformation.

### Simple demo script

* Create a S3 bucket
* Upload a csv file
* Create a database in Athena
* Define SQL query and run them in the Editor.

### Deeper dive

* [Product documentation](https://docs.aws.amazon.com/athena/latest/ug/what-is.html)
* [Getting started](https://docs.aws.amazon.com/athena/latest/ug/getting-started.html)
* [How do I analyze my Amazon S3 server access logs using Athena?](https://aws.amazon.com/premiumsupport/knowledge-center/analyze-logs-athena/)

## [Elastic MapReduce - EMR](https://aws.amazon.com/emr)

It helps creating an Hadoop cluster (HPFS) to process big data. The cluster can have hundred of EC2 instances. 

It comes bundled with Spark, HBase, Presto, Flink. For auto scaling of the task nodes, it uses Spot instances. Master node should be reserved instance.

## [QuickSight](https://aws.amazon.com/quicksight)

Dashboard tool, serverless, machine learning powered BI service.

Integrated with RDS, Aurora, Athena, S3, RedShift, OpenSearch, Timestream, with Saleforce, Jira... It can integrate to any JDBC compliant database. It can import CSV, XLSX, JSON, TSV files and log files.

If data is imported inside QuickSight, it uses in memory computation using SPICE engine.

With enterprise edition we can define groups of users.

## [Glue](https://aws.amazon.com/glue)

* It is a serverless, managed service to do ETL to do data pipeline. You can discover and connect to over 70 diverse data sources, manage your data in a centralized data catalog, and visually create, run, and monitor ETL pipelines to load data into your data lakes.
* It can also do a data catalog, by starting some crawler to different data sources.
* To avoid reprocessing data, it use Job Bookmarks.
* Glue Elastic View is a feature to combine and replicate data across multiple data stores using SQL. It is like virtual table.
* Glue DataBrew to clean and normalize data using pre-built transformation.
* Glue Studio, GUI to create, run and monitor ETL jobs
* Glue Streaming ETL built on Apache Spark Structured Streaming to do data streaming compatible with Kafka, MSK and Kinesis data streaming.

## [Lake Formation](https://aws.amazon.com/lake-formation)

An abstraction layer on top of Glue to build data lake in days instead of month. The lake is on S3. It adds access control at the column level.

## Example of a big data ingestion pipeline

The requirements are:

* Use serverless ingestion pipeline.
* Collect and transform data in real-time.
* Support SQL query on transformed data.
* Persist SQL results into S3.
* Keep into warehouse and create dashboard.
* Data could come from IoT devices

A potential architecture will be:

![](./diagrams/data-pipeline.drawio.png)