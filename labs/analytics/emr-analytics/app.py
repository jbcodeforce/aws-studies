#!/usr/bin/env python3
import os

import aws_cdk as cdk

from emr_analytics.emr_analytics_stack import EmrAnalyticsStack


app = cdk.App()
EmrAnalyticsStack(app, "EmrAnalyticsStack",
    s3_log_bucket="s3_bucket_logs",
    s3_script_bucket="s3_bucket_scripts",
    spark_script="gender-age-count.py",
    )

app.synth()
