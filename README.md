# 🛒 Đề tài: Cân bằng tải dựa trên nội dung HTTPS với Terraform (Web Bán Hàng)

Dự án nhóm triển khai kiến trúc Application Load Balancer (ALB) định tuyến lưu lượng theo đường dẫn URL (`/`, `/products/*`, `/checkout/*`) sử dụng Terraform và AWS, tích hợp cơ chế dự phòng Tính sẵn sàng cao (High Availability - HA), giả lập môi trường Cloud offline và kịch bản diễn tập sự cố (Chaos Testing / Đánh sập máy chủ).

---

## 👥 Phân công nhiệm vụ thành viên (Cập nhật mới)

### 1. Phạm Đinh Gia Bảo - Hạ tầng mạng lõi & Giả lập môi trường Cloud (Core Infra & Cloud Emulation)
* **Mục tiêu:** Dựng bộ khung hệ thống mạng và thiết lập môi trường giả lập Cloud offline (không tốn chi phí thuê AWS).
* **Nhiệm vụ:**
  - Quản lý kho chứa GitHub, tạo khung thư mục chung và cấu hình tương thích đa nền tảng (`.gitattributes` cho Windows và macOS).
  - Viết cấu hình mạng cơ bản (`VPC`, `Subnets`, `Security Groups` mở cổng 80/443) trong file `main.tf`.
  - Nghiên cứu và thiết lập giải pháp **Giả lập môi trường Cloud** (LocalStack / Docker / mạng cục bộ) để nhóm có thể chạy thử nghiệm `terraform apply` và kết nối nhiều máy tính cùng lúc mà không tốn chi phí thẻ tín dụng.

### 2. Ngô Khánh Hưng - Bảo mật HTTPS & Cơ chế Dự phòng HA (Security & High Availability)
* **Mục tiêu:** Đảm bảo an toàn thông tin với HTTPS và thiết kế cơ chế dự phòng Tính sẵn sàng cao (HA) khi Load Balancer gặp sự cố.
* **Nhiệm vụ:**
  - Viết code vào file `security.tf` cấu hình chứng chỉ `SSL/TLS` (RSA 2048-bit, AWS ACM / Self-signed) gắn vào cổng 443 của ALB, thiết lập quy tắc tự động chuyển hướng HTTP (301 Redirect) sang HTTPS.
  - Phụ trách nghiên cứu và triển khai giải pháp **Tính sẵn sàng cao (High Availability - HA)**: Cấu hình Load Balancer dự phòng (Secondary ALB) và cơ chế DNS Failover (Route 53) để khi Load Balancer chính bị lỗi thì hệ thống vẫn duy trì kết nối cho người dùng.
  - Tổng hợp số liệu, xuất sơ đồ kiến trúc hạ tầng mạng, soạn thảo Báo cáo Word và Slide thuyết trình.

### 3. Huỳnh Nhật Hòa - Cụm máy chủ Backend & Giả lập Tấn công / Đánh sập máy chủ (Target Groups & Chaos Testing)
* **Mục tiêu:** Tạo cụm máy chủ đích nhận lưu lượng và xây dựng kịch bản mô phỏng sự cố/tấn công đánh sập máy chủ để thử thách độ bền hệ thống.
* **Nhiệm vụ:**
  - Viết code vào file `targets.tf` để khai báo 3 `Target Groups` (`tg_frontend`, `tg_products`, `tg_checkout`) và cấu hình Health Check.
  - Viết script khởi tạo (User Data / Nginx) cho 3 máy chủ backend mẫu trả về nội dung phân biệt (*"Trang chủ"*, *"Trang sản phẩm"*, *"Trang thanh toán"*).
  - Xây dựng công cụ và kịch bản **Giả lập tấn công / Mô phỏng sự cố (Chaos Testing / Fault Injection)**: Trực tiếp thực hiện các tình huống đánh sập đột ngột máy chủ Sản phẩm hoặc máy chủ Thanh toán để kiểm tra xem Load Balancer có tự động cô lập máy lỗi (Unhealthy) và giữ cho các dịch vụ còn lại hoạt động bình thường hay không.

---

## 📂 Cấu trúc thư mục dự án
- `main.tf` — [Phạm Đinh Gia Bảo] Cấu hình VPC, Subnets, ALB, Listener Rules và môi trường Cloud.
- `targets.tf` — [Huỳnh Nhật Hòa] Cấu hình Target Groups, Health Checks và Backend EC2.
- `security.tf` — [Ngô Khánh Hưng] Cấu hình SSL/TLS, HTTPS Redirect và tính năng HA Failover.
- `variables.tf` — Khai báo các biến đầu vào dùng chung (region, CIDR, v.v.)
- `outputs.tf` — Xuất các thông tin đầu ra quan trọng (DNS của ALB, ARN, v.v.)
- `scripts/` — Chứa kịch bản User Data cài Nginx, công cụ chạy thử nghiệm (`run_local_demo.py`) và kịch bản mô phỏng sự cố đánh sập máy chủ.
- `certs/` — Chứng chỉ SSL/TLS tự ký chuẩn UTF-8 phục vụ kiểm thử HTTPS.
- `demo_pages/` — Mã nguồn giao diện HTML của 3 phân hệ thương mại điện tử.
