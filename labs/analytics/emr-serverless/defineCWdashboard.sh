export APPID=$(./getApplicationId.sh My_First_Application)
aws cloudformation create-stack --region us-west-2 \
    --stack-name emr-serverless-dashboard \
    --template-body file:///$(pwd)/cloudwatch-dashboard.yaml \
    --parameters ParameterKey=ApplicationID,ParameterValue=$APPID