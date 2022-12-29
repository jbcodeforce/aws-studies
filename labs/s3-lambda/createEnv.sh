echo "Create S3 buckets"
aws s3api create-bucket --bucket jb-405-robot-in --region eu-west-2  --create-bucket-configuration LocationConstraint=eu-west-2
aws s3api create-bucket --bucket jb-405-robot-out --region eu-west-2  --create-bucket-configuration LocationConstraint=eu-west-2

echo "Add IAM policy"
aws iam create-policy --policy-name s3-rw-permission --policy-document file://iam-policy.json

# aws ian create-role --role-name s3-data-transformation --assume-role-policy-document file://Test-Role-Trust-Policy.json