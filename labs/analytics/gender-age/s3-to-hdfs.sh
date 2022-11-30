clusterID=$(aws emr list-clusters --cluster-states WAITING | jq '.Clusters[0].Id' | sed -e  's/\"//g')
aws emr add-steps --cluster-id $clusterID --steps file://./s3-hdfs-step.json