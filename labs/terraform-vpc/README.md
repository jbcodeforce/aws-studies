# VPC with Terraform

The Terraform configuration below:

* Creates a VPC
* Creates an Internet Gateway and attaches it to the VPC to allow traffic within the VPC to be reachable by the outside world.
* Creates a public and private subnet
* Creates a route table for the public and private subnets and associates the table with both subnets
* Creates a NAT Gateway to enable private subnets to reach out to the internet without needing an externally routable IP address assigned to each resource.

1. Run the `terraform init` command in the same directory. The terraform init command initializes the plugins and providers which are required to work with resources.

1. Run the `terraform plan` command. This is an optional, yet recommended action to ensure your configuration’s syntax is correct and gives you an overview of which resources will be provisioned in your infrastructure.

1. Provision the AWS VPC and resources using `terraform apply`.

When we need to stop this deployment use the command; `terraform destroy`

## Deeper dive

* [Getting started with AWS and Terraform from Hashicorp](https://developer.hashicorp.com/terraform/tutorials/aws-get-started).
* [How to destroy resources with Terrafform](https://spacelift.io/blog/how-to-destroy-terraform-resources).