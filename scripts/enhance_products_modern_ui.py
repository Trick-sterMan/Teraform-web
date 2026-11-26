import re
import os

base_dir = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web"
products_path = os.path.join(base_dir, "demo_pages/products/index.html")

with open(products_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add modern CSS enhancements
modern_products_css = '''
        /* ==============================================================
           GIAO DIỆN HIỆN ĐẠI & SỐNG ĐỘNG (PRODUCTS CATALOG ENHANCEMENTS)
           ============================================================== */
        body {
            background-color: #f8fafc;
            background-image: 
                radial-gradient(at 0% 0%, rgba(5, 150, 105, 0.05) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.06) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(59, 130, 246, 0.04) 0px, transparent 50%);
            background-attachment: fixed;
        }

        /* Modern Product Card Enhancements */
        .product-card {
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 20px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            background: #ffffff;
        }
        .product-card:hover {
            transform: translateY(-7px) scale(1.01) !important;
            box-shadow: 0 20px 35px -10px rgba(0,0,0,0.12) !important;
            border-color: #a7f3d0 !important;
        }
        .product-img-box {
            border-radius: 16px !important;
            background: #ffffff !important;
            transition: all 0.3s ease;
        }
        .product-card:hover .product-img-box {
            box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        }
        .btn-cart-mini {
            background: #ecfdf5 !important;
            color: #059669 !important;
            border: 1.5px solid #a7f3d0 !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
            transition: all 0.2s ease !important;
        }
        .btn-cart-mini:hover {
            background: #059669 !important;
            color: white !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(5,150,105,0.3);
        }
        .btn-buy-now {
            background: linear-gradient(135deg, #059669, #047857) !important;
            color: white !important;
            border: none !important;
            font-weight: 800 !important;
            border-radius: 10px !important;
            position: relative;
            overflow: hidden;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 12px rgba(5,150,105,0.25);
        }
        .btn-buy-now:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(5,150,105,0.4);
        }
        .brand-nav-pills {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        .brand-nav-pill {
            padding: 0.45rem 0.95rem;
            border-radius: 9999px;
            border: 1.5px solid #e2e8f0;
            background: white;
            font-size: 0.825rem;
            font-weight: 700;
            color: #475569;
            cursor: pointer;
            transition: all 0.25s ease;
        }
        .brand-nav-pill:hover {
            transform: translateY(-2px);
            border-color: #059669;
            color: #059669;
            background: #f0fdf4;
        }
        .brand-nav-pill.active {
            background: #059669;
            color: white;
            border-color: #059669;
            box-shadow: 0 4px 12px rgba(5,150,105,0.3);
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
            background: linear-gradient(135deg, #d1fae5, #ecfdf5);
            border: 1px solid #a7f3d0;
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
            color: #059669;
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
'''

html = html.replace('</style>', modern_products_css + '\n    </style>', 1)

# 2. Add Live Toast markup before </body>
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

# 3. Add JS for Live Toast
live_toast_js = '''
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

        setTimeout(function() {
            updateLiveToast();
            setInterval(function() {
                updateLiveToast();
            }, 14000);
        }, 4000);
'''

html = html.replace('</script>', live_toast_js + '\n    </script>', 1)

with open(products_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved modern UI for products/index.html successfully!")
