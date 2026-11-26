#!/usr/bin/env python3
"""
==============================================================================
CÔNG CỤ GIẢ LẬP TẤN CÔNG & MÔ PHỎNG SỰ CỐ ĐÁNH SẬP MÁY CHỦ (CHAOS TESTING)
Người phụ trách: Huỳnh Nhật Hòa
Đề tài: Cân bằng tải dựa trên nội dung HTTPS với Terraform
==============================================================================
Chức năng chính:
1. Kiểm tra trạng thái sức khỏe (Health Check) của toàn bộ hệ thống (ALB & 3 Backend).
2. Giả lập gửi lượng truy cập lớn (Stress Test / HTTP Flood) vào hệ thống.
3. Kiểm thử kịch bản cách ly lỗi khi một dịch vụ backend gặp sự cố.
==============================================================================
"""

import urllib.request
import ssl
import time
import sys
import argparse

# Bỏ qua xác thực SSL Self-signed khi kiểm thử nội bộ
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

SERVICES = {
    "ALB HTTPS (Chính)": "https://localhost:8443/",
    "ALB HTTP (Redirect)": "http://localhost:8080/",
    "Backend 1 (Frontend)": "http://localhost:8081/",
    "Backend 2 (Products)": "http://localhost:8082/",
    "Backend 3 (Checkout)": "http://localhost:8083/",
}

def check_health():
    print("=" * 70)
    print("🔍 [HEALTH CHECK] ĐANG KIỂM TRA TÌNH TRẠNG CÁC MÁY CHỦ VÀ LOAD BALANCER...")
    print("=" * 70)
    for name, url in SERVICES.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ChaosTester/1.0"})
            start_time = time.time()
            with urllib.request.urlopen(req, context=ctx, timeout=2) as resp:
                latency = round((time.time() - start_time) * 1000, 2)
                print(f"✅ {name:<25} | Mã: {resp.status} OK | Độ trễ: {latency:>6} ms")
        except urllib.error.HTTPError as e:
            print(f"🔄 {name:<25} | Mã: {e.code} (Chuyển hướng / Lỗi HTTP)")
        except Exception as e:
            print(f"❌ {name:<25} | MẤT KẾT NỐI (Đã sập / Offline)")
    print("=" * 70)

def simulate_stress_test(target_url, count=50):
    print("=" * 70)
    print(f"⚡ [STRESS TEST] ĐANG GIẢ LẬP TẤN CÔNG LƯU LƯỢNG CAO ({count} REQUESTS)...")
    print(f"🎯 Mục tiêu: {target_url}")
    print("=" * 70)
    
    success = 0
    failed = 0
    total_time = 0

    for i in range(1, count + 1):
        try:
            start_time = time.time()
            req = urllib.request.Request(target_url, headers={"User-Agent": f"StressBot/{i}"})
            with urllib.request.urlopen(req, context=ctx, timeout=2) as resp:
                elapsed = (time.time() - start_time) * 1000
                total_time += elapsed
                success += 1
                if i % 10 == 0:
                    print(f"   👉 Đã gửi {i}/{count} requests - Trạng thái: {resp.status} OK")
        except Exception:
            failed += 1

    avg_time = round(total_time / success, 2) if success > 0 else 0
    print("-" * 70)
    print(f"📊 KẾT QUẢ DIỄN TẬP TẢI:")
    print(f"   - Thành công: {success}/{count} ({round(success/count*100, 1)}%)")
    print(f"   - Thất bại:   {failed}/{count}")
    print(f"   - Độ trễ phản hồi trung bình: {avg_time} ms")
    if failed == 0:
        print("🏆 KẾT LUẬN: Bộ cân bằng tải ALB hoạt động cực kỳ ổn định, chịu tải xuất sắc!")
    print("=" * 70)

def simulate_incident_report():
    print("=" * 70)
    print("🚨 [KỊCH BẢN SỰ CỐ] MÔ PHỎNG MÁY CHỦ SẢN PHẨM BỊ TẤN CÔNG / SẬP BẤT NGỜ")
    print("=" * 70)
    print("1. Tình huống: Ngày săn sale, lượt xem sản phẩm tăng đột biến làm nghẽn máy chủ Products.")
    print("2. Tác động tới kiến trúc Cân bằng tải nội dung:")
    print("   👉 Trang sản phẩm (/products/): Bị gián đoạn hoặc báo bảo trì.")
    print("   👉 Trang chủ (/)               : VẪN HOẠT ĐỘNG BÌNH THƯỜNG (Cụm Frontend độc lập).")
    print("   👉 Trang thanh toán (/checkout/): VẪN HOẠT ĐỘNG BÌNH THƯỜNG (Cụm Checkout độc lập).")
    print("-" * 70)
    print("💡 BẢO VỆ DOANH THU: Khách hàng đã chọn món vào giỏ vẫn tiến hành quẹt thẻ thanh toán")
    print("   được bình thường mà không bị mất đơn hàng nhờ kiến trúc tách biệt dịch vụ (Fault Isolation)!")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chaos Testing & Attack Simulation Tool")
    parser.add_argument("--check", action="store_true", help="Kiểm tra sức khỏe hệ thống")
    parser.add_argument("--stress", type=str, default="https://localhost:8443/", help="Gửi tải giả lập vào URL")
    parser.add_argument("--count", type=int, default=30, help="Số lượng requests giả lập")
    parser.add_argument("--scenario", action="store_true", help="In kịch bản diễn tập sự cố để thuyết trình")

    args = parser.parse_args()

    if args.check:
        check_health()
    elif args.scenario:
        simulate_incident_report()
    else:
        # Mặc định chạy kiểm tra và in kịch bản
        check_health()
        print()
        simulate_incident_report()
