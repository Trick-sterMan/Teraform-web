import re, os

PROD_HTML = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html"
FRONT_HTML = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/frontend/index.html"

# Build map from product name to poster path from PROD_HTML
with open(PROD_HTML, "r", encoding="utf-8") as f:
    prod_text = f.read()

prod_cards = prod_text.split('<div class="product-card')[1:]
prod_poster_map = {}
for c in prod_cards:
    name_m = re.search(r'<h3 class="product-name">(.*?)</h3>', c)
    img_m = re.search(r'<img[^>]+src="([^"]+)"', c)
    if name_m and img_m:
        prod_poster_map[name_m.group(1).strip()] = img_m.group(1).strip()

print(f"Extracted {len(prod_poster_map)} poster mappings from products catalog.")

# Update FRONT_HTML
with open(FRONT_HTML, "r", encoding="utf-8") as f:
    front_text = f.read()

front_cards = front_text.split('<div class="product-card')
new_front = [front_cards[0]]
updated_count = 0

for c in front_cards[1:]:
    full = '<div class="product-card' + c
    name_m = re.search(r'<h3 class="product-name">(.*?)</h3>', full)
    if name_m:
        name = name_m.group(1).strip()
        poster = prod_poster_map.get(name)
        if not poster:
            # Fuzzy match
            for k, v in prod_poster_map.items():
                if k.lower() in name.lower() or name.lower() in k.lower():
                    poster = v
                    break
        if poster:
            full = re.sub(
                r'(<img[^>]+src=")[^"]+(")',
                rf'\g<1>{poster}\g<2>',
                full,
                count=1
            )
            full = re.sub(
                r'(<button type="button" class="variant-pill active"[^>]+data-img=")[^"]+(")',
                rf'\g<1>{poster}\g<2>',
                full
            )
            updated_count += 1
            print(f"  Frontend updated: {name} -> {poster}")
    new_front.append(full[len('<div class="product-card'):])

new_front_html = '<div class="product-card'.join(new_front)
with open(FRONT_HTML, "w", encoding="utf-8") as f:
    f.write(new_front_html)

print(f"Saved {updated_count} updated cards in demo_pages/frontend/index.html")
