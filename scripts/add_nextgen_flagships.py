import re
import html

def format_vnd(amount):
    return f"{amount:,.0f} ₫".replace(",", ".")

def generate_product_card(brand, tag, stock, img, alt, category, name, specs, storage_variants, color_variants, promo, price, old_price):
    storage_btns = []
    for i, s in enumerate(storage_variants):
        active = " active" if i == 0 else ""
        price_diff = f" (+{s['diff']}tr)" if s.get('diff') else ""
        storage_btns.append(f'<button type="button" class="variant-pill{active}" onclick="selectStorage(this)" data-price="{s["price"]}" data-oldprice="{s["old_price"]}">{s["label"]}{price_diff}</button>')
    storage_html = "\n                                    ".join(storage_btns)

    color_btns = []
    for i, c in enumerate(color_variants):
        active = " active" if i == 0 else ""
        color_btns.append(f'<button type="button" class="variant-pill{active}" onclick="selectColor(this)" data-img="{c["img"]}">{c["label"]}</button>')
    color_html = "\n                                    ".join(color_btns)

    # Clean double quotes in alt and specs
    alt_clean = html.escape(alt, quote=True)
    specs_clean = specs.replace('"', '&quot;')

    card = f"""                    <div class="product-card" data-brand="{brand}">
                        <button type="button" class="btn-wishlist" onclick="toggleWishlist(this)" title="Thêm vào yêu thích">🤍</button>
                        <span class="tag-badge">{tag}</span>
                        <span class="stock-tag">{stock}</span>
                        <div class="product-img-box">
                            <img src="{img}" alt="{alt_clean}" class="product-img">
                            <button type="button" class="btn-quick-view" onclick="openQuickView(this)">👁️ Xem nhanh</button>
                        </div>
                        <div class="product-category">{category}</div>
                        <h3 class="product-name">{name}</h3>
                        <div class="product-specs">{specs_clean}</div>
                        <div class="variant-section">
                            <div class="variant-group" data-type="storage">
                                <span class="variant-label">Dung lượng:</span>
                                <div class="variant-options">
                                    {storage_html}
                                </div>
                            </div>
                            <div class="variant-group" data-type="color">
                                <span class="variant-label">Màu sắc:</span>
                                <div class="variant-options">
                                    {color_html}
                                </div>
                            </div>
                        </div>
                        <div class="card-promo">{promo}</div>
                        <div class="price-row">
                            <span class="current-price">{format_vnd(price)}</span>
                            <span class="old-price">{format_vnd(old_price)}</span>
                        </div>
                        <div class="card-actions">
                            <button type="button" class="btn-cart-mini" onclick="addToCart(this)">Thêm giỏ</button>
                            <button type="button" class="btn-buy-now" onclick="buyNow(this)">Mua ngay</button>
                        </div>
                    </div>"""
    return card

