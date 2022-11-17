# Resilience

Resiliency is the ability of a workload to recover from infrastructure or service disruptions, dynamically acquire computing resources to meet demand, and mitigate disruptions, such as misconfigurations or transient network issues.

Apply the sharing responsibility of resiliency. 

## Fault isolation concepts

* Control plane is a complex orchestration with many dependencies so are more difficult to make them resilient. But the lower level of APIs makes it less risky. Still they will fail more often. Latency is not a strong requirement, 100s ms.   
* Do not rely on Auto scaling group for EC2 in case of AZ failure, but plan for overcapacity to support the load after AZ failure.
* Examples of control plan and data plane

    | Service | Control plane | Data plane |
    | --- | --- | --- |
    | Amazon S3 | create bucket, put bucket policy | GetObject, PutObject |
    | DynamoDB | Create table, update table | GetItem ... |
    | ELB | CreateLoadBalancer, CreateTargetGroup | The load balancer itself |
    | Route 53 | CreateHostedZone ... | DNS resolution, health checks |
    | IAM | CreateRole | Authn, Authz |
    | RDS | Create DB instance | The data base |

* Static stability: system still running even dependencies fail without the need to make changes. Use the following approaches: prevent circular dependencies, pre-provision capacity, maintain existing state, eliminate synchronous interaction.
* One way AWS achieve static statbility is by removing control plane deplendencis from the data plane in AWS services. 
* Relying on data plane operaions for recovery can help make your system more staticall stable, this may include pre-provisioning resources, or relying on data plane operations.

## Region, AZ

* Non-AZ affinity: a write operation can cross AZs and with data replications it can make a lot of hops 
* AZ-affinity helps to reduce the number of hops, but it enforces using NLB and not ALB.

## AWS Partitions

There are Isolated infrastructure and services. There are commercial partition, China , and GovCloud partition. Within a partition there are regions.
Not cross IAM definition sharing. 

| Type | Service | Planes |
| --- | --- | --- | 
| Zonal  | RDS, EC2, EBS | Control plane is regional while data plane is zonal |
| Regional | S3, SQS, DynamoDB | Control plane  and data plane are regional |
| Global | CloudFront, Global accelerator, Route 53, IAM |  Control plane is single region  and data plane is global |

There are three categories of global services: partitional, Edge and globally-scoped operations.
Global services havd a single control plane and a distributed, highly available data plane.
Avoid control plane dependencies in global services in your recovery path, implement static stability.

## Cell-based architecture and shuffle sharding

Goal is to reduce the blast-radius. Use the concept of `Cell` which is a construct to isolate compute, routing, and storage (workload). Cells are not AZs but cross AZs. Cell shares nothing with each other. Cell can scale-up and out. Cell have a maximum size.

It is not fitting for all type of workloads. 

API Gateway uses this Cell-based architecture.

Some e-commerce fullfilment delivery centers use cell-based architecture. 

Considerations to address:

* Cell size
* Router robustness
* Partitioning dimension
* Cross-cell use cases
* Cell migration
* Alignment to AZs and Regions

Shards is another construct to isolate blast radius, but now at the level of resources.  Any serverless services is using the concept of shuffle sharding. 

## High Availability

Availability = uptime / (uptime + downtime)

Availability = a1 * a2 *.... * an  . It cannot be better than it's least available dependency.

Spare components improves availability.

### Measuring availability

Metrics to consider:

* Mean time between failure MTBF, try to increase it
* Mean time to detection MTTD
* Mean time to repair MTTR

* consider server-side and client-side request success rate. Define what unit of work to be used: HTTP request, message in queue, async job.
* define downtime, for example, drop below 95% availabiltiy for any API during a 5 minutes window. 

**Use CW embedded metric format EMF to combine logs and metrics**

## Latency

Latency impacts availability. Analyze histograms for latency distribution trends. Use percentiles and trimmed man to measure latency.

## Multi-AZ patterns: AZ gray failure

* System follows differential observability. 
* Different perspective: system versus application

Detection tools:

* cloudwatch contributor insights. 

## Disaster recovery

## Resilience Patterns

* client side, use circuit braker, retries with jitter, multiplexing connection with new protocol like HTTP/3, gRPC
* server side, apply caching strategy, cache-aside is more resilient, inline cache, like DynamoDB DAX, may be a single point of failure. 
