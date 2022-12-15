#!/bin/bash

export APPID=$(./getApplicationId.sh My_First_Application)
export ROLEARN=$(aws iam list-roles | jq -r '.Roles[] | select(.RoleName=="EMRServerlessS3RuntimeRole") | .Arn')
aws emr-serverless start-job-run \
    --application-id $APPID \
    --execution-role-arn $ROLEARN \
    --name WordCountJob \
    --job-driver '{
        "sparkSubmit": {
          "entryPoint": "s3://jb-data-set/scripts/wordcount.py",
          "entryPointArguments": ["s3://jb-data-set/emr-serverless-spark/output"],
          "sparkSubmitParameters": "--conf spark.executor.cores=1 --conf spark.executor.memory=4g --conf spark.driver.cores=1 --conf spark.driver.memory=4g --conf spark.executor.instances=1"
        }
    }' \
    --configuration-overrides '
    {
    "monitoringConfiguration": {
        "s3MonitoringConfiguration": {
            "logUri": "s3://jb-data-set/emr-serverless-spark/logs/"
        }
    }
  }'