apple_products = [
    {
        "brand": "Apple",
        "tag": "⚡ Đặt Trước Thế Hệ Mới 2025",
        "stock": "📅 Dự kiến giao Q3/2025",
        "img": "/assets/iphone_17_pro_max.jpg",
        "alt": "iPhone 17 Pro Max Siêu Phẩm Đỉnh Cao 2025",
        "category": "Siêu Flagship Apple Thế Hệ Kế Tiếp",
        "name": "iPhone 17 Pro Max",
        "specs": 'Chip Apple A19 Pro 2nm TSMC cực mạnh • Màn hình 6.9" ProMotion 120Hz viền mỏng kỷ lục 1.15mm • Cụm 3 camera 48MP zoom quang 10x • Khung viền Titan Ceramic siêu cứng',
        "storage_variants": [
            {"label": "256GB", "price": 38990000, "old_price": 42990000},
            {"label": "512GB", "price": 44490000, "old_price": 48990000, "diff": "5.5"},
            {"label": "1TB", "price": 50990000, "old_price": 55990000, "diff": "12"},
            {"label": "2TB", "price": 58990000, "old_price": 64990000, "diff": "20"}
        ],
        "color_variants": [
            {"label": "Titan Bạc Ánh Xanh", "img": "/assets/iphone_17_pro_max.jpg"},
            {"label": "Titan Đen Vũ Trụ (Space Black)", "img": "/assets/iphone_17_pro_max_black.jpg"}
        ],
        "promo": "🎁 Đặt trước cọc 2.000.000₫ • Tặng gói bảo hành VIP 2 năm 1 đổi 1 & Bộ sạc 45W GaN Apple",
        "price": 38990000,
        "old_price": 42990000
    },
    {
        "brand": "Apple",
        "tag": "⚡ Đặt Trước Thế Hệ Mới 2025",
        "stock": "📅 Dự kiến giao Q3/2025",
        "img": "/assets/iphone_17_pro_max_black.jpg",
        "alt": "iPhone 17 Pro Flagship Nhỏ Gọn 2025",
        "category": "Smartphone Apple Cao Cấp Tương Lai",
        "name": "iPhone 17 Pro",
        "specs": 'Chip Apple A19 Pro 2nm thế hệ mới • Màn hình 6.3" Super Retina XDR 120Hz ProMotion • Camera Tetraprism 48MP Zoom 5x • Nút bấm xúc giác Dynamic Haptic Button',
        "storage_variants": [
            {"label": "128GB", "price": 32990000, "old_price": 35990000},
            {"label": "256GB", "price": 35990000, "old_price": 38990000, "diff": "3"},
            {"label": "512GB", "price": 41490000, "old_price": 44990000, "diff": "8.5"},
            {"label": "1TB", "price": 47990000, "old_price": 51990000, "diff": "15"}
        ],
        "color_variants": [
            {"label": "Titan Đen Vũ Trụ", "img": "/assets/iphone_17_pro_max_black.jpg"},
            {"label": "Titan Bạc Ánh Kim", "img": "/assets/iphone_17_pro_max.jpg"}
        ],
        "promo": "🎁 Nhận cọc ưu đãi giảm 1.500.000₫ • Tặng ốp da cao cấp Finewoven & Cáp sạc bọc dù 100W",
        "price": 32990000,
        "old_price": 35990000
    },
    {
        "brand": "Apple",
        "tag": "✨ Đột Phá Thiết Kế Siêu Mỏng",
        "stock": "📅 Dự kiến giao Q3/2025",
        "img": "/assets/iphone_17_air.jpg",
        "alt": "iPhone 17 Air Siêu Mỏng Kỷ Lục 5.6mm",
        "category": "iPhone Siêu Mỏng Kỷ Lục 2025",
        "name": "iPhone 17 Air (Slim 5.6mm)",
        "specs": 'Độ mỏng không tưởng chỉ 5.6mm • Vỏ hợp kim Titanium-Aluminium nguyên khối • Chip Apple A19 Bionic • Màn hình OLED ProMotion 6.6" 120Hz viền vô cực',
        "storage_variants": [
            {"label": "128GB", "price": 30990000, "old_price": 33990000},
            {"label": "256GB", "price": 33990000, "old_price": 37490000, "diff": "3"},
            {"label": "512GB", "price": 38990000, "old_price": 42990000, "diff": "8"}
        ],
        "color_variants": [
            {"label": "Xanh Thiên Thanh (Sky Blue)", "img": "/assets/iphone_17_air.jpg"},
            {"label": "Trắng Ngọc Trai (Cloud White)", "img": "/assets/iphone_17_air_white.jpg"}
        ],
        "promo": "🎁 Tặng củ sạc siêu mỏng MagSafe Air 35W & Bao da cao cấp trị giá 1.800.000₫",
        "price": 30990000,
        "old_price": 33990000
    },
    {
        "brand": "Apple",
        "tag": "⚡ Thế Hệ 2025 Tiêu Chuẩn",
        "stock": "📅 Dự kiến giao Q3/2025",
        "img": "/assets/iphone_17_air_white.jpg",
        "alt": "iPhone 17 Tiêu Chuẩn Màn Hình 120Hz",
        "category": "Smartphone Apple 2025 Đột Phá",
        "name": "iPhone 17",
        "specs": 'Lần đầu trang bị màn hình 120Hz ProMotion trên dòng tiêu chuẩn • Chip A19 Bionic 3nm N3P • Camera kép Fusion 48MP zoom lossless 2x • Kính Ceramic Shield 2025',
        "storage_variants": [
            {"label": "128GB", "price": 24990000, "old_price": 27490000},
            {"label": "256GB", "price": 27990000, "old_price": 30990000, "diff": "3"},
            {"label": "512GB", "price": 32990000, "old_price": 36490000, "diff": "8"}
        ],
        "color_variants": [
            {"label": "Trắng Băng Giá (Cloud White)", "img": "/assets/iphone_17_air_white.jpg"},
            {"label": "Xanh Lam Tinh Khiết", "img": "/assets/iphone_17_air.jpg"}
        ],
        "promo": "🎁 Đặt cọc nhận voucher 1.000.000₫ • Tặng ốp lưng MagSafe chính hãng & Sạc nhanh 25W",
        "price": 24990000,
        "old_price": 27490000
    },
    {
        "brand": "Apple",
        "tag": "🚀 Đỉnh Cao Công Nghệ 2026",
        "stock": "📅 Bản Concept Độc Quyền 2026",
        "img": "/assets/iphone_17_pro_max.jpg",
        "alt": "iPhone 18 Pro Max Face ID Tàng Hình",
        "category": "Siêu Flagship Đột Phá 2026",
        "name": "iPhone 18 Pro Max",
        "specs": 'Công nghệ Face ID ẩn dưới màn hình tàng hình hoàn toàn • Chip Apple A20 Pro 1.8nm • Màn hình 6.9" 144Hz ProMotion • Camera tiềm vọng zoom quang học 15x liên tục',
        "storage_variants": [
            {"label": "256GB", "price": 42990000, "old_price": 46990000},
            {"label": "512GB", "price": 48990000, "old_price": 53990000, "diff": "6"},
            {"label": "1TB", "price": 55990000, "old_price": 61990000, "diff": "13"},
            {"label": "2TB", "price": 64990000, "old_price": 71990000, "diff": "22"}
        ],
        "color_variants": [
            {"label": "Titan Vũ Trụ Tối Thượng", "img": "/assets/iphone_17_pro_max_black.jpg"},
            {"label": "Titan Hologram Tự Nhiên", "img": "/assets/iphone_17_pro_max.jpg"}
        ],
        "promo": "🎁 Đặc quyền khách hàng VIP: Khắc tên laser độc bản & Bộ quà tặng Apple Ecosystem 2026",
        "price": 42990000,
        "old_price": 46990000
    },
    {
        "brand": "Apple",
        "tag": "🔥 Siêu Phẩm Màn Gập 2026",
        "stock": "📅 Bản Đặt Hàng Trước 2026",
        "img": "/assets/iphone_18_duo.jpg",
        "alt": "iPhone 18 Fold Duo Màn Gập Đôi Siêu Phẩm",
        "category": "Điện Thoại Gập Đầu Tiên Của Apple",
        "name": "iPhone 18 Fold Duo Màn Gập",
        "specs": 'Màn hình kép Dynamic Duo OLED 8.1" không nếp gấp gập mở linh hoạt • Khung bản lề Titanium Liquid Metal siêu bền • Chip Apple M5 Fold Edition • Hỗ trợ Apple Pencil Pro',
        "storage_variants": [
            {"label": "512GB", "price": 68990000, "old_price": 75990000},
            {"label": "1TB", "price": 76990000, "old_price": 84990000, "diff": "8"}
        ],
        "color_variants": [
            {"label": "Space Titanium Đen Ánh Kim", "img": "/assets/iphone_18_duo.jpg"},
            {"label": "Titan Bạc Siêu Nhẹ", "img": "/assets/iphone_17_pro_max.jpg"}
        ],
        "promo": "🎁 Gói bảo hành rơi vỡ AppleCare+ VIP 2 năm & Bao da da bê thủ công trị giá 3.500.000₫",
        "price": 68990000,
        "old_price": 75990000
    }
]

