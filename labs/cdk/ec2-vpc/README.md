
# EC2 with VPC and subnets

The Cloud Formation created from this cdk includes:

* One VPC.
* One public subnet and one private subnet.
* One Bastion Host deployed in Public subnet with pem associated to an existing key-pair
* An EC2 instance in the private subnet, with a security group to get SSH from 

The goal is to demonstrate SSH to the EC2 instance via the Bastion Host.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux or within the docker container:

```sh
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Synthesize the CloudFormation template for this code.

```
$ cdk synth
```

## Demonstration script

* From this `ec2-vpc` folder deploy with `cdk deploy` and wait at least 250 s
* Go to the EC2 instances, select the simpleHTTPserver to display that it does not have a public IP address, but a Security Group with an inbound rule for SSH from internal subnet.
* In EC2 instance list, select the Bastion Host, open connect terminal on it.
* Get the .pem file for the key-pair used to define the EC2 instance of the HTTP Server, an create a file in the bastion host to keep this client certificate (file `key.pem`)
* Then ssh to this host:

```sh
ssh ec2-user@10.10.2.253 -i key.pem
```
* In the HTTP server host, we can do `curl localhost` to see the HTTP page served by httpd.
* Terminate with `cdk destroy`

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `cdk destroy`     remove all the resources/stacks. 
 * `cdk metadata Ec2VpcStack` to see all created resources.
