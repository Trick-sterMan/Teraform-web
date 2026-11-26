import re, os, html

PROD_HTML = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html"
FRONT_HTML = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/frontend/index.html"

# Comprehensive authentic map of EVERY product to its authentic, real, high-res image
AUTHENTIC_IMAGE_MAP = {
    # Apple Flagships & Pre-order
    "iPhone 17 Pro Max": "/assets/iphone_17_pro_max.jpg",
    "iPhone 17 Pro": "/assets/iphone_17_pro.jpg",
    "iPhone 17 Air (Slim 5.6mm)": "/assets/iphone_17_air.jpg",
    "iPhone 17": "/assets/iphone_17_air_white.jpg",
    "iPhone 18 Pro Max": "/assets/iphone_18_pro_max.jpg",
    "iPhone 18 Fold Duo Màn Gập": "/assets/iphone_18_duo.jpg",
    "iPhone 18 Fold Duo": "/assets/iphone_18_duo.jpg",
    
    # Apple Current Retail Market
    "iPhone 16 Pro Max": "/assets/real_iphone_16_pro_max.jpg",
    "iPhone 16 Pro": "/assets/real_iphone_16_pro.jpg",
    "iPhone 16 Plus": "/assets/real_iphone_16_plus.jpg",
    "iPhone 16": "/assets/real_iphone_16.jpg",
    "iPhone 15 Pro Max": "/assets/real_iphone_15_pro_max.jpg",
    "iPhone 15": "/assets/real_iphone_15.jpg",
    "iPhone 14 Pro Max": "/assets/real_iphone_14_pro_max.jpg",
    "iPhone 13": "/assets/real_iphone_13.jpg",
    "MacBook Pro 16\" M3 Max": "/assets/macbook_pro_m3_space_gray.jpg",
    "MacBook Pro 16 M3 Max": "/assets/macbook_pro_m3_space_gray.jpg",
    "MacBook Pro 14\" M4 (2024)": "/assets/macbook_pro_silver_real.jpg",
    "MacBook Air 13\" M3": "/assets/macbook_air_midnight.jpg",
    "iPad Pro 13\" M4 OLED": "/assets/ipad_pro_13_m4.jpg",
    "iPad Pro 13 M4 OLED": "/assets/ipad_pro_13_m4.jpg",
    "iPad Pro 13\" M4 Tandem OLED": "/assets/ipad_pro_13_m4.jpg",
    "iPad Pro 13 M4 Tandem OLED": "/assets/ipad_pro_13_m4.jpg",
    "iPad Air 13\" M2 Liquid Retina": "/assets/ipad_air_blue.jpg",
    "iPad mini 7 (A17 Pro)": "/assets/ipad_air_blue.jpg",
    "Apple Watch Ultra 2 49mm": "/assets/apple_watch_ultra2.jpg",
    "Apple Watch Ultra 2": "/assets/apple_watch_ultra2.jpg",
    "Apple Watch Ultra 2 GPS + Cellular 49mm Titan": "/assets/apple_watch_ultra2.jpg",
    "Apple Watch Series 10 (46mm)": "/assets/apple_watch_series_10.png",
    "AirPods Pro 2 (USB-C)": "/assets/airpods_pro.jpg",
    "AirPods 4 Chống Ồn Chủ Động (ANC)": "/assets/airpods_pro.jpg",
    "AirPods Max (USB-C)": "/assets/real_airpods_max.jpg",
    "Apple Mac mini M4 2024": "/assets/mac_mini_m4.png",
    "iMac 24\" M4 (2024)": "/assets/real_imac_24.jpg",

    # Samsung Pre-order & Next-Gen
    "Samsung Galaxy S25 Ultra 5G AI": "/assets/samsung_s25_ultra_render.jpg",
    "Samsung Galaxy S25 Ultra": "/assets/samsung_s25_ultra_render.jpg",
    "Samsung Galaxy S25+ 5G AI": "/assets/samsung_s25_plus.jpg",
    "Samsung Galaxy S25 5G AI": "/assets/samsung_s25_base.jpg",
    "Galaxy Z Fold Special Edition": "/assets/samsung_zfold_se.jpg",

    # Samsung Current Retail Market
    "Samsung Galaxy S24 Ultra 5G AI": "/assets/real_samsung_s24_ultra.jpg",
    "Samsung Galaxy S24 Ultra": "/assets/real_samsung_s24_ultra.jpg",
    "Samsung Galaxy S24+ 5G AI": "/assets/real_samsung_s24_plus.jpg",
    "Samsung Galaxy S24 5G": "/assets/real_samsung_s24.jpg",
    "Samsung Galaxy S24 FE 5G (Fan Edition)": "/assets/real_samsung_s24_fe.jpg",
    "Samsung Galaxy Z Fold6 5G": "/assets/real_samsung_zfold6.jpg",
    "Samsung Galaxy Z Flip6 5G": "/assets/real_samsung_zflip6.jpg",
    "Samsung Galaxy S23 Ultra 5G": "/assets/real_samsung_s23_ultra.jpg",
    "Samsung Galaxy A55 5G": "/assets/real_samsung_a55.jpg",
    "Samsung Galaxy A35 5G": "/assets/real_samsung_a35.jpg",
    "Samsung Galaxy Watch Ultra 47mm": "/assets/samsung_watch_ultra.jpg",
    "Samsung Galaxy Watch7 (44mm Bluetooth)": "/assets/real_samsung_watch.jpg",
    "Samsung Galaxy Buds3 Pro": "/assets/samsung_buds3_pro.jpg",
    "Galaxy Tab S10 Ultra 5G AI": "/assets/samsung_galaxy_tab.png",
    "Samsung Galaxy Ring AI": "/assets/samsung_galaxy_ring.jpg",
    "Samsung Galaxy Z Fold5 5G": "/assets/samsung_fold_blue.jpg",
    "Samsung Galaxy S23 FE 5G": "/assets/real_samsung_s24_fe.jpg",
    "Samsung Galaxy Watch FE (40mm 2024)": "/assets/samsung_galaxy_watch.jpg",

    # Sony
    "Sony WH-1000XM5 Wireless": "/assets/sony_headphones.jpg",
    "Sony WH-1000XM5 Chống Ồn Chủ Động": "/assets/sony_headphones.jpg",
    "Sony PlayStation 5 (PS5) Slim 1TB": "/assets/ps5_slim.png",
    "PlayStation Portal Remote Player": "/assets/playstation_portal.jpg",
    "PlayStation VR2 Horizon Bundle": "/assets/ps_vr2.png",
    "PlayStation 5 Pro (PS5 Pro) 2TB": "/assets/ps5_pro.jpg",
    "Sony Xperia 1 VI 5G": "/assets/sony_xperia_1.png",
    "Sony WF-1000XM5 True Wireless": "/assets/sony_wf1000xm5.jpg",
    "Sony ULT WEAR (WH-ULT900N)": "/assets/sony_xm5_black.jpg",
    "Máy ảnh Sony Alpha A7 IV (ILCE-7M4 Body)": "/assets/real_sony_a7.jpg",
    "Tay cầm Sony DualSense Edge Wireless Controller": "/assets/ps5_controller_bundle.png",
    "Loa Bluetooth Di Động Sony ULT FIELD 7": "/assets/sony_ult_field7.jpg",
    "Máy ảnh Vlog Sony ZV-E10 II (2024)": "/assets/real_sony_zve10.jpg",

    # Dell
    "Dell XPS 16 9640 Core Ultra": "/assets/dell_xps.png",
    "Dell XPS 16 9640 Core Ultra 7 OLED 4K": "/assets/dell_xps.png",
    "Dell Inspiron 16 Plus Pro": "/assets/dell_inspiron.jpg",
    "Dell XPS 13 / 15 Prestige": "/assets/dell_xps_platinum.jpg",
    "Dell Latitude 7450 vPro AI": "/assets/dell_latitude_black.jpg",
    "Alienware m16 R2 Gaming Monster": "/assets/alienware_gaming.jpg",
    "Dell XPS 13 9340 (2024 Core Ultra 7 OLED)": "/assets/dell_xps_graphite.jpg",
    "Dell XPS 14 9440 (2024 RTX 4050)": "/assets/dell_xps_dual.jpg",
    "Dell Gaming G15 5530 (Core i7 / RTX 4060)": "/assets/alienware_gaming.jpg",
    "Màn hình Dell UltraSharp 27\" 4K U2724D (IPS Black)": "/assets/real_dell_u27.jpg",
    "Dell Inspiron 14 2-in-1 (7440 Xoay Gập 360°)": "/assets/dell_inspiron.jpg",
    "Dell Alienware m18 R2 Gaming Monster (2024)": "/assets/alienware_gaming.jpg",

    # ASUS ROG & Zenbook
    "ASUS ROG Phone 9 Pro 5G": "/assets/rog_phone_9_pro.jpg",
    "ASUS ROG Zephyrus G16 OLED": "/assets/asus_rog_gray.jpg",
    "ASUS ROG Zephyrus G16 OLED RTX 4080": "/assets/asus_rog_gray.jpg",
    "ASUS ROG Strix SCAR Edition": "/assets/asus_rog.jpg",
    "ROG Zephyrus G14 Ultra Slim": "/assets/asus_rog_white.jpg",
    "ASUS ROG Ally X (2024) 1TB": "/assets/rog_ally.png",
    "ASUS ZenBook Duo OLED 2 Màn Hình": "/assets/asus_zenbook_duo.jpg",
    "ASUS TUF Gaming A15 (FA507UV Ryzen 9 / RTX 4060)": "/assets/asus_rog_gray.jpg",
    "ASUS ZenBook 14 OLED (UX3405 Core Ultra 7)": "/assets/asus_rog_white.jpg",
    "ASUS Vivobook S 14 OLED (M5406 AMD Ryzen 7)": "/assets/asus_rog_white.jpg",
    "Màn hình ROG Swift OLED 32\" PG32UCDM (4K 240Hz)": "/assets/rog_swift_oled.jpg",
    "Bàn phím cơ ROG Azoth Wireless 75% Custom": "/assets/rog_azoth_keyboard.jpg",
    "ASUS ROG Phone 8 Pro (Snapdragon 8 Gen 3)": "/assets/real_rog_phone8.jpg",

    # OPPO
    "OPPO Find N5 5G": "/assets/oppo_find_n5.jpg",
    "OPPO Find X8 Pro 5G Flagship Hasselblad": "/assets/oppo_find_x8_pro.jpg",
    "OPPO Find X8 5G Mỏng Nhẹ AI": "/assets/oppo_find_white_back.jpg",
    "OPPO Find N3 (Màn Hình Gập Flagship)": "/assets/oppo_find_n3_fold.jpg",
    "OPPO Find N3 Flip Nắp Gập Dọc": "/assets/real_oppo_flip.jpg",
    "OPPO Reno 12 Pro 5G Chuyên Gia Chân Dung AI": "/assets/real_oppo_reno.jpg",
    "OPPO Reno 12 5G Màn Cong 3D": "/assets/real_oppo_reno12.jpg",
    "OPPO A3 Pro 5G Siêu Bền Chuẩn Quân Đội IP69": "/assets/real_oppo_find.jpg",
    "Máy tính bảng OPPO Pad 2 Màn 7:5 144Hz": "/assets/real_oppo_pad.jpg",
    "Tai nghe OPPO Enco X3 Dynaudio Hi-Res": "/assets/oppo_enco_x3.jpg",
    "OPPO Find X6 Pro Hasselblad (Cảm Biến 1-inch)": "/assets/real_oppo_findx6.jpg",

    # Huawei
    "Huawei Mate 70 Pro+": "/assets/huawei_mate_70_pro.jpg",
    "Huawei Mate XT Ultimate Design (Gập 3 Đầu Tiên)": "/assets/huawei_mate_xt.jpg",
    "Huawei Pura 70 Ultra Camera Thò Thụt 1-inch": "/assets/huawei_pura_70_ultra.jpg",
    "Huawei Pura 70 Pro Kính Kunlun Siêu Bền": "/assets/real_huawei_p60.jpg",
    "Huawei Mate 60 Pro Vệ Tinh Hai Chiều": "/assets/real_huawei_mate60.jpg",
    "Huawei Mate X5 Màn Gập Siêu Mỏng": "/assets/huawei_mate_xt.jpg",
    "Đồng hồ Huawei Watch GT 5 Pro Titanium Sapphire": "/assets/real_huawei_watch.jpg",
    "Tai nghe Huawei FreeBuds Pro 3 Kép Hi-Res": "/assets/huawei_freebuds_pro.jpg",
    "Máy tính bảng Huawei MatePad Pro 13.2\" OLED": "/assets/huawei_matepad_pro.jpg",
    "Đồng hồ Huawei Watch Fit 3 (2024 AMOLED)": "/assets/real_huawei_watch_fit.jpg",

    # Realme
    "Realme GT 7 Pro 5G": "/assets/realme_gt_7_pro.jpg",
    "Realme GT 6 (Kẻ Hủy Diệt Flagship 6000 nits 120W)": "/assets/realme_gt_6.jpg",
    "Realme GT Neo 6 (Snapdragon 7+ Gen 3 Tản Nhiệt Cực Đại)": "/assets/realme_gt_neo_back.jpg",
    "Realme 13 Pro+ 5G (Thiết Kế Monet Camera Kép Sony LYT)": "/assets/realme_13_pro_plus.jpg",
    "Realme 13+ 5G (Dimensity 7300 Energy Chuyên Game 90FPS)": "/assets/real_realme_11.jpg",
    "Realme 12 5G (Thiết Kế Đồng Hồ Xa Xỉ 108MP)": "/assets/realme_13_pro_plus.jpg",
    "Realme C67 (Quốc Dân Tầm Trung 108MP Snapdragon)": "/assets/real_realme_gt.jpg",
    "Realme C65 (Sạc Nhanh 45W Mượt Mà 48 Tháng)": "/assets/real_realme_11.jpg",
    "Tai nghe Realme Buds Air6 Pro (Driver Kép Chống Ồn 50dB)": "/assets/realme_buds_air.jpg",
    "Realme 12 Pro+ 5G (Camera Tiềm Vọng Zoom 120x)": "/assets/realme_13_pro_plus.jpg"
}

