from aws_cdk import (
    # Duration,
    Stack,
    aws_iam,
    aws_ec2,
    aws_eks
    # aws_sqs as sqs,
)
from constructs import Construct

cidr="10.10.0.0/16"
key_name = "my-key-pair"


class EksCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        self.vpc = aws_ec2.Vpc(self, "VPC",
                           max_azs=2,
                           ip_addresses=aws_ec2.IpAddresses.cidr(cidr),
                           nat_gateways=1,
                           enable_dns_hostnames=True,
                           enable_dns_support=True,
                           subnet_configuration=[
                               aws_ec2.SubnetConfiguration(
                                   name="public",
                                   subnet_type=aws_ec2.SubnetType.PUBLIC,
                                   cidr_mask=24),
                               aws_ec2.SubnetConfiguration(
                                   subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS,
                                   name="private",
                                   cidr_mask=24) # could be /16 to have more instances, but this is a demo scope.
                           ]
                           )
        # Create an IAM role for worker groups and kubernetes RBAC configuration
        self.eks_admin_role = aws_iam.Role(self, 'eksAdmin',
                                    assumed_by=aws_iam.ServicePrincipal(service='ec2.amazonaws.com'),
                                                                          role_name='eks-cluster-role', 
                                                                          managed_policies=
                                                                                [aws_iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AdministratorAccess')])
        self.eks_instance_profile = aws_iam.CfnInstanceProfile(self, 'instanceprofile',
                                                      roles=[self.eks_admin_role.role_name],
                                                      instance_profile_name='eks-cluster-role')
                                      
    
                            

        self.cluster = aws_eks.Cluster(self, 'demo-cluster',
                                  masters_role=self.eks_admin_role,
                                  vpc=self.vpc,
                                  default_capacity=0,
                                  vpc_subnets=[aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS)],
                                  version=aws_eks.KubernetesVersion.V1_23,
                                  output_cluster_name=True
                                  )

        self.nodegroup = self.cluster.add_nodegroup_capacity('eks-nodegroup',
                                                   instance_types=[aws_ec2.InstanceType('t3.large'),
                                                                   aws_ec2.InstanceType('m5.large'),
                                                                   aws_ec2.InstanceType('c5.large')],
                                                   disk_size=50,
                                                   min_size=2,
                                                   max_size=2,
                                                   desired_size=2,
                                                   subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                                   remote_access=aws_eks.NodegroupRemoteAccess(
                                                                        ssh_key_name='eks-ssh-keypair'),
                                                   capacity_type=aws_eks.CapacityType.SPOT)


