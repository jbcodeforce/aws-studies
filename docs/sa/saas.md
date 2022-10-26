# Software as a Service

A licensing and delivery model whereby software is centrally managed and hosted by a provider and available to customers on a subsciption or pay-per-user basis.

Everything done in SaaS is about multi-tenancy, data isolation and sharing resources like compute, storage. Features are deployed to all tenants. There are multiple patterns for multitenancy, some linked to business requirements and sometime technical reasons: 

* **Silo**: one tenant to get unique set of infrastructure resources. As environments are partitioned, there is no cross-tenant impacts. Agility is compromised.
* **Bridge**: a mix of silo and pool. 
* **Pool**: shared resources, centralized management, simplified deployment. Compliance is a challenge and cross-tenants impacts as all or nothing is available.

## Agility

Agility is the major requirements to go to SaaS, which means

* on-boarding without friction: including environment provisioning
* Frequent feature release: get to customer hand as quick as possible. Release on daily release can be possible.
* Rapid market response, to pivot to a new direction
* Instant customer feedback: with metrics on feature adoption.

The important metrics to consider:

* Usage, consumption, system/tenant health
* Survey and customer satisfaction
* Engagement data

## Landscape

![](./diagrams/saas-landscape.drawio.svg)

* **Frictionless On-Boarding**: complex solution to provision all the environment
* **Authentication**: idnetity is a very important element of SaaS
* **App services**: build microservices with multitenancy.
* **Storage partitioning**: data partitioning, how to isolate data for tenant.
* Tenant isolation: need to have strong boundaries, not just authentication. Need to classify your tenants and build APIs to support those classifications
* The administration services are supporting the SaaS business. 

The conceptual architecture includes the following components with custom microservices:

![](./diagrams/saas-conceptual.drawio.svg){ width=600 }

_Amazon cognito is used as an OpenID identity provider_.

Which maps to the following provisionned environment with classical HA deployment within a region / VPC, two AZs, private and public subnets and gateway & application load balancer. 

![](./diagrams/saas-env.drawio.svg){ width=600 }

Microservices runs in ECS as containers. 

IAM roles and policies are used to support isolation. 

For Silo Isolation model can includes VPC based per tenant or account driven. Bridge or Pool runs in the SaaS VPC, and Web and App tiers are shared and persist in same DB (may be different schema or tenantid in tables). IAM policies can help isolate some resources in AWS services like S3 bucket. 

## Operations

For SaaS we need to focusing on monitoring the environments and applications health, and sometime at the tenant level. 
May be considering the following dashboard elements:

* Most active tenants
* Tenant resources consumption
* Microservices usage

## Deeper dive

The content on this note comes from:

* [Saas at AWS](https://aws.amazon.com/solutions/saas/#)
* [Tod Golding form AWS SaaS factory: Deconstructing SaaS: A Deep Dive into Building Multi-tenant Solu](https://www.youtube.com/watch?v=kmVUbngCyOw) has the diagrams above plus a deep discussion on how to secure and support tenants to access pooled resources like content in DynamoDB. (Need further study)
* [Serverless SaaS documentation](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/serverless-saas.html)
* [DevCon 2022: Building a customizable, multi-tenant serverless orchestration framework for bulk-data ingestion](https://broadcast.amazon.com/videos/611469?ref=home&src=featured-playlist)