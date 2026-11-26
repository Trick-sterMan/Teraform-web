import re

poster_map = {
    "iPhone 17 Pro Max": "/assets/poster_iphone_17_pro_max.jpg",
    "iPhone 17 Pro": "/assets/poster_iphone_17_pro.jpg",
    "iPhone 17 Air (Slim 5.6mm)": "/assets/poster_iphone_17_air.jpg",
    "iPhone 17": "/assets/poster_iphone_17_base.jpg",
    "iPhone 18 Pro Max": "/assets/poster_iphone_18_pro_max.jpg",
    "iPhone 18 Fold Duo Màn Gập": "/assets/poster_iphone_18_duo.jpg",
    "iPhone 18 Fold Duo": "/assets/poster_iphone_18_duo.jpg",
    "iPhone 16 Pro Max": "/assets/poster_iphone_16_pro_max.jpg",
    "Samsung Galaxy S25 Ultra 5G AI": "/assets/poster_samsung_s25_ultra.jpg",
    "Samsung Galaxy S25 Ultra": "/assets/poster_samsung_s25_ultra.jpg",
    "Samsung Galaxy S25+ 5G AI": "/assets/poster_samsung_s25_plus.jpg",
    "Samsung Galaxy S25 5G AI": "/assets/poster_samsung_s25_base.jpg",
    "Galaxy Z Fold Special Edition": "/assets/poster_samsung_zfold_se.jpg",
    "Samsung Galaxy S24 Ultra 5G AI": "/assets/poster_samsung_s24_ultra.jpg",
    "Samsung Galaxy S24 Ultra": "/assets/poster_samsung_s24_ultra.jpg",
    "Realme GT 7 Pro 5G": "/assets/poster_realme_gt7_pro.jpg",
    "Huawei Mate 70 Pro+": "/assets/poster_huawei_mate70_pro.jpg",
    "OPPO Find N5 5G": "/assets/poster_oppo_find_n5.jpg",
    "ASUS ROG Phone 9 Pro 5G": "/assets/poster_rog_phone_9_pro.jpg",
    "PlayStation 5 Pro (PS5 Pro) 2TB": "/assets/poster_ps5_pro.jpg",
    "Dell XPS 16 9640 Core Ultra": "/assets/poster_dell_xps16.jpg",
    "Dell XPS 16 9640": "/assets/poster_dell_xps16.jpg",
    "Apple Watch Ultra 2 49mm": "/assets/poster_apple_watch_ultra2.jpg",
    "Apple Watch Ultra 2": "/assets/poster_apple_watch_ultra2.jpg",
    "iPad Pro 13\" M4 OLED": "/assets/poster_ipad_pro_13.jpg",
    "iPad Pro 13 M4 OLED": "/assets/poster_ipad_pro_13.jpg",
    "MacBook Pro 16\" M3 Max": "/assets/poster_macbook_pro_16.jpg",
    "MacBook Pro 16 M3 Max": "/assets/poster_macbook_pro_16.jpg"
}

def update_page_posters(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    parts = html.split('<div class="product-card')
    new_parts = [parts[0]]

    count = 0
    for card_part in parts[1:]:
        card = '<div class="product-card' + card_part
        name_m = re.search(r'<h3 class="product-name">(.*?)</h3>', card)
        if name_m:
            name = name_m.group(1).strip()
            # Find best match in poster_map
            matched_poster = None
            if name in poster_map:
                matched_poster = poster_map[name]
            else:
                for k, v in poster_map.items():
                    if k.lower() in name.lower() or name.lower() in k.lower():
                        matched_poster = v
                        break
            
            if matched_poster:
                # Update main img src
                card = re.sub(
                    r'(<img[^>]+src=")[^"]+(")',
                    rf'\g<1>{matched_poster}\g<2>',
                    card,
                    count=1
                )
                # Update active variant pill if present
                card = re.sub(
                    r'(<button type="button" class="variant-pill active"[^>]+data-img=")[^"]+(")',
                    rf'\g<1>{matched_poster}\g<2>',
                    card
                )
                count += 1
        new_parts.append(card[len('<div class="product-card'):])

    new_html = '<div class="product-card'.join(new_parts)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Updated {count} product cards in {file_path}")

update_page_posters("/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html")
update_page_posters("/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/frontend/index.html")
