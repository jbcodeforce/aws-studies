# Coding practices

## [SDK](https://aws.amazon.com/developer/tools/)

Supports a lot of languages to integrate with a lot of managed services from your business application.

## [DevOps](https://aws.amazon.com/devops/)

## [CloudFormation](./cloudFormation.md)

See [separate note](./cloudFormation.md).

## [CodeCommit](https://docs.aws.amazon.com/codecommit/)

Version control fully managed service to manage Git repositories. HA, secured, encryption at rest and in transit. 

Be sure to get the Git Credentials for the IAM user we will use to do the Git repository actions. 

* [Setup SSH connection to CodeCommit](https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-unixes.html)

## Elastic Beanstalk

[Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk) is a developer centric view of the deployment of web apps on AWS using EC2, ALB, ELB, RDS, ASG...
It is a managed service and it automatically manages capacity provisioning, load balancing, scaling, health, configuration...

An application is a collection of Beanstalk components (environments, versions, configurations).

It defines two preconfigured environments:

* Web Server Tier: classical ELB, Auto scaling group and EC2s.
* Worker environment with the use of SQS queue.

It uses [CloudFormation](#cloudformation) to deploy the application and the environment.

## [Elastic Container Registry](https://docs.aws.amazon.com/ecr/)

AWS managed container image registry service that is secure, scalable, and reliable. 

An Amazon ECR **repository** contains your Docker _images_, Open Container Initiative (OCI) images, and OCI compatible artifacts. One repository per app.

![](./images/ecr-repo-create.png)

Client must authenticate to Amazon ECR registries as an AWS user before it can push and pull images.

You can control access to your repositories and the images within them with repository policies.

As a developer you need AWS CLI and Docker.

[Pricing](https://aws.amazon.com/ecr/pricing/): pay for the amount of data you store in your repositories and for the data transfer from your image pushes and pulls.  50 GB per month of always-free storage for their public repositories. For private 500MB first year.
Data transfer to services within the same region is free of charge.

### Demonstration

* Create one ECR repository per app or microservice.
* From you Laptop you docker build with the ECR repo URL.

```sh
aws ecr help
# Get the authentication token and authenticate the docker client
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <...>.amazonaws.com

# Can also use the docker cli, see The View push commands for your repository
docker tag jbcodeforce/autonomous-car-ride:latest <...>.amazonaws.com/jbcodeforce/autonomous-car-ride:latest
docker push  <...>.amazonaws.com/jbcodeforce/autonomous-car-ride:latest
```

If you want to run your application using docker engine inside of EC2, create a simple EC2 and then ssh to it and add docker, and do a docker run. Here are the installation you need:

```sh
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-get install docker-ce docker-ce-cli containerd.io
apt-cache madison docker-ce
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo apt install docker.io
```

## App Runner

## [Chalice](https://aws.github.io/chalice/index.html)

A python framework to build serverless applications. We can have a REST API deployed to Amazon API Gateway and AWS Lambda in minutes.

## [Serverless Application Model](https://aws.amazon.com/serverless/sam/)

SAM is an open-source framework for building serverless applications. It provides shorthand syntax to express functions, APIs, databases, and event source mappings.
During deployment, SAM transforms and expands the SAM syntax into AWS CloudFormation syntax.

SAM CLI provides a Lambda-like execution environment that lets you locally build, test, and debug applications defined by SAM templates or through the AWS Cloud Development Kit (CDK).

* [Install](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html), which can be summarized as:

```sh
brew install aws-sam-cli
# or upgrade
brew upgrade aws-sam-cli
sam --version
```

* [Serverless pattern collection](https://serverlessland.com/patterns?framework=SAM)

## [CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)

AWS CodePipeline is a continuous delivery service.

* [Getting started](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html#welcome-get-started)
* Pricing 1$ / month per pipeline. All pipelines are free for the first 30 days.

## [CodeBuild](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodeBuild.html)

AWS CodeBuild is a fully managed build service that compiles source code, runs tests, and produces software packages that are ready to deploy.

## CodeDeploy

## [CodeStar](https://aws.amazon.com/codestar/)

AWS CodeStar provides a unified user interface, enabling you to easily manage your software development activities in one place.

To start a project, you can choose from a variety of AWS CodeStar templates for Amazon EC2, AWS Lambda, and AWS Elastic Beanstalk. You have the option to choose AWS CodeCommit or GitHub to use as your project’s source control.

There is no additional charge for AWS CodeStar.

* [Getting started](https://docs.aws.amazon.com/codestar/latest/userguide/getting-started-topnode.html)
* [Product documentation](https://docs.aws.amazon.com/codestar/)

## CloudWatch

## [AWS Proton](https://docs.aws.amazon.com/proton/latest/userguide/Welcome.html)

Automated infrastructure as code provisioning and deployment of serverless and container-based applications.