samsung_products = [
    {
        "brand": "Samsung",
        "tag": "⚡ Đặt Trước Galaxy AI 2025",
        "stock": "📅 Dự kiến giao Q1/2025",
        "img": "/assets/samsung_s25_ultra_render.jpg",
        "alt": "Samsung Galaxy S25 Ultra 5G AI Flagship 2025",
        "category": "Siêu Phẩm Galaxy Flagship 2025",
        "name": "Samsung Galaxy S25 Ultra 5G AI",
        "specs": 'Chip Snapdragon 8 Elite for Galaxy (3nm) siêu hiệu năng • Thiết kế phẳng bo cong công thái học viền siêu mỏng • Camera 200MP cảm biến AI thế hệ mới • Kính cường lực Armor Crystal chống chói',
        "storage_variants": [
            {"label": "256GB", "price": 34990000, "old_price": 38990000},
            {"label": "512GB", "price": 39990000, "old_price": 43990000, "diff": "5"},
            {"label": "1TB", "price": 45990000, "old_price": 50990000, "diff": "11"}
        ],
        "color_variants": [
            {"label": "Xám Titan (Titanium Gray)", "img": "/assets/samsung_s25_ultra_render.jpg"},
            {"label": "Bạc Titan Ánh Xanh", "img": "/assets/samsung_s25_ultra.jpg"}
        ],
        "promo": "🎁 Đặt trước nhận Voucher nâng cấp dung lượng 512GB miễn phí trị giá 5.000.000₫ + Ốp lưng S Pen",
        "price": 34990000,
        "old_price": 38990000
    },
    {
        "brand": "Samsung",
        "tag": "⚡ Đặt Trước Galaxy AI 2025",
        "stock": "📅 Dự kiến giao Q1/2025",
        "img": "/assets/samsung_s25_plus.jpg",
        "alt": "Samsung Galaxy S25+ 5G AI Màn Hình Lớn 2025",
        "category": "Smartphone Galaxy AI Cao Cấp 2025",
        "name": "Samsung Galaxy S25+ 5G AI",
        "specs": 'Màn hình 6.7" Dynamic AMOLED 2X QHD+ 3000 nits • Chip Snapdragon 8 Elite đỉnh cao • Hệ sinh thái Galaxy AI 2.0 toàn diện • Khung Armor Aluminum cường lực',
        "storage_variants": [
            {"label": "256GB", "price": 26990000, "old_price": 29990000},
            {"label": "512GB", "price": 30990000, "old_price": 34490000, "diff": "4"}
        ],
        "color_variants": [
            {"label": "Bạc Ánh Kim (Titanium Silver)", "img": "/assets/samsung_s25_plus.jpg"},
            {"label": "Đen Phantom Black", "img": "/assets/samsung_s25_black.png"}
        ],
        "promo": "🎁 Tặng Củ sạc nhanh Samsung 45W Type-C & Tai nghe Galaxy Buds FE chính hãng",
        "price": 26990000,
        "old_price": 29990000
    },
    {
        "brand": "Samsung",
        "tag": "⚡ Đặt Trước Thế Hệ Mới 2025",
        "stock": "📅 Dự kiến giao Q1/2025",
        "img": "/assets/samsung_s25_black.png",
        "alt": "Samsung Galaxy S25 5G Nhỏ Gọn 2025",
        "category": "Galaxy AI Flagship Nhỏ Gọn 2025",
        "name": "Samsung Galaxy S25 5G AI",
        "specs": 'Thiết kế nhỏ gọn 6.2" Dynamic AMOLED 2X viền đều siêu mỏng • Chip Snapdragon 8 Elite xử lý AI tại chỗ • Pin dung lượng nâng cấp với tản nhiệt buồng hơi Vapor Chamber lớn hơn',
        "storage_variants": [
            {"label": "128GB", "price": 21990000, "old_price": 24490000},
            {"label": "256GB", "price": 23990000, "old_price": 26990000, "diff": "2"}
        ],
        "color_variants": [
            {"label": "Đen Huyền Bí Phantom Black", "img": "/assets/samsung_s25_black.png"},
            {"label": "Bạc Ánh Xanh Tinh Khiết", "img": "/assets/samsung_s25_plus.jpg"}
        ],
        "promo": "🎁 Tặng bao da Smart View chính hãng & Gói bảo hành rơi vỡ Samsung Care+ 1 năm",
        "price": 21990000,
        "old_price": 24490000
    },
    {
        "brand": "Samsung",
        "tag": "👑 Siêu Phẩm Gập Mỏng Kỷ Lục",
        "stock": "📅 Phiên Bản Giới Hạn Limited",
        "img": "/assets/samsung_zfold_se.jpg",
        "alt": "Samsung Galaxy Z Fold Special Edition 200MP Mỏng 10.6mm",
        "category": "Điện Thoại Gập Siêu Mỏng Đỉnh Cao",
        "name": "Galaxy Z Fold Special Edition",
        "specs": 'Độ mỏng kỷ lục chỉ 10.6mm khi gập và 4.9mm khi mở • Màn hình trong 8.0" cực đại và màn ngoài 6.5" 21:9 • Lần đầu camera 200MP trên dòng Fold • Mặt lưng vân sọc Titan sang trọng',
        "storage_variants": [
            {"label": "512GB", "price": 56990000, "old_price": 62990000}
        ],
        "color_variants": [
            {"label": "Titan Đen Sọc (Shadow Black)", "img": "/assets/samsung_zfold_se.jpg"}
        ],
        "promo": "🎁 Tặng bộ bao da sọc Titan cao cấp kèm S Pen Pro & Dịch vụ hỗ trợ đặc quyền Concierge 24/7",
        "price": 56990000,
        "old_price": 62990000
    }
]

