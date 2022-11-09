from typing_extensions import runtime
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
)


class PythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        myLambda = _lambda.Function(self,
                    'HelloHandler',
                    runtime= _lambda.Runtime.PYTHON_3_7,
                    code=_lambda.Code.fromAsset('lambda'),
                    hanlder='hello.handler')
        
