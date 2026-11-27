import os, sys, re, shutil
import html

BASE_DIR = '/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web'
PROD_HTML = os.path.join(BASE_DIR, 'demo_pages/products/index.html')
NESTED_HTML = os.path.join(BASE_DIR, 'demo_pages/products/products/index.html')

with open(PROD_HTML, 'r', encoding='utf-8') as f:
    content = f.read()

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

# 1. Define iPhone Pro Max Cards (13 Pro Max, 12 Pro Max, 11 Pro Max)
card_iphone_13_pm = generate_product_card(
    brand="Apple",
    tag="👑 Huyền Thoại 120Hz",
    stock="✓ Còn hàng",
    img="/assets/real_iphone_13_pro_max_sierra_blue.jpg",
    alt="iPhone 13 Pro Max",
    category="Điện Thoại Apple VN/A",
    name="iPhone 13 Pro Max",
    specs="Chip Apple A15 Bionic 5-core GPU • Màn hình Super Retina XDR 6.7\" ProMotion 120Hz • 3 Camera Pro 12MP Macro • Pin trâu vượt trội",
    storage_variants=[
        {"label": "128GB", "price": 17990000, "old_price": 23990000},
        {"label": "256GB", "price": 19990000, "old_price": 26990000},
        {"label": "512GB", "price": 22990000, "old_price": 29990000},
        {"label": "1TB", "price": 25990000, "old_price": 33990000}
    ],
    color_variants=[
        {"label": "Xanh Sierra Blue", "img": "/assets/real_iphone_13_pro_max_sierra_blue.jpg"},
        {"label": "Xám Than Chì Graphite", "img": "/assets/real_iphone_13_pro_max_graphite.jpg"}
    ],
    promo="🎁 Tặng củ sạc nhanh Apple 20W + Dán cường lực miễn phí",
    price=17990000,
    old_price=23990000
)

card_iphone_12_pm = generate_product_card(
    brand="Apple",
    tag="💎 Khung Thép & LiDAR",
    stock="✓ Còn hàng",
    img="/assets/real_iphone_12_pro_max_pacific_blue.jpg",
    alt="iPhone 12 Pro Max",
    category="Điện Thoại Apple VN/A",
    name="iPhone 12 Pro Max",
    specs="Chip Apple A14 Bionic 5nm • Màn hình Super Retina XDR 6.7\" Ceramic Shield • 3 Camera 12MP LiDAR Night Mode • Kết nối 5G tốc độ cao",
    storage_variants=[
        {"label": "128GB", "price": 13990000, "old_price": 18990000},
        {"label": "256GB", "price": 15990000, "old_price": 20990000},
        {"label": "512GB", "price": 17990000, "old_price": 23990000}
    ],
    color_variants=[
        {"label": "Xanh Pacific Blue", "img": "/assets/real_iphone_12_pro_max_pacific_blue.jpg"},
        {"label": "Xám Than Chì Graphite", "img": "/assets/real_iphone_12_pro_max_graphite.jpg"}
    ],
    promo="🎁 Tặng sạc nhanh 20W + Bảo hành 12 tháng 1 đổi 1",
    price=13990000,
    old_price=18990000
)

card_iphone_11_pm = generate_product_card(
    brand="Apple",
    tag="👑 Khởi Nguyên Pro Max",
    stock="✓ Còn hàng",
    img="/assets/real_iphone_11_pro_max_midnight_green.jpg",
    alt="iPhone 11 Pro Max",
    category="Điện Thoại Apple VN/A",
    name="iPhone 11 Pro Max",
    specs="Chip Apple A13 Bionic • Màn hình Super Retina XDR OLED 6.5\" siêu nét • 3 Camera Pro 12MP chụp góc siêu rộng • Kính mờ sang trọng",
    storage_variants=[
        {"label": "64GB", "price": 8990000, "old_price": 12990000},
        {"label": "256GB", "price": 10990000, "old_price": 14990000},
        {"label": "512GB", "price": 12490000, "old_price": 16990000}
    ],
    color_variants=[
        {"label": "Xanh Rêu Midnight Green", "img": "/assets/real_iphone_11_pro_max_midnight_green.jpg"},
        {"label": "Xám Không Gian Space Gray", "img": "/assets/real_iphone_11_pro_max_space_gray.jpg"}
    ],
    promo="🎁 Tặng củ sạc nhanh 20W + Kính cường lực trọn đời máy",
    price=8990000,
    old_price=12990000
)

