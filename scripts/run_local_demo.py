#!/usr/bin/env python3
"""
==============================================================================
HỆ THỐNG MÔ PHỎNG AWS APPLICATION LOAD BALANCER & BACKEND CỤC BỘ (WINDOWS & MAC)
ĐỀ TÀI: CÂN BẰNG TẢI DỰA TRÊN NỘI DUNG HTTPS VỚI TERRAFORM
==============================================================================
Chạy thử nghiệm 100% trên máy tính cá nhân - KHÔNG CẦN TÀI KHOẢN AWS / KHÔNG CẦN VISA:
- Cổng 8080 (HTTP):
    * Mô phỏng Listener cổng 80: Tự động chuyển hướng (Redirect 301) sang HTTPS cổng 8443.
- Cổng 8443 (HTTPS - SSL/TLS):
    * Mô phỏng Application Load Balancer (ALB) định tuyến dựa trên Path qua giao thức HTTPS:
      + /                    -> Phục vụ từ Target Group 1 (Frontend - Trang chủ)
      + /products, /products/* -> Phục vụ từ Target Group 2 (Products - Sản phẩm)
      + /checkout, /checkout/* -> Phục vụ từ Target Group 3 (Checkout - Thanh toán)
- Cổng 8081: Máy chủ ảo EC2 Backend 1 (Frontend Server)
- Cổng 8082: Máy chủ ảo EC2 Backend 2 (Products Server)
- Cổng 8083: Máy chủ ảo EC2 Backend 3 (Checkout Server)
==============================================================================
"""

import http.server
import socketserver
import threading
import ssl
import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO_DIR = os.path.join(BASE_DIR, "demo_pages")
CERTS_DIR = os.path.join(BASE_DIR, "certs")

# 1. Đảm bảo các file HTML demo đã được tạo
frontend_html = os.path.join(DEMO_DIR, "frontend", "index.html")
if not os.path.exists(frontend_html):
    print("⏳ Thư mục demo_pages chưa có file HTML, đang tự động trích xuất...")
    extract_script = os.path.join(BASE_DIR, "scripts", "extract_demo_html.py")
    subprocess.run([sys.executable, extract_script], check=True)

# 2. Xử lý backend cho từng Target Group (Tắt log thừa và xử lý ngắt kết nối trình duyệt mượt mà)
def create_directory_handler(directory):
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
        def log_message(self, format, *args):
            pass
        def handle_one_request(self):
            try:
                super().handle_one_request()
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                pass
    return CustomHandler

def run_target_server(port, folder_name):
    folder_path = os.path.join(DEMO_DIR, folder_name)
    handler = create_directory_handler(folder_path)
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"Lỗi khởi chạy backend cổng {port}: {e}")

# 3. Router ALB định tuyến theo Path trên cổng HTTPS (Cổng 8443)
class ALBRouterHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def translate_path(self, path):
        # Rule 1: /products và /products/* -> Target Group Products
        if path == "/products" or path.startswith("/products/"):
            rel_path = path.lstrip("/")
            full_path = os.path.join(DEMO_DIR, "products", rel_path)
            if os.path.isdir(full_path):
                full_path = os.path.join(full_path, "index.html")
            return full_path

        # Rule 2: /checkout và /checkout/* -> Target Group Checkout
        elif path == "/checkout" or path.startswith("/checkout/"):
            rel_path = path.lstrip("/")
            full_path = os.path.join(DEMO_DIR, "checkout", rel_path)
            if os.path.isdir(full_path):
                full_path = os.path.join(full_path, "index.html")
            return full_path

        # Default Rule: / -> Target Group Frontend
        else:
            rel_path = path.lstrip("/")
            full_path = os.path.join(DEMO_DIR, "frontend", rel_path)
            if os.path.isdir(full_path):
                full_path = os.path.join(full_path, "index.html")
            return full_path

    def end_headers(self):
        if self.path == "/products" or self.path.startswith("/products/"):
            self.send_header("X-ALB-Rule", "Priority 10: /products/* -> tg_products")
        elif self.path == "/checkout" or self.path.startswith("/checkout/"):
            self.send_header("X-ALB-Rule", "Priority 20: /checkout/* -> tg_checkout")
        else:
            self.send_header("X-ALB-Rule", "Default: / -> tg_frontend")
        self.send_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        super().end_headers()

