import os, sys, re, shutil

file_path = '/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update brand-count-badge for Apple to 30 sản phẩm
content = re.sub(
    r'(<h2 class="brand-title">Apple Authorized Reseller \(AAR VN/A\)</h2>\s*<span class="brand-count-badge">)\d+ sản phẩm(</span>)',
    r'\g<1>30 sản phẩm\g<2>',
    content
)

# 2. Update iPhone 13 Pro Max card
new_13_pm = '''<div class="product-card" data-brand="Apple">
                        <button type="button" class="btn-wishlist" onclick="toggleWishlist(this)" title="Thêm vào yêu thích">🤍</button>
                        <span class="tag-badge">👑 Huyền Thoại 120Hz</span>
                        <span class="stock-tag">✓ Còn hàng</span>
                        <div class="product-img-box">
                            <img src="/assets/real_iphone_13_pro_max_sierra_blue.jpg" alt="iPhone 13 Pro Max" class="product-img">
                            <button type="button" class="btn-quick-view" onclick="openQuickView(this)">👁️ Xem nhanh</button>
                        </div>
                        <div class="product-category">Điện Thoại Apple VN/A</div>
                        <h3 class="product-name">iPhone 13 Pro Max</h3>
                        <div class="product-specs">Chip Apple A15 Bionic 5-core GPU • Màn hình Super Retina XDR 6.7" ProMotion 120Hz • 3 Camera Pro 12MP Macro • Pin trâu vượt trội</div>
                        <div class="variant-section">
                            <div class="variant-group" data-type="storage">
                                <span class="variant-label">Dung lượng:</span>
                                <div class="variant-options">
                                    <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="17990000" data-oldprice="23990000">128GB</button>
                                    <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="19990000" data-oldprice="26990000">256GB</button>
                                    <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="22990000" data-oldprice="29990000">512GB</button>
                                    <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="25990000" data-oldprice="33990000">1TB</button>
                                </div>
                            </div>
                            <div class="variant-group" data-type="color">
                                <span class="variant-label">Màu sắc:</span>
                                <div class="variant-options">
                                    <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_13_pro_max_sierra_blue.jpg">Xanh Sierra Blue</button>
                                    <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/real_iphone_13_pro_max_graphite.jpg">Xám Than Chì Graphite</button>
                                </div>
                            </div>
                        </div>
                        <div class="card-promo">🎁 Tặng củ sạc nhanh Apple 20W + Dán cường lực miễn phí</div>
                        <div class="price-row">
                            <span class="current-price">17.990.000 ₫</span>
                            <span class="old-price">23.990.000 ₫</span>
                        </div>
                        <div class="card-actions">
                            <button type="button" class="btn-cart-mini" onclick="addToCart(this)">Thêm giỏ</button>
                            <button type="button" class="btn-buy-now" onclick="buyNow(this)">Mua ngay</button>
                        </div>
                    </div>'''

pattern_13 = r'<div class="product-card" data-brand="Apple">\s*<button type="button" class="btn-wishlist"[^>]*>.*?</button>\s*<span class="tag-badge">👑 Huyền Thoại 120Hz</span>.*?<h3 class="product-name">iPhone 13 Pro Max</h3>.*?</div>\s*</div>'
match_13 = re.search(pattern_13, content, re.DOTALL)
if match_13:
    content = content[:match_13.start()] + new_13_pm + content[match_13.end():]
    print('Updated iPhone 13 Pro Max card')
else:
    print('WARNING: iPhone 13 Pro Max pattern not matched!')

