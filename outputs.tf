# ==============================================================================
# CÁC GIÁ TRỊ OUTPUTS CỦA DỰ ÁN
# ==============================================================================

# 1. DNS của Application Load Balancer để truy cập từ trình duyệt
output "alb_dns_name" {
  description = "Địa chỉ DNS công khai của Application Load Balancer"
  value       = aws_lb.ecommerce_lb.dns_name
}

# 2. Các liên kết kiểm tra demo hệ thống
output "demo_urls" {
  description = "Các đường dẫn URL dùng để kiểm tra 3 dịch vụ"
  value = {
    home_page     = "http://${aws_lb.ecommerce_lb.dns_name}/"
    products_page = "http://${aws_lb.ecommerce_lb.dns_name}/products/"
    checkout_page = "http://${aws_lb.ecommerce_lb.dns_name}/checkout/"
  }
}

# 3. Thông tin Target Groups
output "target_groups" {
  description = "ARN và tên của 3 Target Groups"
  value = {
    tg_frontend = {
      name = aws_lb_target_group.tg_frontend.name
      arn  = aws_lb_target_group.tg_frontend.arn
    }
    tg_products = {
      name = aws_lb_target_group.tg_products.name
      arn  = aws_lb_target_group.tg_products.arn
    }
    tg_checkout = {
      name = aws_lb_target_group.tg_checkout.name
      arn  = aws_lb_target_group.tg_checkout.arn
    }
  }
}

# 4. Địa chỉ IP của các máy chủ ảo EC2 backend (để kiểm tra trực tiếp nếu cần)
output "backend_instances" {
  description = "IP công khai và nội bộ của các máy chủ Backend"
  value = {
    frontend = {
      id         = aws_instance.frontend.id
      public_ip  = aws_instance.frontend.public_ip
      private_ip = aws_instance.frontend.private_ip
    }
    products = {
      id         = aws_instance.products.id
      public_ip  = aws_instance.products.public_ip
      private_ip = aws_instance.products.private_ip
    }
    checkout = {
      id         = aws_instance.checkout.id
      public_ip  = aws_instance.checkout.public_ip
      private_ip = aws_instance.checkout.private_ip
    }
  }
}
