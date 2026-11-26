# ==============================================================================
# HA.TF - PHAN HIGH AVAILABILITY (THANH VIEN PHAN HA)
# De tai: Can bang tai dua tren noi dung HTTPS voi Terraform
# Kien truc: Active-Passive failover - ALB chinh + ALB phu du phong
# ==============================================================================
# LUU Y QUAN TRONG:
#   File nay la BAN THIET KE AWS day du.
#   Tat ca resource AWS deu boc bang bien enable_aws_ha (mac dinh = false).
#   Moi truong demo local: dat enable_aws_ha = false (mac dinh) -> khong tao gi tren AWS,
#   khong loi khi chay terraform apply trong moi truong gia lap.
#   Khi deploy AWS that: doi enable_aws_ha = true trong terraform.tfvars.
#
#   De chay HA THAT su trong moi truong LOCAL, su dung:
#     python scripts/run_ha_local.py
# ==============================================================================

# ============================================================
# BIEN HA (khai bao ngay trong file nay, khong sua variables.tf)
# ============================================================

variable "enable_aws_ha" {
  description = "Bat/tat tao resource HA tren AWS that. Mac dinh false (moi truong local/gia lap)."
  type        = bool
  default     = false
}

variable "ha_domain_name" {
  description = "Ten mien chinh da co Hosted Zone tren Route 53 (chi dung khi enable_aws_ha = true)."
  type        = string
  default     = "example.internal"
}

variable "ha_subdomain" {
  description = "Ten subdomain cho endpoint HA public (chi dung khi enable_aws_ha = true)."
  type        = string
  default     = "app"
}

# ============================================================
# BUOC 1: EC2 DU PHONG (BACKUP SERVER)
# Dat o public_2 (ap-southeast-1b) - khac AZ voi frontend/products (public_1)
# Tai su dung backend_sg va lb_sg cua thanh vien 2 (targets.tf)
# ============================================================

resource "aws_instance" "backup_server" {
  count = var.enable_aws_ha ? 1 : 0

  ami                         = data.aws_ami.amazon_linux_2023.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public_2.id
  vpc_security_group_ids      = [aws_security_group.backend_sg.id]
  associate_public_ip_address = true

  # Script khoi tao: phuc vu du 3 duong dan /  /products/  /checkout/
  # va them header X-Served-By: backup de chung minh request den server nao
  user_data_base64 = filebase64("${path.module}/scripts/user_data_backup.sh")

  tags = {
    Name      = "ecommerce-backup-server"
    Role      = "Backup-HA"
    ManagedBy = "Terraform - HA Module"
    AZ        = "ap-southeast-1b"
  }
}

# ============================================================
# BUOC 2: TARGET GROUP DU PHONG (tg_backup)
# Health check / vi day la server tich hop ca 3 dich vu
# ============================================================

resource "aws_lb_target_group" "backup_tg" {
  count = var.enable_aws_ha ? 1 : 0

  name        = "tg-backup-ha"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "instance"

  health_check {
    enabled             = true
    path                = "/"
    protocol            = "HTTP"
    port                = "traffic-port"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200-399"
  }

  tags = {
    Name = "tg-backup-ha"
    Role = "HA-Backup"
  }
}

# Dang ky EC2 backup vao target group backup
resource "aws_lb_target_group_attachment" "backup_attachment" {
  count = var.enable_aws_ha ? 1 : 0

  target_group_arn = aws_lb_target_group.backup_tg[0].arn
  target_id        = aws_instance.backup_server[0].id
  port             = 80
}

# ============================================================
# BUOC 3: ALB PHU (BACKUP LOAD BALANCER)
# Dat o ca 2 subnet de dam bao Multi-AZ
# Su dung lai lb_sg cua thanh vien 1 (main.tf)
# ============================================================

resource "aws_lb" "backup_lb" {
  count = var.enable_aws_ha ? 1 : 0

  name               = "ecommerce-backup-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]

  enable_deletion_protection = false

  tags = {
    Name        = "ecommerce-backup-lb"
    Environment = "Project-Team"
    Role        = "HA-Backup-ALB"
  }
}

# Listener HTTP cong 80 cho ALB backup -> forward thang ve tg_backup
resource "aws_lb_listener" "backup_http" {
  count = var.enable_aws_ha ? 1 : 0

  load_balancer_arn = aws_lb.backup_lb[0].arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backup_tg[0].arn
  }
}

# ============================================================
# BUOC 4: ROUTE 53 HEALTH CHECK CHO ALB CHINH
# 3 health check HTTP don le (/, /products/, /checkout/)
# Gop thanh 1 CALCULATED health check (ca 3 khoe moi tinh la khoe)
# Dung HTTP cong 80 (chap nhan 2xx/3xx ke ca redirect 301 sang HTTPS)
# ============================================================