realme_products = [
    {
        "brand": "Realme",
        "tag": "⚡ Siêu Flagship 2025 Mới Nhất",
        "stock": "✓ Đã Ra Mắt - Sẵn Hàng",
        "img": "/assets/realme_gt_7_pro.jpg",
        "alt": "Realme GT 7 Pro Siêu Phẩm Snapdragon 8 Elite",
        "category": "Kẻ Hủy Diệt Flagship Mới Nhất 2025",
        "name": "Realme GT 7 Pro 5G",
        "specs": 'Chip Snapdragon 8 Elite 3nm đầu tiên thế giới • Pin Titan Silicon 6500mAh siêu bền • Sạc siêu nhanh 120W Ultra Dart • Chuẩn kháng nước bụi IP68/IP69 quay chụp dưới nước chuyên nghiệp',
        "storage_variants": [
            {"label": "256GB / 12GB", "price": 16990000, "old_price": 18990000},
            {"label": "512GB / 16GB", "price": 19490000, "old_price": 21990000, "diff": "2.5"}
        ],
        "color_variants": [
            {"label": "Cam Hỏa Tinh (Mars Orange)", "img": "/assets/realme_gt_7_pro.jpg"},
            {"label": "Xám Thiên Thạch (Titan Gray)", "img": "/assets/realme_gt_6.jpg"}
        ],
        "promo": "🎁 Tặng tai nghe không dây Realme Buds Air 6 + Gói bảo hành VIP 1 đổi 1 trong 12 tháng",
        "price": 16990000,
        "old_price": 18990000
    }
]

