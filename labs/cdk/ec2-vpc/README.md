
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

To manually create a virtualenv on MacOS and Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `cdk destroy`     remove all the resources/stacks. 
 * `cdk metadata Ec2VpcStack` to see all created resources.
