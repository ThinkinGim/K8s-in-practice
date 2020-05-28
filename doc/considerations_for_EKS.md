- Cluster security group: It's part of EKS creation to allow communication between control plane and Nodes internally in the Kubernetes cluster. By default, it has the rule for each, in and out, to allow incoming traffic from which has this Security Group and to allow a traffic to go out to wherever. It has to keep allow to communicate freely for each others, between control plan and nodes or node to node, but it needs to restrict egress by specifying for particular purpose.

- ControlPlaneSecurityGroup: 

> https://kubernetes.io/docs/concepts/architecture/control-plane-node-communication/
> https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html