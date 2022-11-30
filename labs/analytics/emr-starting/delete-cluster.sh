
clusterID=$(aws emr list-clusters --cluster-states WAITING | jq '.Clusters[0].Id' | sed -e  's/\"//g')
aws emr terminate-clusters --cluster-ids $clusterID
