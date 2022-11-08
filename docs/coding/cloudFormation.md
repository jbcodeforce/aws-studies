# [CloudFormation](https://docs.aws.amazon.com/cloudformation/index.html)

Create and provision AWS infrastructure deployments predictably and repeatedly. Move as Infrastructure as code. Repeat infrastructure between regions or accounts.

The infrastructure is defined in Stack. See example of EC2 with a webserver and a security group in the folder [labs/CF]

```yaml
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
```

You use the Parameters section to declare values that can be passed to the template when you create the stack.

```yaml
Parameters:      
  KeyName:
    ConstraintDescription: must be the name of an existing EC2 KeyPair.
    Description: Name of an existing EC2 KeyPair to enable SSH access to the instances
    Type: AWS::EC2::KeyPair::KeyName

```

See the [getting started guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/GettingStarted.Walkthrough.html).

* The Ref function returns the value of the object it refers to.
* Mappings to declare conditional values that are evaluated in a similar manner as a look up table statement
* Ensure that all dependent resources that the template requires are available

See [template details](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/gettingstarted.templatebasics.html).