#!/bin/bash
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
        .product-img-box { height: 200px; display: flex; align-items: center; justify-content: center; margin-bottom: 0.75rem; background: #ffffff; border-radius: 14px; overflow: hidden; position: relative; padding: 10px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
        .product-img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; transition: transform 0.3s ease; display: block; border-radius: 6px; }
        .product-card:hover .product-img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; transition: transform 0.3s ease; display: block; border-radius: 6px; }
        /* Interactive Variants Selector */
        .variant-section { display: flex; flex-direction: column; gap: 0.45rem; margin-bottom: 0.75rem; background: #f8fafc; padding: 0.55rem 0.7rem; border-radius: 10px; border: 1px solid var(--border); }
        .variant-group { display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap; }
        .variant-label { font-size: 0.72rem; font-weight: 700; color: var(--text-muted); min-width: 68px; }
        .variant-options { display: flex; gap: 0.35rem; flex-wrap: wrap; flex: 1; }
        .variant-pill { font-size: 0.75rem; border: 1.5px solid var(--border); padding: 0.2rem 0.55rem; border-radius: 6px; cursor: pointer; font-weight: 600; color: #475569; background: #fff; transition: all 0.2s ease; user-select: none; display: inline-flex; align-items: center; justify-content: center; outline: none; }
        .variant-pill:hover { border-color: var(--primary); color: var(--primary); background: #eff6ff; transform: translateY(-1px); box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .variant-pill.active { border-color: var(--primary); background: #eff6ff; color: var(--primary); font-weight: 700; box-shadow: 0 0 0 2px rgba(37,99,235,0.25); }
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

    
        /* Prominent active variant pills */
        .variant-pill {
            font-size: 0.75rem !important;
            padding: 0.28rem 0.65rem !important;
            border-radius: 8px !important;
            border: 1.5px solid #cbd5e1 !important;
            background: #ffffff !important;
            color: #334155 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
        }
        .variant-pill:hover {
            border-color: #2563eb !important;
            color: #2563eb !important;
            background: #eff6ff !important;
            transform: translateY(-1px) !important;
        }
        .variant-pill.active {
            background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            border-color: #1d4ed8 !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
            transform: scale(1.03) !important;
        }

    </style>
</head>
<body>
    <!-- Dynamic Infinite Marquee Ribbon -->
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

        <!-- Hero Banner Section: Interactive Multi-Slide Tech Showcase -->
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
    </section>

    <!-- Trust Badges -->
    <div class="trust-grid">
        <div class="trust-item">
            <div class="trust-icon">🚀</div>
            <div>
                <div class="trust-title">Giao Hàng Siêu Tốc 2H</div>
                <div class="trust-desc">Nội thành Hà Nội & TP.HCM</div>
            </div>

    <!-- Interactive Brand Showcase Section -->
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
    </section>
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
                        <!-- Live Flash Sale Countdown Ribbon -->
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

        <h2 class="section-title">Sản Phẩm Bán Chạy Nhất</h2>
                <p class="section-subtitle">Được săn đón nhiều nhất tuần qua tại hệ thống CloudMart</p>
            </div>
            <a href="/products/" class="see-all-link">Xem thêm sản phẩm &rarr;</a>
        </div>

        <div class="product-grid">

            <!-- Product: iPhone 17 Pro Max -->
            <div class="product-card" style="border: 2px solid #3b82f6;">
                <span class="tag-discount" style="background: #2563eb;">⚡ ĐẶT TRƯỚC 2025</span>
                <div class="product-img-box">
                    <img src="/assets/real_iphone_17_pro_max_silver.jpg" alt="iPhone 17 Pro Max" class="product-img">
                </div>
                <div class="product-category">Apple Store Flagship</div>
                <h3 class="product-name">iPhone 17 Pro Max</h3>
                <div class="product-rating">★★★★★ <span>(Đặt trước Q3/2025)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="storage">
                        <span class="variant-label">Dung lượng:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="38990000" data-oldprice="42990000">256GB</button>
                            <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="44490000" data-oldprice="48990000">512GB</button>
                        </div>
                    </div>
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_17_pro_max_silver.jpg">Titan Bạc Ánh Xanh</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_17_pro_max_black.jpg">Titan Đen</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">38.990.000 ₫</span>
                    <span class="old-price">42.990.000 ₫</span>
                </div>
                <a href="/products/" class="btn-add-cart">Đặt trước ngay &rarr;</a>
            </div>

            <!-- Product: iPhone 18 Fold Duo -->
            <div class="product-card" style="border: 2px solid #8b5cf6;">
                <span class="tag-discount" style="background: #7c3aed;">🔥 MÀN GẬP 2026</span>
                <div class="product-img-box">
                    <img src="/assets/real_iphone_18_duo_fold.jpg" alt="iPhone 18 Fold Duo" class="product-img">
                </div>
                <div class="product-category">Apple Innovation</div>
                <h3 class="product-name">iPhone 18 Fold Duo Màn Gập</h3>
                <div class="product-rating">★★★★★ <span>(Bản Concept 2026)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="storage">
                        <span class="variant-label">Dung lượng:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="68990000" data-oldprice="75990000">512GB</button>
                            <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="76990000" data-oldprice="84990000">1TB</button>
                        </div>
                    </div>
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_18_duo_fold.jpg">Mặt Trước Gập</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/real_iphone_18_duo_fold_rear.jpg">Mặt Lưng Titanium</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">68.990.000 ₫</span>
                    <span class="old-price">75.990.000 ₫</span>
                </div>
                <a href="/products/" class="btn-add-cart">Đặt trước ngay &rarr;</a>
            </div>

            <!-- Product: Samsung Galaxy S25 Ultra -->
            <div class="product-card" style="border: 2px solid #10b981;">
                <span class="tag-discount" style="background: #059669;">⚡ GALAXY AI 2025</span>
                <div class="product-img-box">
                    <img src="/assets/real_samsung_s25_ultra_silverblue.jpg" alt="Samsung Galaxy S25 Ultra" class="product-img">
                </div>
                <div class="product-category">Samsung Galaxy AI</div>
                <h3 class="product-name">Samsung Galaxy S25 Ultra 5G AI</h3>
                <div class="product-rating">★★★★★ <span>(Đặt trước Q1/2025)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="storage">
                        <span class="variant-label">Dung lượng:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="34990000" data-oldprice="38990000">256GB</button>
                            <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="39990000" data-oldprice="43990000">512GB</button>
                        </div>
                    </div>
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_samsung_s25_ultra_silverblue.jpg">Xám Titan</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/real_samsung_s25_ultra.jpg">Bạc Ánh Xanh</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">34.990.000 ₫</span>
                    <span class="old-price">38.990.000 ₫</span>
                </div>
                <a href="/products/" class="btn-add-cart">Đặt trước ngay &rarr;</a>
            </div>

            <!-- Product: Galaxy Z Fold Special Edition -->
            <div class="product-card" style="border: 2px solid #f59e0b;">
                <span class="tag-discount" style="background: #d97706;">👑 MỎNG 10.6MM</span>
                <div class="product-img-box">
                    <img src="/assets/real_samsung_zfold_se.jpg" alt="Galaxy Z Fold Special Edition" class="product-img">
                </div>
                <div class="product-category">Samsung Premium Fold</div>
                <h3 class="product-name">Galaxy Z Fold Special Edition</h3>
                <div class="product-rating">★★★★★ <span>(Bản Giới Hạn)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="storage">
                        <span class="variant-label">Dung lượng:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="56990000" data-oldprice="62990000">512GB</button>
                        </div>
                    </div>
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_samsung_zfold_se.jpg">Titan Đen Sọc</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">56.990.000 ₫</span>
                    <span class="old-price">62.990.000 ₫</span>
                </div>
                <a href="/products/" class="btn-add-cart">Đặt trước ngay &rarr;</a>
            </div>
            <!-- Product 1: Apple MacBook Pro -->
            <div class="product-card">
                <span class="tag-discount">-12%</span>
                <div class="product-img-box">
                    <img src="/assets/macbook_pro_m3_space_gray.jpg" alt="MacBook Pro 16 M3 Max" class="product-img">
                </div>
                <div class="product-category">Apple Store</div>
                <h3 class="product-name">MacBook Pro 16" M3 Max</h3>
                <div class="product-rating">★★★★★ <span>(142 đánh giá)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="storage">
                        <span class="variant-label">Dung lượng:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="68990000" data-oldprice="78500000">512GB</button>
                            <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="74990000" data-oldprice="84500000">1TB (+6tr)</button>
                        </div>
                    </div>
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/macbook_pro_m3_space_gray.jpg">Bạc Silver</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/macbook_pro_m3_space_gray.jpg">Xám Space Gray</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/macbook_air_gold.jpg">Vàng Gold</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">68.990.000 ₫</span>
                    <span class="old-price">78.500.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 2: Apple iPhone 16 Pro Max -->
            <div class="product-card">
                <span class="tag-discount">-8%</span>
                <div class="product-img-box">
                    <img src="/assets/real_iphone_16_pro_max.jpg" alt="iPhone 16 Pro Max" class="product-img">
                </div>
                <div class="product-category">Apple Store</div>
                <h3 class="product-name">iPhone 16 Pro Max</h3>
                <div class="product-rating">★★★★★ <span>(389 đánh giá)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="storage">
                        <span class="variant-label">Dung lượng:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="34490000" data-oldprice="37990000">256GB</button>
                            <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="39990000" data-oldprice="43490000">512GB (+5.5tr)</button>
                            <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="45990000" data-oldprice="49990000">1TB (+11.5tr)</button>
                        </div>
                    </div>
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_16_pro_max.jpg">Titan Sa Mạc</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_16_pro_white.jpg">Titan Trắng</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_16_green.jpg">Xanh Mát</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">34.490.000 ₫</span>
                    <span class="old-price">37.990.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 3: Samsung Galaxy S24 Ultra -->
            <div class="product-card">
                <span class="tag-discount">-15%</span>
                <div class="product-img-box">
                    <img src="/assets/real_samsung_s24_ultra.jpg" alt="Samsung Galaxy S24 Ultra" class="product-img">
                </div>
                <div class="product-category">Samsung Flagship</div>
                <h3 class="product-name">Samsung Galaxy S24 Ultra 5G AI</h3>
                <div class="product-rating">★★★★★ <span>(215 đánh giá)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="storage">
                        <span class="variant-label">Dung lượng:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="29990000" data-oldprice="35490000">256GB</button>
                            <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="33990000" data-oldprice="39990000">512GB (+4tr)</button>
                        </div>
                    </div>
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_samsung_s24_ultra.jpg">Xám Titan</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s24_black.jpg">Đen Titan</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">29.990.000 ₫</span>
                    <span class="old-price">35.490.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 4: Sony WH-1000XM5 -->
            <div class="product-card">
                <span class="tag-discount">-20%</span>
                <div class="product-img-box">
                    <img src="/assets/sony_headphones.jpg" alt="Sony WH-1000XM5" class="product-img">
                </div>
                <div class="product-category">Sony Electronics</div>
                <h3 class="product-name">Sony WH-1000XM5 Chống Ồn Chủ Động</h3>
                <div class="product-rating">★★★★★ <span>(96 đánh giá)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/sony_headphones.jpg">Bạc Platinum</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/sony_xm5_black.jpg">Đen Nhám</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">7.990.000 ₫</span>
                    <span class="old-price">9.990.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 5: Dell XPS 16 -->
            <div class="product-card">
                <span class="tag-discount">-10%</span>
                <div class="product-img-box">
                    <img src="/assets/dell_xps.png" alt="Dell XPS 16 9640" class="product-img">
                </div>
                <div class="product-category">Dell Technologies</div>
                <h3 class="product-name">Dell XPS 16 9640 Core Ultra 7 OLED 4K</h3>
                <div class="product-rating">★★★★★ <span>(64 đánh giá)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="storage">
                        <span class="variant-label">Cấu hình:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="54990000" data-oldprice="59990000">Ultra 7 / 32GB</button>
                            <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="62990000" data-oldprice="68990000">Ultra 9 / 64GB (+8tr)</button>
                        </div>
                    </div>
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/dell_xps.png">Platinum</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/dell_xps_graphite.jpg">Graphite</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">54.990.000 ₫</span>
                    <span class="old-price">61.000.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 6: Apple Watch Ultra 2 -->
            <div class="product-card">
                <span class="tag-discount">-15%</span>
                <div class="product-img-box">
                    <img src="/assets/apple_watch_ultra2.jpg" alt="Apple Watch Ultra 2" class="product-img">
                </div>
                <div class="product-category">Apple Watch</div>
                <h3 class="product-name">Apple Watch Ultra 2 GPS + Cellular 49mm Titan</h3>
                <div class="product-rating">★★★★★ <span>(78 đánh giá)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Loại dây:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/apple_watch_ultra2.jpg">Alpine Cam</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/apple_watch_ocean.jpg">Ocean Xanh</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/apple_watch_ultra_natural.jpg">Titan Tự Nhiên</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">19.890.000 ₫</span>
                    <span class="old-price">23.490.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 7: iPad Pro M4 -->
            <div class="product-card">
                <span class="tag-discount">-10%</span>
                <div class="product-img-box">
                    <img src="/assets/ipad_pro_13_m4.jpg" alt="iPad Pro 13 M4 OLED" class="product-img">
                </div>
                <div class="product-category">Apple Store</div>
                <h3 class="product-name">iPad Pro 13" M4 Tandem OLED</h3>
                <div class="product-rating">★★★★★ <span>(112 đánh giá)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="storage">
                        <span class="variant-label">Dung lượng:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="36990000" data-oldprice="41990000">256GB Wifi</button>
                            <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="42990000" data-oldprice="47990000">512GB 5G (+6tr)</button>
                        </div>
                    </div>
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/ipad_pro_13_m4.jpg">Space Black</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/ipad_pro_silver.jpg">Silver</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">36.990.000 ₫</span>
                    <span class="old-price">41.990.000 ₫</span>
                </div>
                <a href="/checkout/" class="btn-add-cart">Mua ngay &rarr;</a>
            </div>

            <!-- Product 8: ASUS ROG Zephyrus G16 -->
            <div class="product-card">
                <span class="tag-discount">-18%</span>
                <div class="product-img-box">
                    <img src="/assets/asus_rog_gray.jpg" alt="ASUS ROG Zephyrus G16" class="product-img">
                </div>
                <div class="product-category">ASUS ROG Gaming</div>
                <h3 class="product-name">ASUS ROG Zephyrus G16 OLED RTX 4080</h3>
                <div class="product-rating">★★★★★ <span>(85 đánh giá)</span></div>
                <div class="variant-section">
                    <div class="variant-group" data-type="color">
                        <span class="variant-label">Màu sắc:</span>
                        <div class="variant-options">
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/asus_rog_gray.jpg">Eclipse Gray</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/asus_rog_white.jpg">Platinum White</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">69.990.000 ₫</span>
                    <span class="old-price">85.000.000 ₫</span>
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

                function formatVND(num) {
            return Number(num).toLocaleString('vi-VN') + ' ₫';
        }

        function selectStorage(btn) {
            var card = btn.closest('.product-card');
            if (!card) return;
            var group = btn.closest('.variant-group');
            if (group) {
                group.querySelectorAll('.variant-pill').forEach(function(p) { p.classList.remove('active'); });
                var labelEl = group.querySelector('.variant-label');
                if (labelEl) {
                    labelEl.innerHTML = 'Dung lượng: <strong style="color: #2563eb; font-weight: 800;">' + btn.innerText.trim() + '</strong>';
                }
            }
            btn.classList.add('active');
            var priceEl = card.querySelector('.current-price');
            var oldPriceEl = card.querySelector('.old-price');
            var newPrice = btn.getAttribute('data-price');
            var newOldPrice = btn.getAttribute('data-oldprice');
            if (newPrice && priceEl) {
                priceEl.innerText = formatVND(newPrice);
                priceEl.style.transition = 'transform 0.15s ease';
                priceEl.style.transform = 'scale(1.1)';
                setTimeout(function() { priceEl.style.transform = 'scale(1)'; }, 180);
            }
            if (newOldPrice && oldPriceEl) oldPriceEl.innerText = formatVND(newOldPrice);
            var optImg = btn.getAttribute('data-img');
            var imgEl = card.querySelector('.product-img');
            if (optImg && imgEl) imgEl.src = optImg;
        }

        function selectColor(btn) {
            var card = btn.closest('.product-card');
            if (!card) return;
            var group = btn.closest('.variant-group');
            if (group) {
                group.querySelectorAll('.variant-pill').forEach(function(p) { p.classList.remove('active'); });
                var labelEl = group.querySelector('.variant-label');
                if (labelEl) {
                    labelEl.innerHTML = 'Màu sắc: <strong style="color: #2563eb; font-weight: 800;">' + btn.innerText.trim() + '</strong>';
                }
            }
            btn.classList.add('active');
            var newImg = btn.getAttribute('data-img');
            var imgEl = card.querySelector('.product-img');
            if (newImg && imgEl) {
                imgEl.style.transition = 'opacity 0.15s ease, transform 0.15s ease';
                imgEl.style.opacity = '0.35';
                imgEl.style.transform = 'scale(0.96)';
                imgEl.src = newImg;
                setTimeout(function() {
                    imgEl.style.opacity = '1';
                    imgEl.style.transform = 'scale(1)';
                }, 120);
            }

            var colorPrice = btn.getAttribute('data-price');
            var priceEl = card.querySelector('.current-price');
            var oldPriceEl = card.querySelector('.old-price');
            if (colorPrice && priceEl) {
                priceEl.innerText = formatVND(colorPrice);
            } else {
                var activeStorage = card.querySelector('.variant-group[data-type="storage"] .variant-pill.active');
                if (activeStorage) {
                    var sPrice = activeStorage.getAttribute('data-price');
                    var sOldPrice = activeStorage.getAttribute('data-oldprice');
                    if (sPrice && priceEl) priceEl.innerText = formatVND(sPrice);
                    if (sOldPrice && oldPriceEl) oldPriceEl.innerText = formatVND(sOldPrice);
                }
            }
            if (priceEl) {
                priceEl.style.transition = 'transform 0.15s ease';
                priceEl.style.transform = 'scale(1.08)';
                setTimeout(function() { priceEl.style.transform = 'scale(1)'; }, 180);
            }
        }

        function initVariantSelectors() {
            document.querySelectorAll('.product-card').forEach(function(card) {
                var sGroup = card.querySelector('.variant-group[data-type="storage"]');
                if (sGroup) {
                    var activeS = sGroup.querySelector('.variant-pill.active');
                    var sLabel = sGroup.querySelector('.variant-label');
                    if (activeS && sLabel && !sLabel.querySelector('strong')) {
                        sLabel.innerHTML = 'Dung lượng: <strong style="color: #2563eb; font-weight: 800;">' + activeS.innerText.trim() + '</strong>';
                    }
                }
                var cGroup = card.querySelector('.variant-group[data-type="color"]');
                if (cGroup) {
                    var activeC = cGroup.querySelector('.variant-pill.active');
                    var cLabel = cGroup.querySelector('.variant-label');
                    if (activeC && cLabel && !cLabel.querySelector('strong')) {
                        cLabel.innerHTML = 'Màu sắc: <strong style="color: #2563eb; font-weight: 800;">' + activeC.innerText.trim() + '</strong>';
                    }
                }

                card.querySelectorAll('.variant-group[data-type="storage"] .variant-pill').forEach(function(pill) {
                    pill.onclick = function(e) { e.preventDefault(); selectStorage(this); };
                });
                card.querySelectorAll('.variant-group[data-type="color"] .variant-pill').forEach(function(pill) {
                    pill.onclick = function(e) { e.preventDefault(); selectColor(this); };
                });
            });
        }
        document.addEventListener('DOMContentLoaded', initVariantSelectors);
        initVariantSelectors();
    
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
            { user: "Anh Đức Trọng (Đà Nẵng)", product: "MacBook Pro 16 M3 Max Silver", time: "7 phút trước", avatar: "💻" },
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

    </script>
    <!-- Real-time Purchase Social Proof Toast -->
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

</body>
</html>
EOF
systemctl enable nginx
systemctl restart nginx