# 2. Define 7 Pro Max Flagships for Other Brands
card_samsung_pm = generate_product_card(
    brand="Samsung",
    tag="👑 Flagship Pro Max 2025",
    stock="✓ Còn hàng",
    img="/assets/samsung_s25_ultra.jpg",
    alt="Samsung Galaxy S25 Pro Max 5G (Titan AI)",
    category="Smartphone Cao Cấp Samsung Pro Max",
    name="Samsung Galaxy S25 Pro Max 5G (Titan AI)",
    specs="Snapdragon 8 Elite for Galaxy • Khung Titan Cấp Vũ Trụ • Camera 200MP Zoom 100x • Bút S-Pen tích hợp & Galaxy AI Pro",
    storage_variants=[
        {"label": "12GB / 256GB", "price": 31990000, "old_price": 35990000},
        {"label": "16GB / 512GB", "price": 35990000, "old_price": 39990000},
        {"label": "16GB / 1TB", "price": 41990000, "old_price": 45990000}
    ],
    color_variants=[
        {"label": "Xanh Titan AI", "img": "/assets/samsung_s25_ultra.jpg"},
        {"label": "Đen Titan Phantom", "img": "/assets/samsung_s24_black.jpg"}
    ],
    promo="🎁 Tặng Galaxy Buds3 Pro + Bao da Smart View trị giá 4.500.000₫",
    price=31990000,
    old_price=35990000
)

card_sony_pm = generate_product_card(
    brand="Sony",
    tag="👑 Flagship Cinema 4K",
    stock="✓ Còn hàng",
    img="/assets/poster_sony_sony_xperia_1_vi_5g.jpg",
    alt="Sony Xperia 1 VI Pro Max (Cinema 4K OLED)",
    category="Điện Thoại Chuyên Nghiệp Sony Master",
    name="Sony Xperia 1 VI Pro Max (Cinema 4K OLED)",
    specs="Màn hình 4K HDR OLED 120Hz Bravia • Ống kính quang học Zeiss T* Zoom liên tục 85-170mm • Snapdragon 8 Gen 3 & DAC Hi-Res Audio",
    storage_variants=[
        {"label": "12GB / 256GB", "price": 28990000, "old_price": 33990000},
        {"label": "16GB / 512GB", "price": 32990000, "old_price": 37990000}
    ],
    color_variants=[
        {"label": "Đen Cổ Điển Sony", "img": "/assets/poster_sony_sony_xperia_1_vi_5g.jpg"},
        {"label": "Bạc Platinum", "img": "/assets/sony_xm5_silver.jpg"}
    ],
    promo="🎁 Tặng tai nghe Sony LinkBuds S + Thẻ nhớ 256GB tốc độ cao",
    price=28990000,
    old_price=33990000
)

card_dell_pm = generate_product_card(
    brand="Dell",
    tag="👑 Trạm Làm Việc Di Động",
    stock="✓ Còn hàng",
    img="/assets/poster_dell_xps16.jpg",
    alt="Dell XPS 16 Pro Max (Core Ultra 9 / RTX 4070)",
    category="Laptop Doanh Nhân Đỉnh Cao",
    name="Dell XPS 16 Pro Max (Core Ultra 9 / RTX 4070)",
    specs="Intel Core Ultra 9 185H NPU AI • NVIDIA RTX 4070 8GB GDDR6 • Màn hình 16.3\" 4K+ OLED Touch 120Hz • Vỏ nhôm CNC nguyên khối",
    storage_variants=[
        {"label": "32GB / 1TB SSD", "price": 68990000, "old_price": 75990000},
        {"label": "64GB / 2TB SSD", "price": 79990000, "old_price": 87990000}
    ],
    color_variants=[
        {"label": "Bạc Platinum Nhôm", "img": "/assets/poster_dell_xps16.jpg"},
        {"label": "Xám Graphite", "img": "/assets/dell_xps.png"}
    ],
    promo="🎁 Tặng Balo Dell Premier + Chuột không dây Bluetooth Dell MS7421W",
    price=68990000,
    old_price=75990000
)

