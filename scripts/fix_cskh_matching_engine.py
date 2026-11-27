import os, sys, re, shutil

file_path = '/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean all malformed opening tags: <div class="product-card" ... data-brand="..."> -> <div class="product-card" data-brand="...">
content = re.sub(
    r'<div class="product-card"[^>]*data-brand="([^"]+)">',
    r'<div class="product-card" data-brand="\1">',
    content
)

# 2. Define the new, rock-solid matching engine
new_matcher_code = '''function findExactProductMatch(query, catalog) {
            if (!query || !catalog || catalog.length === 0) return null;
            var rawQ = query.trim();
            var lowerQ = rawQ.toLowerCase();

            // 0. Khớp tên 100% nếu truyền đúng tên máy (ví dụ nhấn từ dropdown hoặc modal xem nhanh)
            for (var i = 0; i < catalog.length; i++) {
                var p = catalog[i];
                if (rawQ === p.name || lowerQ === p.name.toLowerCase()) return p;
            }

            // Làm sạch các từ đệm tiếng Việt
            var cleanQ = lowerQ
                .replace(/giá|bao nhiêu|báo giá|bao nhieu|cho hỏi|máy|chi tiết|thông tin|tư vấn|giới thiệu|muốn biết|cần biết|hỏi về|xem|thế nào|sao|tiền|tôi|mình|cho em|cho anh|cho chị|shop ơi|ad ơi/g, ' ')
                .replace(/\\s+/g, ' ')
                .trim();

            if (!cleanQ) return null;

            // Khớp chính xác sau khi bỏ từ đệm
            for (var j = 0; j < catalog.length; j++) {
                var cProd = catalog[j];
                if (cleanQ === cProd.name.toLowerCase()) return cProd;
            }

            // Chuẩn hóa khoảng trắng số (fold 5 -> fold5, s 24 -> s24...)
            var normQ = cleanQ
                .replace(/fold\\s*([0-9]+)/g, 'fold$1')
                .replace(/flip\\s*([0-9]+)/g, 'flip$1')
                .replace(/s\\s*([0-9]+)\\s*\\+/g, 's$1+')
                .replace(/s\\s*([0-9]+)\\s*plus/g, 's$1+')
                .replace(/s\\s*([0-9]+)/g, 's$1')
                .replace(/gt\\s*([0-9]+)/g, 'gt$1')
                .replace(/xm\\s*([0-9]+)/g, 'xm$1')
                .replace(/note\\s*([0-9]+)/g, 'note$1');

            // 1. Nhận diện HÃNG YÊU CẦU từ câu hỏi để cô lập 100%
            var targetBrand = null;
            if (normQ.includes('apple') || normQ.includes('iphone') || normQ.includes('macbook') || normQ.includes('ipad') || normQ.includes('airpods') || normQ.includes('imac')) {
                targetBrand = 'Apple';
            } else if (normQ.includes('samsung') || normQ.includes('galaxy') || normQ.includes('z fold') || normQ.includes('z flip') || normQ.includes('fold5') || normQ.includes('fold6') || normQ.includes('flip6')) {
                targetBrand = 'Samsung';
            } else if (normQ.includes('sony') || normQ.includes('playstation') || normQ.includes('ps5') || normQ.includes('xperia') || normQ.includes('dualsense') || normQ.includes('bravia')) {
                targetBrand = 'Sony';
            } else if (normQ.includes('dell') || normQ.includes('alienware') || normQ.includes('xps')) {
                targetBrand = 'Dell';
            } else if (normQ.includes('asus') || normQ.includes('rog') || normQ.includes('tuf') || normQ.includes('zenbook') || normQ.includes('zephyrus')) {
                targetBrand = 'ASUS';
            } else if (normQ.includes('oppo') || normQ.includes('reno') || normQ.includes('find x') || normQ.includes('find n')) {
                targetBrand = 'OPPO';
            } else if (normQ.includes('huawei') || normQ.includes('mate') || normQ.includes('pura') || normQ.includes('matepad')) {
                targetBrand = 'Huawei';
            } else if (normQ.includes('realme') || normQ.includes('celmi')) {
                targetBrand = 'Realme';
            }

            // 2. Nhận diện hậu tố phiên bản (Pro Max, Pro, Plus, Ultra, SE, FE, Fold, Flip, Mini, Air...)
            var hasProMax = normQ.includes('pro max') || normQ.includes('promax');
            var hasPro = !hasProMax && normQ.includes('pro');
            var hasPlus = normQ.includes('plus') || normQ.includes('+');
            var hasUltra = normQ.includes('ultra');
            var hasFE = normQ.includes('fe');
            var hasSE = normQ.includes('special edition') || normQ.includes('fold se') || normQ.includes('z fold se');
            var hasAir = normQ.includes('air');
            var hasMini = normQ.includes('mini');

            var scored = [];

            catalog.forEach(function(prod) {
                var t = prod.name.toLowerCase();
                var cat = (prod.category || '').toLowerCase();
                var specs = (prod.specs || '').toLowerCase();
                var brand = prod.brand || '';

                var normT = t
                    .replace(/fold\\s*([0-9]+)/g, 'fold$1')
                    .replace(/flip\\s*([0-9]+)/g, 'flip$1')
                    .replace(/s\\s*([0-9]+)\\s*\\+/g, 's$1+')
                    .replace(/s\\s*([0-9]+)\\s*plus/g, 's$1+')
                    .replace(/s\\s*([0-9]+)/g, 's$1')
                    .replace(/gt\\s*([0-9]+)/g, 'gt$1')
                    .replace(/xm\\s*([0-9]+)/g, 'xm$1');

                var score = 0;

                // A. CÔ LẬP THƯƠNG HIỆU: Khách hỏi hãng A thì tuyệt đối không tư vấn hãng B
                if (targetBrand && brand !== targetBrand) {
                    return;
                }
                if (targetBrand && brand === targetBrand) {
                    score += 1500;
                }

                // B. Khớp chuỗi trực tiếp
                if (normT.includes(normQ)) {
                    score += 3000 + normQ.length * 30;
                }

                // C. Phân biệt theo số thế hệ (18, 17, 16, 15, 14, 13, 12, 11, 25, 24, 23, 9, 8, 7, 6, 5...)
                var genNumbers = ['18', '17', '16', '15', '14', '13', '12', '11', '25', '24', '23', '9', '8', '7', '6', '5', '4', '3', '2', '1'];
                genNumbers.forEach(function(num) {
                    var re = new RegExp('\\\\b' + num + '\\\\b');
                    var inQ = re.test(normQ) || normQ.includes('s' + num) || normQ.includes('fold' + num) || normQ.includes('flip' + num) || normQ.includes('gt' + num) || normQ.includes('m' + num);
                    var inT = re.test(normT) || normT.includes('s' + num) || normT.includes('fold' + num) || normT.includes('flip' + num) || normT.includes('gt' + num) || normT.includes('m' + num);
                    if (inQ && inT) {
                        score += 2000;
                    } else if (inQ && !inT) {
                        score -= 4000; // Phạt nặng nếu sai số thế hệ
                    }
                });

                // D. Phân cấp Hậu tố (Pro Max, Pro, Plus, Ultra, FE, SE, Air...)
                var tHasProMax = normT.includes('pro max') || normT.includes('promax');
                var tHasPro = !tHasProMax && normT.includes('pro');
                var tHasPlus = normT.includes('plus') || normT.includes('+');
                var tHasUltra = normT.includes('ultra');
                var tHasFE = normT.includes('fe');
                var tHasSE = normT.includes('special edition') || normT.includes('se');
                var tHasAir = normT.includes('air');

                // PRO MAX
                if (hasProMax) {
                    if (tHasProMax) score += 3500;
                    else score -= 4500;
                } else if (tHasProMax) {
                    score -= 1500;
                }

                // PRO
                if (hasPro) {
                    if (tHasPro) score += 3000;
                    else score -= 3000;
                } else if (tHasPro && !hasProMax) {
                    score -= 1200;
                }

                // ULTRA
                if (hasUltra) {
                    if (tHasUltra) score += 3500;
                    else score -= 4000;
                } else if (tHasUltra) {
                    score -= 1500;
                }

                // PLUS
                if (hasPlus) {
                    if (tHasPlus) score += 3500;
                    else score -= 4000;
                } else if (tHasPlus) {
                    score -= 1500;
                }

                // FE
                if (hasFE) {
                    if (tHasFE) score += 3500;
                    else score -= 4000;
                } else if (tHasFE) {
                    score -= 1500;
                }

                // SE
                if (hasSE) {
                    if (tHasSE) score += 4000;
                    else score -= 4000;
                }

                // AIR
                if (hasAir) {
                    if (tHasAir) score += 3500;
                    else score -= 4000;
                } else if (tHasAir) {
                    score -= 1500;
                }

                // E. Danh mục thiết bị (tai nghe, laptop, tablet, dong ho)
                var isHeadphone = normQ.includes('tai nghe') || normQ.includes('headphone') || normQ.includes('earphone') || normQ.includes('buds') || normQ.includes('airpods') || normQ.includes('xm5');
                if (isHeadphone) {
                    if (t.includes('tai nghe') || t.includes('buds') || t.includes('airpods') || t.includes('xm5') || cat.includes('tai nghe')) score += 2500;
                    else score -= 3000;
                }

                var isLaptop = normQ.includes('laptop') || normQ.includes('macbook') || normQ.includes('xps') || normQ.includes('zenbook') || normQ.includes('tuf');
                if (isLaptop) {
                    if (t.includes('macbook') || t.includes('xps') || t.includes('zenbook') || t.includes('laptop') || cat.includes('laptop')) score += 2500;
                    else score -= 3000;
                }

                var isTablet = normQ.includes('ipad') || normQ.includes('may tinh bang') || normQ.includes('tab') || normQ.includes('matepad');
                if (isTablet) {
                    if (t.includes('ipad') || t.includes('tab') || t.includes('matepad') || cat.includes('may tinh bang') || cat.includes('tablet')) score += 2500;
                    else score -= 3000;
                }

                var isWatch = normQ.includes('dong ho') || normQ.includes('watch');
                if (isWatch) {
                    if (t.includes('watch') || cat.includes('dong ho')) score += 2500;
                    else score -= 3000;
                }

                // F. Khớp token từ vựng
                var tokens = normQ.split(/\\s+/);
                tokens.forEach(function(tok) {
                    if (tok.length >= 2) {
                        if (normT.includes(tok)) score += 300 * tok.length;
                        else if (cat.includes(tok)) score += 100 * tok.length;
                        else if (specs.includes(tok)) score += 50 * tok.length;
                    }
                });

                if (score > 100) {
                    scored.push({ prod: prod, score: score });
                }
            });

            if (scored.length === 0) return null;
            scored.sort(function(a, b) { return b.score - a.score; });
            return scored[0].prod;
        }

        function generateBotReply(q) {
            var lower = q.toLowerCase();
            var catalog = getCatalogProductsData();

            setTimeout(function() {
                // 1. Tìm đúng sản phẩm mà khách hàng yêu cầu
                var exactProduct = findExactProductMatch(q, catalog);

                if (exactProduct) {
                    var replyText = 'Dạ em xin gửi quý khách thông tin giới thiệu và báo giá chi tiết của đúng sản phẩm <strong>' + exactProduct.name + '</strong> mà quý khách đang quan tâm ạ:';
                    replyText += createPriceCardHTML(exactProduct);
                    appendBotMessage(replyText);
                    return;
                }

                // 1b. Gợi ý dòng máy nếu khách hỏi nhiều dòng hoặc chung chung (VD: iPhone 16 & 17, các dòng S24)
                if (lower.includes('iphone 16') && lower.includes('17')) {
                    var iphones = catalog.filter(function(p) { return p.brand === 'Apple' && (p.name.includes('iPhone 17') || p.name.includes('iPhone 16')); }).slice(0, 3);
                    if (iphones.length > 0) {
                        var ipHtml = 'Dạ CloudMart xin giới thiệu bảng giá ưu đãi các dòng <strong>iPhone 16 & 17 Series</strong> chính hãng VN/A:';
                        iphones.forEach(function(item) { ipHtml += createPriceCardHTML(item); });
                        appendBotMessage(ipHtml);
                        return;
                    }
                }

                // 2. Các câu hỏi chính sách thông thường nếu khách không hỏi đích danh máy
                if (lower.includes('bảo hành') || lower.includes('1 đổi 1') || lower.includes('đổi trả')) {
                    appendBotMessage('🛡️ <strong>Chính sách Bảo Hành & 1 Đổi 1:</strong><br>• Cam kết 100% hàng phân phối chính hãng (VN/A, Samsung Vina, Sony, Dell, ASUS).<br>• Đổi mới 1-1 trong 30 ngày nếu phát sinh lỗi phần cứng.<br>• Bảo hành 12 - 24 tháng tại trung tâm ủy quyền toàn quốc, hỗ trợ miễn phí lấy máy tận nhà!<br><button type="button" onclick="openCskhModal()" style="background: #ecfdf5; border: 1px solid #059669; color: #059669; font-weight: 700; padding: 4px 8px; border-radius: 6px; cursor: pointer; margin-top: 4px;">Xem chi tiết chính sách</button>');
                } else if (lower.includes('trả góp') || lower.includes('thẻ tín dụng') || lower.includes('lãi suất')) {
                    appendBotMessage('💳 <strong>Chính sách Trả Góp 0%:</strong><br>• Áp dụng cho thẻ tín dụng liên kết hơn 25 ngân hàng (VCB, MB, Techcombank, VPBank...).<br>• Kỳ hạn linh hoạt 3, 6, 9, 12 tháng.<br>• Không cần chứng minh thu nhập, kích hoạt ngay tại trang Thanh toán!');
                } else if (lower.includes('giao hàng') || lower.includes('ship') || lower.includes('vận chuyển') || lower.includes('đồng kiểm')) {
                    appendBotMessage('🚚 <strong>Chính sách Giao Hàng & Đồng Kiểm:</strong><br>• Giao siêu tốc trong 2H tại nội thành TP.HCM & Hà Nội.<br>• Khách hàng được <strong>mở hộp đồng kiểm</strong> tem seal máy và phụ kiện trước khi thanh toán.<br>• Miễn phí giao hàng toàn quốc!');
                } else if (lower.includes('vietqr') || lower.includes('giảm 500k') || lower.includes('voucher') || lower.includes('khuyến mãi')) {
                    appendBotMessage('⚡ <strong>Ưu đãi VietQR 24/7:</strong><br>• Giảm ngay 500.000₫ khi quét mã VietQR Napas 247 qua App ngân hàng.<br>• Nhập mã voucher <code>CLOUDMART10</code> tại trang thanh toán để được giảm thêm 1.500.000₫!');
                } else {
                    appendBotMessage('Dạ quý khách cần tư vấn hoặc báo giá dòng máy cụ thể nào ạ? Quý khách vui lòng nhập tên chính xác sản phẩm (ví dụ: <em>iPhone 16 Pro Max, Samsung S24 Ultra, Z Fold5, MacBook Pro 16...</em>) hoặc chọn nhanh ở thanh <strong>"🏷️ Tra giá nhanh"</strong> ngay phía trên để em báo giá đúng sản phẩm đó cho quý khách nhé!');
                }
            }, 300);
        }'''

# Replace from `function findExactProductMatch` up to `function setupQuickViewAskPrice()`
start_idx = content.find('function findExactProductMatch(')
end_idx = content.find('function setupQuickViewAskPrice()')
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_matcher_code + '\n\n        ' + content[end_idx:]
    print('Replaced matcher and generateBotReply successfully!')
else:
    print('ERROR: start_idx or end_idx not found!')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

nested_path = '/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/products/index.html'
shutil.copy2(file_path, nested_path)
print('Synchronized products/index.html and products/products/index.html')
