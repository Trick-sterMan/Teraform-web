import re

target_file = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html"
with open(target_file, "r", encoding="utf-8") as f:
    html = f.read()

updates = {
    # Apple specific next-gen distinct renders
    "iPhone 17 Pro": "/assets/iphone_17_pro.jpg",
    "iPhone 18 Pro Max": "/assets/iphone_18_pro_max.jpg",
    
    # Samsung specific next-gen distinct renders
    "Samsung Galaxy S25 5G AI": "/assets/samsung_s25_base.jpg",
    
    # Realme distinct images
    "Realme GT Neo 6 (Snapdragon 7+ Gen 3 Tản Nhiệt Cực Đại)": "/assets/realme_gt_neo_back.jpg",
    
    # OPPO distinct images
    "OPPO Find X8 5G Mỏng Nhẹ AI": "/assets/oppo_find_white_back.jpg"
}

parts = html.split('<div class="product-card"')
new_parts = [parts[0]]

count = 0
for card in parts[1:]:
    name_m = re.search(r'<h3 class="product-name">(.*?)</h3>', card)
    if name_m:
        name = name_m.group(1).strip()
        if name in updates:
            correct_img = updates[name]
            card = re.sub(
                r'(<img[^>]+src=")[^"]+(")',
                rf'\g<1>{correct_img}\g<2>',
                card,
                count=1
            )
            card = re.sub(
                r'(<button type="button" class="variant-pill active"[^>]+data-img=")[^"]+(")',
                rf'\g<1>{correct_img}\g<2>',
                card
            )
            count += 1
            print(f"Updated {name} -> {correct_img}")
    new_parts.append(card)

new_html = '<div class="product-card"'.join(new_parts)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Successfully applied {count} dedicated renders and photos!")
