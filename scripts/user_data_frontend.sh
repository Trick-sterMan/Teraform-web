#!/bin/bash
# ==============================================================================
# Script khởi tạo Frontend Server (Trang chủ) - Siêu thực tế thương mại điện tử
# ==============================================================================
set -e

dnf update -y || yum update -y
dnf install -y nginx || yum install -y nginx

mkdir -p /var/www/html
mkdir -p /usr/share/nginx/html

cat << 'EOF' > /var/www/html/index.html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudMart | Siêu Thị Công Nghệ Trực Tuyến Hàng Đầu</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --secondary: #0f172a;
            --accent: #f59e0b;
            --danger: #ef4444;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --success: #10b981;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--bg); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; overflow-x: hidden; }

        /* Top Announcement Bar */
        .top-bar { background: #0f172a; color: #94a3b8; font-size: 0.8rem; padding: 0.5rem 1.5rem; display: flex; justify-content: space-between; align-items: center; }
        .top-bar strong { color: #f8fafc; }
        .top-links a { color: #94a3b8; text-decoration: none; margin-left: 1rem; transition: 0.2s; }
        .top-links a:hover { color: #fff; }

        /* Cloud System Monitor Badge Bar */
        .cloud-badge-bar { background: linear-gradient(90deg, #1e3a8a, #2563eb); color: white; padding: 0.55rem 1.5rem; font-size: 0.85rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.15); }
        .cloud-badge-bar .sys-info { display: flex; gap: 1rem; align-items: center; }
        .cloud-pill { background: rgba(255,255,255,0.2); padding: 0.2rem 0.65rem; border-radius: 9999px; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.02em; display: inline-flex; align-items: center; gap: 0.35rem; }
        .cloud-pill .dot { width: 7px; height: 7px; border-radius: 50%; background: #4ade80; display: inline-block; box-shadow: 0 0 8px #4ade80; }

        /* Main Navigation */
        header { background: var(--card-bg); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 50; box-shadow: var(--shadow-sm); }
        .nav-container { max-width: 1240px; margin: 0 auto; padding: 0.9rem 1.5rem; display: flex; align-items: center; justify-content: space-between; gap: 2rem; }
        .brand-logo { font-size: 1.5rem; font-weight: 800; color: var(--primary); text-decoration: none; display: flex; align-items: center; gap: 0.5rem; letter-spacing: -0.03em; }
        .brand-logo span { color: var(--secondary); }

        .search-wrapper { flex: 1; max-width: 520px; position: relative; }
        .search-input { width: 100%; padding: 0.7rem 1rem 0.7rem 2.8rem; border-radius: 9999px; border: 1.5px solid var(--border); outline: none; font-size: 0.9rem; transition: 0.2s; background: #f8fafc; }
        .search-input:focus { border-color: var(--primary); background: #fff; box-shadow: 0 0 0 4px rgba(37,99,235,0.1); }
        .search-icon { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); font-size: 1rem; color: #94a3b8; }

        .nav-menu { display: flex; align-items: center; gap: 1.25rem; }
        .nav-link { text-decoration: none; color: #475569; font-weight: 600; font-size: 0.95rem; padding: 0.5rem 0.85rem; border-radius: 8px; transition: 0.2s; }
        .nav-link:hover, .nav-link.active { color: var(--primary); background: #eff6ff; }
        .cart-btn { background: var(--primary); color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 9999px; font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem; text-decoration: none; transition: 0.2s; }
        .cart-btn:hover { background: var(--primary-hover); transform: translateY(-1px); }
        .cart-badge { background: #ef4444; color: white; font-size: 0.75rem; border-radius: 9999px; padding: 0.1rem 0.45rem; font-weight: 700; }

        /* Flash Sale Header Strip */
        .flash-sale-bar { max-width: 1240px; margin: 1.25rem auto 0; padding: 0 1.5rem; }
        .flash-sale-inner { background: linear-gradient(90deg, #dc2626, #ea580c); color: white; border-radius: 14px; padding: 0.75rem 1.5rem; display: flex; justify-content: space-between; align-items: center; box-shadow: var(--shadow-md); }
        .flash-title { display: flex; align-items: center; gap: 0.6rem; font-weight: 800; font-size: 1.05rem; }
        .countdown-box { display: flex; align-items: center; gap: 0.4rem; font-weight: 700; }
        .timer-unit { background: rgba(0,0,0,0.3); padding: 0.25rem 0.5rem; border-radius: 6px; font-family: monospace; font-size: 1rem; }

        /* Hero Banner */
        .hero-section { max-width: 1240px; margin: 1.25rem auto 0; padding: 0 1.5rem; }
        .hero-card { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%); border-radius: 24px; padding: 3.5rem 3rem; color: white; display: flex; align-items: center; justify-content: space-between; overflow: hidden; position: relative; box-shadow: var(--shadow-xl); }
        .hero-card::after { content: ""; position: absolute; right: -50px; bottom: -50px; width: 350px; height: 350px; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); border-radius: 50%; }
        .hero-content { max-width: 580px; z-index: 2; }
        .hero-tag { display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(255,255,255,0.15); backdrop-filter: blur(8px); padding: 0.35rem 0.9rem; border-radius: 9999px; font-size: 0.825rem; font-weight: 600; margin-bottom: 1.25rem; }
        .hero-title { font-size: 3rem; font-weight: 800; line-height: 1.15; margin-bottom: 1rem; letter-spacing: -0.02em; }
        .hero-desc { font-size: 1.1rem; color: #cbd5e1; margin-bottom: 2rem; line-height: 1.6; }
        .hero-actions { display: flex; gap: 1rem; }
        .btn-cta { background: #ffffff; color: var(--secondary); padding: 0.85rem 1.8rem; border-radius: 12px; font-weight: 700; text-decoration: none; font-size: 1rem; transition: 0.2s; display: inline-flex; align-items: center; gap: 0.5rem; }
        .btn-cta:hover { background: #f1f5f9; transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2); }
        .btn-secondary-cta { background: rgba(255,255,255,0.12); color: white; border: 1.5px solid rgba(255,255,255,0.25); padding: 0.85rem 1.8rem; border-radius: 12px; font-weight: 600; text-decoration: none; font-size: 1rem; transition: 0.2s; }
        .btn-secondary-cta:hover { background: rgba(255,255,255,0.2); }
        .hero-visual { font-size: 8rem; z-index: 2; animation: float 3s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }

        /* Trust Badges */
        .trust-grid { max-width: 1240px; margin: 2rem auto; padding: 0 1.5rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem; }
        .trust-item { background: white; border: 1px solid var(--border); border-radius: 14px; padding: 1.25rem 1.5rem; display: flex; align-items: center; gap: 1rem; box-shadow: var(--shadow-sm); }
        .trust-icon { font-size: 2rem; background: #eff6ff; width: 48px; height: 48px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
        .trust-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 0.2rem; }
        .trust-desc { font-size: 0.8rem; color: var(--text-muted); }

        /* Categories Section */
        .section-container { max-width: 1240px; margin: 2rem auto; padding: 0 1.5rem; }
        .section-head { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.5rem; }
        .section-title { font-size: 1.65rem; font-weight: 800; color: var(--secondary); letter-spacing: -0.02em; }
        .section-subtitle { font-size: 0.95rem; color: var(--text-muted); margin-top: 0.25rem; }
        .see-all-link { color: var(--primary); font-weight: 600; text-decoration: none; font-size: 0.95rem; display: flex; align-items: center; gap: 0.3rem; }
        .see-all-link:hover { text-decoration: underline; }

        .cat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; }
        .cat-card { background: white; border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem 1rem; text-align: center; text-decoration: none; color: var(--text-main); transition: 0.2s; box-shadow: var(--shadow-sm); }
        .cat-card:hover { transform: translateY(-4px); border-color: var(--primary); box-shadow: var(--shadow-md); }
        .cat-emoji { font-size: 2.75rem; margin-bottom: 0.75rem; }
        .cat-name { font-weight: 700; font-size: 0.95rem; }
        .cat-count { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem; }

        /* Featured Products Grid */
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }
        .product-card { background: white; border: 1px solid var(--border); border-radius: 18px; padding: 1.25rem; transition: 0.25s; display: flex; flex-direction: column; position: relative; box-shadow: var(--shadow-sm); }
        .product-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-xl); border-color: #cbd5e1; }
        .tag-discount { position: absolute; top: 1rem; left: 1rem; background: #ef4444; color: white; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.6rem; border-radius: 6px; }
        .product-img-box { height: 180px; display: flex; align-items: center; justify-content: center; font-size: 5rem; margin-bottom: 1rem; background: #f8fafc; border-radius: 12px; }
        .product-category { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--primary); letter-spacing: 0.05em; margin-bottom: 0.35rem; }
        .product-name { font-size: 1.05rem; font-weight: 700; color: var(--secondary); margin-bottom: 0.5rem; line-height: 1.4; }
        .product-rating { display: flex; align-items: center; gap: 0.35rem; font-size: 0.85rem; color: #f59e0b; margin-bottom: 0.75rem; }
        .product-rating span { color: var(--text-muted); font-size: 0.8rem; }
        .price-row { display: flex; align-items: baseline; gap: 0.6rem; margin-top: auto; margin-bottom: 1rem; }
        .current-price { font-size: 1.25rem; font-weight: 800; color: #0f172a; }
        .old-price { font-size: 0.85rem; color: #94a3b8; text-decoration: line-through; }
        .btn-add-cart { width: 100%; background: #eff6ff; color: var(--primary); border: 1.5px solid #bfdbfe; padding: 0.65rem; border-radius: 10px; font-weight: 700; font-size: 0.9rem; cursor: pointer; transition: 0.2s; text-decoration: none; text-align: center; display: block; }
        .btn-add-cart:hover { background: var(--primary); color: white; border-color: var(--primary); }

        /* Architecture Banner */
        .arch-banner { max-width: 1240px; margin: 3rem auto; padding: 0 1.5rem; }
        .arch-card { background: #0f172a; border-radius: 20px; padding: 2rem 2.5rem; color: #94a3b8; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; border: 1px solid #334155; }
        .arch-card h3 { color: #f8fafc; font-size: 1.25rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem; }
        .arch-card p { font-size: 0.9rem; line-height: 1.6; }
        .arch-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 0.85rem; }
        .arch-table td { padding: 0.5rem 0; border-bottom: 1px solid #1e293b; }
        .arch-table td:first-child { color: #64748b; font-weight: 600; width: 40%; }
        .arch-table td:last-child { color: #38bdf8; font-weight: 700; }

        /* Live Purchase Notification (Social Proof) */
        .live-order-toast { position: fixed; bottom: 1.5rem; left: 1.5rem; background: white; border: 1px solid var(--border); border-radius: 14px; padding: 0.85rem 1.2rem; display: flex; align-items: center; gap: 0.85rem; box-shadow: var(--shadow-xl); z-index: 90; animation: slideUp 0.4s ease-out; }
        @keyframes slideUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .live-order-icon { width: 40px; height: 40px; border-radius: 50%; background: #eff6ff; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
        .live-order-text { font-size: 0.825rem; color: #334155; }
        .live-order-text strong { color: var(--secondary); display: block; }
        .live-order-time { font-size: 0.75rem; color: #94a3b8; }

        /* Chat Widget Button */
        .chat-widget-btn { position: fixed; bottom: 1.5rem; right: 1.5rem; background: var(--primary); color: white; width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: var(--shadow-xl); cursor: pointer; border: none; z-index: 90; transition: transform 0.2s; }
        .chat-widget-btn:hover { transform: scale(1.08); }

        /* Footer */
        footer { background: #0b1120; color: #64748b; padding: 3.5rem 1.5rem 1.5rem; margin-top: auto; border-top: 1px solid #1e293b; }
        .footer-grid { max-width: 1240px; margin: 0 auto 2.5rem; display: grid; grid-template-columns: 2fr repeat(3, 1fr); gap: 3rem; }
        .footer-brand h4 { color: white; font-size: 1.3rem; margin-bottom: 0.75rem; }
        .footer-brand p { font-size: 0.875rem; line-height: 1.6; max-width: 300px; }
        .footer-col h5 { color: white; font-size: 0.95rem; font-weight: 700; margin-bottom: 1.2rem; }
        .footer-col ul { list-style: none; }
        .footer-col li { margin-bottom: 0.65rem; }
        .footer-col a { color: #94a3b8; text-decoration: none; font-size: 0.875rem; transition: 0.2s; }
        .footer-col a:hover { color: #38bdf8; }
        .footer-bottom { max-width: 1240px; margin: 0 auto; padding-top: 1.5rem; border-top: 1px solid #1e293b; display: flex; justify-content: space-between; font-size: 0.825rem; }

        @media (max-width: 768px) {
            .hero-card { flex-direction: column; text-align: center; padding: 2.5rem 1.5rem; }
            .hero-actions { justify-content: center; }
            .hero-visual { display: none; }
            .arch-card { grid-template-columns: 1fr; }
            .footer-grid { grid-template-columns: 1fr; }
            .live-order-toast { display: none; }
        }
    </style>
</head>
<body>
    <!-- Top Announcement Bar -->
    <div class="top-bar">
        <div>⚡ <strong>Khuyến mãi đặc biệt:</strong> Giảm 10% cho đơn hàng đầu tiên với mã <code>CLOUDMART10</code></div>
        <div class="top-links">
            <a href="/">Hỗ trợ 24/7</a>
            <a href="/">Tra cứu đơn hàng</a>
            <a href="/">Hotline: 1800 6868</a>
        </div>
    </div>

    <!-- Live Cloud Architecture Header Badge -->
    <div class="cloud-badge-bar">
        <div class="sys-info">
            <span class="cloud-pill"><span class="dot"></span> AWS ALB Online</span>
            <span>Target Group: <strong>tg_frontend</strong></span>
            <span>| Định tuyến URL: <strong>Mặc định (/)</strong></span>
        </div>
        <div>
            <span class="cloud-pill">Backend: Nginx on EC2 • Phụ trách: Huỳnh Nhật Hòa</span>
        </div>
    </div>

    <!-- Main Navigation Bar -->
    <header>
        <div class="nav-container">
            <a href="/" class="brand-logo">
                🛒 Cloud<span>Mart</span>
            </a>

            <div class="search-wrapper">
                <span class="search-icon">🔍</span>
                <input type="text" class="search-input" placeholder="Tìm kiếm iPhone 16, MacBook Pro M3, phụ kiện chính hãng...">
            </div>

            <nav class="nav-menu">
                <a href="/" class="nav-link active">Trang chủ</a>
                <a href="/products/" class="nav-link">Sản phẩm</a>
                <a href="/checkout/" class="nav-link">Thanh toán</a>
                <a href="/checkout/" class="cart-btn">
                    <span>Giỏ hàng</span>
                    <span class="cart-badge">2</span>
                </a>
            </nav>
        </div>
    </header>

    <!-- Flash Sale Bar with Real-time Countdown -->
    <div class="flash-sale-bar">
        <div class="flash-sale-inner">
            <div class="flash-title">
                <span>⚡ FLASH SALE CÔNG NGHỆ HÔM NAY</span>
                <span style="font-size: 0.85rem; font-weight: 500; opacity: 0.9;">| Giảm sốc đến 40%</span>
            </div>
            <div class="countdown-box">
                <span style="font-size: 0.85rem;">Kết thúc trong:</span>
                <span class="timer-unit" id="cd-hours">04</span> :
                <span class="timer-unit" id="cd-mins">28</span> :
                <span class="timer-unit" id="cd-secs">50</span>
            </div>
        </div>
    </div>

    <!-- Hero Banner Section -->
    <section class="hero-section">
        <div class="hero-card">
            <div class="hero-content">
                <div class="hero-tag">🔥 ĐẠI TIỆC CÔNG NGHỆ 2026</div>
                <h1 class="hero-title">Đẳng Cấp Công Nghệ Thế Hệ Mới</h1>
                <p class="hero-desc">Trải nghiệm sức mạnh đột phá từ Apple M3 Series, Galaxy AI và hệ sinh thái phụ kiện cao cấp với mức giá ưu đãi nhất thị trường.</p>
                <div class="hero-actions">
                    <a href="/products/" class="btn-cta">Khám Phá Danh Mục &rarr;</a>
                    <a href="/checkout/" class="btn-secondary-cta">Giỏ Hàng & Thanh Toán</a>
                </div>
            </div>
            <div class="hero-visual">💻</div>
        </div>
    </section>

    <!-- Trust Badges -->
    <div class="trust-grid">
        <div class="trust-item">
            <div class="trust-icon">🚀</div>
            <div>
                <div class="trust-title">Giao Hàng Siêu Tốc 2H</div>
                <div class="trust-desc">Nội thành Hà Nội & TP.HCM</div>
            </div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">🛡️</div>
            <div>
                <div class="trust-title">100% Chính Hãng</div>
                <div class="trust-desc">Bảo hành 12 tháng tại hãng</div>
            </div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">🔄</div>
            <div>
                <div class="trust-title">Đổi Trả Trong 30 Ngày</div>
                <div class="trust-desc">Lỗi 1 đổi 1 nhanh chóng</div>
            </div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">💳</div>
            <div>
                <div class="trust-title">Thanh Toán Linh Hoạt</div>
                <div class="trust-desc">VietQR, Thẻ quốc tế, Trả góp 0%</div>
            </div>
        </div>
    </div>

    <!-- Categories Section -->
    <section class="section-container">
        <div class="section-head">
            <div>
                <h2 class="section-title">Danh Mục Nổi Bật</h2>
                <p class="section-subtitle">Lựa chọn các thiết bị công nghệ chính hãng theo nhu cầu của bạn</p>
            </div>
            <a href="/products/" class="see-all-link">Xem tất cả danh mục &rarr;</a>
        </div>
        <div class="cat-grid">
            <a href="/products/" class="cat-card">
                <div class="cat-emoji">💻</div>
                <div class="cat-name">Laptop & Mac</div>
                <div class="cat-count">128 sản phẩm</div>
            </a>
            <a href="/products/" class="cat-card">
                <div class="cat-emoji">📱</div>
                <div class="cat-name">Điện Thoại</div>
                <div class="cat-count">245 sản phẩm</div>
            </a>
            <a href="/products/" class="cat-card">
                <div class="cat-emoji">🎧</div>
                <div class="cat-name">Tai Nghe & Âm Thanh</div>
                <div class="cat-count">86 sản phẩm</div>
            </a>
            <a href="/products/" class="cat-card">
                <div class="cat-emoji">⌚</div>
                <div class="cat-name">Smartwatch</div>
                <div class="cat-count">54 sản phẩm</div>
            </a>
            <a href="/products/" class="cat-card">
                <div class="cat-emoji">🖥️</div>
                <div class="cat-name">Màn Hình & PC</div>
                <div class="cat-count">72 sản phẩm</div>
            </a>
            <a href="/products/" class="cat-card">
                <div class="cat-emoji">🎮</div>
                <div class="cat-name">Gaming Gear</div>
                <div class="cat-count">60 sản phẩm</div>
            </a>
        </div>
    </section>

    <!-- Featured Products Section -->
    <section class="section-container">
        <div class="section-head">
            <div>
                <h2 class="section-title">Sản Phẩm Bán Chạy Nhất</h2>
                <p class="section-subtitle">Được săn đón nhiều nhất tuần qua tại hệ thống CloudMart</p>
            </div>
            <a href="/products/" class="see-all-link">Xem thêm sản phẩm &rarr;</a>
        </div>

        <div class="product-grid">
            <!-- Product 1 -->
            <div class="product-card">
                <span class="tag-discount">-12%</span>
                <div class="product-img-box">💻</div>
                <div class="product-category">Laptop Apple</div>
                <h3 class="product-name">MacBook Pro 16" M3 Max (36GB / 512GB)</h3>
                <div class="product-rating">★★★★★ <span>(142 đánh giá)</span></div>
                <div class="price-row">
                    <span class="current-price">68.990.000 ₫</span>
                    <span class="old-price">78.500.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 2 -->
            <div class="product-card">
                <span class="tag-discount">-8%</span>
                <div class="product-img-box">📱</div>
                <div class="product-category">Smartphone</div>
                <h3 class="product-name">iPhone 16 Pro Max 256GB - Titan Tự Nhiên</h3>
                <div class="product-rating">★★★★★ <span>(389 đánh giá)</span></div>
                <div class="price-row">
                    <span class="current-price">34.490.000 ₫</span>
                    <span class="old-price">37.990.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 3 -->
            <div class="product-card">
                <span class="tag-discount">-20%</span>
                <div class="product-img-box">🎧</div>
                <div class="product-category">Âm thanh cao cấp</div>
                <h3 class="product-name">Sony WH-1000XM5 Chống Ồn Chủ Động</h3>
                <div class="product-rating">★★★★★ <span>(96 đánh giá)</span></div>
                <div class="price-row">
                    <span class="current-price">7.990.000 ₫</span>
                    <span class="old-price">9.990.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 4 -->
            <div class="product-card">
                <span class="tag-discount">-15%</span>
                <div class="product-img-box">⌚</div>
                <div class="product-category">Smartwatch</div>
                <h3 class="product-name">Apple Watch Ultra 2 GPS + Cellular 49mm</h3>
                <div class="product-rating">★★★★★ <span>(78 đánh giá)</span></div>
                <div class="price-row">
                    <span class="current-price">19.890.000 ₫</span>
                    <span class="old-price">23.490.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>
        </div>
    </section>

    <!-- Cloud Architecture Monitor Card -->
    <div class="arch-banner">
        <div class="arch-card">
            <div>
                <h3>☁️ Thông Tin Kiến Trúc Đám Mây (AWS ALB)</h3>
                <p>Trang web này đóng vai trò <strong>Frontend Web Server</strong> trong mô hình cân bằng tải theo nội dung (Path-based Routing) sử dụng Application Load Balancer.</p>
                <p style="margin-top: 0.75rem;">Khi người dùng truy cập đường dẫn gốc <code>/</code>, ALB tự động điều hướng request về <strong>Target Group: tg_frontend</strong>.</p>
            </div>
            <div>
                <table class="arch-table">
                    <tr><td>Component:</td><td>Frontend Web Server (Cluster Node 1)</td></tr>
                    <tr><td>AWS Target Group:</td><td>tg_frontend (Port 80 HTTP)</td></tr>
                    <tr><td>Health Check URL:</td><td>HTTP 200 OK tại /</td></tr>
                    <tr><td>Mạng VPC:</td><td>10.0.0.0/16 (Public Subnet 1)</td></tr>
                    <tr><td>Thành viên phụ trách:</td><td>Huỳnh Nhật Hòa (Target Groups & Demo Web)</td></tr>
                </table>
            </div>
        </div>
    </div>

    <!-- Live Social Proof Toast (Thông báo mua hàng trực tiếp) -->
    <div class="live-order-toast" id="socialProof">
        <div class="live-order-icon">🛍️</div>
        <div>
            <div class="live-order-text"><strong id="spCustomer">Nguyễn Văn T. (TP.HCM)</strong> vừa đặt mua iPhone 16 Pro Max</div>
            <div class="live-order-time" id="spTime">2 phút trước • Đã xác nhận thanh toán VietQR</div>
        </div>
    </div>

    <!-- Floating Chat Widget -->
    <button class="chat-widget-btn" onclick="alert('Trợ lý AI CloudMart: Xin chào! Bạn cần tư vấn sản phẩm công nghệ nào hôm nay?')">💬</button>

    <!-- Footer -->
    <footer>
        <div class="footer-grid">
            <div class="footer-brand">
                <h4>🛒 CloudMart E-Commerce</h4>
                <p>Hệ thống bán hàng trực tuyến ứng dụng kiến trúc cân bằng tải thông minh Application Load Balancer trên nền tảng AWS và Terraform.</p>
            </div>
            <div class="footer-col">
                <h5>Dịch Vụ & Sản Phẩm</h5>
                <ul>
                    <li><a href="/products/">Laptop & MacBook</a></li>
                    <li><a href="/products/">Điện thoại thông minh</a></li>
                    <li><a href="/products/">Phụ kiện & Âm thanh</a></li>
                    <li><a href="/checkout/">Thanh toán đơn hàng</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h5>Hỗ Trợ Khách Hàng</h5>
                <ul>
                    <li><a href="/">Chính sách bảo hành</a></li>
                    <li><a href="/">Quy định đổi trả hàng</a></li>
                    <li><a href="/">Phương thức vận chuyển</a></li>
                    <li><a href="/">Bảo mật thông tin</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h5>Đồ Án Nhóm</h5>
                <ul>
                    <li><a href="/">1. Phạm Đinh Gia Bảo (Core ALB)</a></li>
                    <li><a href="/">2. Huỳnh Nhật Hòa (Targets & Web)</a></li>
                    <li><a href="/">3. Ngô Khánh Hưng (Security & SSL)</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <div>© 2026 CloudMart E-Commerce System. All Rights Reserved.</div>
            <div>Đồ án Cân bằng tải HTTPS ALB với Terraform</div>
        </div>
    </footer>

    <script>
        // Countdown Timer Simulation
        var h = 4, m = 28, s = 50;
        setInterval(function() {
            if (s > 0) s--;
            else { s = 59; if (m > 0) m--; else { m = 59; h--; } }
            document.getElementById('cd-hours').innerText = (h < 10 ? '0' : '') + h;
            document.getElementById('cd-mins').innerText = (m < 10 ? '0' : '') + m;
            document.getElementById('cd-secs').innerText = (s < 10 ? '0' : '') + s;
        }, 1000);

        // Social Proof notification cycle
        var customers = [
            { name: "Trần Minh H. (Hà Nội)", item: "MacBook Pro 16 M3 Max", time: "1 phút trước" },
            { name: "Lê Thị B. (Đà Nẵng)", item: "Tai nghe Sony WH-1000XM5", time: "3 phút trước" },
            { name: "Hoàng Anh K. (Cần Thơ)", item: "Apple Watch Ultra 2", time: "5 phút trước" }
        ];
        var idx = 0;
        setInterval(function() {
            var c = customers[idx % customers.length];
            document.getElementById('spCustomer').innerText = c.name;
            document.getElementById('spTime').innerText = c.time + " • Đã xác nhận đơn hàng";
            idx++;
        }, 8000);
    </script>
</body>
</html>
EOF

cp /var/www/html/index.html /usr/share/nginx/html/index.html
systemctl daemon-reload
systemctl enable nginx
systemctl restart nginx
