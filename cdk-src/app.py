#!/usr/bin/env python3

from aws_cdk import core

from kip_eks import (
    EksStack,
    Stack_Parameter_Group
)

app = core.App()
"""
If you want to be done with default generated resources on cdk-eks, it would write a parameter named 'env' which is instance of aws_cdk.core.Environment.
Otherwise, it could be done with 'params' which is instance of kip_eks.Stack_Parameter_Group to pass to the info of exisisted resources.
"""
# EksStack(app, "kip-cluster-default", env=core.Environment(account="1234567", region="ap-northeast-1"))

# EksStack(app, "kip-cluster-with-param", params=Stack_Parameter_Group(cluster_id="CLUSTER_NAME", vpc_id="vpc-00000000", subnet_ids=["subnet-00000000","subnet-00000000"]), env=core.Environment(account="1234567", region="ap-northeast-1"))

app.synth()
