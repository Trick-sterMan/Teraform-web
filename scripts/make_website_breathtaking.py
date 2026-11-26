import os
import shutil
import html.parser

base = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web"
prod_path = os.path.join(base, "demo_pages/products/index.html")
fe_path = os.path.join(base, "demo_pages/frontend/index.html")
chk_path = os.path.join(base, "demo_pages/checkout/index.html")

with open(prod_path, "r", encoding="utf-8") as f:
    prod_html = f.read()

with open(fe_path, "r", encoding="utf-8") as f:
    fe_html = f.read()

with open(chk_path, "r", encoding="utf-8") as f:
    chk_html = f.read()

marquee_html = """    <!-- Dynamic Infinite Marquee Ribbon -->
    <div class="marquee-ribbon">
        <div class="marquee-content">
            <span class="marquee-badge">🔥 DEAL SỐT 2026</span>
            <span>iPhone 18 Fold Duo &amp; Pro Max chính thức cập bến CloudMart • Tặng gói AppleCare+ 2 năm trị giá 5.990.000₫</span>
            <span class="marquee-sep">✦</span>
            <span class="marquee-badge badge-green">⚡ GALAXY AI</span>
            <span>Samsung Galaxy S25 Ultra 5G AI giảm ngay 3.500.000₫ khi thanh toán VietQR</span>
            <span class="marquee-sep">✦</span>
            <span class="marquee-badge badge-blue">🚀 HỎA TỐC 2H</span>
            <span>Miễn phí giao hàng hỏa tốc trong 2 giờ nội thành Hà Nội &amp; TP.HCM • Đổi mới 1-1 trong 30 ngày</span>
            <span class="marquee-sep">✦</span>
            <span class="marquee-badge badge-purple">💎 VOUCHER 1TR</span>
            <span>Nhập mã TECH2026 giảm thêm 1.000.000₫ cho đơn hàng flagship hoặc laptop từ 25 triệu</span>
            <span class="marquee-sep">✦</span>
        </div>
        <div class="marquee-content" aria-hidden="true">
            <span class="marquee-badge">🔥 DEAL SỐT 2026</span>
            <span>iPhone 18 Fold Duo &amp; Pro Max chính thức cập bến CloudMart • Tặng gói AppleCare+ 2 năm trị giá 5.990.000₫</span>
            <span class="marquee-sep">✦</span>
            <span class="marquee-badge badge-green">⚡ GALAXY AI</span>
            <span>Samsung Galaxy S25 Ultra 5G AI giảm ngay 3.500.000₫ khi thanh toán VietQR</span>
            <span class="marquee-sep">✦</span>
            <span class="marquee-badge badge-blue">🚀 HỎA TỐC 2H</span>
            <span>Miễn phí giao hàng hỏa tốc trong 2 giờ nội thành Hà Nội &amp; TP.HCM • Đổi mới 1-1 trong 30 ngày</span>
            <span class="marquee-sep">✦</span>
            <span class="marquee-badge badge-purple">💎 VOUCHER 1TR</span>
            <span>Nhập mã TECH2026 giảm thêm 1.000.000₫ cho đơn hàng flagship hoặc laptop từ 25 triệu</span>
            <span class="marquee-sep">✦</span>
        </div>
    </div>
"""

