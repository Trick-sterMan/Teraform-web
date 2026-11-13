#!/usr/bin/env python3
import os
import re

base_dir = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web"

def extract_html(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"cat << 'EOF' > [^\n]+\n(<!DOCTYPE html>.*?)\nEOF", content, re.DOTALL)
    if match:
        return match.group(1)
    return ""

html_fe = extract_html(f"{base_dir}/scripts/user_data_frontend.sh")
html_prod = extract_html(f"{base_dir}/scripts/user_data_products.sh")
html_check = extract_html(f"{base_dir}/scripts/user_data_checkout.sh")

# Write Frontend
with open(f"{base_dir}/demo_pages/frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html_fe)

# Write Products
with open(f"{base_dir}/demo_pages/products/products/index.html", "w", encoding="utf-8") as f:
    f.write(html_prod)
with open(f"{base_dir}/demo_pages/products/index.html", "w", encoding="utf-8") as f:
    f.write(html_prod)

# Write Checkout
with open(f"{base_dir}/demo_pages/checkout/checkout/index.html", "w", encoding="utf-8") as f:
    f.write(html_check)
with open(f"{base_dir}/demo_pages/checkout/index.html", "w", encoding="utf-8") as f:
    f.write(html_check)

print("Generated HTML demo files successfully!")
