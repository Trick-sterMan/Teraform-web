import os
import shutil
import html.parser
import subprocess

base = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web"
prod_path = os.path.join(base, "demo_pages/products/index.html")
fe_path = os.path.join(base, "demo_pages/frontend/index.html")

with open(prod_path, "r", encoding="utf-8") as f:
    prod_html = f.read()

with open(fe_path, "r", encoding="utf-8") as f:
    fe_html = f.read()

# Improved variant JS for products/index.html
products_variant_js = """        function formatVND(num) {
            return Number(num).toLocaleString('vi-VN') + ' ₫';
        }

        // Hàm chọn Dung lượng (Storage) -> cập nhật giá lập tức với hiệu ứng động
        function selectStorage(btn) {
            var card = btn.closest('.product-card');
            if (!card) return;
            var group = btn.closest('.variant-group');
            if (group) {
                group.querySelectorAll('.variant-pill').forEach(function(p) { p.classList.remove('active'); });
                var labelEl = group.querySelector('.variant-label');
                if (labelEl) {
                    labelEl.innerHTML = 'Dung lượng: <strong style="color: #059669; font-weight: 800;">' + btn.innerText.trim() + '</strong>';
                }
            }
            btn.classList.add('active');

            var newPrice = btn.getAttribute('data-price');
            var newOldPrice = btn.getAttribute('data-oldprice');
            var priceEl = card.querySelector('.current-price');
            var oldPriceEl = card.querySelector('.old-price');

            if (newPrice && priceEl) {
                priceEl.innerText = formatVND(newPrice);
                priceEl.style.transition = 'transform 0.15s ease, color 0.15s ease';
                priceEl.style.transform = 'scale(1.12)';
                priceEl.style.color = '#10b981';
                setTimeout(function() {
                    priceEl.style.transform = 'scale(1)';
                    priceEl.style.color = '';
                }, 200);
            }
            if (newOldPrice && oldPriceEl) {
                oldPriceEl.innerText = formatVND(newOldPrice);
            }

            var optImg = btn.getAttribute('data-img');
            var imgEl = card.querySelector('.product-img');
            if (optImg && imgEl) {
                imgEl.src = optImg;
            }
            showToast('Đã chọn dung lượng: ' + btn.innerText.trim() + (newPrice ? ' • ' + formatVND(newPrice) : ''));
        }

        // Hàm chọn Màu sắc (Color) -> chuyển đúng ảnh màu và cập nhật hiển thị giá
        function selectColor(btn) {
            var card = btn.closest('.product-card');
            if (!card) return;
            var group = btn.closest('.variant-group');
            if (group) {
                group.querySelectorAll('.variant-pill').forEach(function(p) { p.classList.remove('active'); });
                var labelEl = group.querySelector('.variant-label');
                if (labelEl) {
                    labelEl.innerHTML = 'Màu sắc: <strong style="color: #059669; font-weight: 800;">' + btn.innerText.trim() + '</strong>';
                }
            }
            btn.classList.add('active');

            // Cập nhật ảnh sản phẩm với hiệu ứng chuyển tiếp mượt mà
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

            // Cập nhật giá theo tùy chọn màu (nếu có giá riêng) hoặc kiểm tra dung lượng đang active
            var colorPrice = btn.getAttribute('data-price');
            var colorOldPrice = btn.getAttribute('data-oldprice');
            var priceEl = card.querySelector('.current-price');
            var oldPriceEl = card.querySelector('.old-price');

            if (colorPrice && priceEl) {
                priceEl.innerText = formatVND(colorPrice);
                if (colorOldPrice && oldPriceEl) oldPriceEl.innerText = formatVND(colorOldPrice);
            } else {
                // Đảm bảo giá đồng bộ với dung lượng đang chọn
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

            var currentPriceText = priceEl ? priceEl.innerText.trim() : '';
            showToast('Đã chọn màu: ' + btn.innerText.trim() + (currentPriceText ? ' • ' + currentPriceText : ''));
        }

        function initVariantSelectors() {
            document.querySelectorAll('.product-card').forEach(function(card) {
                // Khởi tạo hiển thị nhãn ban đầu cho Dung lượng và Màu sắc
                var sGroup = card.querySelector('.variant-group[data-type="storage"]');
                if (sGroup) {
                    var activeS = sGroup.querySelector('.variant-pill.active');
                    var sLabel = sGroup.querySelector('.variant-label');
                    if (activeS && sLabel && !sLabel.querySelector('strong')) {
                        sLabel.innerHTML = 'Dung lượng: <strong style="color: #059669; font-weight: 800;">' + activeS.innerText.trim() + '</strong>';
                    }
                }
                var cGroup = card.querySelector('.variant-group[data-type="color"]');
                if (cGroup) {
                    var activeC = cGroup.querySelector('.variant-pill.active');
                    var cLabel = cGroup.querySelector('.variant-label');
                    if (activeC && cLabel && !cLabel.querySelector('strong')) {
                        cLabel.innerHTML = 'Màu sắc: <strong style="color: #059669; font-weight: 800;">' + activeC.innerText.trim() + '</strong>';
                    }
                }

                card.querySelectorAll('.variant-group[data-type="storage"] .variant-pill').forEach(function(pill) {
                    pill.onclick = function(e) {
                        e.preventDefault();
                        selectStorage(this);
                    };
                });
                card.querySelectorAll('.variant-group[data-type="color"] .variant-pill').forEach(function(pill) {
                    pill.onclick = function(e) {
                        e.preventDefault();
                        selectColor(this);
                    };
                });
            });
        }
        document.addEventListener('DOMContentLoaded', initVariantSelectors);
        initVariantSelectors();"""