card_asus_pm = generate_product_card(
    brand="ASUS",
    tag="👑 Quái Thú Gaming 24GB",
    stock="✓ Còn hàng",
    img="/assets/poster_asus_asus_rog_phone_8_pro_snapdragon_8_gen_3.jpg",
    alt="ASUS ROG Phone 9 Pro Max (24GB / 1TB Gaming)",
    category="Smartphone Chuyên Game Đỉnh Nhất",
    name="ASUS ROG Phone 9 Pro Max (24GB / 1TB Gaming)",
    specs="Snapdragon 8 Elite Gaming Edition • Màn hình AMOLED 185Hz siêu mượt • Tản nhiệt buồng hơi 3D + Nút AirTrigger cảm ứng siêu nhạy",
    storage_variants=[
        {"label": "16GB / 512GB", "price": 28990000, "old_price": 32990000},
        {"label": "24GB / 1TB Ultimate", "price": 33990000, "old_price": 38990000}
    ],
    color_variants=[
        {"label": "Đen Phantom ROG", "img": "/assets/poster_asus_asus_rog_phone_8_pro_snapdragon_8_gen_3.jpg"},
        {"label": "Trắng Moonlight", "img": "/assets/asus_rog_white.jpg"}
    ],
    promo="🎁 Tặng Quạt Tản Nhiệt AeroActive Cooler X Pro chính hãng",
    price=28990000,
    old_price=32990000
)

card_oppo_pm = generate_product_card(
    brand="OPPO",
    tag="👑 Camera Hasselblad 120x",
    stock="✓ Còn hàng",
    img="/assets/oppo_find_n5.jpg",
    alt="OPPO Find X8 Pro Max 5G (Hasselblad Zoom 120x)",
    category="Flagship Nhiếp Ảnh OPPO Hasselblad",
    name="OPPO Find X8 Pro Max 5G (Hasselblad Zoom 120x)",
    specs="Hệ thống 4 camera Hasselblad 50MP Dual Periscope • Chip MediaTek Dimensity 9400 3nm • Pin Silicon-Carbon 5910mAh sạc 80W SuperVOOC",
    storage_variants=[
        {"label": "16GB / 512GB", "price": 26990000, "old_price": 30990000},
        {"label": "16GB / 1TB", "price": 30990000, "old_price": 34990000}
    ],
    color_variants=[
        {"label": "Xanh Đảo Ngọc", "img": "/assets/oppo_find_n5.jpg"},
        {"label": "Đen Vũ Trụ", "img": "/assets/oppo_find_n3_fold_black.jpg"}
    ],
    promo="🎁 Tặng Tai nghe OPPO Enco X3 + Ốp lưng từ tính độc quyền",
    price=26990000,
    old_price=30990000
)

card_huawei_pm = generate_product_card(
    brand="Huawei",
    tag="👑 Kính Kunlun Thò Thụt",
    stock="✓ Còn hàng",
    img="/assets/huawei_pura_70_ultra.jpg",
    alt="Huawei Pura 70 Pro Max (Camera 1-inch Kính Kunlun)",
    category="Flagship Siêu Cấp Kính Kunlun",
    name="Huawei Pura 70 Pro Max (Camera 1-inch Kính Kunlun)",
    specs="Cảm biến 1-inch cơ chế thò thụt độc quyền • Kính cường lực Kunlun Glass siêu bền • Chip Kirin 9010 & Liên lạc vệ tinh 2 chiều",
    storage_variants=[
        {"label": "16GB / 512GB", "price": 27990000, "old_price": 32990000},
        {"label": "16GB / 1TB Master", "price": 32990000, "old_price": 37990000}
    ],
    color_variants=[
        {"label": "Xanh Ngọc Lục Bảo", "img": "/assets/huawei_pura_70_ultra.jpg"},
        {"label": "Đen Vân Da Họa Tiết", "img": "/assets/huawei_pura_70_pro_black.jpg"}
    ],
    promo="🎁 Tặng Huawei FreeBuds Pro 3 + Đế sạc không dây siêu tốc 80W",
    price=27990000,
    old_price=32990000
)

