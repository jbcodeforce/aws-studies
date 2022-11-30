clusterID=$(aws emr list-clusters --cluster-states WAITING | jq '.Clusters[0].Id' | sed -e  's/\"//g')
aws emr add-steps \
--cluster-id $clusterID \
--steps Type=Spark,Name="SparkApplication",ActionOnFailure=CONTINUE,Args=[s3://jb-data-set/restaurants/red-violations.py,--data_source,s3://jb-data-set/restaurants/food_establishment_data.csv,--output_uri,s3://jb-data-set/restaurants/results]							