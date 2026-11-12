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
  region = "ap-southeast-1"
}

# 1. Tạo mạng ảo VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "ecommerce-vpc"
  }
}

# 2. Tạo 2 Subnet công khai (Public Subnets) ở 2 Availability Zones khác nhau
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-southeast-1a"

  tags = { Name = "ecommerce-public-subnet-1" }
}

resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-southeast-1b"

  tags = { Name = "ecommerce-public-subnet-2" }
}

# 3. Tạo Internet Gateway để mạng VPC thông ra ngoài Internet
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = { Name = "ecommerce-igw" }
}

# 4. Tạo bảng định tuyến (Route Table) cho Public Subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = { Name = "ecommerce-public-rt" }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}

# 5. Tạo Security Group cho Load Balancer (Mở cổng 80 và 443)
resource "aws_security_group" "lb_sg" {
  name        = "ecommerce-lb-sg"
  description = "Cho phép truy cập HTTP va HTTPS tu internet"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "ecommerce-lb-sg" }
}

# 6. Khai báo Application Load Balancer (ALB)
resource "aws_lb" "ecommerce_lb" {
  name               = "ecommerce-content-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]

  enable_deletion_protection = false

  tags = { Environment = "Project-Team" }
}

# 7. Khai báo Listener cổng 80 (Chuyển hướng hoặc định tuyến mặc định)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.ecommerce_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Trang chu (Default Home)"
      status_code  = "200"
    }
  }
}

# 8. Cấu hình Listener Rules định tuyến theo nội dung đường dẫn URL (/products/* và /checkout/*)
# Lưu ý: Các biến target_group_arn bên dưới sẽ liên kết với phần Target Groups do Thành viên 2 viết sau này.

resource "aws_lb_listener_rule" "products_rule" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 10

  action {
    type             = "forward"
    target_group_arn = "/* Sẽ điền ARN của Target Group sản phẩm từ Thành viên 2 */" 
  }

  condition {
    path_pattern {
      values = ["/products/*"]
    }
  }
}

resource "aws_lb_listener_rule" "checkout_rule" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 20

  action {
    type             = "forward"
    target_group_arn = "/* Sẽ điền ARN của Target Group thanh toán từ Thành viên 2 */"
  }

  condition {
    path_pattern {
      values = ["/checkout/*"]
    }
  }
}