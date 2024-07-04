"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import ec2

#replace with a valid cidr block
CIDR_BLOCKS = ["XX.XX.XX.XX/XX"]

#exclude .pem extension
KEY_PAIR = "<your-key-pair-file>" 


sg = ec2.SecurityGroup("web-server-sg", description="Security group for the web server")
allow_ssh = ec2.SecurityGroupRule("AllowSSH", type="ingress", from_port=22, to_port=22, protocol="tcp", 
					cidr_blocks=CIDR_BLOCKS, security_group_id=sg.id)

allow_ssh = ec2.SecurityGroupRule("AllowHTTP", type="ingress", from_port=80, to_port=80, protocol="tcp", 
					cidr_blocks=CIDR_BLOCKS, security_group_id=sg.id)

allow_all = ec2.SecurityGroupRule("AllowEgress", type="egress", from_port=0, to_port=0, protocol="-1", 
					cidr_blocks=["0.0.0.0/0"], security_group_id=sg.id)


ec2_instance = ec2.Instance("web-server", 
			ami="ami-04a81a99f5ec58529", 
			instance_type = "t3.nano",
			vpc_security_group_ids=[sg.id],
			#key_name = "demo-key-personal-acc.pem",
			key_name = KEY_PAIR,
			tags = {"name": "web"}
			)


pulumi.export('public_ip', ec2_instance.public_ip)
pulumi.export('public_url', pulumi.Output.concat("http://", ec2_instance.public_dns))