# 3. Add iPhone 12 Pro Max and iPhone 11 Pro Max
cards_12_11 = '''
                    <div class="product-card" data-brand="Apple">
                        <button type="button" class="btn-wishlist" onclick="toggleWishlist(this)" title="Thêm vào yêu thích">🤍</button>
                        <span class="tag-badge">💎 Khung Thép & LiDAR</span>
                        <span class="stock-tag">✓ Còn hàng</span>
                        <div class="product-img-box">
                            <img src="/assets/real_iphone_12_pro_max_pacific_blue.jpg" alt="iPhone 12 Pro Max" class="product-img">
                            <button type="button" class="btn-quick-view" onclick="openQuickView(this)">👁️ Xem nhanh</button>
                        </div>
                        <div class="product-category">Điện Thoại Apple VN/A</div>
                        <h3 class="product-name">iPhone 12 Pro Max</h3>
                        <div class="product-specs">Chip Apple A14 Bionic 5nm • Màn hình Super Retina XDR 6.7" Ceramic Shield • 3 Camera 12MP LiDAR Night Mode • Kết nối 5G tốc độ cao</div>
                        <div class="variant-section">
                            <div class="variant-group" data-type="storage">
                                <span class="variant-label">Dung lượng:</span>
                                <div class="variant-options">
                                    <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="13990000" data-oldprice="18990000">128GB</button>
                                    <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="15990000" data-oldprice="20990000">256GB</button>
                                    <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="17990000" data-oldprice="23990000">512GB</button>
                                </div>
                            </div>
                            <div class="variant-group" data-type="color">
                                <span class="variant-label">Màu sắc:</span>
                                <div class="variant-options">
                                    <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_12_pro_max_pacific_blue.jpg">Xanh Pacific Blue</button>
                                    <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/real_iphone_12_pro_max_graphite.jpg">Xám Than Chì Graphite</button>
                                </div>
                            </div>
                        </div>
                        <div class="card-promo">🎁 Tặng sạc nhanh 20W + Bảo hành 12 tháng 1 đổi 1</div>
                        <div class="price-row">
                            <span class="current-price">13.990.000 ₫</span>
                            <span class="old-price">18.990.000 ₫</span>
                        </div>
                        <div class="card-actions">
                            <button type="button" class="btn-cart-mini" onclick="addToCart(this)">Thêm giỏ</button>
                            <button type="button" class="btn-buy-now" onclick="buyNow(this)">Mua ngay</button>
                        </div>
                    </div>

                    <div class="product-card" data-brand="Apple">
                        <button type="button" class="btn-wishlist" onclick="toggleWishlist(this)" title="Thêm vào yêu thích">🤍</button>
                        <span class="tag-badge">👑 Khởi Nguyên Pro Max</span>
                        <span class="stock-tag">✓ Còn hàng</span>
                        <div class="product-img-box">
                            <img src="/assets/real_iphone_11_pro_max_midnight_green.jpg" alt="iPhone 11 Pro Max" class="product-img">
                            <button type="button" class="btn-quick-view" onclick="openQuickView(this)">👁️ Xem nhanh</button>
                        </div>
                        <div class="product-category">Điện Thoại Apple VN/A</div>
                        <h3 class="product-name">iPhone 11 Pro Max</h3>
                        <div class="product-specs">Chip Apple A13 Bionic • Màn hình Super Retina XDR OLED 6.5" siêu nét • 3 Camera Pro 12MP chụp góc siêu rộng • Kính mờ sang trọng</div>
                        <div class="variant-section">
                            <div class="variant-group" data-type="storage">
                                <span class="variant-label">Dung lượng:</span>
                                <div class="variant-options">
                                    <button type="button" class="variant-pill active" onclick="selectStorage(this)" data-price="8990000" data-oldprice="12990000">64GB</button>
                                    <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="10990000" data-oldprice="14990000">256GB</button>
                                    <button type="button" class="variant-pill" onclick="selectStorage(this)" data-price="12490000" data-oldprice="16990000">512GB</button>
                                </div>
                            </div>
                            <div class="variant-group" data-type="color">
                                <span class="variant-label">Màu sắc:</span>
                                <div class="variant-options">
                                    <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_11_pro_max_midnight_green.jpg">Xanh Rêu Midnight Green</button>
                                    <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/real_iphone_11_pro_max_space_gray.jpg">Xám Không Gian Space Gray</button>
                                </div>
                            </div>
                        </div>
                        <div class="card-promo">🎁 Tặng củ sạc nhanh 20W + Kính cường lực trọn đời máy</div>
                        <div class="price-row">
                            <span class="current-price">8.990.000 ₫</span>
                            <span class="old-price">12.990.000 ₫</span>
                        </div>
                        <div class="card-actions">
                            <button type="button" class="btn-cart-mini" onclick="addToCart(this)">Thêm giỏ</button>
                            <button type="button" class="btn-buy-now" onclick="buyNow(this)">Mua ngay</button>
                        </div>
                    </div>'''

pattern_13_base = r'(<h3 class="product-name">iPhone 13</h3>.*?</div>\s*</div>)'
match_13_base = re.search(pattern_13_base, content, re.DOTALL)
if match_13_base:
    idx = match_13_base.end()
    content = content[:idx] + '\n' + cards_12_11 + content[idx:]
    print('Inserted iPhone 12 Pro Max and 11 Pro Max successfully!')
else:
    print('WARNING: iPhone 13 base card not found!')

# 4. Update specificModelTerms in chatbot
target_terms = "'14 pro max', '13 pro max', '13',"
replacement_terms = "'14 pro max', '13 pro max', '13', '12 pro max', '12', '11 pro max', '11',"
if target_terms in content:
    content = content.replace(target_terms, replacement_terms)
    print('Updated specificModelTerms in chatbot')
else:
    print('WARNING: target_terms not found in chatbot script')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

nested_path = '/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/products/index.html'
shutil.copy2(file_path, nested_path)
print('Synchronized products/index.html and products/products/index.html')
