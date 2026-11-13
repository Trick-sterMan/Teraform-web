# ==============================================================================
# PHẦN CỦA THÀNH VIÊN 2: HUỲNH NHẬT HÒA
# Mục tiêu: Tạo nơi nhận lưu lượng từ Load Balancer và dựng 3 trang web mẫu.
# - Khai báo 3 Target Groups (tg_frontend, tg_products, tg_checkout) & Health Check
# - Khai báo Security Group cho máy chủ Backend EC2
# - Khởi tạo 3 máy chủ ảo EC2 với script Nginx (User Data) cho 3 dịch vụ
# - Đăng ký (Attach) các máy chủ ảo vào Target Group tương ứng
# ==============================================================================

# 1. Tìm AMI Amazon Linux 2023 mới nhất tại Region hiện tại
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# 2. Tạo Security Group cho các máy chủ Backend EC2
# Chỉ nhận lưu lượng cổng 80 từ Security Group của Load Balancer để đảm bảo bảo mật
resource "aws_security_group" "backend_sg" {
  name        = "ecommerce-backend-sg"
  description = "Cho phep truy cap HTTP tu Load Balancer toi cac may chu backend"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.lb_sg.id]
  }

  egress {
    description = "Allow all outbound traffic (tai goi cai dat, update nginx)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ecommerce-backend-sg"
  }
}

# ==============================================================================
# 3. Khai báo 3 Target Groups và cấu hình Health Check
# ==============================================================================

# Target Group 1: Frontend (Trang chủ)
resource "aws_lb_target_group" "tg_frontend" {
  name        = "tg-frontend"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "instance"

  health_check {
    enabled             = true
    path                = "/"
    protocol            = "HTTP"
    port                = "traffic-port"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200"
  }

  tags = {
    Name = "tg-frontend"
    Role = "Frontend"
  }
}

# Target Group 2: Products (Trang sản phẩm - /products/*)
resource "aws_lb_target_group" "tg_products" {
  name        = "tg-products"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "instance"

  health_check {
    enabled             = true
    path                = "/products/"
    protocol            = "HTTP"
    port                = "traffic-port"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200"
  }

  tags = {
    Name = "tg-products"
    Role = "Products"
  }
}

# Target Group 3: Checkout (Trang thanh toán - /checkout/*)
resource "aws_lb_target_group" "tg_checkout" {
  name        = "tg-checkout"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "instance"

  health_check {
    enabled             = true
    path                = "/checkout/"
    protocol            = "HTTP"
    port                = "traffic-port"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200"
  }

  tags = {
    Name = "tg-checkout"
    Role = "Checkout"
  }
}

# ==============================================================================
# 4. Khởi tạo 3 máy chủ ảo EC2 mẫu (Backend Servers) với User Data Nginx
# ==============================================================================

# Máy chủ 1: Frontend Server
resource "aws_instance" "frontend" {
  ami                         = data.aws_ami.amazon_linux_2023.id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public_1.id
  vpc_security_group_ids      = [aws_security_group.backend_sg.id]
  associate_public_ip_address = true
  user_data                   = file("${path.module}/scripts/user_data_frontend.sh")

  tags = {
    Name = "ecommerce-frontend-server"
    Role = "Frontend"
  }
}

# Máy chủ 2: Products Server
resource "aws_instance" "products" {
  ami                         = data.aws_ami.amazon_linux_2023.id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public_1.id
  vpc_security_group_ids      = [aws_security_group.backend_sg.id]
  associate_public_ip_address = true
  user_data                   = file("${path.module}/scripts/user_data_products.sh")

  tags = {
    Name = "ecommerce-products-server"
    Role = "Products"
  }
}

# Máy chủ 3: Checkout Server (Đặt ở Subnet 2 để đạt tính sẵn sàng cao - Multi-AZ)
resource "aws_instance" "checkout" {
  ami                         = data.aws_ami.amazon_linux_2023.id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public_2.id
  vpc_security_group_ids      = [aws_security_group.backend_sg.id]
  associate_public_ip_address = true
  user_data                   = file("${path.module}/scripts/user_data_checkout.sh")

  tags = {
    Name = "ecommerce-checkout-server"
    Role = "Checkout"
  }
}

# ==============================================================================
# 5. Đăng ký các máy chủ EC2 vào từng Target Group tương ứng
# ==============================================================================

resource "aws_lb_target_group_attachment" "frontend" {
  target_group_arn = aws_lb_target_group.tg_frontend.arn
  target_id        = aws_instance.frontend.id
  port             = 80
}

resource "aws_lb_target_group_attachment" "products" {
  target_group_arn = aws_lb_target_group.tg_products.arn
  target_id        = aws_instance.products.id
  port             = 80
}

resource "aws_lb_target_group_attachment" "checkout" {
  target_group_arn = aws_lb_target_group.tg_checkout.arn
  target_id        = aws_instance.checkout.id
  port             = 80
}
