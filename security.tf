# ==============================================================================
# PHAN CUA THANH VIEN 3: NGO KHANH HUNG
# Muc tieu: Bao mat HTTPS - Cau hinh chung chi SSL/TLS va Listener cong 443
# ==============================================================================
# Chien luoc: Dung AWS ACM voi Self-Signed Certificate (khong can domain that)
# - Tao private key va self-signed cert bang TLS provider
# - Import vao AWS ACM
# - Gan vao HTTPS Listener cong 443 cua ALB
# - Cau hinh redirect HTTP -> HTTPS tren Listener cong 80
# ==============================================================================

# ==============================================================================
# BUOC 1: TAO SELF-SIGNED TLS CERTIFICATE (khong can mua domain that)
# ==============================================================================
# LUU Y: Provider "tls" can duoc them vao block required_providers trong main.tf
# Xem huong dan ben duoi.
# ==============================================================================

# 1a. Tao RSA Private Key 2048-bit
resource "tls_private_key" "self_signed" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

# 1b. Tao Self-Signed Certificate tu private key tren
resource "tls_self_signed_cert" "ecommerce" {
  private_key_pem = tls_private_key.self_signed.private_key_pem

  # Thong tin chu the (Subject) cua chung chi
  subject {
    common_name         = "ecommerce-alb.internal"
    organization        = "Nhom Do An Terraform"
    organizational_unit = "Security & DevOps"
    country             = "VN"
    province            = "Ho Chi Minh"
    locality            = "Ho Chi Minh City"
  }

  # Chung chi co hieu luc 1 nam (8760 gio)
  validity_period_hours = 8760

  # Cac quyen su dung ma chung chi nay cho phep
  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "server_auth",
  ]
}

# ==============================================================================
# BUOC 2: IMPORT CERTIFICATE VAO AWS CERTIFICATE MANAGER (ACM)
# ==============================================================================

resource "aws_acm_certificate" "ecommerce_cert" {
  private_key      = tls_private_key.self_signed.private_key_pem
  certificate_body = tls_self_signed_cert.ecommerce.cert_pem

  tags = {
    Name        = "ecommerce-self-signed-cert"
    Environment = "Project-Team"
    ManagedBy   = "Terraform - Thanh vien 3: Ngo Khanh Hung"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# ==============================================================================
# BUOC 3: TAO HTTPS LISTENER CONG 443 (CHINH) - Gan chung chi SSL/TLS
# ==============================================================================

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.ecommerce_lb.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.ecommerce_cert.arn

  # Mac dinh: Chuyen ve trang Frontend neu khong khop rule nao
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg_frontend.arn
  }
}

# ==============================================================================
# BUOC 4: CAU HINH LISTENER RULES CHO CONG 443 (HTTPS)
# Sao chep cac quy tac dinh tuyen tuong tu HTTP nhung ap dung cho HTTPS
# ==============================================================================

# Rule 1: /products/* -> Target Group Products
resource "aws_lb_listener_rule" "https_products_rule" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 10

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg_products.arn
  }

  condition {
    path_pattern {
      values = ["/products/*"]
    }
  }
}

# Rule 2: /checkout/* -> Target Group Checkout
resource "aws_lb_listener_rule" "https_checkout_rule" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 20

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg_checkout.arn
  }

  condition {
    path_pattern {
      values = ["/checkout/*"]
    }
  }
}

# ==============================================================================
# BUOC 5: CAU HINH REDIRECT HTTP -> HTTPS TREN CONG 80
# Thay the default_action "forward" trong main.tf bang "redirect"
# ==============================================================================

resource "aws_lb_listener_rule" "http_to_https_redirect" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 1

  action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
}

# ==============================================================================
# BUOC 6: CAP NHAT SECURITY GROUP - Dam bao cong 443 da mo (tham khao main.tf)
# Security Group lb_sg trong main.tf da mo san cong 443, phan nay bo sung
# Security Group rieng cho HTTPS de quan ly ro rang hon
# ==============================================================================

resource "aws_security_group_rule" "alb_https_ingress" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.lb_sg.id
  description       = "Allow HTTPS inbound - Thanh vien 3 confirm"
}
