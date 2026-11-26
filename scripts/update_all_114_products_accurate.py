import os
import re
import shutil
import html.parser

base = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web"
prod_path = os.path.join(base, "demo_pages/products/index.html")
fe_path = os.path.join(base, "demo_pages/frontend/index.html")

with open(prod_path, "r", encoding="utf-8") as f:
    prod_html = f.read()

with open(fe_path, "r", encoding="utf-8") as f:
    fe_html = f.read()

# Exact replacements to fix all mismatches in products/index.html
replacements = [
    # 1. Apple iPhone 17 Pro colors
    (
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_17_pro_max_orange.jpg">Titan Đen Vũ Trụ</button>',
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_17_pro_max_orange.jpg">Titan Cam Sa Mạc (Cosmic Orange)</button>'
    ),
    # 2. Apple iPhone 17 colors
    (
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_17_mist_blue.jpg">Trắng Băng Giá (Cloud White)</button>\n                                    <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_17_air_white.jpg">Xanh Lam Tinh Khiết</button>',
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_17_mist_blue.jpg">Xanh Lam Sương Mù (Mist Blue)</button>\n                                    <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_17_air_white.jpg">Trắng Mây Tinh Khiết (Cloud White)</button>'
    ),
    # 3. iPad mini 7 image
    (
        '<img src="/assets/ipad_air_blue.jpg" alt="iPad mini 7 Siêu Di Động (A17 Pro)" class="product-img">',
        '<img src="/assets/poster_apple_ipad_mini_7_a17_pro.jpg" alt="iPad mini 7 Siêu Di Động (A17 Pro)" class="product-img">'
    ),
    (
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/ipad_air_blue.jpg">Xanh Hiện Đại</button>',
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/poster_apple_ipad_mini_7_a17_pro.jpg">Tím Khói / Xanh Starlight</button>'
    ),
    # 4. Samsung Z Fold5 color label
    (
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/samsung_fold_blue.jpg">Đen Phantom (Icy Black)</button>',
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/samsung_fold_blue.jpg">Xanh Icy Blue</button>'
    ),
    # 5. Dell G15 5530 image
    (
        '<img src="/assets/alienware_gaming.jpg" alt="Dell Gaming G15 5530 (Core i7 / RTX 4060)" class="product-img">',
        '<img src="/assets/poster_dell_dell_gaming_g15_5530_core_i7_rtx_4060.jpg" alt="Dell Gaming G15 5530 (Core i7 / RTX 4060)" class="product-img">'
    ),
    (
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/alienware_gaming.jpg">Xám Kim Loại (Dark Shadow)</button>',
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/poster_dell_dell_gaming_g15_5530_core_i7_rtx_4060.jpg">Xám Kim Loại (Dark Shadow)</button>'
    ),
    # 6. OPPO Find X8 Pro
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s25_black.png">Đen Không Gian</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/oppo_find_x8_pro_black.jpg">Đen Không Gian (Space Black)</button>'
    ),
    # 7. OPPO Find X8
    (
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/oppo_find_white_back.jpg">Xám Tinh Vân</button>\n                                    <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_16_pink_real.jpg">Hồng Sa Mạc</button>',
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/oppo_find_white_back.jpg">Trắng Tinh Khôi</button>\n                                    <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/oppo_find_x8_black.jpg">Đen Không Gian</button>'
    ),
    # 8. OPPO Find N3
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_zfold_se.jpg">Đen Cổ Điển Da</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/oppo_find_n3_fold_black.jpg">Đen Cổ Điển Da (Classic Black)</button>'
    ),
    # 9. OPPO Find N3 Flip
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s24_black.jpg">Đen Hổ Phách</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/oppo_find_n3_flip_black.jpg">Đen Hổ Phách (Sleek Black)</button>'
    ),
    # 10. OPPO Reno 12 Pro
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s24_black.jpg">Nâu Không Gian</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/oppo_reno12_pro_brown.jpg">Nâu Không Gian (Space Brown)</button>'
    ),
    # 11. OPPO Reno 12
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_16_ultramarine_real.jpg">Nâu Nhám Bạc</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/oppo_reno12_silver.jpg">Bạc Nhám Titan</button>'
    ),
    # 12. OPPO A3 Pro
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s24_black.jpg">Đen Tinh Thể</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/oppo_a3_pro_black.jpg">Đen Tinh Thể (Starry Black)</button>'
    ),
    # 13. Huawei Mate XT
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_zfold_se.jpg">Đen Huyền Bí Da</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/huawei_mate_xt_black.jpg">Đen Huyền Bí Da (Obsidian Black)</button>'
    ),
    # 14. Huawei Pura 70 Ultra
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s25_black.png">Đen Cổ Điển Da</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/huawei_pura_70_ultra_black.jpg">Đen Cổ Điển Da (Classic Black)</button>'
    ),
    # 15. Huawei Pura 70 Pro
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s24_black.jpg">Đen Lông Vũ</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/huawei_pura_70_pro_black.jpg">Đen Lông Vũ (Feather Black)</button>'
    ),
    # 16. Huawei Mate 60 Pro
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_16_pro_white_titanium.jpg">Bạc Bạch Sa</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/huawei_mate60_silver.jpg">Bạc Bạch Sa (White Sand Silver)</button>'
    ),
    # 17. Huawei Mate X5
    (
        '<img src="/assets/huawei_mate_xt.jpg" alt="Huawei Mate X5 Màn Gập Siêu Mỏng" class="product-img">',
        '<img src="/assets/poster_huawei_huawei_mate_x5_m_n_g_p_si_u_m_ng.jpg" alt="Huawei Mate X5 Màn Gập Siêu Mỏng" class="product-img">'
    ),
    (
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/huawei_mate_xt.jpg">Tím Ảo Ảnh</button>\n                                    <button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s24_black.jpg">Đen Lông Vũ</button>',
        '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/poster_huawei_huawei_mate_x5_m_n_g_p_si_u_m_ng.jpg">Tím Ảo Ảnh (Phantom Purple)</button>'
    ),
    # 18. Huawei FreeBuds Pro 3
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_buds3_pro.jpg">Bạc Ánh Sương</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/huawei_freebuds_pro_silver.jpg">Bạc Ánh Sương (Silver Frost)</button>'
    ),
    # 19. Realme GT 6
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/rog_phone_9_pro.jpg">Xanh Lục Bảo (Razor Green)</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/realme_gt6_green.jpg">Xanh Lục Bảo (Razor Green)</button>'
    ),
    # 20. Realme GT Neo 6
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_16_pro_white_titanium.jpg">Bạc Kim Loại</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/realme_gt_neo6_silver.jpg">Bạc Kim Loại (Silver Mirror)</button>'
    ),
    # 21. Realme 13 Pro+
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_16_pro_desert_rear.png">Vàng Hoàng Kim Monet</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/realme_13_pro_plus_gold.jpg">Vàng Hoàng Kim Monet (Monet Gold)</button>'
    ),
    # 22. Realme 13+
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_16_pro_desert_rear.png">Vàng Kim Vinh Quang</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/realme_13_plus_gold.jpg">Vàng Kim Vinh Quang (Victory Gold)</button>'
    ),
    # 23. Realme 12
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s24_series.jpg">Tím Hoàng Hôn</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/realme_12_purple.jpg">Tím Hoàng Hôn (Twilight Purple)</button>'
    ),
    # 24. Realme C67
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s24_black.jpg">Đen Đá Núi Lửa</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/realme_c67_black.jpg">Đen Đá Núi Lửa (Black Rock)</button>'
    ),
    # 25. Realme C65
    (
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s24_black.jpg">Đen Huyền Ảo</button>',
        '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/realme_c65_black.jpg">Đen Huyền Ảo (Starlight Black)</button>'
    ),
]

applied_count = 0
for old, new in replacements:
    if old in prod_html:
        prod_html = prod_html.replace(old, new)
        applied_count += 1
    else:
        print(f"Warning: pattern not matched in products: {old[:60]}...")

print(f"Applied {applied_count}/{len(replacements)} replacements in demo_pages/products/index.html")

# Write updated products/index.html
with open(prod_path, "w", encoding="utf-8") as f:
    f.write(prod_html)

# Also update frontend/index.html with the same exact fixes where applicable
fe_applied = 0
for old, new in replacements:
    if old in fe_html:
        fe_html = fe_html.replace(old, new)
        fe_applied += 1

print(f"Applied {fe_applied} replacements in demo_pages/frontend/index.html")

with open(fe_path, "w", encoding="utf-8") as f:
    f.write(fe_html)

# Sync to nested directory
shutil.copyfile(prod_path, os.path.join(base, "demo_pages/products/products/index.html"))

# Sync to user_data_*.sh scripts
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

print("Synchronized all files and scripts successfully!")
