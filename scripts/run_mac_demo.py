#!/usr/bin/env python3
"""
Mô phỏng hoàn chỉnh hệ thống AWS Application Load Balancer & 3 Target Groups trên Mac:
- Port 8080: Giả lập AWS Application Load Balancer (ALB) định tuyến dựa trên Path:
    * Đường dẫn mặc định (/)        -> Phục vụ từ Target Group Frontend
    * Đường dẫn (/products/*)       -> Phục vụ từ Target Group Products
    * Đường dẫn (/checkout/*)       -> Phục vụ từ Target Group Checkout
- Port 8081: Máy chủ Frontend Server trực tiếp
- Port 8082: Máy chủ Products Server trực tiếp
- Port 8083: Máy chủ Checkout Server trực tiếp
"""

import http.server
import socketserver
import threading
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO_DIR = os.path.join(BASE_DIR, "demo_pages")

def create_directory_handler(directory):
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
        def log_message(self, format, *args):
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
        print(f"Error starting port {port}: {e}")

class ALBRouterHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def translate_path(self, path):
        # Mô phỏng chính xác thuật toán định tuyến ALB của AWS:
        # 1. Rule 1: /products/* -> Thư mục products
        if path.startswith("/products"):
            rel_path = path.lstrip("/")
            full_path = os.path.join(DEMO_DIR, "products", rel_path)
            if os.path.isdir(full_path):
                full_path = os.path.join(full_path, "index.html")
            return full_path

        # 2. Rule 2: /checkout/* -> Thư mục checkout
        elif path.startswith("/checkout"):
            rel_path = path.lstrip("/")
            full_path = os.path.join(DEMO_DIR, "checkout", rel_path)
            if os.path.isdir(full_path):
                full_path = os.path.join(full_path, "index.html")
            return full_path

        # 3. Default Rule: / -> Thư mục frontend
        else:
            rel_path = path.lstrip("/")
            full_path = os.path.join(DEMO_DIR, "frontend", rel_path)
            if os.path.isdir(full_path):
                full_path = os.path.join(full_path, "index.html")
            return full_path

    def end_headers(self):
        if self.path.startswith("/products"):
            self.send_header("X-ALB-Rule", "Priority 10: /products/* -> tg_products")
        elif self.path.startswith("/checkout"):
            self.send_header("X-ALB-Rule", "Priority 20: /checkout/* -> tg_checkout")
        else:
            self.send_header("X-ALB-Rule", "Default: / -> tg_frontend")
        super().end_headers()

def run_alb_simulator(port=8080):
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("0.0.0.0", port), ALBRouterHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting port {port}: {e}")

if __name__ == "__main__":
    print("=" * 65)
    print("🚀 ĐANG CHẠY GIẢ LẬP ALB & 3 TARGET GROUPS TRÊN MAC")
    print("=" * 65)

    t_fe = threading.Thread(target=run_target_server, args=(8081, "frontend"), daemon=True)
    t_prod = threading.Thread(target=run_target_server, args=(8082, "products"), daemon=True)
    t_check = threading.Thread(target=run_target_server, args=(8083, "checkout"), daemon=True)
    t_alb = threading.Thread(target=run_alb_simulator, args=(8080,), daemon=True)

    t_fe.start()
    t_prod.start()
    t_check.start()
    t_alb.start()

    print("✅ [Cổng 8081] Backend 1: Target Group Frontend (Trang chủ)")
    print("✅ [Cổng 8082] Backend 2: Target Group Products (Trang sản phẩm)")
    print("✅ [Cổng 8083] Backend 3: Target Group Checkout (Trang thanh toán)")
    print("-" * 65)
    print("🌟 [Cổng 8080] BỘ CÂN BẰNG TẢI (ALB Simulator):")
    print("   👉 http://localhost:8080/")
    print("=" * 65)

    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng hệ thống.")
        sys.exit(0)
