terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-1" # Chọn vùng Singapore (gần Việt Nam nhất)
}

# 1. Khai báo khung Application Load Balancer (ALB)
resource "aws_lb" "ecommerce_lb" {
  name               = "ecommerce-content-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [] # Sẽ cập nhật nhóm bảo mật sau
  subnets            = [] # Sẽ cập nhật danh sách subnet sau

  enable_deletion_protection = false

  tags = {
    Environment = "Project-Team"
  }
}