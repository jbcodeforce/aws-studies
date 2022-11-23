import aws_cdk as core
import aws_cdk.assertions as assertions

from ecs_fargate_flask.ecs_fargate_flask_stack import EcsFargateFlaskStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ecs_fargate_flask/ecs_fargate_flask_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EcsFargateFlaskStack(app, "ecs-fargate-flask")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
