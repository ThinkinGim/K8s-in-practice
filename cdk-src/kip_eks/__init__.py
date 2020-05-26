import os 
import typing
import yaml
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    core
)

class Stack_Parameter_Group():

    def __init__(self, cluster_id:typing.Optional[str]=None, vpc_id:typing.Optional[str]=None, subnet_ids:typing.Optional[typing.List[str]]=None) -> None:
        """Stack Parameters

        :param cluster_id: 
        :param vpc_id:
        :param subnet_ids:
        """
        self._params = {}
        if cluster_id is not None: self._params["cluster_id"] = cluster_id
        if vpc_id is not None: self._params["vpc_id"] = vpc_id
        if subnet_ids is not None: self._params["subnet_ids"] = subnet_ids

    @property
    def cluster_subnet_list(self) -> typing.Optional[typing.List[str]]:
        return self._params.get('subnet_ids')

    @property
    def cluster_id(self) -> typing.Optional[str]:
        return self._params.get('cluster_id')

    @property
    def vpc_id(self) -> typing.Optional[str]:
        return self._params.get('vpc_id')

class EksStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, params:typing.Optional[Stack_Parameter_Group]=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc=None
        cluster_id=id+"-cluster"
        cluster_subnets=None

        if params is not None:
            if params.cluster_id is not None: cluster_id=params.cluster_id
            if params.vpc_id is not None:
                vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=params.vpc_id)
                vpc_subnets = (vpc.isolated_subnets + vpc.private_subnets + vpc.public_subnets)

                if params.cluster_subnet_list is not None:
                    cluster_subnets = []
                    for subnet in vpc_subnets:
                        if any(subnet.subnet_id in s for s in params.cluster_subnet_list):
                            cluster_subnets.append(ec2.SubnetSelection(subnets=[subnet]))
                    if not cluster_subnets: cluster_subnets=None
                else:
                    cluster_subnets=vpc.private_subnets

        kip_cluster = eks.Cluster(
            self, 
            id=cluster_id,
            default_capacity=0,
            kubectl_enabled=True,
            cluster_name=cluster_id,
            core_dns_compute_type=None,
            # masters_role=None,
            output_cluster_name=False,
            output_config_command=True,
            output_masters_role_arn=False,
            # role=None,
            # security_group=None,
            # version=None,
            vpc=vpc,
            vpc_subnets=cluster_subnets
        )