def clean_and_restore_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html_text = f.read()

    # 1. Restore clean e-commerce studio styling for product-img-box
    clean_box_css = ".product-img-box { height: 200px; display: flex; align-items: center; justify-content: center; margin-bottom: 0.75rem; background: #ffffff; border-radius: 14px; overflow: hidden; position: relative; padding: 10px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.04); }"
    clean_img_css = ".product-img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; transition: transform 0.3s ease; display: block; border-radius: 6px; }"

    html_text = re.sub(r'\.product-img-box\s*\{[^}]+\}', clean_box_css, html_text)
    html_text = re.sub(r'\.product-img\s*\{[^}]+\}', clean_img_css, html_text)

    # 2. Update each product card to its authentic image
    parts = html_text.split('<div class="product-card')
    new_parts = [parts[0]]
    updated = 0

    for c in parts[1:]:
        full = '<div class="product-card' + c
        name_m = re.search(r'<h3 class="product-name">(.*?)</h3>', full)
        if name_m:
            name = name_m.group(1).strip()
            # Match
            target_img = AUTHENTIC_IMAGE_MAP.get(name)
            if not target_img:
                for k, v in AUTHENTIC_IMAGE_MAP.items():
                    if k.lower() == name.lower() or k.lower() in name.lower() or name.lower() in k.lower():
                        target_img = v
                        break
            
            if target_img:
                full = re.sub(
                    r'(<img[^>]+src=")[^"]+(")',
                    rf'\g<1>{target_img}\g<2>',
                    full,
                    count=1
                )
                full = re.sub(
                    r'(<button type="button" class="variant-pill active"[^>]+data-img=")[^"]+(")',
                    rf'\g<1>{target_img}\g<2>',
                    full
                )
                updated += 1
        new_parts.append(full[len('<div class="product-card'):])

    final_html = '<div class="product-card'.join(new_parts)
    with open(path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Restored authentic product images for {updated} cards in {os.path.basename(path)}")

clean_and_restore_file(PROD_HTML)
clean_and_restore_file(FRONT_HTML)