# Replace in products/index.html
start_marker = "function formatVND(num) {"
end_marker = "initVariantSelectors();"
idx1 = prod_html.find(start_marker)
if idx1 != -1:
    idx2 = prod_html.find(end_marker, idx1)
    if idx2 != -1:
        prod_html = prod_html[:idx1] + products_variant_js + prod_html[idx2 + len(end_marker):]
        print("Replaced products variant JS successfully!")

# Improved variant JS for frontend/index.html
frontend_variant_js = """        function formatVND(num) {
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
        initVariantSelectors();"""

f_start = "function formatVND(num) {"
f_end = "initVariantSelectors();"
f_idx1 = fe_html.find(f_start)
if f_idx1 != -1:
    f_idx2 = fe_html.find(f_end, f_idx1)
    if f_idx2 != -1:
        fe_html = fe_html[:f_idx1] + frontend_variant_js + fe_html[f_idx2 + len(f_end):]
        print("Replaced frontend variant JS successfully!")

# Ensure crystal clear CSS for variant-pill active in products
prod_pill_css = """
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
            border-color: #059669 !important;
            color: #059669 !important;
            background: #ecfdf5 !important;
            transform: translateY(-1px) !important;
        }
        .variant-pill.active {
            background: linear-gradient(135deg, #059669, #047857) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            border-color: #047857 !important;
            box-shadow: 0 4px 12px rgba(5, 150, 105, 0.35) !important;
            transform: scale(1.03) !important;
        }
"""
if "/* Prominent active variant pills */" not in prod_html:
    prod_html = prod_html.replace("</style>", prod_pill_css + "\n    </style>", 1)

# Ensure crystal clear CSS for variant-pill active in frontend
fe_pill_css = """
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
"""
if "/* Prominent active variant pills */" not in fe_html:
    fe_html = fe_html.replace("</style>", fe_pill_css + "\n    </style>", 1)

# Save demo files
with open(prod_path, "w", encoding="utf-8") as f:
    f.write(prod_html)

with open(fe_path, "w", encoding="utf-8") as f:
    f.write(fe_html)

# Sync nested directories
shutil.copyfile(prod_path, os.path.join(base, "demo_pages/products/products/index.html"))

# Sync AWS deployment scripts
chk_path = os.path.join(base, "demo_pages/checkout/index.html")
with open(chk_path, "r", encoding="utf-8") as f:
    chk_html = f.read()

fe_script = f"""#!/bin/bash
set -e
dnf update -y || yum update -y
dnf install -y nginx || yum install -y nginx
mkdir -p /var/www/html
mkdir -p /usr/share/nginx/html
cat << 'EOF' > /var/www/html/index.html
{fe_html}
EOF
systemctl enable nginx
systemctl restart nginx
"""
with open(os.path.join(base, "scripts/user_data_frontend.sh"), "w", encoding="utf-8") as f:
    f.write(fe_script)

prod_script = f"""#!/bin/bash
set -e
dnf update -y || yum update -y
dnf install -y nginx || yum install -y nginx
mkdir -p /var/www/html/products
mkdir -p /usr/share/nginx/html/products
cat << 'EOF' > /var/www/html/products/index.html
{prod_html}
EOF
systemctl enable nginx
systemctl restart nginx
"""
with open(os.path.join(base, "scripts/user_data_products.sh"), "w", encoding="utf-8") as f:
    f.write(prod_script)

print("All files updated and synchronized successfully!")
