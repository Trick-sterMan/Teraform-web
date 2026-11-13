#!/bin/bash
# ==============================================================================
# Script khởi tạo Products Server (Trang sản phẩm) - Siêu thực tế thương mại điện tử
# ==============================================================================
set -e

dnf update -y || yum update -y
dnf install -y nginx || yum install -y nginx

mkdir -p /var/www/html/products
mkdir -p /usr/share/nginx/html/products

cat << 'EOF' > /var/www/html/products/index.html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Danh Mục Sản Phẩm Công Nghệ | CloudMart</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #059669;
            --primary-hover: #047857;
            --secondary: #0f172a;
            --accent: #f59e0b;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--bg); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; }

        /* Top Announcement Bar */
        .top-bar { background: #064e3b; color: #a7f3d0; font-size: 0.8rem; padding: 0.5rem 1.5rem; display: flex; justify-content: space-between; align-items: center; }
        .top-bar strong { color: #fff; }
        .top-links a { color: #a7f3d0; text-decoration: none; margin-left: 1rem; }
        .top-links a:hover { color: #fff; }

        /* Cloud System Monitor Badge Bar */
        .cloud-badge-bar { background: linear-gradient(90deg, #065f46, #059669); color: white; padding: 0.55rem 1.5rem; font-size: 0.85rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.15); }
        .cloud-badge-bar .sys-info { display: flex; gap: 1rem; align-items: center; }
        .cloud-pill { background: rgba(255,255,255,0.2); padding: 0.2rem 0.65rem; border-radius: 9999px; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.02em; display: inline-flex; align-items: center; gap: 0.35rem; }
        .cloud-pill .dot { width: 7px; height: 7px; border-radius: 50%; background: #6ee7b7; display: inline-block; box-shadow: 0 0 8px #6ee7b7; }

        /* Main Navigation */
        header { background: var(--card-bg); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 50; box-shadow: var(--shadow-sm); }
        .nav-container { max-width: 1240px; margin: 0 auto; padding: 0.9rem 1.5rem; display: flex; align-items: center; justify-content: space-between; gap: 2rem; }
        .brand-logo { font-size: 1.5rem; font-weight: 800; color: #059669; text-decoration: none; display: flex; align-items: center; gap: 0.5rem; letter-spacing: -0.03em; }
        .brand-logo span { color: var(--secondary); }

        .search-wrapper { flex: 1; max-width: 520px; position: relative; }
        .search-input { width: 100%; padding: 0.7rem 1rem 0.7rem 2.8rem; border-radius: 9999px; border: 1.5px solid var(--border); outline: none; font-size: 0.9rem; transition: 0.2s; background: #f8fafc; }
        .search-input:focus { border-color: var(--primary); background: #fff; box-shadow: 0 0 0 4px rgba(5,150,105,0.1); }
        .search-icon { position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); font-size: 1rem; color: #94a3b8; }

        .nav-menu { display: flex; align-items: center; gap: 1.25rem; }
        .nav-link { text-decoration: none; color: #475569; font-weight: 600; font-size: 0.95rem; padding: 0.5rem 0.85rem; border-radius: 8px; transition: 0.2s; }
        .nav-link:hover, .nav-link.active { color: var(--primary); background: #ecfdf5; }
        .cart-btn { background: var(--primary); color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 9999px; font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem; text-decoration: none; transition: 0.2s; }
        .cart-btn:hover { background: var(--primary-hover); transform: translateY(-1px); }
        .cart-badge { background: #ef4444; color: white; font-size: 0.75rem; border-radius: 9999px; padding: 0.1rem 0.45rem; font-weight: 700; }

        /* Breadcrumb */
        .breadcrumb-bar { max-width: 1240px; margin: 1.25rem auto 0; padding: 0 1.5rem; font-size: 0.85rem; color: var(--text-muted); display: flex; align-items: center; gap: 0.5rem; }
        .breadcrumb-bar a { color: var(--text-muted); text-decoration: none; }
        .breadcrumb-bar a:hover { color: var(--primary); }
        .breadcrumb-bar span.current { color: var(--primary); font-weight: 600; }

        /* Main Content Layout (Sidebar + Product Grid) */
        .catalog-container { max-width: 1240px; margin: 1.5rem auto 3rem; padding: 0 1.5rem; display: grid; grid-template-columns: 260px 1fr; gap: 2rem; align-items: start; }

        /* Filter Sidebar */
        .filter-sidebar { background: white; border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; box-shadow: var(--shadow-sm); position: sticky; top: 90px; }
        .filter-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: center; }
        .filter-reset { font-size: 0.8rem; color: var(--primary); text-decoration: none; font-weight: 600; cursor: pointer; }
        .filter-group { border-bottom: 1px solid var(--border); padding-bottom: 1.25rem; margin-bottom: 1.25rem; }
        .filter-group:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
        .filter-group-title { font-size: 0.9rem; font-weight: 700; color: var(--secondary); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.03em; }
        .filter-option { display: flex; align-items: center; gap: 0.6rem; font-size: 0.875rem; color: #475569; margin-bottom: 0.5rem; cursor: pointer; }
        .filter-option input[type="checkbox"] { accent-color: var(--primary); width: 16px; height: 16px; }

        /* Catalog Main Header & Tools */
        .catalog-main { display: flex; flex-direction: column; gap: 1.5rem; }
        .toolbar-card { background: white; border: 1px solid var(--border); border-radius: 14px; padding: 1rem 1.5rem; display: flex; justify-content: space-between; align-items: center; box-shadow: var(--shadow-sm); }
        .results-count { font-size: 0.95rem; color: var(--text-muted); }
        .results-count strong { color: var(--secondary); }
        .sort-select { padding: 0.5rem 1rem; border-radius: 8px; border: 1px solid var(--border); outline: none; font-size: 0.875rem; color: var(--secondary); font-weight: 600; background: #fff; cursor: pointer; }

        /* Product Cards Grid */
        .product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
        .product-card { background: white; border: 1px solid var(--border); border-radius: 18px; padding: 1.25rem; transition: 0.25s; display: flex; flex-direction: column; position: relative; box-shadow: var(--shadow-sm); }
        .product-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-xl); border-color: #cbd5e1; }
        .tag-badge { position: absolute; top: 1rem; left: 1rem; background: var(--primary); color: white; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.6rem; border-radius: 6px; }
        .tag-badge.sale { background: #ef4444; }
        .stock-tag { position: absolute; top: 1rem; right: 1rem; font-size: 0.75rem; font-weight: 700; color: #059669; background: #ecfdf5; padding: 0.2rem 0.5rem; border-radius: 6px; }
        .product-img-box { height: 180px; display: flex; align-items: center; justify-content: center; font-size: 5rem; margin-bottom: 0.75rem; background: #f8fafc; border-radius: 12px; }
        .product-category { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--primary); letter-spacing: 0.05em; margin-bottom: 0.25rem; }
        .product-name { font-size: 1.05rem; font-weight: 700; color: var(--secondary); margin-bottom: 0.35rem; line-height: 1.35; }
        .product-specs { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.75rem; line-height: 1.4; }

        /* Interactive Variants Selector */
        .variant-selector { display: flex; gap: 0.4rem; margin-bottom: 0.75rem; }
        .variant-pill { font-size: 0.75rem; border: 1px solid var(--border); padding: 0.2rem 0.55rem; border-radius: 6px; cursor: pointer; font-weight: 600; color: #475569; background: #f8fafc; }
        .variant-pill.active { border-color: var(--primary); background: #ecfdf5; color: var(--primary); }

        /* Promotion Box inside Card */
        .card-promo { background: #fffbeb; border: 1px dashed #fcd34d; border-radius: 8px; padding: 0.4rem 0.6rem; font-size: 0.75rem; color: #b45309; font-weight: 600; margin-bottom: 0.85rem; display: flex; align-items: center; gap: 0.35rem; }

        .product-rating { display: flex; align-items: center; gap: 0.35rem; font-size: 0.85rem; color: #f59e0b; margin-bottom: 0.5rem; }
        .price-row { display: flex; align-items: baseline; gap: 0.6rem; margin-top: auto; margin-bottom: 1rem; }
        .current-price { font-size: 1.3rem; font-weight: 800; color: #064e3b; }
        .old-price { font-size: 0.85rem; color: #94a3b8; text-decoration: line-through; }
        .card-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; }
        .btn-buy-now { background: var(--primary); color: white; border: none; padding: 0.65rem; border-radius: 8px; font-weight: 700; font-size: 0.875rem; cursor: pointer; text-decoration: none; text-align: center; transition: 0.2s; }
        .btn-buy-now:hover { background: var(--primary-hover); }
        .btn-cart-mini { background: #ecfdf5; color: var(--primary); border: 1.5px solid #a7f3d0; padding: 0.65rem; border-radius: 8px; font-weight: 700; font-size: 0.875rem; cursor: pointer; transition: 0.2s; text-align: center; }
        .btn-cart-mini:hover { background: #d1fae5; }

        /* Architecture Banner */
        .arch-banner { background: #0f172a; border-radius: 18px; padding: 1.75rem 2rem; color: #94a3b8; margin-top: 2rem; border: 1px solid #334155; }
        .arch-banner h3 { color: #f8fafc; font-size: 1.15rem; margin-bottom: 0.5rem; }
        .arch-banner p { font-size: 0.875rem; line-height: 1.5; }

        /* Toast Notification */
        .toast { position: fixed; bottom: 2rem; right: 2rem; background: #064e3b; color: white; padding: 1rem 1.5rem; border-radius: 12px; font-size: 0.9rem; font-weight: 600; box-shadow: var(--shadow-xl); display: none; z-index: 100; border-left: 5px solid #34d399; }

        /* Footer */
        footer { background: #0b1120; color: #64748b; padding: 3.5rem 1.5rem 1.5rem; margin-top: auto; border-top: 1px solid #1e293b; }
        .footer-grid { max-width: 1240px; margin: 0 auto 2.5rem; display: grid; grid-template-columns: 2fr repeat(3, 1fr); gap: 3rem; }
        .footer-brand h4 { color: white; font-size: 1.3rem; margin-bottom: 0.75rem; }
        .footer-brand p { font-size: 0.875rem; line-height: 1.6; max-width: 300px; }
        .footer-col h5 { color: white; font-size: 0.95rem; font-weight: 700; margin-bottom: 1.2rem; }
        .footer-col ul { list-style: none; }
        .footer-col li { margin-bottom: 0.65rem; }
        .footer-col a { color: #94a3b8; text-decoration: none; font-size: 0.875rem; }
        .footer-bottom { max-width: 1240px; margin: 0 auto; padding-top: 1.5rem; border-top: 1px solid #1e293b; display: flex; justify-content: space-between; font-size: 0.825rem; }

        @media (max-width: 860px) {
            .catalog-container { grid-template-columns: 1fr; }
            .filter-sidebar { display: none; }
            .footer-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- Top Announcement Bar -->
    <div class="top-bar">
        <div>⚡ <strong>Ưu đãi VietQR:</strong> Giảm thêm 500.000₫ khi thanh toán chuyển khoản qua mã VietQR</div>
        <div class="top-links">
            <a href="/">Hỗ trợ khách hàng</a>
            <a href="/">Hotline: 1800 6868</a>
        </div>
    </div>

    <!-- Live Cloud Architecture Header Badge -->
    <div class="cloud-badge-bar">
        <div class="sys-info">
            <span class="cloud-pill"><span class="dot"></span> AWS ALB Routed</span>
            <span>Target Group: <strong>tg_products</strong></span>
            <span>| Path Pattern: <strong>/products/*</strong></span>
        </div>
        <div>
            <span class="cloud-pill">Backend Node: EC2 Products (Nginx) • Huỳnh Nhật Hòa</span>
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
                <input type="text" class="search-input" id="searchInput" oninput="searchFilter()" placeholder="Tìm theo tên máy, hãng (Apple, Sony, Dell)...">
            </div>

            <nav class="nav-menu">
                <a href="/" class="nav-link">Trang chủ</a>
                <a href="/products/" class="nav-link active">Sản phẩm</a>
                <a href="/checkout/" class="nav-link">Thanh toán</a>
                <a href="/checkout/" class="cart-btn">
                    <span>Giỏ hàng</span>
                    <span class="cart-badge" id="cartCount">2</span>
                </a>
            </nav>
        </div>
    </header>

    <!-- Breadcrumb Bar -->
    <div class="breadcrumb-bar">
        <a href="/">Trang chủ</a>
        <span>/</span>
        <a href="/products/">Danh mục</a>
        <span>/</span>
        <span class="current">Thiết bị công nghệ cao cấp</span>
    </div>

    <!-- Catalog Main Section -->
    <div class="catalog-container">
        <!-- Filter Sidebar -->
        <aside class="filter-sidebar">
            <div class="filter-title">
                <span>Bộ Lọc Sản Phẩm</span>
                <span class="filter-reset" onclick="resetFilters()">Đặt lại</span>
            </div>

            <div class="filter-group">
                <div class="filter-group-title">Thương Hiệu</div>
                <label class="filter-option"><input type="checkbox" class="brand-cb" value="Apple" checked onchange="filterProducts()"> Apple chính hãng (VN/A)</label>
                <label class="filter-option"><input type="checkbox" class="brand-cb" value="Sony" checked onchange="filterProducts()"> Sony Electronics</label>
                <label class="filter-option"><input type="checkbox" class="brand-cb" value="Dell" checked onchange="filterProducts()"> Dell Technologies</label>
            </div>

            <div class="filter-group">
                <div class="filter-group-title">Hình thức thanh toán hỗ trợ</div>
                <label class="filter-option"><input type="checkbox" checked disabled> ⚡ Quét mã VietQR 24/7</label>
                <label class="filter-option"><input type="checkbox" checked disabled> 💳 Trả góp 0% thẻ tín dụng</label>
                <label class="filter-option"><input type="checkbox" checked disabled> 📱 Ví MoMo / Apple Pay</label>
            </div>
        </aside>

        <!-- Product Listing Content -->
        <main class="catalog-main">
            <div class="toolbar-card">
                <div class="results-count">Hiển thị <strong id="productCount">6</strong> sản phẩm công nghệ nổi bật</div>
                <div>
                    <label style="font-size: 0.85rem; color: var(--text-muted); margin-right: 0.5rem;">Sắp xếp theo:</label>
                    <select class="sort-select">
                        <option>Bán chạy nhất</option>
                        <option>Giá: Từ cao đến thấp</option>
                        <option>Giá: Từ thấp đến cao</option>
                    </select>
                </div>
            </div>

            <div class="product-grid" id="productGrid">
                <!-- Product 1 -->
                <div class="product-card" data-brand="Apple">
                    <span class="tag-badge sale">-12%</span>
                    <span class="stock-tag">✓ Sẵn hàng</span>
                    <div class="product-img-box">💻</div>
                    <div class="product-category">Laptop Apple</div>
                    <h3 class="product-name">MacBook Pro 16" M3 Max</h3>
                    <div class="product-specs">M3 Max 16-Core • 36GB RAM • Màn hình Liquid Retina XDR 120Hz</div>
                    <div class="variant-selector">
                        <span class="variant-pill active">512GB</span>
                        <span class="variant-pill">1TB (+6tr)</span>
                        <span class="variant-pill">Space Black</span>
                    </div>
                    <div class="card-promo">🎁 Tặng Hub Type-C 8 in 1 trị giá 890.000₫</div>
                    <div class="price-row">
                        <span class="current-price">68.990.000 ₫</span>
                        <span class="old-price">78.500.000 ₫</span>
                    </div>
                    <div class="card-actions">
                        <button class="btn-cart-mini" onclick="addToCart('MacBook Pro 16')">Thêm giỏ</button>
                        <a href="/checkout/" class="btn-buy-now">Mua ngay</a>
                    </div>
                </div>

                <!-- Product 2 -->
                <div class="product-card" data-brand="Apple">
                    <span class="tag-badge">Mới</span>
                    <span class="stock-tag">⚡ Chỉ còn 2</span>
                    <div class="product-img-box">📱</div>
                    <div class="product-category">Smartphone</div>
                    <h3 class="product-name">iPhone 16 Pro Max 256GB</h3>
                    <div class="product-specs">A18 Pro 3nm • Camera 48MP Zoom 5x • Viền Titan tự nhiên</div>
                    <div class="variant-selector">
                        <span class="variant-pill active">Titan Tự Nhiên</span>
                        <span class="variant-pill">Titan Sa Mạc</span>
                    </div>
                    <div class="card-promo">🎁 Giảm 500k khi quét mã VietQR</div>
                    <div class="price-row">
                        <span class="current-price">34.490.000 ₫</span>
                        <span class="old-price">37.990.000 ₫</span>
                    </div>
                    <div class="card-actions">
                        <button class="btn-cart-mini" onclick="addToCart('iPhone 16 Pro Max')">Thêm giỏ</button>
                        <a href="/checkout/" class="btn-buy-now">Mua ngay</a>
                    </div>
                </div>

                <!-- Product 3 -->
                <div class="product-card" data-brand="Sony">
                    <span class="tag-badge sale">-20%</span>
                    <span class="stock-tag">✓ Sẵn hàng</span>
                    <div class="product-img-box">🎧</div>
                    <div class="product-category">Âm thanh cao cấp</div>
                    <h3 class="product-name">Sony WH-1000XM5 Wireless</h3>
                    <div class="product-specs">Chống ồn Auto NC Optimizer • Pin 30 giờ • LDAC Hi-Res Audio</div>
                    <div class="variant-selector">
                        <span class="variant-pill active">Đen Nhám</span>
                        <span class="variant-pill">Bạc Platinum</span>
                    </div>
                    <div class="card-promo">🎁 Tặng bao da chống sốc cao cấp</div>
                    <div class="price-row">
                        <span class="current-price">7.990.000 ₫</span>
                        <span class="old-price">9.990.000 ₫</span>
                    </div>
                    <div class="card-actions">
                        <button class="btn-cart-mini" onclick="addToCart('Tai nghe Sony XM5')">Thêm giỏ</button>
                        <a href="/checkout/" class="btn-buy-now">Mua ngay</a>
                    </div>
                </div>

                <!-- Product 4 -->
                <div class="product-card" data-brand="Apple">
                    <span class="tag-badge">Chính hãng</span>
                    <span class="stock-tag">✓ Sẵn hàng</span>
                    <div class="product-img-box">⌚</div>
                    <div class="product-category">Smartwatch</div>
                    <h3 class="product-name">Apple Watch Ultra 2 49mm</h3>
                    <div class="product-specs">Khung Titan cấp hàng không • Chống nước 100m • GPS tần số kép</div>
                    <div class="variant-selector">
                        <span class="variant-pill active">Dây Alpine</span>
                        <span class="variant-pill">Dây Ocean</span>
                    </div>
                    <div class="card-promo">🎁 Trả góp 0% lãi suất qua thẻ</div>
                    <div class="price-row">
                        <span class="current-price">19.890.000 ₫</span>
                        <span class="old-price">23.490.000 ₫</span>
                    </div>
                    <div class="card-actions">
                        <button class="btn-cart-mini" onclick="addToCart('Apple Watch Ultra')">Thêm giỏ</button>
                        <a href="/checkout/" class="btn-buy-now">Mua ngay</a>
                    </div>
                </div>

                <!-- Product 5 -->
                <div class="product-card" data-brand="Apple">
                    <span class="tag-badge sale">-15%</span>
                    <span class="stock-tag">⚡ Chỉ còn 1</span>
                    <div class="product-img-box">🖥️</div>
                    <div class="product-category">Máy tính bảng</div>
                    <h3 class="product-name">iPad Pro 13" M4 OLED</h3>
                    <div class="product-specs">Màn Tandem OLED siêu mỏng 5.1mm • Chip Apple M4 thế hệ mới</div>
                    <div class="variant-selector">
                        <span class="variant-pill active">256GB Wifi</span>
                        <span class="variant-pill">512GB 5G</span>
                    </div>
                    <div class="card-promo">🎁 Giảm 30% khi mua kèm Apple Pencil Pro</div>
                    <div class="price-row">
                        <span class="current-price">36.990.000 ₫</span>
                        <span class="old-price">41.990.000 ₫</span>
                    </div>
                    <div class="card-actions">
                        <button class="btn-cart-mini" onclick="addToCart('iPad Pro M4')">Thêm giỏ</button>
                        <a href="/checkout/" class="btn-buy-now">Mua ngay</a>
                    </div>
                </div>

                <!-- Product 6 -->
                <div class="product-card" data-brand="Dell">
                    <span class="tag-badge">Hot</span>
                    <span class="stock-tag">✓ Sẵn hàng</span>
                    <div class="product-img-box">💻</div>
                    <div class="product-category">Laptop Windows</div>
                    <h3 class="product-name">Dell XPS 16 9640 Core Ultra</h3>
                    <div class="product-specs">Intel Core Ultra 7 • RTX 4060 8GB • 32GB RAM • Màn hình OLED 4K Touch</div>
                    <div class="variant-selector">
                        <span class="variant-pill active">Graphite</span>
                        <span class="variant-pill">Platinum</span>
                    </div>
                    <div class="card-promo">🎁 Tặng Balo Dell Gaming cao cấp</div>
                    <div class="price-row">
                        <span class="current-price">54.990.000 ₫</span>
                        <span class="old-price">59.990.000 ₫</span>
                    </div>
                    <div class="card-actions">
                        <button class="btn-cart-mini" onclick="addToCart('Dell XPS 16')">Thêm giỏ</button>
                        <a href="/checkout/" class="btn-buy-now">Mua ngay</a>
                    </div>
                </div>
            </div>

            <!-- Architecture Banner -->
            <div class="arch-banner">
                <h3>☁️ Cơ Chế Định Tuyến Cân Bằng Tải (AWS ALB Listener Rule)</h3>
                <p>Yêu cầu HTTP tới đường dẫn <code>/products/*</code> được Application Load Balancer so khớp bằng <strong>Listener Rule (Priority 10)</strong> và chuyển tiếp toàn bộ lưu lượng tới <strong>Target Group: tg_products</strong> chứa cụm máy chủ sản phẩm.</p>
            </div>
        </main>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="toast">Đã thêm sản phẩm vào giỏ hàng thành công!</div>

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
        var count = 2;
        function addToCart(name) {
            count++;
            document.getElementById('cartCount').innerText = count;
            showToast('Đã thêm "' + name + '" vào giỏ hàng thành công!');
        }

        function showToast(msg) {
            var t = document.getElementById('toast');
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(function() {
                t.style.display = 'none';
            }, 2500);
        }

        function filterProducts() {
            var checkboxes = document.querySelectorAll('.brand-cb');
            var selectedBrands = [];
            checkboxes.forEach(function(cb) {
                if (cb.checked) selectedBrands.push(cb.value);
            });

            var cards = document.querySelectorAll('.product-card');
            var visible = 0;
            cards.forEach(function(card) {
                var brand = card.getAttribute('data-brand');
                if (selectedBrands.includes(brand)) {
                    card.style.display = 'flex';
                    visible++;
                } else {
                    card.style.display = 'none';
                }
            });
            document.getElementById('productCount').innerText = visible;
        }

        function resetFilters() {
            document.querySelectorAll('.brand-cb').forEach(function(cb) { cb.checked = true; });
            document.getElementById('searchInput').value = '';
            filterProducts();
        }

        function searchFilter() {
            var kw = document.getElementById('searchInput').value.toLowerCase();
            var cards = document.querySelectorAll('.product-card');
            var visible = 0;
            cards.forEach(function(card) {
                var text = card.innerText.toLowerCase();
                if (text.includes(kw)) {
                    card.style.display = 'flex';
                    visible++;
                } else {
                    card.style.display = 'none';
                }
            });
            document.getElementById('productCount').innerText = visible;
        }
    </script>
</body>
</html>
EOF

cp /var/www/html/products/index.html /usr/share/nginx/html/products/index.html
cp /var/www/html/products/index.html /var/www/html/index.html
cp /var/www/html/products/index.html /usr/share/nginx/html/index.html
systemctl daemon-reload
systemctl enable nginx
systemctl restart nginx
