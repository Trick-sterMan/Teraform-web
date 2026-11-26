import re, os

PROD_HTML = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html"
FRONT_HTML = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/frontend/index.html"

# Update maps
distinct_updates = {
    # iPhone 17 distinct authentic photos
    "iPhone 17 Pro Max": {
        "img": "/assets/real_iphone_17_pro_max_silver.jpg",
        "variants": [
            ("Titan Bạc Silver", "/assets/real_iphone_17_pro_max_silver.jpg"),
            ("Cam Vũ Trụ (Cosmic Orange)", "/assets/real_iphone_17_pro_max_orange.jpg")
        ]
    },
    "iPhone 17 Pro": {
        "img": "/assets/real_iphone_17_pro_max_orange.jpg",
        "variants": [
            ("Cam Vũ Trụ (Cosmic Orange)", "/assets/real_iphone_17_pro_max_orange.jpg"),
            ("Titan Bạc Silver", "/assets/real_iphone_17_pro_max_silver.jpg")
        ]
    },
    "iPhone 17 Air (Slim 5.6mm)": {
        "img": "/assets/real_iphone_17_lineup_all.jpg",
        "variants": [
            ("Dòng Air Siêu Mỏng 5.6mm", "/assets/real_iphone_17_lineup_all.jpg"),
            ("Trắng Ngọc Trai", "/assets/real_iphone_17_white.jpg")
        ]
    },
    "iPhone 17": {
        "img": "/assets/real_iphone_17_mist_blue.jpg",
        "variants": [
            ("Xanh Lam (Mist Blue)", "/assets/real_iphone_17_mist_blue.jpg"),
            ("Tím Oải Hương (Lavender)", "/assets/real_iphone_17_lavender.jpg"),
            ("Trắng Tinh Khiết (White)", "/assets/real_iphone_17_white.jpg"),
            ("Đen Huyền Bí (Black)", "/assets/real_iphone_17_black.jpg")
        ]
    },
    
    # Samsung Galaxy S25 distinct authentic photos
    "Samsung Galaxy S25 Ultra 5G AI": {
        "img": "/assets/real_samsung_s25_ultra_silverblue.jpg",
        "variants": [
            ("Titan Bạc Ánh Xanh (Silverblue)", "/assets/real_samsung_s25_ultra_silverblue.jpg"),
            ("Xám Titan (Titanium Gray)", "/assets/samsung_s25_ultra_render.jpg")
        ]
    },
    "Samsung Galaxy S25 Ultra": {
        "img": "/assets/real_samsung_s25_ultra_silverblue.jpg",
        "variants": [
            ("Titan Bạc Ánh Xanh", "/assets/real_samsung_s25_ultra_silverblue.jpg")
        ]
    },
    "Samsung Galaxy S25+ 5G AI": {
        "img": "/assets/real_samsung_s25_plus.jpg",
        "variants": [
            ("Bạc Ánh Kim (Silver)", "/assets/real_samsung_s25_plus.jpg")
        ]
    },
    "Samsung Galaxy S25 5G AI": {
        "img": "/assets/real_samsung_s25_black_front.png",
        "variants": [
            ("Đen Huyền Bí Phantom Black", "/assets/real_samsung_s25_black_front.png")
        ]
    }
}

def update_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    parts = html.split('<div class="product-card')
    new_parts = [parts[0]]
    count = 0

    for c in parts[1:]:
        full = '<div class="product-card' + c
        name_m = re.search(r'<h3 class="product-name">(.*?)</h3>', full)
        if name_m:
            name = name_m.group(1).strip()
            if name in distinct_updates:
                cfg = distinct_updates[name]
                # Replace main image
                full = re.sub(
                    r'(<img[^>]+src=")[^"]+(")',
                    rf'\g<1>{cfg["img"]}\g<2>',
                    full,
                    count=1
                )
                # Replace active pill data-img
                full = re.sub(
                    r'(<button type="button" class="variant-pill active"[^>]+data-img=")[^"]+(")',
                    rf'\g<1>{cfg["img"]}\g<2>',
                    full
                )
                count += 1
                print(f"  [{os.path.basename(path)}] Updated {name} -> {cfg['img']}")
        new_parts.append(full[len('<div class="product-card'):])

    final_html = '<div class="product-card'.join(new_parts)
    with open(path, "w", encoding="utf-8") as f:
        f.write(final_html)

update_file(PROD_HTML)
update_file(FRONT_HTML)
print("Updated both pages with distinct authentic photos!")
