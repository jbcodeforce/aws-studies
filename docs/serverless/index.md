# Serverless

## Container

A container is a standardized unit that packages your code and its dependencies. This package is designed to run reliably on any platform, because the container creates its own independent environment

The difference between containers and virtual machines (VMs) can be illustrated by the following figure:

![](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1664424000/W1-B7tRILgL6sJPSvaUMAw/tincan/d03722b85f9d2b3a05e4c74bd586ea9b1f52f81a/assets/XkRO9PIy-4njgJWl_dCQbrVwmpaNKxmTs.jpg)

In AWS, containers run on EC2 instances. For example, you might have a large instance and run a few containers on that instance. While running one instance is easy to manage, it lacks high availability and scalability. Most companies and organizations run many containers on many EC2 instances across several Availability Zones

## Amazon Elastic Container Service (Amazon ECS)

[Amazon ECS](https://aws.amazon.com/ecs/) is an end-to-end container orchestration service that helps you spin up new containers and manage them across a cluster of EC2 instances.

To run and manage your containers, you need to install the Amazon ECS container agent on your EC2 instances.

![](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1664424000/W1-B7tRILgL6sJPSvaUMAw/tincan/d03722b85f9d2b3a05e4c74bd586ea9b1f52f81a/assets/6ahbH2Kz0xMwwHgD_YiX8p1udFI_1rzlu.jpg)

To prepare your application to run on Amazon ECS, you create a task definition. The task definition is a text file, in JSON format, that describes one or more containers. 

Apply docker compose to Amazon ECS and Fargate

[ecs anywhere](https://press.aboutamazon.com/news-releases/news-release-details/aws-announces-general-availability-amazon-ecs-anywhere)

## EKS

[Amazon EKS](https://aws.amazon.com/eks/) is a fully managed Kubernetes service. 

* An EC2 instance with the ECS agent installed and configured is called a container instance. In Amazon EKS, it is called a worker node.
* An ECS container is called a task. In Amazon EKS, it is called a pod.
* While Amazon ECS runs on AWS native technology, Amazon EKS runs on top of Kubernetes.

## Fargate

When running ECS and EKS on EC2, you are still responsible for maintaining the underlying EC2 instances.

AWS Fargate is a purpose-built serverless compute engine for containers. Fargate scales and manages the infrastructure, it removes the need to provision and manage servers, let you specify and pay for resources per application, and improves security through application isolation by design.

It natively integrates with AWS Identity and Access Management (IAM) and Amazon Virtual Private Cloud (VPC)

## Lambda

AWS Lambda, you can run code without provisioning or managing servers or containers.

Upload your source code, and Lambda takes care of everything required to run and scale your code with high availability.

A  Lambda function has three primary components – trigger, code, and configuration.

![]()

Triggers describe when a Lambda function should run. A trigger integrates your Lambda function with other AWS services, enabling you to run your Lambda function in response to certain API calls that occur in your AWS account.

you pay only for what you use it. 

[Tutorial: Resize Images on the Fly with Amazon S3, AWS Lambda, and Amazon API Gateway](https://aws.amazon.com/blogs/compute/resize-images-on-the-fly-with-amazon-s3-aws-lambda-and-amazon-api-gateway/)

[10 Things Serverless Architects Should Know](https://aws.amazon.com/blogs/architecture/ten-things-serverless-architects-should-know/)
