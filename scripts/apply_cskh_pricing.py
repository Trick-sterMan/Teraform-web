import re
from html.parser import HTMLParser

with open('/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. New CSS for Price Card & Lookup in Chat & CSKH Hub
price_chat_css = """
        /* Interactive Chat Price Card */
        .chat-price-card { background: white; border: 1.5px solid #a7f3d0; border-radius: 14px; padding: 12px; margin-top: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.06); }
        .chat-price-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px dashed #e2e8f0; }
        .chat-price-thumb { width: 50px; height: 50px; border-radius: 8px; background: #f8fafc; border: 1px solid #cbd5e1; padding: 4px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
        .chat-price-thumb img { max-width: 100%; max-height: 100%; object-fit: contain; }
        .chat-price-title { font-size: 0.9rem; font-weight: 800; color: #0f172a; line-height: 1.25; }
        .chat-price-brand { font-size: 0.7rem; color: #059669; font-weight: 700; text-transform: uppercase; }
        .chat-price-main { display: flex; align-items: baseline; gap: 8px; margin-bottom: 6px; }
        .chat-price-num { font-size: 1.15rem; font-weight: 800; color: #059669; }
        .chat-price-old { font-size: 0.8rem; color: #94a3b8; text-decoration: line-through; }
        .chat-price-variants { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px; font-size: 0.775rem; margin-bottom: 8px; }
        .chat-price-variant-row { display: flex; justify-content: space-between; padding: 2px 0; border-bottom: 1px dashed #edf2f7; }
        .chat-price-variant-row:last-child { border-bottom: none; }
        .chat-price-highlight { font-size: 0.775rem; background: #ecfdf5; border-left: 3px solid #10b981; padding: 6px 8px; border-radius: 0 6px 6px 0; margin-bottom: 8px; color: #065f46; }
        .chat-price-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 6px; }
        .btn-chat-add { background: #ecfdf5; border: 1px solid #10b981; color: #059669; font-size: 0.75rem; font-weight: 700; padding: 6px; border-radius: 6px; cursor: pointer; text-align: center; }
        .btn-chat-add:hover { background: #d1fae5; }
        .btn-chat-buy { background: #059669; border: none; color: white; font-size: 0.75rem; font-weight: 700; padding: 6px; border-radius: 6px; cursor: pointer; text-align: center; }
        .btn-chat-buy:hover { background: #047857; }

        /* Quick Price Lookup Bar inside Chat Window */
        .chat-lookup-bar { padding: 6px 10px; background: #ecfdf5; border-bottom: 1px solid #a7f3d0; display: flex; align-items: center; gap: 6px; }
        .chat-lookup-select { flex: 1; padding: 4px 8px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 0.775rem; font-weight: 600; outline: none; background: white; cursor: pointer; }

        /* CSKH Pricing Table in Knowledge Hub */
        .cskh-price-table-wrap { max-height: 400px; overflow-y: auto; border: 1px solid #cbd5e1; border-radius: 12px; margin-top: 1rem; }
        .cskh-price-table { width: 100%; border-collapse: collapse; font-size: 0.825rem; }
        .cskh-price-table th { background: #f8fafc; padding: 10px 12px; text-align: left; font-weight: 700; color: #1e293b; border-bottom: 2px solid #e2e8f0; position: sticky; top: 0; z-index: 5; }
        .cskh-price-table td { padding: 8px 12px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
        .cskh-price-table tr:hover { background: #f0fdf4; }
"""

content = content.replace('</style>', price_chat_css + '\n    </style>', 1)
print('Injected price chat CSS')

# 2. Add Quick Price Lookup dropdown directly under chat-header
chat_header_marker = """        <div class="chat-header">
            <div class="chat-header-info">
                <div class="chat-avatar">🤖</div>
                <div>
                    <div class="chat-header-title">CloudMart Smart Advisor</div>
                    <div class="chat-header-sub"><span style="width: 6px; height: 6px; border-radius: 50%; background: #4ade80;"></span> Trực tuyến • Tư vấn 24/7</div>
                </div>
            </div>
            <button type="button" class="chat-header-close" onclick="toggleChatWindow()">✕</button>
        </div>"""

chat_header_new = """        <div class="chat-header">
            <div class="chat-header-info">
                <div class="chat-avatar">🤖</div>
                <div>
                    <div class="chat-header-title">CloudMart Smart Advisor</div>
                    <div class="chat-header-sub"><span style="width: 6px; height: 6px; border-radius: 50%; background: #4ade80;"></span> Trực tuyến • Báo giá tức thì</div>
                </div>
            </div>
            <button type="button" class="chat-header-close" onclick="toggleChatWindow()">✕</button>
        </div>

        <!-- Quick Price Lookup Bar -->
        <div class="chat-lookup-bar">
            <span style="font-size: 0.75rem; font-weight: 700; color: #065f46; white-space: nowrap;">🏷️ Tra giá nhanh:</span>
            <select class="chat-lookup-select" id="chatProductSelect" onchange="handleChatSelectPrice(this)">
                <option value="">-- Chọn máy để xem bảng giá --</option>
            </select>
        </div>"""

content = content.replace(chat_header_marker, chat_header_new, 1)
print('Injected chat lookup bar')

# 3. Add Tab 0: Bảng Báo Giá 40 Sản Phẩm into CSKH Knowledge Hub
cskh_tabs_marker = """            <!-- Hub Navigation Tabs -->
            <div class="cskh-tabs">
                <button type="button" class="cskh-tab active" onclick="selectCskhTab('tab-warranty', this)">🛡️ Bảo Hành & 1 Đổi 1</button>
                <button type="button" class="cskh-tab" onclick="selectCskhTab('tab-payment', this)">💳 Trả Góp 0% & VietQR</button>
                <button type="button" class="cskh-tab" onclick="selectCskhTab('tab-shipping', this)">🚚 Vận Chuyển & Đồng Kiểm</button>
                <button type="button" class="cskh-tab" onclick="selectCskhTab('tab-faq', this)">❓ Câu Hỏi Thường Gặp (FAQ)</button>
            </div>"""

cskh_tabs_new = """            <!-- Hub Navigation Tabs -->
            <div class="cskh-tabs">
                <button type="button" class="cskh-tab active" onclick="selectCskhTab('tab-pricing', this)">💰 Bảng Báo Giá 40 Sản Phẩm</button>
                <button type="button" class="cskh-tab" onclick="selectCskhTab('tab-warranty', this)">🛡️ Bảo Hành & 1 Đổi 1</button>
                <button type="button" class="cskh-tab" onclick="selectCskhTab('tab-payment', this)">💳 Trả Góp 0% & VietQR</button>
                <button type="button" class="cskh-tab" onclick="selectCskhTab('tab-shipping', this)">🚚 Vận Chuyển & Đồng Kiểm</button>
                <button type="button" class="cskh-tab" onclick="selectCskhTab('tab-faq', this)">❓ Câu Hỏi Thường Gặp (FAQ)</button>
            </div>

            <!-- Tab 0: Bảng báo giá sản phẩm -->
            <div class="cskh-content-pane active" id="tab-pricing">
                <div style="display: flex; justify-content: space-between; align-items: center; gap: 1rem; flex-wrap: wrap;">
                    <p style="font-size: 0.85rem; color: #64748b; margin: 0;">Tra cứu giá niêm yết, ưu đãi quét mã VietQR và mức trả góp 0% cho từng dòng máy:</p>
                    <input type="text" id="cskhPriceSearch" oninput="filterCskhPriceTable(this.value)" placeholder="Lọc theo tên máy (iPhone, S25, ROG...)..." style="padding: 0.45rem 0.85rem; border-radius: 8px; border: 1.5px solid #cbd5e1; font-size: 0.8rem; outline: none; min-width: 220px;">
                </div>
                <div class="cskh-price-table-wrap">
                    <table class="cskh-price-table">
                        <thead>
                            <tr>
                                <th>Sản phẩm</th>
                                <th>Hãng</th>
                                <th>Giá chính hãng</th>
                                <th>Ưu đãi VietQR (-500k)</th>
                                <th>Trả góp 0% / tháng</th>
                                <th>Tư vấn & Mua</th>
                            </tr>
                        </thead>
                        <tbody id="cskhPriceTableBody">
                            <!-- Rendered by JS -->
                        </tbody>
                    </table>
                </div>
            </div>"""

content = content.replace(cskh_tabs_marker, cskh_tabs_new, 1)
content = content.replace('<div class="cskh-content-pane active" id="tab-warranty">', '<div class="cskh-content-pane" id="tab-warranty">', 1)
print('Injected Pricing Tab in CSKH Hub')

# 4. Add '💬 Tư vấn & Báo giá' button in Quick View modal
qv_actions_marker = """                <div class="qv-actions">
                    <button type="button" class="btn-cart-mini" id="qvBtnAdd" style="padding: 0.8rem; font-size: 0.95rem;">Thêm vào giỏ</button>
                    <button type="button" class="btn-buy-now" id="qvBtnBuy" style="padding: 0.8rem; font-size: 0.95rem;">Mua ngay</button>
                </div>"""

qv_actions_new = """                <div class="qv-actions">
                    <button type="button" class="btn-cart-mini" id="qvBtnAdd" style="padding: 0.8rem; font-size: 0.95rem;">Thêm vào giỏ</button>
                    <button type="button" class="btn-buy-now" id="qvBtnBuy" style="padding: 0.8rem; font-size: 0.95rem;">Mua ngay</button>
                </div>
                <button type="button" id="qvBtnAskPrice" style="width: 100%; margin-top: 0.65rem; background: #ecfdf5; border: 1.5px solid #10b981; color: #059669; padding: 0.65rem; border-radius: 10px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 0.875rem;">
                    <span>💬</span> Hỏi báo giá chi tiết & ưu đãi máy này
                </button>"""

content = content.replace(qv_actions_marker, qv_actions_new, 1)
print('Added ask price button in Quick View')

# 5. JavaScript logic for dynamic catalog pricing advisor
js_script = """
        // ==============================================================
        // BỘ NÃO TƯ VẤN & BÁO GIÁ ĐỘNG TỪ 40 SẢN PHẨM CATALOG
        // ==============================================================
        function getCatalogProductsData() {
            var cards = document.querySelectorAll('.product-card');
            var list = [];
            cards.forEach(function(card) {
                var nameEl = card.querySelector('.product-name');
                var priceEl = card.querySelector('.current-price');
                var oldPriceEl = card.querySelector('.old-price');
                var imgEl = card.querySelector('.product-img');
                var promoEl = card.querySelector('.card-promo');
                var brand = card.getAttribute('data-brand') || '';

                var name = nameEl ? nameEl.innerText.trim() : '';
                var priceText = priceEl ? priceEl.innerText.trim() : '0 ₫';
                var priceNum = parseInt(priceText.replace(/[^0-9]/g, ''), 10) || 0;
                var oldPriceText = oldPriceEl ? oldPriceEl.innerText.trim() : '';
                var img = imgEl ? imgEl.getAttribute('src') : '';
                var promo = promoEl ? promoEl.innerText.trim() : '';

                var storageVariants = [];
                card.querySelectorAll('.variant-group[data-type="storage"] .variant-pill, .variant-group:first-child .variant-pill').forEach(function(pill) {
                    var label = pill.innerText.trim();
                    var pNum = parseInt(pill.getAttribute('data-price'), 10) || priceNum;
                    storageVariants.push({ label: label, priceFormatted: Number(pNum).toLocaleString('vi-VN') + ' ₫' });
                });

                var colors = [];
                card.querySelectorAll('.variant-group[data-type="color"] .variant-pill').forEach(function(pill) {
                    colors.push(pill.innerText.trim());
                });

                var vietqrPrice = Math.max(0, priceNum - 500000);
                var monthlyInstallment = Math.round(priceNum / 12);

                list.push({
                    card: card,
                    name: name,
                    brand: brand,
                    priceNum: priceNum,
                    priceFormatted: priceText,
                    oldPriceFormatted: oldPriceText,
                    vietqrPriceFormatted: Number(vietqrPrice).toLocaleString('vi-VN') + ' ₫',
                    installmentMonthlyFormatted: Number(monthlyInstallment).toLocaleString('vi-VN') + ' ₫/tháng',
                    img: img,
                    promo: promo,
                    variants: storageVariants,
                    colors: colors
                });
            });
            return list;
        }

        function createPriceCardHTML(prod) {
            var variantsHtml = '';
            if (prod.variants && prod.variants.length > 0) {
                variantsHtml += '<div class="chat-price-variants">' +
                    '<strong style="color: #1e293b; display: block; margin-bottom: 4px;">📊 Giá chi tiết từng phiên bản:</strong>';
                prod.variants.forEach(function(v) {
                    variantsHtml += '<div class="chat-price-variant-row"><span>' + v.label + '</span><strong style="color: #059669;">' + v.priceFormatted + '</strong></div>';
                });
                variantsHtml += '</div>';
            }

            var colorsHtml = prod.colors && prod.colors.length > 0 ? ('<div style="font-size: 0.72rem; color: #64748b; margin-bottom: 6px;">🎨 Màu sắc: <strong>' + prod.colors.join(', ') + '</strong></div>') : '';
            var promoHtml = prod.promo ? ('<div style="font-size: 0.72rem; color: #b45309; background: #fffbeb; padding: 4px 6px; border-radius: 4px; margin-bottom: 6px;">' + prod.promo + '</div>') : '';

            var cardHtml = '<div class="chat-price-card">' +
                '<div class="chat-price-header">' +
                    '<div class="chat-price-thumb"><img src="' + prod.img + '" alt="' + prod.name + '"></div>' +
                    '<div>' +
                        '<div class="chat-price-brand">' + prod.brand + ' CHÍNH HÃNG</div>' +
                        '<div class="chat-price-title">' + prod.name + '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="chat-price-main">' +
                    '<span class="chat-price-num">' + prod.priceFormatted + '</span>' +
                    (prod.oldPriceFormatted ? ('<span class="chat-price-old">' + prod.oldPriceFormatted + '</span>') : '') +
                '</div>' +
                colorsHtml +
                variantsHtml +
                '<div class="chat-price-highlight">' +
                    '<div>⚡ Giá thanh toán VietQR: <strong>' + prod.vietqrPriceFormatted + '</strong> (-500k)</div>' +
                    '<div>💳 Trả góp 0% (12 tháng): chỉ từ <strong>' + prod.installmentMonthlyFormatted + '</strong></div>' +
                '</div>' +
                promoHtml +
                '<div class="chat-price-actions">' +
                    '<button type="button" class="btn-chat-add" onclick="addChatProductToCart(\\'' + prod.name.replace(/'/g, "\\\\'") + '\\')">🛒 Thêm vào giỏ</button>' +
                    '<button type="button" class="btn-chat-buy" onclick="buyChatProductNow(\\'' + prod.name.replace(/'/g, "\\\\'") + '\\')">⚡ Mua ngay</button>' +
                '</div>' +
            '</div>';
            return cardHtml;
        }

        function addChatProductToCart(name) {
            addToCart(name);
            openCartDrawer();
        }

        function buyChatProductNow(name) {
            addToCart(name);
            window.location.href = '/checkout/';
        }

        function handleChatSelectPrice(select) {
            var val = select.value;
            if (!val) return;
            appendUserMessage('Cho mình xin bảng giá chi tiết máy ' + val);
            select.value = '';
            generateBotReply('giá ' + val);
        }

        function generateBotReply(q) {
            var lower = q.toLowerCase();
            var catalog = getCatalogProductsData();

            setTimeout(function() {
                // 1. Tìm kiếm sản phẩm tương thích nhất trong danh mục 40 máy
                var matchedProducts = [];
                catalog.forEach(function(p) {
                    var pNameLower = p.name.toLowerCase();
                    if (lower.includes(pNameLower) || pNameLower.includes(lower)) {
                        matchedProducts.push(p);
                    } else {
                        var cleanQ = lower.replace(/giá|bao nhiêu|báo giá|bao nhieu|cho hỏi|máy|chi tiết|bao|nhiêu/g, '').trim();
                        var tokens = cleanQ.split(/\s+/);
                        var matchCount = 0;
                        tokens.forEach(function(tok) {
                            if (tok && tok.length > 1 && pNameLower.includes(tok)) matchCount++;
                        });
                        if (matchCount >= 2 || (tokens.length === 1 && tokens[0].length >= 3 && pNameLower.includes(tokens[0]))) {
                            matchedProducts.push(p);
                        }
                    }
                });

                if (matchedProducts.length > 0) {
                    var topProds = matchedProducts.slice(0, 2);
                    var replyText = 'Dạ em gửi quý khách <strong>Bảng báo giá chính hãng & Ưu đãi</strong> tốt nhất hôm nay cho sản phẩm quý khách đang quan tâm ạ:';
                    topProds.forEach(function(prod) {
                        replyText += createPriceCardHTML(prod);
                    });
                    appendBotMessage(replyText);
                    return;
                }

                // 2. Các câu hỏi chính sách thông thường
                if (lower.includes('bảo hành') || lower.includes('1 đổi 1') || lower.includes('đổi trả')) {
                    appendBotMessage('🛡️ <strong>Chính sách Bảo Hành & 1 Đổi 1:</strong><br>• Cam kết 100% hàng phân phối chính hãng (VN/A, Samsung Vina, Sony, Dell, ASUS).<br>• Đổi mới 1-1 trong 30 ngày nếu phát sinh lỗi phần cứng.<br>• Bảo hành 12 - 24 tháng tại trung tâm ủy quyền toàn quốc, hỗ trợ miễn phí lấy máy tận nhà!<br><button type="button" onclick="openCskhModal()" style="background: #ecfdf5; border: 1px solid #059669; color: #059669; font-weight: 700; padding: 4px 8px; border-radius: 6px; cursor: pointer; margin-top: 4px;">Xem chi tiết chính sách</button>');
                } else if (lower.includes('trả góp') || lower.includes('thẻ tín dụng') || lower.includes('lãi suất')) {
                    appendBotMessage('💳 <strong>Chính sách Trả Góp 0%:</strong><br>• Áp dụng cho thẻ tín dụng liên kết hơn 25 ngân hàng (VCB, MB, Techcombank, VPBank...).<br>• Kỳ hạn linh hoạt 3, 6, 9, 12 tháng.<br>• Không cần chứng minh thu nhập, kích hoạt ngay tại trang Thanh toán!');
                } else if (lower.includes('giao hàng') || lower.includes('ship') || lower.includes('vận chuyển') || lower.includes('đồng kiểm')) {
                    appendBotMessage('🚚 <strong>Chính sách Giao Hàng & Đồng Kiểm:</strong><br>• Giao siêu tốc trong 2H tại nội thành TP.HCM & Hà Nội.<br>• Khách hàng được <strong>mở hộp đồng kiểm</strong> tem seal máy và phụ kiện trước khi thanh toán.<br>• Miễn phí giao hàng toàn quốc!');
                } else if (lower.includes('vietqr') || lower.includes('giảm 500k') || lower.includes('voucher') || lower.includes('khuyến mãi')) {
                    appendBotMessage('⚡ <strong>Ưu đãi VietQR 24/7:</strong><br>• Giảm ngay 500.000₫ khi quét mã VietQR Napas 247 qua App ngân hàng.<br>• Nhập mã voucher <code>CLOUDMART10</code> tại trang thanh toán để được giảm thêm 1.500.000₫!');
                } else {
                    appendBotMessage('Dạ quý khách cần báo giá hoặc tư vấn sản phẩm cụ thể nào ạ? Quý khách có thể chọn nhanh dòng máy ở thanh <strong>"🏷️ Tra giá nhanh"</strong> ngay phía trên hoặc mở Bảng giá tổng hợp:<br><button type="button" onclick="openCskhModal(); selectCskhTab(\\'tab-pricing\\', document.querySelectorAll(\\'.cskh-tab\\')[0]);" style="background: var(--primary); color: white; border: none; font-weight: 700; padding: 6px 12px; border-radius: 6px; cursor: pointer; margin-top: 6px;">💰 Mở Bảng Giá 40 Máy</button>');
                }
            }, 500);
        }

        // Bật nút hỏi giá trong Quick View
        function setupQuickViewAskPrice() {
            var btn = document.getElementById('qvBtnAskPrice');
            if (btn) {
                btn.onclick = function() {
                    var name = document.getElementById('qvName').innerText;
                    closeQuickView();
                    toggleChatWindow();
                    appendUserMessage('Cho mình xin báo giá chi tiết sản phẩm ' + name);
                    generateBotReply('giá ' + name);
                };
            }
        }

        // Khởi tạo danh sách sản phẩm trong dropdown chat & Bảng giá CSKH Hub
        function populateChatDropdownAndCskhPriceTable() {
            var catalog = getCatalogProductsData();
            var select = document.getElementById('chatProductSelect');
            var tbody = document.getElementById('cskhPriceTableBody');

            if (select && select.options.length <= 1) {
                catalog.forEach(function(p) {
                    var opt = document.createElement('option');
                    opt.value = p.name;
                    opt.innerText = p.name + ' (' + p.priceFormatted + ')';
                    select.appendChild(opt);
                });
            }

            if (tbody) {
                var html = '';
                catalog.forEach(function(p) {
                    html += '<tr>' +
                        '<td><div style="display: flex; align-items: center; gap: 8px;"><img src="' + p.img + '" style="width: 36px; height: 36px; object-fit: contain; border-radius: 6px; border: 1px solid #e2e8f0; padding: 2px;"><strong style="color: #0f172a;">' + p.name + '</strong></div></td>' +
                        '<td><span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 0.72rem;">' + p.brand + '</span></td>' +
                        '<td><strong style="color: #059669;">' + p.priceFormatted + '</strong>' + (p.oldPriceFormatted ? ('<div style="font-size: 0.72rem; color: #94a3b8; text-decoration: line-through;">' + p.oldPriceFormatted + '</div>') : '') + '</td>' +
                        '<td><strong style="color: #047857;">' + p.vietqrPriceFormatted + '</strong></td>' +
                        '<td><span style="color: #d97706; font-weight: 700;">' + p.installmentMonthlyFormatted + '</span></td>' +
                        '<td><button type="button" onclick="askPriceInChat(\\'' + p.name.replace(/'/g, "\\\\'") + '\\')" style="background: #ecfdf5; border: 1px solid #10b981; color: #059669; font-weight: 700; font-size: 0.72rem; padding: 4px 8px; border-radius: 6px; cursor: pointer;">💬 Hỏi giá</button></td>' +
                    '</tr>';
                });
                tbody.innerHTML = html;
            }
        }

        function askPriceInChat(name) {
            closeCskhModal();
            var win = document.getElementById('chatWindow');
            if (win && !win.classList.contains('active')) win.classList.add('active');
            appendUserMessage('Báo giá chi tiết máy ' + name);
            generateBotReply('giá ' + name);
        }

        function filterCskhPriceTable(kw) {
            var k = kw.toLowerCase().trim();
            var rows = document.querySelectorAll('#cskhPriceTableBody tr');
            rows.forEach(function(row) {
                var text = row.innerText.toLowerCase();
                row.style.display = (!k || text.includes(k)) ? '' : 'none';
            });
        }
"""

# Replace generateBotReply function with new dynamic pricing logic
m = re.search(r'function generateBotReply\(q\) \{[\s\S]*?\n        \}', content)
if m:
    content = content.replace(m.group(0), js_script, 1)
    print('Replaced generateBotReply with dynamic catalog pricing engine')
else:
    print('Warning: generateBotReply not found')

# Add setup calls into DOMContentLoaded
content = content.replace(
    "document.addEventListener('DOMContentLoaded', function() {\n            updateWishlistBadges();\n        });",
    "document.addEventListener('DOMContentLoaded', function() {\n            updateWishlistBadges();\n            setupQuickViewAskPrice();\n            setTimeout(populateChatDropdownAndCskhPriceTable, 300);\n        });",
    1
)

# Validate strictly
VOID_TAGS = {'link', 'meta', 'input', 'img', 'hr', 'br', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}

class StrictParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() not in VOID_TAGS:
            self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag.lower() in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f'Closing </{tag}> with empty stack at {self.getpos()}')
            return
        last, pos = self.stack.pop()
        if last.lower() != tag.lower():
            self.errors.append(f'Expected </{last}> (opened at {pos}), but got </{tag}> at {self.getpos()}')

p = StrictParser()
p.feed(content)
print('Validation errors:', len(p.errors))
print('Unclosed tags remaining:', len(p.stack))

if len(p.errors) == 0 and len(p.stack) == 0:
    for target in ['/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html',
                   '/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/products/index.html']:
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
    print('SUCCESS: Both products index.html files updated with dynamic pricing chat & hub!')
else:
    print('Aborting write due to errors!')
