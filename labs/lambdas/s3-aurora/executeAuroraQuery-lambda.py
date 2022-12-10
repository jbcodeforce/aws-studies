import time
import boto3

# Code template for executing an athena query and save the results in S3

query = 'SELECT * FROM inputtablename'
DATABASE = 'customers'
output='s3://test-bucket-jbcodeforce/'

def lambda_handler(event, context):
    client = boto3.client('athena')

    # Execution
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': output,
        }
    )
    return response