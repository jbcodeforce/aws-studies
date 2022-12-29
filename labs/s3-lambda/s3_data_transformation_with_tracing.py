import json
from json import JSONEncoder
import urllib.parse
import boto3 # AWS Python SDK
import re # python regex module
import os
import time

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

# Code to convert Robocopy Log File to JSON Format
# Adapted from my Python Regular Expressions Course
# https://www.udemy.com/course/python-regular-expressions/



print('Loading function')

s3 = boto3.client('s3')

# Destination bucket for transformed files

DESTINATION_BUCKET = os.environ['DESTINATION_BUCKET']

class LogMetrics:
    def __init__(self):
        self.log_file_name = '' # log file name 
        self.directory = {} # source and destionation directory paths
        self.metrics = []; # metrics row
        self.error = False  
        self.error_message = ''

# http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
        
# https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-subsegments.html
@xray_recorder.capture('## process_robocopy_log')
def process_robocopy_log(bucket, key, file_name):    
    #time.sleep(1)
    # Extract source and destination directory    
    PATTERN_DIRECTORY_NAME = r'(?i)^\s+(?P<type>Source|Dest)\s+:\s+(?P<dir>.+)'
    
    # Locate Errors
    PATTERN_ERROR = r'(?i)^(?P<ts>\d{4}(/\d{2}){2}\s+(\d{2}:){2}\d{2})\s+error(?P<error>.+)'            
    
    # Extract Metrics columns
    PATTERN_METRICS = \
     r'(?i)^\s+(?P<type>dirs|files|bytes)\s+:\s+'\
     r'(?P<total>\d{1,})\s+(?P<copied>\d{1,})\s+'\
     r'(?P<skipped>\d{1,})\s+(?P<mismatch>\d{1,})\s+'\
     r'(?P<failed>\d{1,})\s+(?P<extras>\d{1,})'
    

    log_metrics = LogMetrics()
    log_metrics.log_file_name = bucket + r'/' + key
    
    with open(file_name,'r', encoding='utf-8') as rdr:            
        for line in rdr:                
            match = re.search(PATTERN_ERROR, line)
        
            if match:
                log_metrics.error = True
                log_metrics.error_message = line
                
            match = re.search(PATTERN_DIRECTORY_NAME, line)
            
            if match:
                log_metrics.directory[match.group('type')] = match.group('dir')
                
            match = re.search(PATTERN_METRICS, line)
            
            if match:
                metricsRow = []
                metricsHeader = []
                captureHeader = False
                
                # Capture Metrics Table Column Header?
                if len(log_metrics.metrics)==0:
                    captureHeader = True
                
                # iterate named groups
                for key,value in match.groupdict().items():
                    if captureHeader:
                        metricsHeader.append(key)
                    
                    metricsRow.append(value)
                    
                # add to output
                if captureHeader:
                    log_metrics.metrics.append(metricsHeader)
                
                log_metrics.metrics.append(metricsRow)                  
                
                
        with open(file_name+'.json','w', encoding='utf-8') as wr:
            json.dump(log_metrics, wr, ensure_ascii=False, cls=MyEncoder, indent=True)
    
    return file_name + ".json"

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    error = False
    
    for record in event['Records']:
        # Get the object from the event and show its content type
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        
        print(f"Source File: {bucket}/{key}")

        # check if source file is a .txt file
        # also prevents possible recursion when transformed file is uploaded to S3 bucket
        if not key.endswith(".txt"):
            print("source file is not a .txt file")
            continue

        temp_file_name = r'/tmp/workingfile.txt'
        try:
            
            # remove existing temp file
            if os.path.exists(temp_file_name):
                os.remove(temp_file_name)
        
            if os.path.exists(temp_file_name + ".json"):
                os.remove(temp_file_name + ".json")

            # download file to local scratch space
            s3.download_file(Bucket=bucket,
                            Key=key,
                            Filename=temp_file_name)
            
            # transform file to json
            # function returns the transformed file name
            temp_file_name = process_robocopy_log (bucket, key, temp_file_name)

            # replace source prefix with destination prefix
            # add json at the end
            transformed_key = key + ".json"
            
            # upload transformed file to S3
            s3.upload_file(Bucket=DESTINATION_BUCKET, 
                        Key=transformed_key,
                        Filename=temp_file_name)
            
            print(f"Transformed File: {DESTINATION_BUCKET}/{transformed_key}")
            
        except Exception as e:
            print(e)
            error = True
    
    if error:
        return "Error when processing files"
    else:
        return "OK"
    
