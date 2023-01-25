from typing import List
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)


class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.default_vpc = ec2.Vpc(
            self,
            "default-allow-all",
            vpc_name="default-allow-all",
            cidr="10.0.0.0/16",
            max_azs=2,
            subnet_configuration=self.create_subnets(),
        )
        
        self.create_security_group('allow-ssh-sg', ports=[22])
        self.create_security_group('allow-https-ssh-sg', ports=[22, 80, 443])
        self.create_security_group('allow-postgres-ssh-sg', ports=[22, 5432])
        self.create_all_tcp_ports_security_group('allow-all-tcp-sg')
        self.create_all_traffic_ports_security_group('allow-all-traffic-sg')
    
    def create_subnets(self) -> List[ec2.SubnetConfiguration]:
        """creates subnets for all the four subnet types"""
        return [
            ec2.SubnetConfiguration(
                name="default-public",
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=24,
            ),
            ec2.SubnetConfiguration(
                name="default-private-isolated",
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                cidr_mask=24,
            ),
            ec2.SubnetConfiguration(
                name="default-private-egress",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                cidr_mask=24,
            ),
            ec2.SubnetConfiguration(
                name="default-private-nat",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                cidr_mask=24,
            ),
        ]

    def create_security_group(self, name: str, ports: List[int]) -> None:
        """creating a security group with allow to specified TCP ports"""
        security_group = ec2.SecurityGroup(
            self,
            name,
            security_group_name=name,
            vpc=self.default_vpc,
            allow_all_ipv6_outbound=True,
            allow_all_outbound=True,
        )

        for port in ports:
            security_group.add_ingress_rule(
                peer=ec2.Peer.any_ipv4(),
                connection=ec2.Port.tcp(port),
            )
        
    def create_all_tcp_ports_security_group(self, name: str) -> None:
        """creating a security group with allow to all TCP ports"""
        security_group = ec2.SecurityGroup(
            self,
            name,
            security_group_name=name,
            vpc=self.default_vpc,
            allow_all_ipv6_outbound=True,
            allow_all_outbound=True,
        )

        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.all_tcp(),
        )

    def create_all_traffic_ports_security_group(self, name: str) -> None:
        """creating a security group with allow to all traffics"""
        security_group = ec2.SecurityGroup(
            self,
            name,
            security_group_name=name,
            vpc=self.default_vpc,
            allow_all_ipv6_outbound=True,
            allow_all_outbound=True,
        )

        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.all_traffic(),
        )
