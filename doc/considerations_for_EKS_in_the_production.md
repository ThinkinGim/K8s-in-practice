## API server endpoint access
- Making only to allow accessing via private network to EKS: K8S has had significant functionalities to control from infrastructure to application. It's true that to provide the way of automation delivery software, however it would be a weakness which can to be hacked. For this reason, it's strongly recommended to set 'API server endpoint access' to 'Private'. (EKS> Cluster> [my-cluster]> Networking> API server endpoint access)

> Even if to allow public access, it could be say it's secured using combination of AWS-IAM and Kubernetes native authentication method.

- When it made 'Private', AWS will set R53 up to resolve endpoint domain of the EKS Cluster as a private IP  in your VPC with no further actions. It means there is no way to command via kubectl to your Cluster from outside of VPC network.

> https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html

## Security Group
- Cluster security group: It's part of EKS creation to allow communication between control plane and Nodes internally in the Kubernetes cluster. By default, it has the rule for each, in and out, to allow incoming traffic from which has this Security Group and to allow a traffic to go out to wherever. It has to keep allow to communicate freely for each others, between control plan and nodes or node to node, but it needs to restrict egress by specifying for particular purpose.

- ControlPlaneSecurityGroup: 

> https://kubernetes.io/docs/concepts/architecture/control-plane-node-communication/
> https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html