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

resource "aws_ecr_repository" "c8-prodge-dashboard-ecr" {
  name                 = "c8-prodge-dashboard-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

data "aws_ecr_image" "c8-prodge-dashboard-ecr-latest_image" {
  repository_name = aws_ecr_repository.c8-prodge-dashboard-ecr.name
  image_tag       = "latest"
}

resource "aws_ecs_task_definition" "c8-prodge-dashboard-task-definition" {
  family = "c8-prodge-dashboard-task-definition"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 3072
  container_definitions = jsonencode([
    {
      name      = "c8-prodge-streamlit-container"
      image     = ""
      cpu       = 10
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}