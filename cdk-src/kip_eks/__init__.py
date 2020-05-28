import typing
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    core
)

class Stack_Parameter_Group():

    def __init__(self, cluster_id:str, vpc_id:str, subnets:[ec2.ISubnet] ) -> None:
        """Stack Parameters

        :param cluster_id: 
        :param vpc_id:
        :param subnet_ids:
        """
        self._params = {}
        self._params["cluster_id"] = cluster_id
        self._params["vpc_id"] = vpc_id
        self._params["subnets"] = subnets

    @property
    def cluster_subnets(self) -> [ec2.ISubnet]:
        return self._params.get('subnets')

    @property
    def cluster_id(self) -> str:
        return self._params.get('cluster_id')

    @property
    def vpc_id(self) -> str:
        return self._params.get('vpc_id')

class EksStack(core.Stack):

    @property
    def cluster(self) -> eks.Cluster:
        return self._kip_cluster

    @property
    def cluster_subnets(self) -> [ec2.ISubnet]:
        return self._cluster_subnets

    def __init__(self, scope: core.Construct, id: str, params:typing.Optional[Stack_Parameter_Group]=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster_vpc=None
        cluster_id=id+"-cluster"
        cluster_subnets=[]
        
        if params is not None:
        #     if params.cluster_id is not None: cluster_id=params.cluster_id
            cluster_vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=params.vpc_id)
            # vpc_subnets = (cluster_vpc.private_subnets + cluster_vpc.public_subnets + cluster_vpc.isolated_subnets)
            cluster_id = params.cluster_id
            
            # cluster_subnets_id = [i.subnet_id for i in params.cluster_subnet_list]
            cluster_subnets = params.cluster_subnets

            print("DEBUG::cluster_subnets")
            print(cluster_subnets)

            self._cluster_subnets = cluster_subnets

            # for subnet in vpc_subnets:
            #     if any(subnet.subnet_id in s for s in cluster_subnets_id):
            #         cluster_subnets.append(subnet)
            # if not cluster_subnets: cluster_subnets=None

        #         if params.cluster_subnet_list is not None:
        #             self._cluster_subnets = []
        #             for subnet in vpc_subnets:
        #                 if any(subnet.subnet_id in s for s in params.cluster_subnet_list):
        #                     self._cluster_subnets.append(subnet)
        #             if not self._cluster_subnets: self._cluster_subnets=None

        self._kip_cluster = eks.Cluster(
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
            vpc=cluster_vpc,
            vpc_subnets=[ec2.SubnetSelection(subnets=cluster_subnets)]
        )

class NodegroupStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, target_cluster: eks.Cluster, vpc_subnets: [ec2.ISubnet], **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        eks.Nodegroup(
            self,
            id=id, 
            cluster=target_cluster,
            ami_type=eks.NodegroupAmiType.AL2_X86_64,
            desired_size=1,
            disk_size=20,
            force_update=False,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
            max_size=1,
            min_size=1,
            nodegroup_name=id,
            subnets=ec2.SubnetSelection(subnets=vpc_subnets)
        )