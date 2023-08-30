provider "aws" {
  region = var.REGION
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

resource "aws_db_instance" "c8-prodge-rds-db" {
  allocated_storage    = 20
  db_name              = "c8-prodge-rds-db"
  engine               = "PostgreSQL"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = var.RDS_USERNAME
  password             = var.RDS_PASSWORD
  publicly_accessible = true
  performance_insights_enabled = false
  port = var.RDS_PORT
  db_subnet_group_name = "public_subnet_group"
  vpc_security_group_ids = [aws_security_group.c8-prodge-rds-sg.id]
}
