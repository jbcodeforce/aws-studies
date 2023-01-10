# [CloudFormation](https://docs.aws.amazon.com/cloudformation/index.html)

Create and manage a collection of related AWS resources as code. The template defines AWS resources, called a stack, as Yaml or JSON. Can be uploaded from a S3 bucket or from our local computer. 

The goal is to use Infrastructure as code and repeat infrastructure setup between regions or accounts. One of the greatest benefits of templates and CloudFormation is the ability to create a set of resources that work together to create an application or solution.

Stacks are defined in region, but StackSets helps to share stacks between accounts and regions.
Stack can be created with other stacks (nested).

To create a stack from AWS templates we can use CLI, API, the Console or start from one of the samples.

Once stack is created, `Change Sets` may be applied to update the running resources. It is like a summary of the proposed changes. There is also the `Drift` detection feature to identify configuration changes between live resources and template. 
It is possible to use a CloudFormation public registry, with 3nd party resources published in APN.

Pay for what the resources it uses. 

## Get started

The infrastructure is defined in Stack. See example of EC2 with a webserver and a security group in the folder [labs/CF](https://github.com/jbcodeforce/aws-studies/tree/main/labs/CF).

```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !FindInMap [AWSRegionArch2AMI, !Ref 'AWS::Region', !FindInMap [AWSInstanceType2Arch, !Ref InstanceType, Arch]]      
      InstanceType:
        Ref: t2-micro
      KeyName:
        Ref: my-key-pair
      SecurityGroups:
      - Ref: WebServerSecurityGroup
      UserData:
        Fn::Base64: !Sub |
           #!/bin/bash -xe
           yum update -y
           yum install -y httpd
           systemctl start httpd
           systemctl enable httpd
           EC2-AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
           echo "<h3>Hello World from $(hostname -f) in AZ= $EC2_AZ </h3>" > /var/www/html/index.html
```

The KeyName property is a literal for an existing keyname in the region where the stack is being created.

We use the `Parameters` section to declare values that can be passed to the template when we create the stack.

```yaml
Parameters:      
  KeyName:
    ConstraintDescription: must be the name of an existing EC2 KeyPair.
    Description: Name of an existing EC2 KeyPair to enable SSH access to the instances
    Type: AWS::EC2::KeyPair::KeyName

```

See the [getting started guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/GettingStarted.Walkthrough.html).

* The `Ref` function returns the value of the object it refers to.
* Use `Mappings` to declare conditional values that are evaluated in a similar manner as a look up table statement
* Ensure that all dependent resources that the template requires are available
* The [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html) function helps to get attribute of a resource.
* Mappings enable us to use an input value as a condition that determines another value. Similar to a switch statement, a mapping associates one set of values with another. Below the ImageId property of the resource Ec2Instance uses the `Fn::FindInMap` function to determine its value by specifying `RegionMap` as the map to use, `AWS::Region` as the input value to map from, and AMI as the label to identify the value to map to.

    ```yaml
    Mappings:
        RegionMap:
            us-east-1:
            AMI: ami-76f0061f
            us-west-1:
            AMI: ami-655a0a20
    Resources:
        Ec2Instance:
            Type: 'AWS::EC2::Instance'
            Properties:
                ImageId: !FindInMap 
                    - RegionMap
                    - !Ref 'AWS::Region'
                    - AMI
    ```

* See [template details](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/gettingstarted.templatebasics.html).
* We can associate the `CreationPolicy` attribute with a resource to prevent its status from reaching create complete until AWS CloudFormation receives a specified number of success signals or the timeout period is exceeded.

Example for S3 bucket and website:

```yaml
Resources:
  HelloBucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      AccessControl: PublicRead
      WebsiteConfiguration:
        IndexDocument: index.html
        ErrorDocument: error.html
```

## Tools

* [Use Cloud formation linter](https://github.com/aws-cloudformation/cfn-lint) to validate the yaml declaration
* [Json to Yaml online tool](https://www.json2yaml.com/)
* Consider [CDK](../#cloud-development-kit-cdk) as a higher abstraction level to generate Cloud Formation stacks.

## Deeper dive

* [Introduction from Tutorial Dojo](https://youtu.be/9Xpuprxg7aY)
* [AWS CloudFormation Workshop](https://catalog.workshops.aws/cfn101/en-US) with Git repo [aws-samples/cfn101-workshop](https://github.com/aws-samples/cfn101-workshop) cloned in Code/Studies folder.
* [Best practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
* [Sample templates for some AWS services](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/sample-templates-services-us-west-1.html)
