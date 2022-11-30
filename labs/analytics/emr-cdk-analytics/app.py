#!/usr/bin/env python3
import os

import aws_cdk as cdk

from emr_analytics.emr_analytics_stack import EmrAnalyticsStack


app = cdk.App()
EmrAnalyticsStack(app, "EmrAnalyticsStack",
    s3_log_bucket="aws-logs-403993201276",
    s3_script_bucket="emr-scripts-403993201276",
    spark_script="gender-age-count.py",
    )

app.synth()