card_realme_pm = generate_product_card(
    brand="Realme",
    tag="👑 Quái Kiệt Pin 6500mAh",
    stock="✓ Còn hàng",
    img="/assets/poster_realme_realme_gt_7_pro_5g.jpg",
    alt="Realme GT 7 Pro Max 5G (Snapdragon 8 Elite 6500mAh)",
    category="Flagship Killer Pin Khủng 120W",
    name="Realme GT 7 Pro Max 5G (Snapdragon 8 Elite 6500mAh)",
    specs="Chipset Snapdragon 8 Elite 3nm • Pin khủng 6500mAh Titan sạc siêu nhanh 120W • Màn hình Samsung Eco² OLED Plus 6000 nits đỉnh sáng",
    storage_variants=[
        {"label": "12GB / 256GB", "price": 16990000, "old_price": 19990000},
        {"label": "16GB / 512GB", "price": 19490000, "old_price": 22990000}
    ],
    color_variants=[
        {"label": "Cam Hỏa Tinh Mars", "img": "/assets/poster_realme_realme_gt_7_pro_5g.jpg"},
        {"label": "Xám Titan Cyber", "img": "/assets/realme_gt_6.jpg"}
    ],
    promo="🎁 Tặng Tai nghe Realme Buds Air6 + Sạc dự phòng 20000mAh",
    price=16990000,
    old_price=19990000
)

# ----------------- INSERT CARDS CAREFULLY -----------------

# 1. Apple Section:
# Find iPhone 13 card and place iPhone 13 Pro Max before it, and iPhone 12 Pro Max + iPhone 11 Pro Max after it!
ip13_card_start = content.find('<h3 class="product-name">iPhone 13</h3>')
if ip13_card_start != -1:
    # Find start of iPhone 13 card
    card_start_idx = content.rfind('<div class="product-card" data-brand="Apple">', 0, ip13_card_start)
    # Find end of iPhone 13 card
    card_end_idx = content.find('</div>\n                    </div>', ip13_card_start) + len('</div>\n                    </div>')
    
    # Insert 13 Pro Max BEFORE iPhone 13
    content = content[:card_start_idx] + card_iphone_13_pm + '\n' + content[card_start_idx:]
    
    # Recalculate end index of iPhone 13 after insertion
    ip13_card_start = content.find('<h3 class="product-name">iPhone 13</h3>')
    card_end_idx = content.find('</div>\n                    </div>', ip13_card_start) + len('</div>\n                    </div>')
    
    # Insert 12 Pro Max and 11 Pro Max AFTER iPhone 13
    apple_later_cards = '\n' + card_iphone_12_pm + '\n' + card_iphone_11_pm
    content = content[:card_end_idx] + apple_later_cards + content[card_end_idx:]
    print('Inserted iPhone 13 Pro Max, iPhone 12 Pro Max, and iPhone 11 Pro Max into Apple section!')

# 2. Samsung Section:
# Insert at top of Samsung product-grid
samsung_anchor = content.find('<div id="brand-samsung"')
if samsung_anchor != -1:
    grid_pos = content.find('<div class="product-grid">', samsung_anchor) + len('<div class="product-grid">')
    content = content[:grid_pos] + '\n' + card_samsung_pm + content[grid_pos:]
    print('Inserted Samsung Galaxy S25 Pro Max!')

# 3. Sony Section:
sony_anchor = content.find('<div id="brand-sony"')
if sony_anchor != -1:
    grid_pos = content.find('<div class="product-grid">', sony_anchor) + len('<div class="product-grid">')
    content = content[:grid_pos] + '\n' + card_sony_pm + content[grid_pos:]
    print('Inserted Sony Xperia 1 VI Pro Max!')

# 4. Dell Section:
dell_anchor = content.find('<div id="brand-dell"')
if dell_anchor != -1:
    grid_pos = content.find('<div class="product-grid">', dell_anchor) + len('<div class="product-grid">')
    content = content[:grid_pos] + '\n' + card_dell_pm + content[grid_pos:]
    print('Inserted Dell XPS 16 Pro Max!')

