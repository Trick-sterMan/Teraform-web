#!/bin/bash
# ==============================================================================
# Script kiểm tra 3 trang web giả lập cục bộ trên Terminal macOS
# Sử dụng Docker để chạy thử 3 container Nginx tương ứng với 3 dịch vụ
# ==============================================================================

echo "========================================================"
echo "🚀 KIỂM TRA GIẢ LẬP 3 MÁY CHỦ WEB DEMO TRÊN MAC"
echo "========================================================"

# Kiểm tra Docker có chạy không
if ! command -v docker &> /dev/null; then
    echo "⚠️ Docker chưa được cài đặt hoặc chưa chạy trong PATH."
    echo "💡 Bạn có thể kiểm tra trực tiếp mã HTML trong thư mục scripts/ hoặc deploy lên AWS với Terraform."
    exit 0
fi

echo "1. Dọn dẹp các container test cũ (nếu có)..."
docker rm -f demo_frontend demo_products demo_checkout 2>/dev/null || true

echo "2. Khởi tạo container Frontend (Cổng 8081)..."
docker run -d --name demo_frontend -p 8081:80 nginx:alpine
docker exec -i demo_frontend sh -c "mkdir -p /usr/share/nginx/html"
docker cp scripts/user_data_frontend.sh demo_frontend:/tmp/
docker exec -i demo_frontend sh -c "
sed -n '/cat << .EOF. > \/var\/www\/html\/index.html/,/EOF/p' /tmp/user_data_frontend.sh | sed '1d;\$d' > /usr/share/nginx/html/index.html
"

echo "3. Khởi tạo container Products (Cổng 8082 - path /products/)..."
docker run -d --name demo_products -p 8082:80 nginx:alpine
docker exec -i demo_products sh -c "mkdir -p /usr/share/nginx/html/products"
docker cp scripts/user_data_products.sh demo_products:/tmp/
docker exec -i demo_products sh -c "
sed -n '/cat << .EOF. > \/var\/www\/html\/products\/index.html/,/EOF/p' /tmp/user_data_products.sh | sed '1d;\$d' > /usr/share/nginx/html/products/index.html
cp /usr/share/nginx/html/products/index.html /usr/share/nginx/html/index.html
"

echo "4. Khởi tạo container Checkout (Cổng 8083 - path /checkout/)..."
docker run -d --name demo_checkout -p 8083:80 nginx:alpine
docker exec -i demo_checkout sh -c "mkdir -p /usr/share/nginx/html/checkout"
docker cp scripts/user_data_checkout.sh demo_checkout:/tmp/
docker exec -i demo_checkout sh -c "
sed -n '/cat << .EOF. > \/var\/www\/html\/checkout\/index.html/,/EOF/p' /tmp/user_data_checkout.sh | sed '1d;\$d' > /usr/share/nginx/html/checkout/index.html
cp /usr/share/nginx/html/checkout/index.html /usr/share/nginx/html/index.html
"

echo ""
echo "========================================================"
echo "✅ ĐÃ KHỞI CHẠY THÀNH CÔNG 3 WEB DEMO CỤC BỘ TRÊN MAC:"
echo "👉 Trang chủ (Frontend):    http://localhost:8081"
echo "👉 Trang sản phẩm:          http://localhost:8082/products/"
echo "👉 Trang thanh toán:        http://localhost:8083/checkout/"
echo "========================================================"
echo "Dùng lệnh sau khi muốn dừng và xóa các container test:"
echo "docker rm -f demo_frontend demo_products demo_checkout"
