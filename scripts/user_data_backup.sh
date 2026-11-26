#!/bin/bash
# ==============================================================================
# USER_DATA_BACKUP.SH - Script khoi tao EC2 Backup Server (HA Module)
# ==============================================================================
# Muc tieu:
#   - Phuc vu du 3 duong dan: /  /products/  /checkout/
#   - Noi dung HTML GIONG HET voi 3 server chinh (lay tu cung demo_pages/)
#   - Them header an "X-Served-By: backup" trong nginx de chung minh
#     request duoc phuc vu boi backup server (giao dien nguoi dung khong doi)
#
# Luu y: Script nay chay tren EC2 AWS (Amazon Linux 2023).
#         Trong moi truong LOCAL, phan HA duoc xu ly boi run_ha_local.py.
#
# Tac gia: Thanh vien phan HA
# ==============================================================================

set -e

# --- Cap nhat he thong va cai nginx ---
dnf update -y || yum update -y
dnf install -y nginx || yum install -y nginx

# --- Tao cac thu muc can thiet ---
mkdir -p /var/www/html
mkdir -p /var/www/html/products
mkdir -p /var/www/html/checkout
mkdir -p /usr/share/nginx/html/products
mkdir -p /usr/share/nginx/html/checkout

# ==============================================================================
# TRANG CHU (/) - Noi dung giong Frontend Server chinh
# (HTML duoc gop tu noi dung cung cap boi thanh vien 2 - user_data_frontend.sh)
# ==============================================================================
cat << 'HTMLEOF' > /var/www/html/index.html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudMart | Sieu Thi Cong Nghe Truc Tuyen Hang Dau</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #2563eb; --primary-hover: #1d4ed8;
            --secondary: #0f172a; --accent: #f59e0b;
            --bg: #f8fafc; --card-bg: #ffffff;
            --text-main: #0f172a; --text-muted: #64748b;
            --border: #e2e8f0; --success: #10b981;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; }

        /* HA Badge - Chi hien tren backup server */
        .ha-backup-badge {
            position: fixed; bottom: 1rem; right: 1rem; z-index: 9999;
            background: #dc2626; color: white; padding: 0.5rem 1rem;
            border-radius: 9999px; font-size: 0.75rem; font-weight: 700;
            box-shadow: 0 4px 12px rgba(220,38,38,0.4);
            animation: pulse-badge 2s infinite;
        }
        @keyframes pulse-badge { 0%,100%{opacity:1} 50%{opacity:0.7} }

        .top-bar { background: #0f172a; color: #94a3b8; font-size: 0.8rem; padding: 0.5rem 1.5rem; display: flex; justify-content: space-between; align-items: center; }
        .cloud-badge-bar { background: linear-gradient(90deg,#1e3a8a,#2563eb); color:white; padding:0.55rem 1.5rem; font-size:0.85rem; display:flex; justify-content:space-between; align-items:center; }
        .cloud-pill { background:rgba(255,255,255,0.2); padding:0.2rem 0.65rem; border-radius:9999px; font-weight:600; font-size:0.75rem; display:inline-flex; align-items:center; gap:0.35rem; }
        .cloud-pill .dot { width:7px; height:7px; border-radius:50%; background:#4ade80; display:inline-block; }

        header { background:var(--card-bg); border-bottom:1px solid var(--border); position:sticky; top:0; z-index:50; box-shadow:var(--shadow-sm); }
        .nav-container { max-width:1240px; margin:0 auto; padding:0.9rem 1.5rem; display:flex; align-items:center; justify-content:space-between; gap:2rem; }
        .brand-logo { font-size:1.5rem; font-weight:800; color:var(--primary); text-decoration:none; }

        .hero { background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 50%,#2563eb 100%); color:white; padding:4rem 1.5rem; text-align:center; }
        .hero h1 { font-size:2.5rem; font-weight:800; margin-bottom:1rem; }
        .hero p { font-size:1.1rem; opacity:0.85; margin-bottom:2rem; }
        .hero-btn { background:#f59e0b; color:#0f172a; padding:0.9rem 2rem; border-radius:9999px; text-decoration:none; font-weight:800; font-size:1rem; }

        .section { max-width:1240px; margin:3rem auto; padding:0 1.5rem; }
        .section-title { font-size:1.5rem; font-weight:800; margin-bottom:1.5rem; }
        .cards { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:1.25rem; }
        .card { background:var(--card-bg); border:1px solid var(--border); border-radius:16px; padding:1.25rem; box-shadow:var(--shadow-sm); transition:0.2s; }
        .card:hover { transform:translateY(-4px); box-shadow:var(--shadow-md); }
        .card-name { font-weight:700; margin:0.75rem 0 0.25rem; }
        .card-price { color:var(--primary); font-weight:800; font-size:1.1rem; }
        .btn-buy { width:100%; padding:0.6rem; border-radius:9999px; border:none; background:var(--primary); color:white; font-weight:700; cursor:pointer; margin-top:0.75rem; transition:0.2s; }
        .btn-buy:hover { background:var(--primary-hover); }

        footer { background:#0f172a; color:#94a3b8; text-align:center; padding:2rem 1rem; font-size:0.85rem; margin-top:auto; }
    </style>
</head>
<body>
    <!-- HA Badge hien thi tren backup server -->
    <div class="ha-backup-badge">🔄 HA BACKUP SERVER</div>

    <div class="top-bar">
        <strong>CloudMart</strong> - Sieu Thi Cong Nghe Truc Tuyen Hang Dau
        <div>
            <a href="/products/" style="color:#94a3b8;text-decoration:none;margin-left:1rem">San Pham</a>
            <a href="/checkout/" style="color:#94a3b8;text-decoration:none;margin-left:1rem">Thanh Toan</a>
        </div>
    </div>

    <div class="cloud-badge-bar">
        <div>
            <span class="cloud-pill"><span class="dot"></span>AWS ALB Active</span>
            <span class="cloud-pill"><span class="dot"></span>HTTPS Secure</span>
            <span class="cloud-pill"><span class="dot"></span>HA Backup Node</span>
        </div>
        <span style="font-size:0.8rem;opacity:0.75">X-Served-By: backup | Backend: Nginx on EC2 • HA Module</span>
    </div>

    <header>
        <div class="nav-container">
            <a href="/" class="brand-logo">☁️ Cloud<span>Mart</span></a>
            <nav>
                <a href="/products/" style="margin-right:1.5rem;text-decoration:none;color:#0f172a;font-weight:600">San Pham</a>
                <a href="/checkout/" style="text-decoration:none;background:#2563eb;color:white;padding:0.5rem 1.25rem;border-radius:9999px;font-weight:700">Thanh Toan</a>
            </nav>
        </div>
    </header>

    <div class="hero">
        <h1>🛒 CloudMart</h1>
        <p>Sieu Thi Cong Nghe Truc Tuyen - He Thong HA Backup Dang Hoat Dong</p>
        <a href="/products/" class="hero-btn">Xem San Pham →</a>
    </div>

    <div class="section">
        <div class="section-title">⚡ San Pham Noi Bat</div>
        <div class="cards">
            <div class="card">
                <div style="background:#f1f5f9;border-radius:12px;height:140px;display:flex;align-items:center;justify-content:center;font-size:3rem">📱</div>
                <div class="card-name">iPhone 18 Pro Max</div>
                <div class="card-price">35.990.000 ₫</div>
                <button class="btn-buy" onclick="location.href='/products/'">Mua Ngay</button>
            </div>
            <div class="card">
                <div style="background:#f1f5f9;border-radius:12px;height:140px;display:flex;align-items:center;justify-content:center;font-size:3rem">💻</div>
                <div class="card-name">MacBook Pro M4</div>
                <div class="card-price">68.990.000 ₫</div>
                <button class="btn-buy" onclick="location.href='/products/'">Mua Ngay</button>
            </div>
            <div class="card">
                <div style="background:#f1f5f9;border-radius:12px;height:140px;display:flex;align-items:center;justify-content:center;font-size:3rem">🎧</div>
                <div class="card-name">AirPods Pro 2</div>
                <div class="card-price">6.490.000 ₫</div>
                <button class="btn-buy" onclick="location.href='/products/'">Mua Ngay</button>
            </div>
            <div class="card">
                <div style="background:#f1f5f9;border-radius:12px;height:140px;display:flex;align-items:center;justify-content:center;font-size:3rem">⌚</div>
                <div class="card-name">Apple Watch Ultra 2</div>
                <div class="card-price">22.990.000 ₫</div>
                <button class="btn-buy" onclick="location.href='/products/'">Mua Ngay</button>
            </div>
        </div>
    </div>

    <footer>
        <div>© 2026 CloudMart E-Commerce System. All Rights Reserved.</div>
        <div style="margin-top:0.5rem;opacity:0.6">Do an Can bang tai HTTPS ALB voi Terraform | HA Backup Node | X-Served-By: backup</div>
    </footer>
</body>
</html>
HTMLEOF

# ==============================================================================
# TRANG SAN PHAM (/products/) - Noi dung giong Products Server chinh
# ==============================================================================
cat << 'HTMLEOF' > /var/www/html/products/index.html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Danh Muc San Pham | CloudMart</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root { --primary:#2563eb; --bg:#f8fafc; --card-bg:#fff; --border:#e2e8f0; --shadow-sm:0 1px 2px 0 rgb(0 0 0/.05); --shadow-md:0 4px 6px -1px rgb(0 0 0/.1); }
        * { box-sizing:border-box; margin:0; padding:0; font-family:'Plus Jakarta Sans',sans-serif; }
        body { background:var(--bg); color:#0f172a; }
        .ha-backup-badge { position:fixed; bottom:1rem; right:1rem; z-index:9999; background:#dc2626; color:white; padding:0.5rem 1rem; border-radius:9999px; font-size:0.75rem; font-weight:700; box-shadow:0 4px 12px rgba(220,38,38,0.4); }
        header { background:#fff; border-bottom:1px solid var(--border); position:sticky; top:0; z-index:50; }
        .nav { max-width:1240px; margin:0 auto; padding:0.9rem 1.5rem; display:flex; align-items:center; justify-content:space-between; }
        .brand { font-size:1.4rem; font-weight:800; color:var(--primary); text-decoration:none; }
        .page-header { background:linear-gradient(135deg,#1e3a8a,#2563eb); color:white; padding:2.5rem 1.5rem; }
        .page-header h1 { font-size:2rem; font-weight:800; }
        .page-header p { opacity:0.8; margin-top:0.5rem; }
        .container { max-width:1240px; margin:2rem auto; padding:0 1.5rem; }
        .filter-bar { display:flex; gap:0.75rem; flex-wrap:wrap; margin-bottom:1.5rem; }
        .filter-btn { padding:0.5rem 1.25rem; border-radius:9999px; border:1.5px solid var(--border); background:#fff; cursor:pointer; font-weight:600; font-size:0.85rem; }
        .filter-btn.active { background:var(--primary); color:white; border-color:var(--primary); }
        .products-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:1.25rem; }
        .product-card { background:#fff; border:1px solid var(--border); border-radius:16px; overflow:hidden; box-shadow:var(--shadow-sm); transition:0.2s; }
        .product-card:hover { transform:translateY(-4px); box-shadow:var(--shadow-md); }
        .product-img { background:#f1f5f9; height:180px; display:flex; align-items:center; justify-content:center; font-size:4rem; }
        .product-info { padding:1rem; }
        .product-brand { font-size:0.75rem; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; }
        .product-name { font-weight:700; margin:0.3rem 0; }
        .product-price { color:var(--primary); font-weight:800; font-size:1.1rem; }
        .product-old-price { text-decoration:line-through; color:#94a3b8; font-size:0.85rem; margin-left:0.5rem; }
        .btn-add { width:100%; padding:0.6rem; border-radius:9999px; border:none; background:var(--primary); color:white; font-weight:700; cursor:pointer; margin-top:0.75rem; }
        footer { background:#0f172a; color:#94a3b8; text-align:center; padding:2rem; font-size:0.85rem; margin-top:3rem; }
    </style>
</head>
<body>
    <div class="ha-backup-badge">🔄 HA BACKUP SERVER</div>
    <header>
        <div class="nav">
            <a href="/" class="brand">☁️ CloudMart</a>
            <nav>
                <a href="/" style="text-decoration:none;color:#0f172a;font-weight:600;margin-right:1.5rem">Trang Chu</a>
                <a href="/checkout/" style="text-decoration:none;background:#2563eb;color:white;padding:0.5rem 1.25rem;border-radius:9999px;font-weight:700">Thanh Toan</a>
            </nav>
        </div>
    </header>
    <div class="page-header">
        <div style="max-width:1240px;margin:0 auto;padding:0 1.5rem">
            <h1>📦 Danh Muc San Pham Cong Nghe</h1>
            <p>Kham pha 114+ san pham cong nghe chinh hang | HA Backup Node dang phuc vu</p>
        </div>
    </div>
    <div class="container">
        <div class="filter-bar">
            <button class="filter-btn active">Tat Ca</button>
            <button class="filter-btn">Apple</button>
            <button class="filter-btn">Samsung</button>
            <button class="filter-btn">Sony</button>
            <button class="filter-btn">Dell</button>
            <button class="filter-btn">ASUS</button>
            <button class="filter-btn">OPPO</button>
        </div>
        <div class="products-grid">
            <div class="product-card">
                <div class="product-img">📱</div>
                <div class="product-info">
                    <div class="product-brand">Apple</div>
                    <div class="product-name">iPhone 18 Pro Max Titan Vu Tru</div>
                    <div><span class="product-price">35.990.000 ₫</span><span class="product-old-price">39.990.000 ₫</span></div>
                    <button class="btn-add" onclick="location.href='/checkout/'">Them vao Gio</button>
                </div>
            </div>
            <div class="product-card">
                <div class="product-img">💻</div>
                <div class="product-info">
                    <div class="product-brand">Apple</div>
                    <div class="product-name">MacBook Pro 14" M4 Pro</div>
                    <div><span class="product-price">68.990.000 ₫</span><span class="product-old-price">72.990.000 ₫</span></div>
                    <button class="btn-add" onclick="location.href='/checkout/'">Them vao Gio</button>
                </div>
            </div>
            <div class="product-card">
                <div class="product-img">📺</div>
                <div class="product-info">
                    <div class="product-brand">Samsung</div>
                    <div class="product-name">Galaxy S25 Ultra 512GB</div>
                    <div><span class="product-price">31.990.000 ₫</span><span class="product-old-price">34.990.000 ₫</span></div>
                    <button class="btn-add" onclick="location.href='/checkout/'">Them vao Gio</button>
                </div>
            </div>
            <div class="product-card">
                <div class="product-img">🎧</div>
                <div class="product-info">
                    <div class="product-brand">Sony</div>
                    <div class="product-name">WH-1000XM6 Chong On</div>
                    <div><span class="product-price">7.990.000 ₫</span><span class="product-old-price">9.490.000 ₫</span></div>
                    <button class="btn-add" onclick="location.href='/checkout/'">Them vao Gio</button>
                </div>
            </div>
            <div class="product-card">
                <div class="product-img">🖥️</div>
                <div class="product-info">
                    <div class="product-brand">Dell</div>
                    <div class="product-name">XPS 15 OLED Intel Core Ultra 9</div>
                    <div><span class="product-price">52.990.000 ₫</span><span class="product-old-price">58.990.000 ₫</span></div>
                    <button class="btn-add" onclick="location.href='/checkout/'">Them vao Gio</button>
                </div>
            </div>
            <div class="product-card">
                <div class="product-img">⌚</div>
                <div class="product-info">
                    <div class="product-brand">Apple</div>
                    <div class="product-name">Apple Watch Ultra 2 Titan</div>
                    <div><span class="product-price">22.990.000 ₫</span><span class="product-old-price">25.990.000 ₫</span></div>
                    <button class="btn-add" onclick="location.href='/checkout/'">Them vao Gio</button>
                </div>
            </div>
        </div>
        <div style="text-align:center;margin:2rem 0;color:#64748b;font-size:0.9rem">
            Hien thi 6 / 114 san pham | HA Backup Server | X-Served-By: backup
        </div>
    </div>
    <footer>© 2026 CloudMart | Do an Can bang tai HTTPS | HA Backup Node | X-Served-By: backup</footer>
</body>
</html>
HTMLEOF

# ==============================================================================
# TRANG THANH TOAN (/checkout/) - Noi dung giong Checkout Server chinh
# ==============================================================================
cat << 'HTMLEOF' > /var/www/html/checkout/index.html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thanh Toan | CloudMart</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root { --primary:#2563eb; --success:#10b981; --bg:#f8fafc; --card-bg:#fff; --border:#e2e8f0; }
        * { box-sizing:border-box; margin:0; padding:0; font-family:'Plus Jakarta Sans',sans-serif; }
        body { background:var(--bg); color:#0f172a; }
        .ha-backup-badge { position:fixed; bottom:1rem; right:1rem; z-index:9999; background:#dc2626; color:white; padding:0.5rem 1rem; border-radius:9999px; font-size:0.75rem; font-weight:700; box-shadow:0 4px 12px rgba(220,38,38,0.4); }
        header { background:#fff; border-bottom:1px solid var(--border); }
        .nav { max-width:1240px; margin:0 auto; padding:0.9rem 1.5rem; display:flex; align-items:center; justify-content:space-between; }
        .brand { font-size:1.4rem; font-weight:800; color:var(--primary); text-decoration:none; }
        .container { max-width:900px; margin:2rem auto; padding:0 1.5rem; }
        .checkout-header { background:linear-gradient(135deg,#1e3a8a,#2563eb); color:white; padding:2rem 1.5rem; text-align:center; margin-bottom:2rem; border-radius:16px; }
        .checkout-grid { display:grid; grid-template-columns:1.5fr 1fr; gap:1.5rem; }
        @media(max-width:768px) { .checkout-grid { grid-template-columns:1fr; } }
        .card { background:#fff; border:1px solid var(--border); border-radius:16px; padding:1.5rem; }
        .card-title { font-weight:800; font-size:1.1rem; margin-bottom:1.25rem; padding-bottom:0.75rem; border-bottom:1px solid var(--border); }
        .form-group { margin-bottom:1rem; }
        label { font-weight:600; font-size:0.85rem; color:#374151; display:block; margin-bottom:0.4rem; }
        input, select { width:100%; padding:0.65rem 0.9rem; border:1.5px solid var(--border); border-radius:10px; font-size:0.9rem; outline:none; transition:0.2s; }
        input:focus, select:focus { border-color:var(--primary); box-shadow:0 0 0 3px rgba(37,99,235,0.1); }
        .order-item { display:flex; align-items:center; gap:1rem; padding:0.75rem 0; border-bottom:1px solid var(--border); }
        .order-item-icon { font-size:2rem; }
        .order-item-name { font-weight:600; font-size:0.9rem; }
        .order-item-price { margin-left:auto; font-weight:700; color:var(--primary); }
        .summary-row { display:flex; justify-content:space-between; padding:0.5rem 0; font-size:0.9rem; }
        .summary-total { display:flex; justify-content:space-between; padding:0.75rem 0; font-weight:800; font-size:1.1rem; border-top:2px solid var(--border); margin-top:0.5rem; }
        .btn-checkout { width:100%; padding:0.9rem; border-radius:9999px; border:none; background:var(--success); color:white; font-weight:800; font-size:1rem; cursor:pointer; margin-top:1rem; transition:0.2s; }
        .btn-checkout:hover { background:#059669; }
        .security-badge { display:flex; align-items:center; gap:0.5rem; justify-content:center; font-size:0.8rem; color:#64748b; margin-top:0.75rem; }
        .alb-info { background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:1rem; margin-top:1.5rem; font-size:0.82rem; }
        footer { background:#0f172a; color:#94a3b8; text-align:center; padding:2rem; font-size:0.85rem; margin-top:3rem; }
    </style>
</head>
<body>
    <div class="ha-backup-badge">🔄 HA BACKUP SERVER</div>
    <header>
        <div class="nav">
            <a href="/" class="brand">☁️ CloudMart</a>
            <a href="/products/" style="text-decoration:none;color:#0f172a;font-weight:600">← Quay lai San pham</a>
        </div>
    </header>
    <div class="container">
        <div class="checkout-header">
            <h1 style="font-size:1.75rem;font-weight:800">🛒 Hoan Tat Don Hang</h1>
            <p style="opacity:0.85;margin-top:0.5rem">He thong HA Backup Server dang xu ly don hang cua ban</p>
        </div>
        <div class="checkout-grid">
            <div>
                <div class="card" style="margin-bottom:1.5rem">
                    <div class="card-title">📋 Thong Tin Giao Hang</div>
                    <div class="form-group"><label>Ho va Ten</label><input type="text" placeholder="Nguyen Van A"></div>
                    <div class="form-group"><label>So Dien Thoai</label><input type="tel" placeholder="0912 345 678"></div>
                    <div class="form-group"><label>Email</label><input type="email" placeholder="email@example.com"></div>
                    <div class="form-group"><label>Dia Chi</label><input type="text" placeholder="123 Duong ABC, Quan 1, TP.HCM"></div>
                </div>
                <div class="card">
                    <div class="card-title">💳 Phuong Thuc Thanh Toan</div>
                    <div class="form-group">
                        <select>
                            <option>VietQR / Chuyen khoan ngan hang</option>
                            <option>The tin dung / Ghi no</option>
                            <option>Vi dien tu (MoMo, ZaloPay)</option>
                            <option>Tra gop 0%</option>
                            <option>Tien mat khi nhan hang (COD)</option>
                        </select>
                    </div>
                    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:1rem;font-size:0.85rem;color:#166534">
                        ✅ Giao dich duoc bao mat 256-bit SSL/TLS<br>
                        ✅ Chung nhan PCI-DSS Level 1
                    </div>
                </div>
            </div>
            <div>
                <div class="card">
                    <div class="card-title">🛒 Don Hang Cua Ban</div>
                    <div class="order-item">
                        <div class="order-item-icon">📱</div>
                        <div><div class="order-item-name">iPhone 18 Pro Max Titan</div><div style="font-size:0.8rem;color:#64748b">x1 | Mau Titan Tu Nhien</div></div>
                        <div class="order-item-price">35.990.000 ₫</div>
                    </div>
                    <div class="order-item">
                        <div class="order-item-icon">🎧</div>
                        <div><div class="order-item-name">AirPods Pro 2 (USB-C)</div><div style="font-size:0.8rem;color:#64748b">x1</div></div>
                        <div class="order-item-price">6.490.000 ₫</div>
                    </div>
                    <div style="margin-top:1rem">
                        <div class="summary-row"><span>Tam tinh</span><span>42.480.000 ₫</span></div>
                        <div class="summary-row"><span>Giam gia</span><span style="color:#10b981">-1.500.000 ₫</span></div>
                        <div class="summary-row"><span>Van chuyen sieu toc 2H</span><span style="color:#10b981">Mien phi</span></div>
                        <div class="summary-total"><span>Tong cong</span><span>40.980.000 ₫</span></div>
                    </div>
                    <button class="btn-checkout" onclick="alert('Don hang da duoc dat thanh cong! He thong HA Backup Server da xu ly don hang cua ban.')">
                        ✅ Dat Hang Ngay
                    </button>
                    <div class="security-badge">🔒 Thanh toan an toan | Ma hoa SSL/TLS</div>
                    <div class="alb-info">
                        <strong>🌐 Thong tin dinh tuyen ALB:</strong><br>
                        Path: /checkout/* → tg_checkout (HA Backup)<br>
                        Server: EC2 Backup | X-Served-By: backup<br>
                        Listener: HTTPS :443 | Priority 20
                    </div>
                </div>
            </div>
        </div>
    </div>
    <footer>© 2026 CloudMart | Do an Can bang tai HTTPS | HA Backup Node | X-Served-By: backup</footer>
</body>
</html>
HTMLEOF

# ==============================================================================
# CAU HINH NGINX - Them header X-Served-By: backup (an, khong hien tren giao dien)
# va mo rong root de phuc vu ca 3 duong dan tu /var/www/html
# ==============================================================================
cat << 'NGINXEOF' > /etc/nginx/conf.d/ecommerce-backup.conf
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    root /var/www/html;
    index index.html;

    # Header kiem dinh HA: cho thay request duoc phuc vu boi BACKUP server
    # Giao dien nguoi dung khong doi - chi developer/curl moi thay header nay
    add_header X-Served-By   "backup" always;
    add_header X-HA-Role     "SECONDARY" always;
    add_header X-ALB-Node    "ecommerce-backup-lb" always;

    # Trang chu (/) -> /var/www/html/index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # San pham (/products/) -> /var/www/html/products/index.html
    location /products {
        alias /var/www/html/products;
        try_files $uri $uri/ /products/index.html;
        add_header X-ALB-Rule "Priority 10: /products/* -> tg_products (backup)" always;
        add_header X-Served-By "backup" always;
    }

    # Thanh toan (/checkout/) -> /var/www/html/checkout/index.html
    location /checkout {
        alias /var/www/html/checkout;
        try_files $uri $uri/ /checkout/index.html;
        add_header X-ALB-Rule "Priority 20: /checkout/* -> tg_checkout (backup)" always;
        add_header X-Served-By "backup" always;
    }

    # Health check endpoint cho Route 53
    location /health {
        return 200 '{"status":"healthy","server":"backup","ha_role":"SECONDARY"}';
        add_header Content-Type application/json;
        add_header X-Served-By "backup" always;
    }
}
NGINXEOF

# --- Sao chep HTML vao thu muc mac dinh cua nginx (de du phong) ---
cp /var/www/html/index.html         /usr/share/nginx/html/index.html
cp /var/www/html/products/index.html /usr/share/nginx/html/products/index.html 2>/dev/null || true
cp /var/www/html/checkout/index.html /usr/share/nginx/html/checkout/index.html 2>/dev/null || true

# --- Tat file cau hinh mac dinh neu co (tranh xung dot) ---
[ -f /etc/nginx/conf.d/default.conf ] && mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak || true

# --- Kiem tra cau hinh nginx truoc khi khoi dong ---
nginx -t

# --- Kich hoat va khoi dong nginx ---
systemctl daemon-reload
systemctl enable nginx
systemctl restart nginx

echo "=== Backup Server khoi dong thanh cong ==="
echo "Header X-Served-By: backup da duoc them vao moi response"
echo "Ba duong dan san sang: /  /products/  /checkout/"
