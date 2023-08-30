provider "aws" {
  region = "${var.region}"
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"

}

resource "aws_security_group" "c8-prodge-rds-sg" {
  name = "c8-prodge-rds-sg"
  description = "Security group that allows comunitciaon opn all ports to RDS inbound and outbound"
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
