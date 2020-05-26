import json
import pytest

from aws_cdk import core
from eks.eks_stack import EksStack


def get_template():
    app = core.App()
    EksStack(app, "eks")
    return json.dumps(app.synth().get_stack("eks").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
