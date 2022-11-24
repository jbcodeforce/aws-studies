# [Elastic Kubernetes Service](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)

[Amazon EKS](https://aws.amazon.com/eks/) is a fully managed Kubernetes service. It supports EC2 to deploy worker nodes or Fargate to deploy serverless containers. 

![](./diagrams/eks-ec2.drawio.svg)

The EKS node types are:

* managed node groups: EC2 (could be On-demand or spot instances) created by you, assigned to a ASG managed by EKS. 
* self-managed nodes: nodes created by you and attached to EKS cluster by an ASG.
* AWS Fargate, which represents a cost optimized deployment for EKS worker nodes.

Data volumes (EBS, EFS, FSx) are defined with StorageClass and they need to have Container Storage Interface compliant driver.

[Pricing calculator](https://aws.amazon.com/eks/pricing/)

## Cluster management

* Access to the console
*  EKS uses IAM to provide authentication to our Kubernetes cluster, and k8s RBAC for authorization.

## ECS comparisons

* An EC2 instance with the ECS agent installed and configured is called a container instance. In Amazon EKS, it is called a worker node.
* An ECS container is called a task. In Amazon EKS, it is called a pod.
* While Amazon ECS runs on AWS native technology, Amazon EKS runs on top of Kubernetes.

## What to do the first time

1. Download `eksctl` ([eksctl.io](https://github.com/weaveworks/eksctl)). (it installs kubectl)

    ```sh
    brew tap weaveworks/tap
    brew install weaveworks/tap/eksctl
    ```

1. Be sure to have a EC2 key pair, if not create one with

    ```sh
    aws ec2 create-key-pair --region us-west-2 --key-name myKeyPair
    ```

1. Create IAM Role with EKS Cluster role and attach the required Amazon EKS IAM managed policy to it. Kubernetes clusters managed by Amazon EKS make calls to other AWS services on your behalf to manage the resources that you use with the service.

    ```sh
    # under the folder labs/eks
    aws iam create-role \
        --role-name myAmazonEKSClusterRole \
        --assume-role-policy-document file://"eks-cluster-role-trust-policy.json"
    # Attach the required Amazon EKS managed IAM policy to the role.
    aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy \
        --role-name myAmazonEKSClusterRole
    ```

## Working with cluster

1. Create cluster to be deployed on EC2, in a VPC, subnets, and security groups. It can be done with different ways:

    * Using cloudformation: 
    
    ```sh
    aws cloudformation create-stack \
        --region us-west-2 \
        --stack-name my-eks-vpc-stack \
        --template-url https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
    ```

    * Using `eksctl`:

    ```sh
    eksctl create cluster \
        --name my-cluster \
        --region us-west-2 \
        --with-oidc \
        --ssh-access \
        --ssh-public-key myKeyPair \
        --instance-types=m5.xlarge \
        --managed
    ```

    Find cluster credentials were added in ~/.kube/config

1. As an alternate, create Fargate profile to declare which pods run on Fargate. 

    * [see instructions](https://docs.aws.amazon.com/eks/latest/userguide/fargate-getting-started.html). 
    * Fargate profiles are associated to namespaces. 
    * Only private subnets are supported for pods that are running on Fargate. 
    * Pods that match a selector are scheduled on Fargate. 
    * Kubernetes affinity/anti-affinity rules do not apply and aren't necessary with Amazon EKS Fargate pod.

1. Verify nodes and pods

    ```sh
    kubectl get nodes -o wide
    # 
    kubectl get pods --all-namespaces -o wide
    ```

1. Add resources like node group, with IAM role of WorkerNode 


### Delete cluster

* List all services

```sh
kubectl get svc --all-namespaces
```

* Delete any services that have an associated EXTERNAL-IP value. These services are fronted by an Elastic Load Balancing load balancer, and you must delete them in Kubernetes to allow the load balancer and associated resources to be properly released.

```sh
kubectl delete svc <service-name>
```

* Delete the cluster

```sh
estctl delete cluster --name <cluster name>
```

## [EKS Blueprint](https://aws.amazon.com/blogs/containers/bootstrapping-clusters-with-eks-blueprints/)

The EKS Blueprints is an open-source development framework that abstracts the complexities of cloud infrastructure from developers.

### Concepts

* A blueprint combines clusters, add-ons, and teams into a cohesive object that can deployed as a whole. 
* Team is a logical grouping of IAM identities that have access to a Kubernetes namespace(s), or cluster administrative access depending upon the team type.
* Once a blueprint is configured, it can be easily deployed across any number of AWS accounts and regions.
* Blueprints also leverage GitOps tooling to facilitate cluster bootstrapping and workload onboarding.

![](https://d2908q01vomqb2.cloudfront.net/fe2ef495a1152561572949784c16bf23abb28057/2022/04/18/eks-blueprints-ref-951x1024.png)

### Hands-on 

This is a summary of the steps to get a running demonstration of creating EKS and Day 2 add-on.

* Prepare a dev environment using Cloud9, be sure to increase the disk space of the EC2 instance to 30 GB for `/` /dev/xvda1 volume.

    ```sh
    pip3 install --user --upgrade boto3
    export instance_id=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
    python -c "import boto3
    import os
    from botocore.exceptions import ClientError 
    ec2 = boto3.client('ec2')
    volume_info = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'attachment.instance-id',
                'Values': [
                    os.getenv('instance_id')
                ]
            }
        ]
    )
    volume_id = volume_info['Volumes'][0]['VolumeId']
    try:
        resize = ec2.modify_volume(    
                VolumeId=volume_id,    
                Size=30
        )
        print(resize)
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidParameterValue':
            print('ERROR MESSAGE: {}'.format(e))"
    if [ $? -eq 0 ]; then
        sudo reboot
    fi
    ```
* Update the CDK to be version 2.5

    ```sh
    rm $(which cdk)
    npm install -g aws-cdk@2.50.0
    cdk --version
    ```
* Install kubectl and AWS CLI

    ```sh
    sudo curl --silent --location -o /usr/local/bin/kubectl https://s3.us-west-2.amazonaws.com/amazon-eks/1.23.7/2022-06-29/bin/linux/amd64/kubectl

    sudo chmod +x /usr/local/bin/kubectl

    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    ```

* Install jq, gettext...

    ```sh
    sudo yum -y install jq gettext bash-completion moreutils
    # Verify the path
    for command in kubectl jq envsubst aws
    do
        which $command &>/dev/null && echo "$command in path" || echo "$command NOT FOUND"
    done

    # Enable kubectl bash_completion
    kubectl completion bash >>  ~/.bash_completion
    . /etc/profile.d/bash_completion.sh
    . ~/.bash_completion
    ```

* Create IAM role named `eks-blueprints-cdk-workshop-admin` with AdministratorAccess, and modify the EC2 instance IAM role in 
* Update Cloud9 workspace to disable Cloud9 to manage IAM credentials dynamically (This is not compatible with the EKS IAM authentication). `Gear > AWS Settings >` . 
* Save region and account as env variable and configure aws CLI:

    ```sh
    echo "export ACCOUNT_ID=${ACCOUNT_ID}" | tee -a ~/.bash_profile
    echo "export AWS_REGION=${AWS_REGION}" | tee -a ~/.bash_profile
    aws configure set default.region ${AWS_REGION}
    aws configure get default.region

    # validate that the Cloud9 IDE is using the correct IAM role
    aws sts get-caller-identity --query Arn | grep eks-blueprints-cdk-workshop-admin -q && echo "IAM role valid" || echo "IAM role NOT valid"
    ```
* bootstrap CDK is not done before. (the following command is to bootstrap CDK in 3 regions)

    ```sh
    cdk bootstrap --trust=$ACCOUNT_ID \
      --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess \
        aws://$ACCOUNT_ID/$AWS_REGION aws://$ACCOUNT_ID/us-east-2 aws://$ACCOUNT_ID/us-east-1
    ```
* To use GitOps approach create a `CodeCommit` Repository. If using GitHub, needs to set Personal Access Token

    ```sh
    aws codecommit create-repository --repository-name my-eks-blueprints-pipeline q
    ```

#### Single Cluster

* Using CDK typescript here are the commands:

```sh
mkdir my-eks-blueprints
cd my-eks-blueprints
cdk init app --language typescript
npm i typescript@~4.8.4
npm i @aws-quickstart/eks-blueprints
```

[See the code in labs/cdk/eks-single]()

* Create a Cluster using the eks-blueprints package, which is published as a npm module.

```js
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as blueprints from '@aws-quickstart/eks-blueprints';

export default class ClusterConstruct extends Construct {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id);

    const account = props?.env?.account!;
    const region = props?.env?.region!;

    const blueprint = blueprints.EksBlueprint.builder()
    .account(account)
    .region(region)
    .addOns()
    .teams()
    .build(scope, id+'-stack');
  }
}
```

And in the app

```js
#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import ClusterConstruct from '../lib/my-eks-blueprints-stack';

const app = new cdk.App();
const account = process.env.CDK_DEFAULT_ACCOUNT!;
const region = process.env.CDK_DEFAULT_REGION;
const env = { account, region }

new ClusterConstruct(app, 'cluster', { env });
```

* Deploy the cluster: `cdk deploy cluster-stack`, then config kubectl

```sh
export KUBE_CONFIG=$(aws cloudformation describe-stacks --stack-name cluster-stack | jq -r '.Stacks[0].Outputs[] | select(.OutputKey|match("ConfigCommand"))| .OutputValue')
$KUBE_CONFIG
kubectl get svc
```

* [EKS Blueprints Patterns](https://github.com/aws-samples/cdk-eks-blueprints-patterns)

#### On board teams

We want two teams: platform and application teams.

```sh
mkdir teams && cd teams && mkdir platform-team && mkdir application-team
aws iam create-user --user-name platform
aws iam create-user --user-name application

```

Under `platform-team` create a `init.ts`, Add a IAM Principal to add users to the platform using their IAM credentials

```
import { ArnPrincipal } from "aws-cdk-lib/aws-iam";
import { PlatformTeam } from '@aws-quickstart/eks-blueprints';

export class TeamPlatform extends PlatformTeam {
    constructor(accountID: string) {
        super({
            name: "platform",
            users: [new ArnPrincipal(`arn:aws:iam::${accountID}:user/platform`)]
        })
    }
}
```

And do the same for application team.
Then modify the cluster definition to add team instances: The `cdk deploy cluster-stack` will create a new namespace for the team application.

```js
import { TeamPlatform, TeamApplication } from '../teams'; 
...
.teams(new TeamPlatform(account), new TeamApplication('burnham',account))
```

A command like `kubectl describe role -n team-burnham` gives information on the role and actions that member can do.

Using Kubernetes constructs such as namespaces, quotas, and network policieswe can prevent applications deployed in different namespaces from communicating with each other.

* To see the application user access limitation, login to the console in incognito mode, use the account ID, application as user and be sure to have setup a password in IAM for the `application` user. Once logged assume the role of cluster-stack-teamburnhamAccessRole3.... Then go to the EKS console. We should see an error message that the Team Burnham user is NOT allowed to list deployments in all the namespaces. But selecting the `team-burnham` namespace we should see pods and other elements.

* The user platform with the role `cluster-stack-teamplatformAccessRole5...` can access the cluster as admin and see all namespaces.

#### Adding add-ons

[See the list of supported add-ons](https://aws-quickstart.github.io/cdk-eks-blueprints/addons/). To add them use the addOn() function in the blueprint:

```
  const blueprint = blueprints.EksBlueprint.builder()
    .account(account)
    .region(region)
    .addOns(new blueprints.ClusterAutoScalerAddOn)
    .teams(new TeamPlatform(account), new TeamApplication('burnham',account))
    .build(scope, id+'-stack');
  }
```

## Deeper Dive

* [Product documentation - Elastic Kubernetes Service](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
* [EKS Blueprints for CDK Workshop](https://catalog.workshops.aws/eks-blueprints-for-cdk/en-US)
* [Getting started with Amazon EKS – eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html)
* [EKS Best Practices Guides](https://aws.github.io/aws-eks-best-practices/security/docs/)
* [EKS Blueprint](https://aws.amazon.com/blogs/containers/bootstrapping-clusters-with-eks-blueprints/)
* [Amazon EKS Blueprints for Terraform](https://aws-ia.github.io/terraform-aws-eks-blueprints/getting-started/)