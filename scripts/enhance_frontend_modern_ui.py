import re
import os

base_dir = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web"
frontend_path = os.path.join(base_dir, "demo_pages/frontend/index.html")

with open(frontend_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add modern CSS enhancements
modern_css = '''
        /* ==============================================================
           GIAO DIỆN HIỆN ĐẠI & SỐNG ĐỘNG (MODERN ULTRA-TECH STYLING)
           ============================================================== */
        body {
            background-color: #f8fafc;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.07) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(16, 185, 129, 0.05) 0px, transparent 50%);
            background-attachment: fixed;
        }

        /* Ambient Glow & Floating Animations */
        .hero-slider-wrap {
            position: relative;
            border-radius: 28px;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.25);
        }
        .hero-card.slide {
            display: none;
            border-radius: 28px;
            padding: 3.5rem 3.5rem;
            color: white;
            align-items: center;
            justify-content: space-between;
            overflow: hidden;
            position: relative;
            min-height: 440px;
            animation: fadeInSlide 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .hero-card.slide.active {
            display: flex;
        }
        @keyframes fadeInSlide {
            from { opacity: 0; transform: scale(0.985); }
            to { opacity: 1; transform: scale(1); }
        }

        .hero-ambient-orb {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            filter: blur(40px);
            z-index: 1;
        }
        .hero-ambient-orb.orb-1 {
            width: 320px;
            height: 320px;
            top: -60px;
            right: 15%;
            background: radial-gradient(circle, rgba(124, 58, 237, 0.35) 0%, transparent 70%);
            animation: floatOrb 8s ease-in-out infinite alternate;
        }
        .hero-ambient-orb.orb-2 {
            width: 260px;
            height: 260px;
            bottom: -50px;
            right: 5%;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%);
            animation: floatOrb 6s ease-in-out infinite alternate-reverse;
        }
        @keyframes floatOrb {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(-25px, 20px) scale(1.15); }
        }

        .pulse-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #a5b4fc;
            display: inline-block;
            box-shadow: 0 0 10px #a5b4fc;
            animation: pulseGlow 1.6s infinite ease-in-out;
        }
        @keyframes pulseGlow {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.4); opacity: 0.6; }
        }

        .hero-highlight-chips {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }
        .hero-chip {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(8px);
            padding: 0.3rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.785rem;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #f8fafc;
        }

        /* Shimmering CTA Button */
        .btn-shimmer {
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.3);
        }
        .btn-shimmer::after {
            content: "";
            position: absolute;
            top: -50%;
            left: -60%;
            width: 40%;
            height: 200%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transform: rotate(25deg);
            animation: shimmerSweep 3.5s infinite;
        }
        @keyframes shimmerSweep {
            0% { left: -60%; }
            25% { left: 140%; }
            100% { left: 140%; }
        }

        /* Glass Product Showcase in Hero */
        .hero-img-glass-wrap {
            position: relative;
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
            padding: 1.25rem;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
            transition: transform 0.4s ease;
        }
        .hero-img-glass-wrap:hover {
            transform: translateY(-6px) scale(1.02);
        }
        .hero-main-img {
            width: 100%;
            height: 260px;
            object-fit: cover;
            border-radius: 16px;
            display: block;
            background: #ffffff;
        }
        .hero-float-badge {
            position: absolute;
            bottom: -15px;
            right: -15px;
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(10px);
            border: 1.5px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 0.65rem 1rem;
            color: white;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            box-shadow: 0 15px 30px rgba(0,0,0,0.4);
            animation: floatBadge 3.5s ease-in-out infinite alternate;
        }
        @keyframes floatBadge {
            0% { transform: translateY(0); }
            100% { transform: translateY(-8px); }
        }
        .badge-icon {
            font-size: 1.5rem;
        }
        .hero-float-badge strong {
            display: block;
            font-size: 0.825rem;
            font-weight: 800;
            color: #facc15;
        }
        .hero-float-badge span {
            font-size: 0.72rem;
            color: #cbd5e1;
        }

        /* Slider Controls */
        .hero-arrow {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: white;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 10;
            transition: all 0.2s ease;
            line-height: 1;
        }
        .hero-arrow:hover {
            background: white;
            color: #0f172a;
            transform: translateY(-50%) scale(1.1);
        }
        .hero-arrow.prev { left: 1rem; }
        .hero-arrow.next { right: 1rem; }

        .hero-dots {
            position: absolute;
            bottom: 1.25rem;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 0.6rem;
            z-index: 10;
        }
        .hero-dot {
            width: 10px;
            height: 10px;
            border-radius: 9999px;
            background: rgba(255, 255, 255, 0.35);
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            padding: 0;
        }
        .hero-dot.active {
            width: 32px;
            background: #ffffff;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
        }

        /* Brand Bar */
        .brand-bar-wrap {
            background: white;
            border: 1.5px solid #e2e8f0;
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        }
        .brand-bar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid #f1f5f9;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .brand-bar-title {
            font-size: 0.85rem;
            font-weight: 800;
            color: #1e293b;
            letter-spacing: 0.04em;
        }
        .brand-bar-sub {
            font-size: 0.785rem;
            color: #64748b;
        }
        .brand-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(135px, 1fr));
            gap: 0.85rem;
        }
        .brand-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 0.85rem 0.5rem;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            text-decoration: none;
            color: #1e293b;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .brand-item:hover {
            transform: translateY(-4px);
            background: white;
            box-shadow: 0 8px 20px rgba(0,0,0,0.06);
            border-color: #cbd5e1;
        }
        .brand-item .brand-icon {
            font-size: 1.75rem;
            margin-bottom: 0.35rem;
            transition: transform 0.2s;
        }
        .brand-item:hover .brand-icon {
            transform: scale(1.15);
        }
        .brand-item .brand-name {
            font-size: 0.875rem;
            font-weight: 800;
        }
        .brand-item .brand-count {
            font-size: 0.72rem;
            color: #64748b;
            margin-top: 2px;
        }
        .brand-item.apple:hover { border-color: #0f172a; }
        .brand-item.samsung:hover { border-color: #2563eb; }
        .brand-item.sony:hover { border-color: #f59e0b; }
        .brand-item.asus:hover { border-color: #ef4444; }

        /* Modern Product Card Enhancements */
        .product-card {
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 20px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.04) !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .product-card:hover {
            transform: translateY(-7px) scale(1.01) !important;
            box-shadow: 0 20px 35px -10px rgba(0,0,0,0.12) !important;
            border-color: #93c5fd !important;
        }
        .product-card .tag-discount {
            border-radius: 8px !important;
            box-shadow: 0 4px 10px rgba(239, 68, 68, 0.35);
        }
        .product-card .btn-add-cart {
            border-radius: 12px !important;
            position: relative;
            overflow: hidden;
            font-weight: 800 !important;
            transition: all 0.25s ease !important;
        }
        .product-card .btn-add-cart:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(37, 99, 235, 0.35);
        }

        /* Live Purchase Notification (Social Proof Toast) */
        .live-sales-toast {
            position: fixed;
            bottom: 1.5rem;
            left: 1.5rem;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1.5px solid #cbd5e1;
            border-radius: 16px;
            padding: 0.75rem 1.1rem;
            display: flex;
            align-items: center;
            gap: 0.85rem;
            box-shadow: 0 15px 35px -5px rgba(0,0,0,0.18);
            z-index: 990;
            animation: slideUpToast 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            max-width: 360px;
            transition: opacity 0.3s, transform 0.3s;
        }
        @keyframes slideUpToast {
            from { transform: translateY(40px) scale(0.95); opacity: 0; }
            to { transform: translateY(0) scale(1); opacity: 1; }
        }
        .live-toast-avatar {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(135deg, #dbeafe, #eff6ff);
            border: 1px solid #bfdbfe;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.35rem;
            flex-shrink: 0;
        }
        .live-toast-content {
            flex: 1;
            min-width: 0;
        }
        .live-toast-header {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .live-toast-user {
            font-size: 0.825rem;
            font-weight: 800;
            color: #0f172a;
        }
        .live-toast-badge {
            background: #dcfce7;
            color: #15803d;
            font-size: 0.675rem;
            font-weight: 700;
            padding: 1px 6px;
            border-radius: 4px;
        }
        .live-toast-product {
            font-size: 0.8rem;
            font-weight: 700;
            color: #2563eb;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-top: 1px;
        }
        .live-toast-meta {
            font-size: 0.7rem;
            color: #64748b;
            margin-top: 2px;
        }
        .live-toast-close {
            background: none;
            border: none;
            color: #94a3b8;
            cursor: pointer;
            font-size: 1rem;
            padding: 2px;
            transition: 0.2s;
        }
        .live-toast-close:hover {
            color: #ef4444;
        }

        /* Radar Wave on Floating CSKH Button */
        .chat-widget-btn {
            position: fixed;
            bottom: 1.5rem;
            right: 1.5rem;
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            width: 58px;
            height: 58px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4);
            cursor: pointer;
            border: 2px solid rgba(255,255,255,0.3);
            z-index: 990;
            transition: all 0.25s ease;
        }
        .chat-widget-btn:hover {
            transform: translateY(-3px) scale(1.06);
            box-shadow: 0 14px 30px rgba(37, 99, 235, 0.5);
        }
        .chat-widget-btn::before {
            content: '';
            position: absolute;
            inset: -6px;
            border-radius: 50%;
            border: 2px solid #60a5fa;
            animation: radarPulse 2.2s infinite ease-out;
            pointer-events: none;
        }
        @keyframes radarPulse {
            0% { transform: scale(0.9); opacity: 1; }
            100% { transform: scale(1.45); opacity: 0; }
        }
'''

html = html.replace('</style>', modern_css + '\n    </style>', 1)

# 2. Replace the static Hero Section with the Interactive Multi-Slide Hero Slider
new_hero_section = '''    <!-- Hero Banner Section: Interactive Multi-Slide Tech Showcase -->
    <section class="hero-section">
        <div class="hero-slider-wrap">
            <!-- Slide 0: iPhone 18 Fold Duo & 18 Pro Max -->
            <div class="hero-card slide active" data-slide="0" style="background: linear-gradient(135deg, #090d16 0%, #1e1b4b 45%, #4338ca 100%);">
                <div class="hero-ambient-orb orb-1"></div>
                <div class="hero-ambient-orb orb-2"></div>
                <div class="hero-content">
                    <div class="hero-tag" style="background: rgba(99, 102, 241, 0.25); border: 1px solid rgba(165, 180, 252, 0.4); color: #e0e7ff;">
                        <span class="pulse-indicator"></span> 🚀 ĐỘT PHÁ CÔNG NGHỆ 2026
                    </div>
                    <h1 class="hero-title">
                        iPhone 18 Fold Duo &amp; Pro Max
                    </h1>
                    <p class="hero-desc">
                        Tuyệt tác màn hình kép Dynamic Duo OLED 8.1" không nếp gấp • Chip Apple M5 Fold Edition • Khung bản lề Titanium Liquid Metal siêu bền.
                    </p>
                    <div class="hero-highlight-chips">
                        <span class="hero-chip">✨ Màn gập Dynamic Duo 8.1"</span>
                        <span class="hero-chip">⚡ Chip Apple M5 siêu mạnh</span>
                        <span class="hero-chip">🛡️ Bản lề Liquid Metal</span>
                    </div>
                    <div class="hero-actions">
                        <a href="/products/" class="btn-cta btn-shimmer">
                            <span>Khám Phá Siêu Phẩm &rarr;</span>
                        </a>
                        <a href="/products/" class="btn-secondary-cta">Xem Tất Cả Danh Mục</a>
                    </div>
                </div>
                <div class="hero-visual">
                    <div class="hero-img-glass-wrap">
                        <img src="/assets/real_iphone_18_duo_fold.jpg" alt="iPhone 18 Fold Duo" class="hero-main-img">
                        <div class="hero-float-badge">
                            <span class="badge-icon">👑</span>
                            <div>
                                <strong>Bản Concept 2026</strong>
                                <span>Đặt trước đặc quyền VIP</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Slide 1: Samsung Galaxy S25 Ultra 5G AI & Z Fold SE -->
            <div class="hero-card slide" data-slide="1" style="background: linear-gradient(135deg, #022c22 0%, #064e3b 45%, #059669 100%);">
                <div class="hero-ambient-orb orb-1" style="background: radial-gradient(circle, rgba(16,185,129,0.3) 0%, transparent 70%);"></div>
                <div class="hero-ambient-orb orb-2" style="background: radial-gradient(circle, rgba(52,211,153,0.2) 0%, transparent 70%);"></div>
                <div class="hero-content">
                    <div class="hero-tag" style="background: rgba(16, 185, 129, 0.25); border: 1px solid rgba(167, 243, 208, 0.4); color: #d1fae5;">
                        <span class="pulse-indicator" style="background: #34d399;"></span> ⚡ THẾ HỆ GALAXY AI 2025
                    </div>
                    <h1 class="hero-title">
                        Galaxy S25 Ultra &amp; Z Fold SE
                    </h1>
                    <p class="hero-desc">
                        Trí tuệ nhân tạo Galaxy AI đỉnh cao thế hệ mới • Camera 200MP bắt trọn chi tiết sắc nét • Z Fold Special Edition mỏng kỷ lục 10.6mm siêu sang.
                    </p>
                    <div class="hero-highlight-chips">
                        <span class="hero-chip">🔮 Galaxy AI Thế Hệ Mới</span>
                        <span class="hero-chip">📸 Camera 200MP AI Zoom</span>
                        <span class="hero-chip">📏 Mỏng kỷ lục 10.6mm</span>
                    </div>
                    <div class="hero-actions">
                        <a href="/products/" class="btn-cta btn-shimmer" style="background: #ffffff; color: #064e3b;">
                            <span>Đặt Trước Nhận Ưu Đãi &rarr;</span>
                        </a>
                        <a href="/products/" class="btn-secondary-cta">Xem Dòng Galaxy</a>
                    </div>
                </div>
                <div class="hero-visual">
                    <div class="hero-img-glass-wrap">
                        <img src="/assets/real_samsung_s25_ultra_silverblue.jpg" alt="Galaxy S25 Ultra" class="hero-main-img">
                        <div class="hero-float-badge" style="border-color: rgba(52,211,153,0.3);">
                            <span class="badge-icon">⚡</span>
                            <div>
                                <strong>Snapdragon 8 Elite</strong>
                                <span>3nm Siêu Hiệu Năng AI</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Slide 2: MacBook Pro M3 Max & Hiệu Năng Pro -->
            <div class="hero-card slide" data-slide="2" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 45%, #2563eb 100%);">
                <div class="hero-ambient-orb orb-1" style="background: radial-gradient(circle, rgba(59,130,246,0.3) 0%, transparent 70%);"></div>
                <div class="hero-ambient-orb orb-2" style="background: radial-gradient(circle, rgba(147,197,253,0.2) 0%, transparent 70%);"></div>
                <div class="hero-content">
                    <div class="hero-tag" style="background: rgba(59, 130, 246, 0.25); border: 1px solid rgba(191, 219, 254, 0.4); color: #dbeafe;">
                        <span class="pulse-indicator" style="background: #60a5fa;"></span> 💻 CHIẾN HẠM ĐỒ HỌA M3 MAX
                    </div>
                    <h1 class="hero-title">
                        MacBook Pro 16" &amp; Sony Hi-Res
                    </h1>
                    <p class="hero-desc">
                        Cấu hình bất khả chiến bại Apple M3 Max 16-Core CPU / 40-Core GPU • Màn hình Liquid Retina XDR 120Hz chuẩn rạp chiếu phim • Âm thanh Dolby Atmos.
                    </p>
                    <div class="hero-highlight-chips">
                        <span class="hero-chip">🚀 40-Core GPU Quái Vật</span>
                        <span class="hero-chip">🌈 Liquid Retina XDR 120Hz</span>
                        <span class="hero-chip">🔋 Pin ấn tượng 22 Giờ</span>
                    </div>
                    <div class="hero-actions">
                        <a href="/products/" class="btn-cta btn-shimmer" style="background: #ffffff; color: #1e3a8a;">
                            <span>Sở Hữu Ngay &rarr;</span>
                        </a>
                        <a href="/checkout/" class="btn-secondary-cta">Giỏ Hàng &amp; Thanh Toán</a>
                    </div>
                </div>
                <div class="hero-visual">
                    <div class="hero-img-glass-wrap">
                        <img src="/assets/macbook_pro_silver.jpg" alt="MacBook Pro M3 Max" class="hero-main-img">
                        <div class="hero-float-badge">
                            <span class="badge-icon">🔥</span>
                            <div>
                                <strong>Apple M3 Max</strong>
                                <span>128GB RAM Thống Nhất</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Slider Navigation Controls -->
            <button type="button" class="hero-arrow prev" onclick="changeHeroSlide(-1)" aria-label="Slide trước">‹</button>
            <button type="button" class="hero-arrow next" onclick="changeHeroSlide(1)" aria-label="Slide tiếp">›</button>

            <!-- Slider Dots -->
            <div class="hero-dots">
                <button type="button" class="hero-dot active" onclick="setHeroSlide(0)"></button>
                <button type="button" class="hero-dot" onclick="setHeroSlide(1)"></button>
                <button type="button" class="hero-dot" onclick="setHeroSlide(2)"></button>
            </div>
        </div>
    </section>'''

hero_old_pattern = r'<!-- Hero Banner Section -->\s*<section class="hero-section">[\s\S]*?</section>'
html = re.sub(hero_old_pattern, new_hero_section, html)

# 3. Add the Interactive Brand Showcase Section right after Trust Badges
brand_section = '''    <!-- Interactive Brand Showcase Section -->
    <section class="section-container" style="margin-top: 1rem; margin-bottom: 2rem;">
        <div class="brand-bar-wrap">
            <div class="brand-bar-header">
                <span class="brand-bar-title">⭐ HỆ SINH THÁI THƯƠNG HIỆU HÀNG ĐẦU TẠI CLOUDMART</span>
                <span class="brand-bar-sub">Cam kết phân phối chính hãng 100% đầy đủ hóa đơn VAT &amp; Bảo hành ủy quyền 12-24 tháng</span>
            </div>
            <div class="brand-grid">
                <a href="/products/" class="brand-item apple">
                    <span class="brand-icon">🍏</span>
                    <span class="brand-name">Apple</span>
                    <span class="brand-count">iPhone, Mac, iPad</span>
                </a>
                <a href="/products/" class="brand-item samsung">
                    <span class="brand-icon">💫</span>
                    <span class="brand-name">Samsung</span>
                    <span class="brand-count">Galaxy S25, Z Fold</span>
                </a>
                <a href="/products/" class="brand-item sony">
                    <span class="brand-icon">🎧</span>
                    <span class="brand-name">Sony</span>
                    <span class="brand-count">Tai nghe, PS5 Pro</span>
                </a>
                <a href="/products/" class="brand-item dell">
                    <span class="brand-icon">💻</span>
                    <span class="brand-name">Dell</span>
                    <span class="brand-count">XPS 13/16, Alienware</span>
                </a>
                <a href="/products/" class="brand-item asus">
                    <span class="brand-icon">🎮</span>
                    <span class="brand-name">ASUS ROG</span>
                    <span class="brand-count">Gaming Phone &amp; PC</span>
                </a>
                <a href="/products/" class="brand-item xiaomi">
                    <span class="brand-icon">⚡</span>
                    <span class="brand-name">Xiaomi</span>
                    <span class="brand-count">15 Pro Leica Flagship</span>
                </a>
                <a href="/products/" class="brand-item marshall">
                    <span class="brand-icon">📻</span>
                    <span class="brand-name">Marshall</span>
                    <span class="brand-count">Loa &amp; Tai Nghe UK</span>
                </a>
            </div>
        </div>
    </section>'''

trust_grid_end = '    <!-- Trust Badges -->\n    <div class="trust-grid">[\s\S]*?    </div>'
html = re.sub(trust_grid_end, lambda m: m.group(0) + '\n\n' + brand_section, html)

# 4. Add the Live Purchase Social Proof Toast markup before </body>
live_toast_markup = '''    <!-- Real-time Purchase Social Proof Toast -->
    <div class="live-sales-toast" id="liveSalesToast">
        <div class="live-toast-avatar" id="liveToastAvatar">🛒</div>
        <div class="live-toast-content">
            <div class="live-toast-header">
                <span class="live-toast-user" id="liveToastUser">Anh Quốc Hùng (TP.HCM)</span>
                <span class="live-toast-badge">Vừa mua</span>
            </div>
            <div class="live-toast-product" id="liveToastProduct">iPhone 18 Pro Max Titan Vũ Trụ</div>
            <div class="live-toast-meta">
                <span id="liveToastTime">2 phút trước</span> • <span>Giao hỏa tốc 2H</span>
            </div>
        </div>
        <button type="button" class="live-toast-close" onclick="closeLiveToast()" title="Đóng">✕</button>
    </div>
'''

html = html.replace('</body>', live_toast_markup + '\n</body>', 1)

# 5. Add Slider & Social Proof JS logic
slider_js = '''
        // ==============================================================
        // TƯƠNG TÁC HERO SLIDER & SOCIAL PROOF THỜI GIAN THỰC
        // ==============================================================
        var currentHeroSlide = 0;
        var totalHeroSlides = 3;
        var heroAutoTimer = null;

        function showHeroSlide(idx) {
            currentHeroSlide = (idx + totalHeroSlides) % totalHeroSlides;
            var slides = document.querySelectorAll('.hero-card.slide');
            var dots = document.querySelectorAll('.hero-dot');
            slides.forEach(function(s, i) {
                if (i === currentHeroSlide) s.classList.add('active');
                else s.classList.remove('active');
            });
            dots.forEach(function(d, i) {
                if (i === currentHeroSlide) d.classList.add('active');
                else d.classList.remove('active');
            });
        }

        function changeHeroSlide(delta) {
            showHeroSlide(currentHeroSlide + delta);
            resetHeroTimer();
        }

        function setHeroSlide(idx) {
            showHeroSlide(idx);
            resetHeroTimer();
        }

        function resetHeroTimer() {
            if (heroAutoTimer) clearInterval(heroAutoTimer);
            heroAutoTimer = setInterval(function() {
                changeHeroSlide(1);
            }, 5500);
        }
        resetHeroTimer();

        // Pause on slider hover
        var sliderWrap = document.querySelector('.hero-slider-wrap');
        if (sliderWrap) {
            sliderWrap.addEventListener('mouseenter', function() { if (heroAutoTimer) clearInterval(heroAutoTimer); });
            sliderWrap.addEventListener('mouseleave', function() { resetHeroTimer(); });
        }

        // Live Purchase Toast Notifications
        var livePurchases = [
            { user: "Anh Quốc Hùng (TP.HCM)", product: "iPhone 18 Pro Max Titan Vũ Trụ", time: "2 phút trước", avatar: "📱" },
            { user: "Chị Thanh Thảo (Hà Nội)", product: "Samsung Galaxy S25 Ultra 5G AI", time: "4 phút trước", avatar: "💫" },
            { user: "Anh Đức Trọng (Đà Nẵng)", product: "MacBook Pro 16\" M3 Max Silver", time: "7 phút trước", avatar: "💻" },
            { user: "Chị Ngọc Mai (Hải Phòng)", product: "iPhone 18 Fold Duo Màn Gập", time: "9 phút trước", avatar: "👑" },
            { user: "Anh Tuấn Kiệt (Bình Dương)", product: "Tai nghe Sony WH-1000XM5 Hi-Res", time: "12 phút trước", avatar: "🎧" },
            { user: "Anh Minh Khang (Cần Thơ)", product: "Galaxy Z Fold Special Edition", time: "15 phút trước", avatar: "⚡" }
        ];
        var liveIdx = 0;

        function updateLiveToast() {
            var item = livePurchases[liveIdx % livePurchases.length];
            var toast = document.getElementById('liveSalesToast');
            if (!toast) return;

            document.getElementById('liveToastUser').innerText = item.user;
            document.getElementById('liveToastProduct').innerText = item.product;
            document.getElementById('liveToastTime').innerText = item.time;
            document.getElementById('liveToastAvatar').innerText = item.avatar;

            toast.style.display = 'flex';
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0) scale(1)';

            liveIdx++;
        }

        function closeLiveToast() {
            var toast = document.getElementById('liveSalesToast');
            if (toast) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(20px) scale(0.9)';
                setTimeout(function() { toast.style.display = 'none'; }, 300);
            }
        }

        // Show first notification after 3 seconds, then repeat every 14 seconds
        setTimeout(function() {
            updateLiveToast();
            setInterval(function() {
                updateLiveToast();
            }, 14000);
        }, 3000);
'''

html = html.replace('</script>', slider_js + '\n    </script>', 1)

with open(frontend_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved modern UI for frontend/index.html successfully!")
