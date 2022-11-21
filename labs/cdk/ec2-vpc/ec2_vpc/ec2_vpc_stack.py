from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam,
    # aws_sqs as sqs,
)
from constructs import Construct

class Ec2VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # VPC
        self.vpc = ec2.Vpc(self, "VPC",
            max_azs=2,
            cidr="10.10.0.0/16",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    name="private",
                    cidr_mask=24)
            ]
            )

        # AMI
        self.amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )

        # Instance Role and SSM Managed Policy
        self.role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        self.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # Create Bastion
        self.bastion = ec2.BastionHostLinux(self, "myBastion",
                                       vpc=self.vpc,
                                       subnet_selection=ec2.SubnetSelection(
                                           subnet_type=ec2.SubnetType.PUBLIC),
                                       instance_name="myBastionHostLinux",
                                       instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"))
                                       
        # Instance with user data
        self.instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=self.amzn_linux,
            vpc = self.vpc,
            role = self.role
            )
    
        CfnOutput(self, "Output", value=self.vpc.vpc_id)