# 5. ASUS Section:
asus_anchor = content.find('<div id="brand-asus"')
if asus_anchor != -1:
    grid_pos = content.find('<div class="product-grid">', asus_anchor) + len('<div class="product-grid">')
    content = content[:grid_pos] + '\n' + card_asus_pm + content[grid_pos:]
    print('Inserted ASUS ROG Phone 9 Pro Max!')

# 6. OPPO Section:
oppo_anchor = content.find('<div id="brand-oppo"')
if oppo_anchor != -1:
    grid_pos = content.find('<div class="product-grid">', oppo_anchor) + len('<div class="product-grid">')
    content = content[:grid_pos] + '\n' + card_oppo_pm + content[grid_pos:]
    print('Inserted OPPO Find X8 Pro Max!')

# 7. Huawei Section:
huawei_anchor = content.find('<div id="brand-huawei"')
if huawei_anchor != -1:
    grid_pos = content.find('<div class="product-grid">', huawei_anchor) + len('<div class="product-grid">')
    content = content[:grid_pos] + '\n' + card_huawei_pm + content[grid_pos:]
    print('Inserted Huawei Pura 70 Pro Max!')

# 8. Realme Section:
realme_anchor = content.find('<div id="brand-realme"')
if realme_anchor != -1:
    grid_pos = content.find('<div class="product-grid">', realme_anchor) + len('<div class="product-grid">')
    content = content[:grid_pos] + '\n' + card_realme_pm + content[grid_pos:]
    print('Inserted Realme GT 7 Pro Max!')

# Update Brand Badges Counts
brand_counts = {
    'Apple': 30,
    'Samsung': 22,
    'Sony': 13,
    'Dell': 12,
    'ASUS': 13,
    'OPPO': 12,
    'Huawei': 11,
    'Realme': 11
}

# Replace badges
content = re.sub(
    r'(<h2 class="brand-title">Apple Authorized Reseller.*?<span class="brand-count-badge">)\d+ sản phẩm(</span>)',
    rf'\g<1>{brand_counts["Apple"]} sản phẩm\g<2>',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'(<h2 class="brand-title">Samsung Galaxy AI.*?<span class="brand-count-badge">)\d+ sản phẩm(</span>)',
    rf'\g<1>{brand_counts["Samsung"]} sản phẩm\g<2>',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'(<h2 class="brand-title">Sony Professional.*?<span class="brand-count-badge">)\d+ sản phẩm(</span>)',
    rf'\g<1>{brand_counts["Sony"]} sản phẩm\g<2>',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'(<h2 class="brand-title">Dell Technologies.*?<span class="brand-count-badge">)\d+ sản phẩm(</span>)',
    rf'\g<1>{brand_counts["Dell"]} sản phẩm\g<2>',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'(<h2 class="brand-title">ASUS Republic of Gamers.*?<span class="brand-count-badge">)\d+ sản phẩm(</span>)',
    rf'\g<1>{brand_counts["ASUS"]} sản phẩm\g<2>',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'(<h2 class="brand-title">OPPO Official Flagship.*?<span class="brand-count-badge">)\d+ sản phẩm(</span>)',
    rf'\g<1>{brand_counts["OPPO"]} sản phẩm\g<2>',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'(<h2 class="brand-title">HUAWEI Flagship Experience.*?<span class="brand-count-badge">)\d+ sản phẩm(</span>)',
    rf'\g<1>{brand_counts["Huawei"]} sản phẩm\g<2>',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'(<h2 class="brand-title">realme Flagship Store.*?<span class="brand-count-badge">)\d+ sản phẩm(</span>)',
    rf'\g<1>{brand_counts["Realme"]} sản phẩm\g<2>',
    content,
    flags=re.DOTALL
)

# Update specificModelTerms in Chatbot
content = content.replace(
    "'14 pro max', '13',",
    "'14 pro max', '13 pro max', '13', '12 pro max', '12', '11 pro max', '11',"
)

# Write to products/index.html and products/products/index.html
with open(PROD_HTML, 'w', encoding='utf-8') as f:
    f.write(content)

shutil.copy2(PROD_HTML, NESTED_HTML)
print('Successfully written and synchronized both products HTML files!')
