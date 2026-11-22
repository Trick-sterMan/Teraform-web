#!/usr/bin/env python3
import os
import re

# Tự động nhận diện thư mục gốc của project (hoạt động tốt trên cả Windows và macOS)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract_html(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"cat << 'EOF' > [^\n]+\n(<!DOCTYPE html>.*?)\nEOF", content, re.DOTALL)
    if match:
        return match.group(1)
    return ""

html_fe = extract_html(os.path.join(base_dir, "scripts", "user_data_frontend.sh"))
html_prod = extract_html(os.path.join(base_dir, "scripts", "user_data_products.sh"))
html_check = extract_html(os.path.join(base_dir, "scripts", "user_data_checkout.sh"))

# Đảm bảo các thư mục tồn tại
os.makedirs(os.path.join(base_dir, "demo_pages", "frontend"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "demo_pages", "products", "products"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "demo_pages", "checkout", "checkout"), exist_ok=True)

# Ghi file Frontend
with open(os.path.join(base_dir, "demo_pages", "frontend", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_fe)

# Ghi file Products (hỗ trợ cả /products và /products/)
with open(os.path.join(base_dir, "demo_pages", "products", "products", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_prod)
with open(os.path.join(base_dir, "demo_pages", "products", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_prod)

# Ghi file Checkout (hỗ trợ cả /checkout và /checkout/)
with open(os.path.join(base_dir, "demo_pages", "checkout", "checkout", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_check)
with open(os.path.join(base_dir, "demo_pages", "checkout", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_check)

print("Đã trích xuất các file demo HTML thành công!")
