# 🛒 Đề tài: Cân bằng tải dựa trên nội dung HTTPS với Terraform (Web Bán Hàng)

Dự án nhóm triển khai kiến trúc Application Load Balancer (ALB) định tuyến lưu lượng theo đường dẫn URL (`/`, `/products/*`, `/checkout/*`) sử dụng Terraform và AWS.

---

## 👥 Phân công nhiệm vụ thành viên

### 1. Phạm Đinh Gia Bảo - Hạ tầng lõi & Định tuyến (Core Infra & Routing)
* **Mục tiêu:** Dựng bộ khung của hệ thống mạng và bộ cân bằng tải chính.
* **Nhiệm vụ:**
  - Quản lý kho chứa GitHub, tạo khung thư mục chung.
  - Viết cấu hình mạng cơ bản (`VPC`, `Subnets`, `Security Groups` mở cổng 80/443) trong file `main.tf`.
  - Khai báo `Application Load Balancer (ALB)` và các `Listener Rules` định tuyến đường dẫn (`/products/*`, `/checkout/*`, `/`).

### 2. Huỳnh Nhật Hòa- Máy chủ đích & Giả lập Backend (Target Groups & Web Demo)
* **Mục tiêu:** Tạo nơi nhận lưu lượng từ Load Balancer và dựng 3 trang web mẫu chứng minh hệ thống chạy đúng.
* **Nhiệm vụ:**
  - Viết code vào file `targets.tf` để khai báo 3 `Target Groups` (`tg_frontend`, `tg_products`, `tg_checkout`) và cấu hình Health Check.
  - Sử dụng Terminal trên Mac viết script khởi tạo (User Data / Nginx) cho máy chủ ảo/container mẫu trả về nội dung phân biệt (*"Trang chủ"*, *"Trang sản phẩm"*, *"Trang thanh toán"*).

### 3. Ngô Khánh Hưng - Bảo mật HTTPS, Tài liệu & Thuyết trình (Security & Docs)
* **Mục tiêu:** Đảm bảo yêu cầu bảo mật HTTPS và hoàn thiện báo cáo đồ án.
* **Nhiệm vụ:**
  - Viết code vào file `security.tf` cấu hình chứng chỉ `SSL/TLS` (AWS ACM hoặc Self-signed) gắn vào cổng 443 của ALB.
  - Chạy thử nghiệm hệ thống, chụp ảnh màn hình (`terraform plan`, `terraform apply`) và kết quả trình duyệt.
  - Vẽ sơ đồ kiến trúc, soạn báo cáo Word và slide thuyết trình.

---

## 📂 Cấu trúc thư mục dự án (Chia file tránh xung đột Git)
- `main.tf` — [Phạm Đinh Gia Bảo] Cấu hình VPC, Subnets, ALB, Listener Rules.
- `targets.tf` — [Huỳnh Nhật Hòa] Cấu hình Target Groups và Backend.
- `security.tf` — [Ngô Khánh Hưng] Cấu hình SSL/TLS và Security Groups.
- `variables.tf` — Khai báo các biến đầu vào dùng chung (region, CIDR, v.v.)
- `outputs.tf` — Xuất các thông tin đầu ra quan trọng (DNS của ALB, ARN, v.v.)