huawei_products = [
    {
        "brand": "Huawei",
        "tag": "⚡ Thế Hệ Flagship Mới Nhất 2025",
        "stock": "📅 Mới Ra Mắt 2024 - 2025",
        "img": "/assets/huawei_mate_70_pro.jpg",
        "alt": "Huawei Mate 70 Pro+ Đột Phá HarmonyOS NEXT",
        "category": "Siêu Phẩm Flagship HarmonyOS NEXT",
        "name": "Huawei Mate 70 Pro+",
        "specs": 'Hệ điều hành HarmonyOS NEXT thuần độc lập 100% • Chip xử lý Kirin 9020 thế hệ mới • Khung viền vật liệu Titanium Basalt • Kết nối vệ tinh Beidou hai chiều thế hệ 3',
        "storage_variants": [
            {"label": "512GB / 16GB", "price": 35990000, "old_price": 39990000},
            {"label": "1TB / 16GB", "price": 41990000, "old_price": 46990000, "diff": "6"}
        ],
        "color_variants": [
            {"label": "Titan Bạc Vân Đá", "img": "/assets/huawei_mate_70_pro.jpg"},
            {"label": "Đen Huyền Vũ (Obsidian Black)", "img": "/assets/huawei_mate_xt.jpg"}
        ],
        "promo": "🎁 Tặng gói bảo hành toàn cầu Huawei Care+ 2 năm & Sạc siêu nhanh không dây 80W SuperCharge",
        "price": 35990000,
        "old_price": 39990000
    }
]