prod_hero_html = """    <!-- Products Magnificent Hero Showcase Banner -->
    <div class="products-hero-banner">
        <div class="products-hero-inner">
            <div class="hero-left">
                <div class="hero-pill-badge">
                    <span class="live-pulse-dot"></span>
                    <span>KỶ NGUYÊN FLAGSHIP 2026 • AI-POWERED ECOSYSTEM</span>
                </div>
                <h1 class="products-hero-heading">
                    Siêu Thị Công Nghệ <span class="gradient-text">Đỉnh Cao 2026</span>
                </h1>
                <p class="products-hero-sub">
                    Trải nghiệm 114+ siêu phẩm công nghệ đột phá: <strong>iPhone 18 Fold Duo</strong> màn gập không nếp gấp, <strong>Galaxy S25 Ultra AI</strong>, <strong>MacBook Pro M3 Max</strong>. Cam kết 100% chính hãng VN/A, bảo hành 1 đổi 1 và giao hỏa tốc 2H.
                </p>
                <div class="products-hero-stats">
                    <div class="hero-stat-box">
                        <div class="stat-number">114+</div>
                        <div class="stat-label">Siêu Phẩm Flagship</div>
                    </div>
                    <div class="hero-stat-box">
                        <div class="stat-number">100%</div>
                        <div class="stat-label">Chính Hãng VN/A</div>
                    </div>
                    <div class="hero-stat-box">
                        <div class="stat-number">2H</div>
                        <div class="stat-label">Giao Siêu Tốc Nội Thành</div>
                    </div>
                    <div class="hero-stat-box">
                        <div class="stat-number">30 Ngày</div>
                        <div class="stat-label">1 Đổi 1 Miễn Phí</div>
                    </div>
                </div>
            </div>
            <div class="hero-right">
                <div class="hero-feature-card">
                    <div class="feature-card-header">
                        <span class="feature-tag">🔥 ĐỘT PHÁ MỚI</span>
                        <span class="feature-price">Từ 34.990.000₫</span>
                    </div>
                    <div class="feature-card-body">
                        <img src="/assets/real_iphone_18_duo_front.jpg" alt="iPhone 18 Fold Duo" class="feature-img">
                        <div class="feature-title">iPhone 18 Fold Duo Màn Gập</div>
                        <div class="feature-sub">Màn OLED 8.1" • Chip Apple M5 Fold • Bản lề Titanium</div>
                        <a href="#brand-apple" class="btn-feature-cta">Khám Phá Ngay →</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

ultra_modern_css = """
        /* ==============================================================
           ULTRA-MODERN 2026 LUXURY TECH STYLING (BREATHTAKING REDESIGN)
           ============================================================== */
        body {
            background-color: #f8fafc;
            background-image: 
                radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(59, 130, 246, 0.09) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(99, 102, 241, 0.07) 0px, transparent 50%);
            background-attachment: fixed;
        }

        /* Dynamic Infinite Marquee Ribbon */
        .marquee-ribbon {
            background: #090d16;
            color: #e2e8f0;
            overflow: hidden;
            white-space: nowrap;
            display: flex;
            font-size: 0.785rem;
            font-weight: 600;
            padding: 0.6rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            position: relative;
            z-index: 1000;
        }
        .marquee-content {
            display: inline-flex;
            align-items: center;
            gap: 1.25rem;
            animation: marqueeScroll 26s linear infinite;
            padding-right: 1.25rem;
            flex-shrink: 0;
        }
        .marquee-ribbon:hover .marquee-content {
            animation-play-state: paused;
        }
        @keyframes marqueeScroll {
            0% { transform: translateX(0); }
            100% { transform: translateX(-100%); }
        }
        .marquee-badge {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            font-size: 0.685rem;
            font-weight: 800;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            letter-spacing: 0.5px;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.4);
        }
        .marquee-badge.badge-green {
            background: linear-gradient(135deg, #10b981, #059669);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
        }
        .marquee-badge.badge-blue {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
        }
        .marquee-badge.badge-purple {
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.4);
        }
        .marquee-sep {
            color: #f59e0b;
            font-size: 0.75rem;
        }

        /* Top Announcement Bar Enhancement */
        .top-bar {
            background: #0f172a !important;
            color: #cbd5e1 !important;
            font-size: 0.8rem !important;
            padding: 0.55rem 1.5rem !important;
            border-bottom: 1px solid rgba(255,255,255,0.06) !important;
        }

        /* Sticky Glass Navbar */
        header {
            position: sticky !important;
            top: 0 !important;
            z-index: 999 !important;
            background: rgba(255, 255, 255, 0.94) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border-bottom: 1.5px solid #e2e8f0 !important;
            box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.08) !important;
        }
        .brand-logo {
            font-size: 1.5rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
            color: #0f172a !important;
        }
        .brand-logo span {
            background: linear-gradient(135deg, #059669, #10b981) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }
        .search-input:focus {
            border-color: #10b981 !important;
            box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.18) !important;
        }
        .cart-btn {
            background: linear-gradient(135deg, #059669, #047857) !important;
            color: white !important;
            font-weight: 800 !important;
            border-radius: 9999px !important;
            padding: 0.6rem 1.25rem !important;
            box-shadow: 0 4px 15px rgba(5, 150, 105, 0.25) !important;
            transition: all 0.25s ease !important;
        }
        .cart-btn:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4) !important;
        }

        /* Products Magnificent Hero Showcase Banner */
        .products-hero-banner {
            background: linear-gradient(135deg, #090d16 0%, #0f172a 45%, #064e3b 100%);
            color: white;
            padding: 3.5rem 1.5rem;
            position: relative;
            overflow: hidden;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.35);
        }
        .products-hero-banner::before {
            content: "";
            position: absolute;
            width: 550px;
            height: 550px;
            border-radius: 50%;
            top: -180px;
            right: 12%;
            background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, transparent 70%);
            filter: blur(60px);
            pointer-events: none;
        }
        .products-hero-banner::after {
            content: "";
            position: absolute;
            width: 420px;
            height: 420px;
            border-radius: 50%;
            bottom: -140px;
            left: 5%;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
            filter: blur(50px);
            pointer-events: none;
        }
        .products-hero-inner {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1.3fr 0.9fr;
            gap: 3rem;
            align-items: center;
            position: relative;
            z-index: 2;
        }
        @media (max-width: 1024px) {
            .products-hero-inner { grid-template-columns: 1fr; gap: 2rem; }
        }
        .hero-pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.35);
            color: #6ee7b7;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.785rem;
            font-weight: 700;
            margin-bottom: 1.25rem;
            letter-spacing: 0.5px;
        }
        .live-pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 10px #10b981;
            animation: livePulse 1.5s infinite;
        }
        @keyframes livePulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(1.4); }
        }
        .products-hero-heading {
            font-size: 2.75rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 1.25rem;
            letter-spacing: -1px;
        }
        .gradient-text {
            background: linear-gradient(135deg, #34d399, #38bdf8, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .products-hero-sub {
            font-size: 1.05rem;
            color: #cbd5e1;
            line-height: 1.65;
            margin-bottom: 2rem;
            max-width: 650px;
        }
        .products-hero-stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }
        @media (max-width: 640px) {
            .products-hero-stats { grid-template-columns: repeat(2, 1fr); }
        }
        .hero-stat-box {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 1rem;
            text-align: center;
            transition: 0.3s;
        }
        .hero-stat-box:hover {
            background: rgba(255, 255, 255, 0.14);
            transform: translateY(-3px);
            border-color: rgba(52, 211, 153, 0.45);
        }
        .stat-number {
            font-size: 1.5rem;
            font-weight: 800;
            color: #34d399;
        }
        .stat-label {
            font-size: 0.75rem;
            color: #94a3b8;
            margin-top: 0.25rem;
            font-weight: 600;
        }
        .hero-feature-card {
            background: rgba(255, 255, 255, 0.09);
            backdrop-filter: blur(16px);
            border: 1.5px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
            padding: 1.75rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
            position: relative;
            transition: 0.3s;
        }
        .hero-feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.45);
            border-color: rgba(52, 211, 153, 0.5);
        }
        .feature-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        .feature-tag {
            background: linear-gradient(135deg, #ef4444, #f59e0b);
            color: white;
            font-size: 0.72rem;
            font-weight: 800;
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
        }
        .feature-price {
            font-size: 0.95rem;
            font-weight: 800;
            color: #34d399;
        }
        .feature-card-body {
            text-align: center;
        }
        .feature-img {
            height: 180px;
            object-fit: contain;
            margin-bottom: 1rem;
            filter: drop-shadow(0 15px 25px rgba(0, 0, 0, 0.4));
            transition: 0.35s;
        }
        .hero-feature-card:hover .feature-img {
            transform: scale(1.06) translateY(-4px);
        }
        .feature-title {
            font-size: 1.2rem;
            font-weight: 800;
            color: white;
            margin-bottom: 0.35rem;
        }
        .feature-sub {
            font-size: 0.8rem;
            color: #94a3b8;
            margin-bottom: 1.25rem;
        }
        .btn-feature-cta {
            display: inline-block;
            width: 100%;
            padding: 0.75rem 1.25rem;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            font-weight: 800;
            font-size: 0.9rem;
            border-radius: 12px;
            text-decoration: none;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
            transition: 0.25s;
        }
        .btn-feature-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5);
            background: linear-gradient(135deg, #059669, #047857);
        }

        /* BRAND PILLS FILTER BAR OVERHAUL */
        .brand-nav-pills {
            display: flex !important;
            gap: 0.6rem !important;
            flex-wrap: wrap !important;
            padding: 0.25rem 0 !important;
        }
        .brand-nav-pill {
            padding: 0.55rem 1.15rem !important;
            border-radius: 9999px !important;
            border: 1.5px solid #cbd5e1 !important;
            background: #ffffff !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            color: #334155 !important;
            cursor: pointer !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03) !important;
        }
        .brand-nav-pill:hover {
            transform: translateY(-2px) !important;
            border-color: #059669 !important;
            color: #059669 !important;
            background: #ecfdf5 !important;
            box-shadow: 0 4px 12px rgba(5,150,105,0.15) !important;
        }
        .brand-nav-pill.active {
            background: linear-gradient(135deg, #059669, #047857) !important;
            color: white !important;
            border-color: #047857 !important;
            box-shadow: 0 4px 15px rgba(5,150,105,0.35) !important;
            transform: translateY(-1px) !important;
        }

        /* LUXURY PRODUCT CARD OVERHAUL */
        .product-card {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 22px !important;
            padding: 1.35rem !important;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04) !important;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
            position: relative !important;
            overflow: hidden !important;
            display: flex !important;
            flex-direction: column !important;
        }
        .product-card:hover {
            transform: translateY(-9px) scale(1.015) !important;
            box-shadow: 0 25px 45px -12px rgba(15, 23, 42, 0.15), 0 0 25px rgba(16, 185, 129, 0.12) !important;
            border-color: #10b981 !important;
        }
        .product-img-box {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
            border-radius: 18px !important;
            padding: 1.5rem 1rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            position: relative !important;
            overflow: hidden !important;
            margin-bottom: 1.1rem !important;
            border: 1px solid #edf2f7 !important;
            transition: 0.3s !important;
        }
        .product-card:hover .product-img-box {
            background: linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%) !important;
            border-color: #a7f3d0 !important;
        }
        .product-img {
            max-width: 100% !important;
            height: 200px !important;
            object-fit: contain !important;
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .product-card:hover .product-img {
            transform: scale(1.08) !important;
        }
        .tag-badge {
            position: absolute;
            top: 1rem;
            left: 1rem;
            background: linear-gradient(135deg, #ef4444, #f59e0b) !important;
            color: white !important;
            font-size: 0.72rem !important;
            font-weight: 800 !important;
            padding: 0.28rem 0.65rem !important;
            border-radius: 9999px !important;
            box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3) !important;
            z-index: 2;
        }
        .stock-tag {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(6px);
            color: #059669 !important;
            font-size: 0.7rem !important;
            font-weight: 800 !important;
            padding: 0.25rem 0.55rem !important;
            border-radius: 9999px !important;
            border: 1px solid #a7f3d0 !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
            z-index: 2;
        }
        .product-category {
            font-size: 0.75rem !important;
            font-weight: 800 !important;
            color: #10b981 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            margin-bottom: 0.35rem !important;
        }
        .product-name {
            font-size: 1.12rem !important;
            font-weight: 800 !important;
            color: #0f172a !important;
            line-height: 1.35 !important;
            margin-bottom: 0.5rem !important;
            transition: color 0.2s;
        }
        .product-card:hover .product-name {
            color: #059669;
        }
        .product-specs {
            font-size: 0.8rem !important;
            color: #64748b !important;
            line-height: 1.5 !important;
            margin-bottom: 0.85rem !important;
        }
        .product-price {
            font-size: 1.35rem !important;
            font-weight: 800 !important;
            color: #059669 !important;
            letter-spacing: -0.5px !important;
            margin-bottom: 1rem !important;
        }
        .btn-cart-mini {
            background: #ecfdf5 !important;
            color: #059669 !important;
            border: 1.5px solid #a7f3d0 !important;
            font-weight: 800 !important;
            font-size: 0.85rem !important;
            padding: 0.65rem 1rem !important;
            border-radius: 12px !important;
            transition: all 0.25s ease !important;
        }
        .btn-cart-mini:hover {
            background: #059669 !important;
            color: white !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(5,150,105,0.3) !important;
        }
        .btn-buy-now {
            background: linear-gradient(135deg, #059669, #047857) !important;
            color: white !important;
            font-weight: 800 !important;
            font-size: 0.85rem !important;
            padding: 0.65rem 1rem !important;
            border-radius: 12px !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 15px rgba(5,150,105,0.25) !important;
            border: none !important;
        }
        .btn-buy-now::after {
            content: "";
            position: absolute;
            top: -50%;
            left: -60%;
            width: 40%;
            height: 200%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transform: rotate(25deg);
            animation: btnShimmer 3s infinite;
        }
        @keyframes btnShimmer {
            0% { left: -60%; }
            25% { left: 140%; }
            100% { left: 140%; }
        }
        .btn-buy-now:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(5,150,105,0.4) !important;
        }

        /* BRAND SECTION HEADERS LUXURY OVERHAUL */
        .brand-header {
            background: linear-gradient(135deg, #ffffff, #f8fafc) !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 20px !important;
            padding: 1.25rem 1.75rem !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            border-left: 6px solid #10b981 !important;
        }
        .brand-logo-badge {
            font-size: 0.95rem !important;
            font-weight: 800 !important;
            padding: 0.4rem 0.9rem !important;
            border-radius: 9999px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
        }
        .brand-title {
            font-size: 1.25rem !important;
            font-weight: 800 !important;
            color: #0f172a !important;
        }
        .brand-count-badge {
            background: #ecfdf5 !important;
            color: #059669 !important;
            border: 1px solid #a7f3d0 !important;
            font-size: 0.8rem !important;
            font-weight: 800 !important;
            padding: 0.35rem 0.75rem !important;
            border-radius: 9999px !important;
        }
"""

# Apply to demo_pages/products/index.html
if "/* ULTRA-MODERN 2026 LUXURY TECH STYLING" not in prod_html:
    prod_html = prod_html.replace("</style>", ultra_modern_css + "\n    </style>", 1)

if 'class="marquee-ribbon"' not in prod_html:
    prod_html = prod_html.replace("<body>", "<body>\n" + marquee_html, 1)

if 'class="products-hero-banner"' not in prod_html:
    prod_html = prod_html.replace("<!-- Breadcrumb Bar -->", prod_hero_html + "\n    <!-- Breadcrumb Bar -->", 1)

with open(prod_path, "w", encoding="utf-8") as f:
    f.write(prod_html)
print("Updated demo_pages/products/index.html successfully!")

# Apply to demo_pages/frontend/index.html
fe_extra_css = """
        /* Dynamic Infinite Marquee Ribbon */
        .marquee-ribbon {
            background: #090d16;
            color: #e2e8f0;
            overflow: hidden;
            white-space: nowrap;
            display: flex;
            font-size: 0.785rem;
            font-weight: 600;
            padding: 0.6rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            position: relative;
            z-index: 1000;
        }
        .marquee-content {
            display: inline-flex;
            align-items: center;
            gap: 1.25rem;
            animation: marqueeScroll 26s linear infinite;
            padding-right: 1.25rem;
            flex-shrink: 0;
        }
        .marquee-ribbon:hover .marquee-content {
            animation-play-state: paused;
        }
        @keyframes marqueeScroll {
            0% { transform: translateX(0); }
            100% { transform: translateX(-100%); }
        }
        .marquee-badge {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            font-size: 0.685rem;
            font-weight: 800;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            letter-spacing: 0.5px;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.4);
        }
        .marquee-badge.badge-green {
            background: linear-gradient(135deg, #10b981, #059669);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
        }
        .marquee-badge.badge-blue {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
        }
        .marquee-badge.badge-purple {
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.4);
        }
        .marquee-sep {
            color: #f59e0b;
            font-size: 0.75rem;
        }

        /* Flash Sale Live Ribbon */
        .flash-sale-ribbon {
            background: linear-gradient(135deg, #ef4444, #f59e0b);
            color: white;
            border-radius: 18px;
            padding: 1rem 1.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(239, 68, 68, 0.25);
            flex-wrap: wrap;
            gap: 1rem;
        }
        .flash-sale-left {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .flash-sale-icon {
            font-size: 1.5rem;
            animation: bounce 1s infinite alternate;
        }
        @keyframes bounce {
            from { transform: translateY(0); }
            to { transform: translateY(-3px); }
        }
        .flash-sale-title {
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: 0.5px;
        }
        .flash-sale-badge {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(4px);
            font-size: 0.75rem;
            font-weight: 800;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
        }
        .flash-sale-timer {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .timer-label {
            font-size: 0.85rem;
            font-weight: 600;
            opacity: 0.9;
        }
        .timer-boxes {
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }
        .timer-box {
            background: #0f172a;
            color: white;
            font-size: 1.1rem;
            font-weight: 800;
            padding: 0.35rem 0.65rem;
            border-radius: 8px;
            min-width: 38px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .timer-colon {
            font-size: 1.2rem;
            font-weight: 800;
        }

        /* LUXURY PRODUCT CARD OVERHAUL FOR FRONTEND */
        .product-card {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 22px !important;
            padding: 1.35rem !important;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04) !important;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .product-card:hover {
            transform: translateY(-9px) scale(1.015) !important;
            box-shadow: 0 25px 45px -12px rgba(15, 23, 42, 0.15), 0 0 25px rgba(37, 99, 235, 0.15) !important;
            border-color: #2563eb !important;
        }
        .product-card:hover .product-img {
            transform: scale(1.08) !important;
        }
"""

if 'class="marquee-ribbon"' not in fe_html:
    fe_html = fe_html.replace("<body>", "<body>\n" + marquee_html, 1)

if "/* Flash Sale Live Ribbon */" not in fe_html:
    fe_html = fe_html.replace("</style>", fe_extra_css + "\n    </style>", 1)

flash_sale_html = """        <!-- Live Flash Sale Countdown Ribbon -->
        <div class="flash-sale-ribbon">
            <div class="flash-sale-left">
                <span class="flash-sale-icon">⚡</span>
                <span class="flash-sale-title">GIỜ VÀNG CÔNG NGHỆ • GIẢM ĐẾN 40%</span>
                <span class="flash-sale-badge">HÔM NAY</span>
            </div>
            <div class="flash-sale-timer">
                <span class="timer-label">Kết thúc trong:</span>
                <div class="timer-boxes">
                    <span class="timer-box" id="flashHours">05</span>
                    <span class="timer-colon">:</span>
                    <span class="timer-box" id="flashMins">42</span>
                    <span class="timer-colon">:</span>
                    <span class="timer-box" id="flashSecs">18</span>
                </div>
            </div>
        </div>
"""

target_str = '<h2 class="section-title">Sản Phẩm Bán Chạy Nhất</h2>'
if 'class="flash-sale-ribbon"' not in fe_html and target_str in fe_html:
    fe_html = fe_html.replace(target_str, flash_sale_html + "\n        " + target_str, 1)

flash_timer_js = """
        // Live Flash Sale Countdown Timer
        var fHours = 5, fMins = 42, fSecs = 18;
        setInterval(function() {
            if (fSecs > 0) {
                fSecs--;
            } else {
                fSecs = 59;
                if (fMins > 0) {
                    fMins--;
                } else {
                    fMins = 59;
                    if (fHours > 0) fHours--;
                }
            }
            var hEl = document.getElementById('flashHours');
            var mEl = document.getElementById('flashMins');
            var sEl = document.getElementById('flashSecs');
            if (hEl && mEl && sEl) {
                hEl.innerText = fHours < 10 ? '0' + fHours : fHours;
                mEl.innerText = fMins < 10 ? '0' + fMins : fMins;
                sEl.innerText = fSecs < 10 ? '0' + fSecs : fSecs;
            }
        }, 1000);
"""

if "Live Flash Sale Countdown Timer" not in fe_html:
    fe_html = fe_html.replace("</script>", flash_timer_js + "\n    </script>", 1)

with open(fe_path, "w", encoding="utf-8") as f:
    f.write(fe_html)
print("Updated demo_pages/frontend/index.html successfully!")

# Sync to nested directory
shutil.copyfile(prod_path, os.path.join(base, "demo_pages/products/products/index.html"))
shutil.copyfile(chk_path, os.path.join(base, "demo_pages/checkout/checkout/index.html"))
print("Synchronized nested directories!")

# Sync to scripts/user_data_*.sh
with open(prod_path, "r", encoding="utf-8") as f:
    final_prod = f.read()

with open(fe_path, "r", encoding="utf-8") as f:
    final_fe = f.read()

with open(chk_path, "r", encoding="utf-8") as f:
    final_chk = f.read()

fe_script = f"""#!/bin/bash
# ==============================================================================
# Script khởi tạo Frontend Server (Trang chủ) - Siêu thực tế thương mại điện tử
# ==============================================================================
set -e

dnf update -y || yum update -y
dnf install -y nginx || yum install -y nginx

mkdir -p /var/www/html
mkdir -p /usr/share/nginx/html

cat << 'EOF' > /var/www/html/index.html
{final_fe}
EOF

systemctl enable nginx
systemctl restart nginx
"""

with open(os.path.join(base, "scripts/user_data_frontend.sh"), "w", encoding="utf-8") as f:
    f.write(fe_script)

prod_script = f"""#!/bin/bash
# ==============================================================================
# Script khởi tạo Products Server (Trang sản phẩm) - Siêu thực tế thương mại điện tử
# ==============================================================================
set -e

dnf update -y || yum update -y
dnf install -y nginx || yum install -y nginx

mkdir -p /var/www/html/products
mkdir -p /usr/share/nginx/html/products

cat << 'EOF' > /var/www/html/products/index.html
{final_prod}
EOF

systemctl enable nginx
systemctl restart nginx
"""

with open(os.path.join(base, "scripts/user_data_products.sh"), "w", encoding="utf-8") as f:
    f.write(prod_script)

chk_script = f"""#!/bin/bash
# ==============================================================================
# Script khởi tạo Checkout Server (Cổng thanh toán & Hóa đơn)
# ==============================================================================
set -e

dnf update -y || yum update -y
dnf install -y nginx || yum install -y nginx

mkdir -p /var/www/html/checkout
mkdir -p /usr/share/nginx/html/checkout

cat << 'EOF' > /var/www/html/checkout/index.html
{final_chk}
EOF

systemctl enable nginx
systemctl restart nginx
"""

with open(os.path.join(base, "scripts/user_data_checkout.sh"), "w", encoding="utf-8") as f:
    f.write(chk_script)

print("Updated user_data_*.sh scripts successfully!")

# Strict HTML verification
class StrictHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.void_tags:
            self.stack.append((tag.lower(), self.getpos()))

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in self.void_tags:
            return
        if not self.stack:
            self.errors.append(f'Unexpected end tag </{t}> at {self.getpos()}')
            return
        last, pos = self.stack.pop()
        if last != t:
            self.errors.append(f'Mismatched tag: expected </{last}> (opened at {pos}), found </{t}> at {self.getpos()}')

all_passed = True
for path in [prod_path, fe_path, chk_path, os.path.join(base, "demo_pages/products/products/index.html"), os.path.join(base, "demo_pages/checkout/checkout/index.html")]:
    parser = StrictHTMLParser()
    with open(path, "r", encoding="utf-8") as handle:
        parser.feed(handle.read())
    print(f"Validated {os.path.relpath(path, base)}: Errors={len(parser.errors)}, Unclosed={len(parser.stack)}")
    if parser.errors or parser.stack:
        all_passed = False
        for e in parser.errors[:3]:
            print(f"  Error: {e}")
        for t, pos in parser.stack[-3:]:
            print(f"  Unclosed: <{t}> at {pos}")

if all_passed:
    print("SUCCESS: ALL HTML FILES VALIDATED WITH 0 ERRORS AND 0 UNCLOSED TAGS!")
else:
    print("WARNING: Some HTML files have validation issues!")
