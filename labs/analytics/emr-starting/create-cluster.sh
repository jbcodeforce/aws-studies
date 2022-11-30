aws emr create-default-roles

aws emr create-cluster --name "EMRCluster-1" --release-label emr-5.36.0 --applications Name=Spark Name=Hadoop \
--ec2-attributes KeyName=my-key-pair --instance-type m5.xlarge --instance-count 2 --use-default-roles