oppo_products = [
    {
        "brand": "OPPO",
        "tag": "⚡ Thế Hệ Gập Mới 2025",
        "stock": "📅 Đặt Trước 2025",
        "img": "/assets/oppo_find_n5.jpg",
        "alt": "OPPO Find N5 Màn Gập Siêu Mỏng 2025",
        "category": "Điện Thoại Màn Gập Flagship Kế Tiếp",
        "name": "OPPO Find N5 5G",
        "specs": 'Bản lề giọt nước Titanium siêu nhẹ • Màn hình gập không nếp nhăn Ultra Flat • Chip Snapdragon 8 Elite • Hệ thống 3 camera tiềm vọng Hasselblad thế hệ mới',
        "storage_variants": [
            {"label": "512GB / 16GB", "price": 46990000, "old_price": 51990000},
            {"label": "1TB / 16GB", "price": 52990000, "old_price": 58990000, "diff": "6"}
        ],
        "color_variants": [
            {"label": "Vàng Sa Mạc Champagne", "img": "/assets/oppo_find_n5.jpg"},
            {"label": "Đen Da Cao Cấp Classic Black", "img": "/assets/oppo_find_n3_fold.jpg"}
        ],
        "promo": "🎁 Tặng tai nghe OPPO Enco X3 Dynaudio trị giá 3.990.000₫ & Bảo hiểm màn hình rơi vỡ 2 năm",
        "price": 46990000,
        "old_price": 51990000
    }
]

target_file = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html"
with open(target_file, "r", encoding="utf-8") as f:
    html_content = f.read()

# 1. Update counts in navigation and header
html_content = html_content.replace("Tất cả (101)", "Tất cả (114)")
html_content = html_content.replace("🍏 Apple (21)", "🍏 Apple (27)")
html_content = html_content.replace("🌌 Samsung (17)", "🌌 Samsung (21)")
html_content = html_content.replace("🟢 OPPO (10)", "🟢 OPPO (11)")
html_content = html_content.replace("🔴 Huawei (9)", "🔴 Huawei (10)")
html_content = html_content.replace("🟡 Celmi / Realme (9)", "🟡 Celmi / Realme (10)")
html_content = html_content.replace('<strong id="productCount">101</strong>', '<strong id="productCount">114</strong>')

# 2. Update brand badges
# Apple: 21 -> 27
html_content = re.sub(
    r'(<h2 class="brand-title">Apple Authorized Reseller \(AAR VN/A\)</h2>\s*<span class="brand-count-badge">)21 sản phẩm(</span>)',
    r'\g<1>27 sản phẩm\g<2>',
    html_content
)
# Samsung: 17 -> 21
html_content = re.sub(
    r'(<h2 class="brand-title">Samsung Galaxy AI Premium Experience Store</h2>\s*<span class="brand-count-badge">)17 sản phẩm(</span>)',
    r'\g<1>21 sản phẩm\g<2>',
    html_content
)
# OPPO: 10 -> 11
html_content = re.sub(
    r'(<h2 class="brand-title">OPPO Flagship & AI Portrait Store</h2>\s*<span class="brand-count-badge">)10 sản phẩm(</span>)',
    r'\g<1>11 sản phẩm\g<2>',
    html_content
)
# Huawei: 9 -> 10
html_content = re.sub(
    r'(<h2 class="brand-title">Huawei Technologies & HarmonyOS</h2>\s*<span class="brand-count-badge">)9 sản phẩm(</span>)',
    r'\g<1>10 sản phẩm\g<2>',
    html_content
)
# Realme: 9 -> 10
html_content = re.sub(
    r'(<h2 class="brand-title">Realme / Celmi Dám Đột Phá \(Dare to Leap\)</h2>\s*<span class="brand-count-badge">)9 sản phẩm(</span>)',
    r'\g<1>10 sản phẩm\g<2>',
    html_content
)

