#!/usr/bin/env python3

import aws_cdk as cdk

from python.python_stack import PythonStack


app = cdk.App()
PythonStack(app, "python")

app.synth()
