from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam,
    # aws_sqs as sqs,
)
from constructs import Construct

cidr="10.10.0.0/16"
key_name = "my-key-pair"
amzn_linux = ec2.MachineImage.latest_amazon_linux(
    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
    edition=ec2.AmazonLinuxEdition.STANDARD,
    virtualization=ec2.AmazonLinuxVirt.HVM,
    storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)

with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class Ec2VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # VPC
        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=2,
                           cidr=cidr,
                           nat_gateways=2,
                           enable_dns_hostnames=True,
                           enable_dns_support=True,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name="public",
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=24),
                               ec2.SubnetConfiguration(
                                   subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                                   name="private",
                                   cidr_mask=24) # could be /16 to have more instances, but this is a demo scope.
                           ]
                           )

        # Instance Role and SSM Managed Policy
        self.role = iam.Role(
            self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        self.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # Create Bastion Host
        self.bastion = ec2.BastionHostLinux(self, "myBastion",
                                            vpc=self.vpc,
                                            subnet_selection=ec2.SubnetSelection(
                                                subnet_type=ec2.SubnetType.PUBLIC),
                                            instance_name="myBastionHostLinux",
                                            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"))
        self.bastion.instance.instance.add_property_override(
            "KeyName", key_name)

        self.bastion.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Internet access SSH")

        self.ec2_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                                  vpc=self.vpc,
                                                  description="SecurityGroup for EC2 in private subnet",
                                                  security_group_name="CDK SecurityGroup",
                                                  allow_all_outbound=True,
                                                  )

        self.ec2_security_group.add_ingress_rule(ec2.Peer.ipv4(cidr), ec2.Port.tcp(22), "allow ssh access from the VPC")
        # Instance with user data
        self.instance = ec2.Instance(self, "myHttpdEC2",
                                     instance_type=ec2.InstanceType("t2.micro"),
                                     instance_name="mySimpleHTTPserver",
                                     machine_image=amzn_linux,
                                     vpc=self.vpc,
                                     role=self.role,
                                     key_name=key_name,
                                     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                     security_group=self.ec2_security_group,
                                     user_data=ec2.UserData.custom(user_data),
                                     )
        self.instance.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "allow http from world")
        self.instance.connections.allow_from_any_ipv4(ec2.Port.tcp(443), "allow https from world")
        
        CfnOutput(self, "VPCid", value=self.vpc.vpc_id)
        CfnOutput(self, "BastionHost_information", value=self.bastion.instance_public_ip, description="BastionHost's Public IP")
        CfnOutput(self, "WebHost_information", value=self.instance.instance_public_ip, description="Web server's Public IP")