# 3. Insert Apple products right at the start of Apple product-grid
apple_cards = "\n\n".join([generate_product_card(**p) for p in apple_products])
apple_anchor = 'Apple Authorized Reseller (AAR VN/A)</h2>'
pos_apple = html_content.find(apple_anchor)
if pos_apple != -1:
    grid_pos = html_content.find('<div class="product-grid">', pos_apple)
    if grid_pos != -1:
        insert_at = grid_pos + len('<div class="product-grid">\n')
        html_content = html_content[:insert_at] + apple_cards + "\n\n" + html_content[insert_at:]
        print("Inserted 6 Apple next-gen flagships successfully")

# 4. Insert Samsung products right at the start of Samsung product-grid
samsung_cards = "\n\n".join([generate_product_card(**p) for p in samsung_products])
samsung_anchor = 'Samsung Galaxy AI Premium Experience Store</h2>'
pos_samsung = html_content.find(samsung_anchor)
if pos_samsung != -1:
    grid_pos = html_content.find('<div class="product-grid">', pos_samsung)
    if grid_pos != -1:
        insert_at = grid_pos + len('<div class="product-grid">\n')
        html_content = html_content[:insert_at] + samsung_cards + "\n\n" + html_content[insert_at:]
        print("Inserted 4 Samsung next-gen flagships successfully")

# 5. Insert OPPO product right at start of OPPO product-grid
oppo_cards = "\n\n".join([generate_product_card(**p) for p in oppo_products])
oppo_anchor = 'OPPO Flagship & AI Portrait Store</h2>'
pos_oppo = html_content.find(oppo_anchor)
if pos_oppo != -1:
    grid_pos = html_content.find('<div class="product-grid">', pos_oppo)
    if grid_pos != -1:
        insert_at = grid_pos + len('<div class="product-grid">\n')
        html_content = html_content[:insert_at] + oppo_cards + "\n\n" + html_content[insert_at:]
        print("Inserted 1 OPPO next-gen flagship successfully")

# 6. Insert Huawei product right at start of Huawei product-grid
huawei_cards = "\n\n".join([generate_product_card(**p) for p in huawei_products])
huawei_anchor = 'Huawei Technologies & HarmonyOS</h2>'
pos_huawei = html_content.find(huawei_anchor)
if pos_huawei != -1:
    grid_pos = html_content.find('<div class="product-grid">', pos_huawei)
    if grid_pos != -1:
        insert_at = grid_pos + len('<div class="product-grid">\n')
        html_content = html_content[:insert_at] + huawei_cards + "\n\n" + html_content[insert_at:]
        print("Inserted 1 Huawei next-gen flagship successfully")

# 7. Insert Realme product right at start of Realme product-grid
realme_cards = "\n\n".join([generate_product_card(**p) for p in realme_products])
realme_anchor = 'Realme / Celmi Dám Đột Phá (Dare to Leap)</h2>'
pos_realme = html_content.find(realme_anchor)
if pos_realme != -1:
    grid_pos = html_content.find('<div class="product-grid">', pos_realme)
    if grid_pos != -1:
        insert_at = grid_pos + len('<div class="product-grid">\n')
        html_content = html_content[:insert_at] + realme_cards + "\n\n" + html_content[insert_at:]
        print("Inserted 1 Realme next-gen flagship successfully")

# 8. Update keyTerms in chatbot
old_keyterms = "var keyTerms = ['16 pro max', '16 pro', '16 plus', '16'"
new_keyterms = "var keyTerms = ['17 pro max', '17 air', '17 pro', '17', '18 pro max', '18 fold', '18 duo', 's25 ultra', 's25+', 's25', 'z fold se', 'gt 7 pro', 'mate 70', 'find n5', '16 pro max', '16 pro', '16 plus', '16'"
html_content = html_content.replace(old_keyterms, new_keyterms)
print("Updated keyTerms in AI Chatbot")

with open(target_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"File updated. New length: {len(html_content)}")
