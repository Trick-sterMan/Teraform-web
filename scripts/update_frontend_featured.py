with open("/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/frontend/index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Add Next-Gen Featured Cards to Frontend Home Page
nextgen_frontend_cards = """
            <!-- Product: iPhone 17 Pro Max -->
            <div class="product-card" style="border: 2px solid #3b82f6;">
                <span class="tag-discount" style="background: #2563eb;">⚡ ĐẶT TRƯỚC 2025</span>
                <div class="product-img-box">
                    <img src="/assets/iphone_17_pro_max.jpg" alt="iPhone 17 Pro Max" class="product-img">
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
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/iphone_17_pro_max.jpg">Titan Bạc Ánh Xanh</button>
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
                    <img src="/assets/iphone_18_duo.jpg" alt="iPhone 18 Fold Duo" class="product-img">
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
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/iphone_18_duo.jpg">Space Titanium</button>
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
                    <img src="/assets/samsung_s25_ultra_render.jpg" alt="Samsung Galaxy S25 Ultra" class="product-img">
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
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/samsung_s25_ultra_render.jpg">Xám Titan</button>
                            <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s25_ultra.jpg">Bạc Ánh Xanh</button>
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
                    <img src="/assets/samsung_zfold_se.jpg" alt="Galaxy Z Fold Special Edition" class="product-img">
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
                            <button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/samsung_zfold_se.jpg">Titan Đen Sọc</button>
                        </div>
                    </div>
                </div>
                <div class="price-row">
                    <span class="current-price">56.990.000 ₫</span>
                    <span class="old-price">62.990.000 ₫</span>
                </div>
                <a href="/products/" class="btn-add-cart">Đặt trước ngay &rarr;</a>
            </div>
"""

pos_grid = text.find('<div class="product-grid">')
if pos_grid != -1:
    insert_at = pos_grid + len('<div class="product-grid">\n')
    new_text = text[:insert_at] + nextgen_frontend_cards + text[insert_at:]
    with open("/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/frontend/index.html", "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Added next-gen flagship cards to frontend home page!")