def run_https_alb(port=8443):
    cert_path = os.path.join(CERTS_DIR, "cert.pem")
    key_path = os.path.join(CERTS_DIR, "key.pem")

    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("0.0.0.0", port), ALBRouterHandler)
        if os.path.exists(cert_path) and os.path.exists(key_path):
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=cert_path, keyfile=key_path)
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            print(f"🔒 [Cổng {port}] HTTPS ALB Listener đã sẵn sàng (Gắn chứng chỉ SSL TLS)!")
        else:
            print("⚠️ Không tìm thấy cert.pem / key.pem trong certs/")
        httpd.serve_forever()
    except Exception as e:
        print(f"❌ Lỗi khởi chạy HTTPS ALB Simulator cổng {port}: {e}")

# 4. Listener HTTP cổng 8080: Redirect 301 sang HTTPS 8443
class HTTPRedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        target_url = f"https://localhost:8443{self.path}"
        self.send_response(301)
        self.send_header("Location", target_url)
        self.send_header("X-ALB-Redirect", "HTTP-to-HTTPS-Redirect-Rule")
        self.end_headers()
        try:
            self.wfile.write(f"Redirecting to {target_url}".encode("utf-8"))
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def do_HEAD(self):
        self.do_GET()

    def log_message(self, format, *args):
        pass

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

def run_http_redirect(port=8080):
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("0.0.0.0", port), HTTPRedirectHandler) as httpd:
            print(f"🔄 [Cổng {port}] HTTP Redirect Listener đã sẵn sàng (Redirect 301 -> HTTPS)!")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Lỗi khởi chạy HTTP Redirect Listener cổng {port}: {e}")

if __name__ == "__main__":
    print("=" * 75)
    print("🛒 CLOUDMART - MÔ PHỎNG AWS APPLICATION LOAD BALANCER & HTTPS ROUTING")
    print("=" * 75)

    # Khởi động 3 máy chủ backend
    t_fe = threading.Thread(target=run_target_server, args=(8081, "frontend"), daemon=True)
    t_prod = threading.Thread(target=run_target_server, args=(8082, "products"), daemon=True)
    t_check = threading.Thread(target=run_target_server, args=(8083, "checkout"), daemon=True)
    t_fe.start()
    t_prod.start()
    t_check.start()

    # Khởi động Listener HTTPS & HTTP Redirect
    t_https = threading.Thread(target=run_https_alb, args=(8443,), daemon=True)
    t_http = threading.Thread(target=run_http_redirect, args=(8080,), daemon=True)
    t_https.start()
    t_http.start()

    print("✅ [Cổng 8081] Backend EC2 1: Target Group Frontend (Trang chủ)")
    print("✅ [Cổng 8082] Backend EC2 2: Target Group Products (Trang sản phẩm)")
    print("✅ [Cổng 8083] Backend EC2 3: Target Group Checkout (Trang thanh toán)")
    print("-" * 75)
    print("🔒 [Cổng 8443] BỘ CÂN BẰNG TẢI CHÍNH - HTTPS APPLICATION LOAD BALANCER:")
    print("   👉 Trang chủ:       https://localhost:8443/")
    print("   👉 Trang sản phẩm:   https://localhost:8443/products/")
    print("   👉 Trang thanh toán: https://localhost:8443/checkout/")
    print("-" * 75)
    print("🔄 [Cổng 8080] LISTENER HTTP CHUYỂN HƯỚNG TỰ ĐỘNG (HTTP 301 -> HTTPS):")
    print("   👉 Thử truy cập:    http://localhost:8080/ -> Tự động chuyển sang HTTPS 8443")
    print("=" * 75)
    print("💡 HƯỚNG DẪN TRÊN TRÌNH DUYỆT:")
    print("   1. Nhớ giữ nguyên cửa sổ Terminal này ĐANG CHẠY (không tắt đi).")
    print("   2. Khi truy cập https://localhost:8443/ nếu thấy 'Kết nối không an toàn':")
    print("      Bấm 'Nâng cao' (Advanced) -> Chọn 'Tiếp tục truy cập localhost (không an toàn)'.")
    print("=" * 75)
    print("Nhấn tổ hợp phím Ctrl + C để dừng mô phỏng.")

    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng hệ thống mô phỏng.")
        sys.exit(0)
