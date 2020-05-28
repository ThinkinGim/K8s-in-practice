import typing
from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class Subnets(core.Stack):

    @property
    def subnets(self) -> [ec2.ISubnet]:
        return self._subnets

    def __init__(self, scope: core.Construct, id: str, vpc_id: str, az_cidr: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._subnets = []
        stack_id = id

        for az in az_cidr.keys():
            cidr_per_zone=az_cidr.get(az)
            for cidr in cidr_per_zone:
                subnet = ec2.Subnet(
                    self,
                    id=stack_id+"-"+az,
                    availability_zone=az,
                    cidr_block=cidr,
                    vpc_id=vpc_id,
                    map_public_ip_on_launch=False
                )
                self.add(subnet)

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)
        selected_subnets = ec2.SubnetSelection(subnets=self._subnets)
        ec2_endpoint = ec2.InterfaceVpcEndpoint(self, stack_id+"ec2", 
            vpc=vpc, 
            service=ec2.InterfaceVpcEndpointAwsService.E_C2,
            subnets=selected_subnets
        )
        ecr_endpoint = ec2.InterfaceVpcEndpoint(self, stack_id+"ecr", 
            vpc=vpc, 
            service=ec2.InterfaceVpcEndpointAwsService.ECR,
            subnets=selected_subnets
        )
        ecr_drk_endpoint = ec2.InterfaceVpcEndpoint(self, stack_id+"drk", 
            vpc=vpc, 
            service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
            subnets=selected_subnets
        )
        s3_endpoint = ec2.GatewayVpcEndpoint(self, stack_id+"s3", 
            vpc=vpc, 
            service=ec2.GatewayVpcEndpointAwsService.S3,
            subnets=[selected_subnets]
        )

    def add(self, subnet: ec2.ISubnet) -> None:
        self._subnets.append(subnet)