resource "aws_route53_health_check" "ha_primary_root" {
  count = var.enable_aws_ha ? 1 : 0

  fqdn              = aws_lb.ecommerce_lb.dns_name
  port              = 80
  type              = "HTTP"
  resource_path     = "/"
  request_interval  = 10
  failure_threshold = 2

  tags = {
    Name = "ha-healthcheck-primary-root"
  }
}

resource "aws_route53_health_check" "ha_primary_products" {
  count = var.enable_aws_ha ? 1 : 0

  fqdn              = aws_lb.ecommerce_lb.dns_name
  port              = 80
  type              = "HTTP"
  resource_path     = "/products/"
  request_interval  = 10
  failure_threshold = 2

  tags = {
    Name = "ha-healthcheck-primary-products"
  }
}

resource "aws_route53_health_check" "ha_primary_checkout" {
  count = var.enable_aws_ha ? 1 : 0

  fqdn              = aws_lb.ecommerce_lb.dns_name
  port              = 80
  type              = "HTTP"
  resource_path     = "/checkout/"
  request_interval  = 10
  failure_threshold = 2

  tags = {
    Name = "ha-healthcheck-primary-checkout"
  }
}

# Health check CALCULATED: ca 3 endpoint khoe -> ALB chinh moi khoe
# child_health_threshold = 3: can du 3/3 child khoe
resource "aws_route53_health_check" "ha_primary_calculated" {
  count = var.enable_aws_ha ? 1 : 0

  type                   = "CALCULATED"
  child_health_threshold = 3

  child_healthchecks = [
    aws_route53_health_check.ha_primary_root[0].id,
    aws_route53_health_check.ha_primary_products[0].id,
    aws_route53_health_check.ha_primary_checkout[0].id,
  ]

  tags = {
    Name = "ha-healthcheck-primary-calculated"
  }
}

# ============================================================
# BUOC 5: ROUTE 53 FAILOVER RECORDS
# app.<domain>  CNAME  TTL 30s
# PRIMARY  -> DNS cua ALB chinh (aws_lb.ecommerce_lb)
# SECONDARY -> DNS cua ALB backup (backup_lb) - len khi primary sap
# Can co Hosted Zone san co (nhap qua bien ha_domain_name)
# ============================================================

data "aws_route53_zone" "ha_zone" {
  count        = var.enable_aws_ha ? 1 : 0
  name         = var.ha_domain_name
  private_zone = false
}

# Ban ghi PRIMARY: tro vao ALB chinh, gan health check CALCULATED
resource "aws_route53_record" "ha_primary" {
  count = var.enable_aws_ha ? 1 : 0

  zone_id = data.aws_route53_zone.ha_zone[0].zone_id
  name    = "${var.ha_subdomain}.${var.ha_domain_name}"
  type    = "CNAME"
  ttl     = 30

  records = [aws_lb.ecommerce_lb.dns_name]

  set_identifier = "primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  health_check_id = aws_route53_health_check.ha_primary_calculated[0].id
}

# Ban ghi SECONDARY: tro vao ALB backup, khong can health check
resource "aws_route53_record" "ha_secondary" {
  count = var.enable_aws_ha ? 1 : 0

  zone_id = data.aws_route53_zone.ha_zone[0].zone_id
  name    = "${var.ha_subdomain}.${var.ha_domain_name}"
  type    = "CNAME"
  ttl     = 30

  records = [aws_lb.backup_lb[0].dns_name]

  set_identifier = "secondary"

  failover_routing_policy {
    type = "SECONDARY"
  }
}

# ============================================================
# BUOC 6: OUTPUTS
# ============================================================

output "ha_primary_url" {
  description = "URL cua ALB CHINH (PRIMARY) trong kien truc HA"
  value = {
    http  = "http://${aws_lb.ecommerce_lb.dns_name}/"
    https = "https://${aws_lb.ecommerce_lb.dns_name}/"
  }
}

output "ha_backup_url" {
  description = "URL cua ALB DU PHONG (SECONDARY) trong kien truc HA"
  value = var.enable_aws_ha ? {
    http = "http://${aws_lb.backup_lb[0].dns_name}/"
  } : { note = "enable_aws_ha = false - chay local HA bang: python scripts/run_ha_local.py" }
}

output "ha_public_url" {
  description = "URL cong khai (Route 53 CNAME failover) - chi kha dung khi enable_aws_ha = true"
  value       = var.enable_aws_ha ? "https://${var.ha_subdomain}.${var.ha_domain_name}/" : "Khong kha dung o moi truong local - Dung https://localhost:7443/ sau khi chay run_ha_local.py"
}

output "ha_architecture_note" {
  description = "Mo ta kien truc HA dang chay"
  value       = var.enable_aws_ha ? "AWS Active-Passive: Route53 CNAME Failover -> ALB chinh (8443) + ALB du phong (backup_lb)" : "LOCAL Active-Passive: HAProxy Python (cong 7443) -> ALB chinh (8443) + ALB backup (9443). Chay: python scripts/run_ha_local.py"
}
