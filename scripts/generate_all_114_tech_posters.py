from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os, sys, re, math, html

BASE_DIR = "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web"
ASSETS_DIR = os.path.join(BASE_DIR, "demo_pages/assets")
PROD_HTML = os.path.join(BASE_DIR, "demo_pages/products/index.html")
FRONT_HTML = os.path.join(BASE_DIR, "demo_pages/frontend/index.html")

def get_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text).strip('_')
    return text[:45]

def create_tech_poster(src_path, dst_path, brand_label, model_title, spec_badge, glow_color, bg_tint):
    W, H = 1000, 1000
    canvas = Image.new('RGB', (W, H), bg_tint)
    draw = ImageDraw.Draw(canvas)

    cx, cy = W // 2, H // 2 - 25

    # 1. Radial Tech Nebula Glow
    max_r = 470
    for r in range(max_r, 0, -10):
        factor = (1.0 - (r / max_r) ** 1.35)
        c = (
            min(255, bg_tint[0] + int(glow_color[0] * factor * 0.95)),
            min(255, bg_tint[1] + int(glow_color[1] * factor * 0.95)),
            min(255, bg_tint[2] + int(glow_color[2] * factor * 0.95))
        )
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    # 2. Concentric Tech Orbit Rings
    for r in [210, 330, 430]:
        ring_color = (
            min(255, glow_color[0] // 3 + 18),
            min(255, glow_color[1] // 3 + 18),
            min(255, glow_color[2] // 3 + 28)
        )
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring_color, width=1)

    # 3. High-Tech Crosshairs and Precision Corner Brackets
    cross_c = (min(255, glow_color[0] // 2), min(255, glow_color[1] // 2), min(255, glow_color[2] // 2))
    draw.line([cx - 450, cy, cx - 420, cy], fill=cross_c, width=2)
    draw.line([cx + 420, cy, cx + 450, cy], fill=cross_c, width=2)
    draw.line([cx, cy - 450, cx, cy - 420], fill=cross_c, width=2)
    draw.line([cx, cy + 420, cx, cy + 450], fill=cross_c, width=2)

    # Corner HUD brackets
    pad = 38
    hud_len = 32
    hud_c = (100, 116, 139)
    draw.line([pad, pad, pad + hud_len, pad], fill=hud_c, width=2)
    draw.line([pad, pad, pad, pad + hud_len], fill=hud_c, width=2)
    draw.line([W - pad - hud_len, pad, W - pad, pad], fill=hud_c, width=2)
    draw.line([W - pad, pad, W - pad, pad + hud_len], fill=hud_c, width=2)
    draw.line([pad, H - pad, pad + hud_len, H - pad], fill=hud_c, width=2)
    draw.line([pad, H - pad - hud_len, pad, H - pad], fill=hud_c, width=2)
    draw.line([W - pad - hud_len, H - pad, W - pad, H - pad], fill=hud_c, width=2)
    draw.line([W - pad, H - pad - hud_len, W - pad, H - pad], fill=hud_c, width=2)

    # 4. Keynote Stage Pedestal & Laser Horizon
    floor_y = H - 195
    for y in range(floor_y, H):
        f = (y - floor_y) / (H - floor_y)
        c = (
            int(bg_tint[0] * (1 - f) + 4 * f),
            int(bg_tint[1] * (1 - f) + 7 * f),
            int(bg_tint[2] * (1 - f) + 14 * f)
        )
        draw.line([0, y, W, y], fill=c)

    laser_c = (min(255, glow_color[0] + 60), min(255, glow_color[1] + 60), min(255, glow_color[2] + 60))
    for x in range(W):
        d = abs(x - cx) / (W / 2)
        if d < 1.0:
            a = math.cos(d * math.pi / 2) ** 3
            draw.point((x, floor_y), fill=(int(laser_c[0] * a), int(laser_c[1] * a), int(laser_c[2] * a)))

    # 5. Load and process foreground device
    if os.path.exists(src_path):
        try:
            fg = Image.open(src_path).convert('RGBA')
            fg.thumbnail((680, 660), Image.Resampling.LANCZOS)

            # Transparent matte for white/light backgrounds
            datas = fg.getdata()
            new_data = []
            for item in datas:
                if item[0] > 235 and item[1] > 235 and item[2] > 235:
                    diff = 255 - min(item[0], item[1], item[2])
                    alpha = int(diff * 14) if diff < 18 else 255
                    new_data.append((item[0], item[1], item[2], min(item[3], alpha)))
                else:
                    new_data.append(item)
            fg.putdata(new_data)

            fg_x = (W - fg.width) // 2
            fg_y = floor_y - fg.height + 65

            # Floor Reflection
            ref = fg.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            ref_h = min(95, ref.height)
            ref = ref.crop((0, 0, ref.width, ref_h))
            ref_datas = ref.getdata()
            ref_new = []
            for idx, itm in enumerate(ref_datas):
                row = idx // ref.width
                f_fade = max(0, 1.0 - (row / ref_h)) * 0.20
                ref_new.append((itm[0], itm[1], itm[2], int(itm[3] * f_fade)))
            ref.putdata(ref_new)
            canvas.paste(ref, (fg_x, floor_y + 1), ref)

            # Drop shadow
            shadow = Image.new('RGBA', (fg.width + 40, 48), (0, 0, 0, 0))
            sdraw = ImageDraw.Draw(shadow)
            sdraw.ellipse([20, 5, fg.width + 20, 43], fill=(0, 0, 0, 185))
            shadow = shadow.filter(ImageFilter.GaussianBlur(14))
            canvas.paste(shadow, (fg_x - 20, floor_y - 24), shadow)

            # Device Paste
            canvas.paste(fg, (fg_x, fg_y), fg)
        except Exception as e:
            print(f"Error processing image {src_path}: {e}")

    # 6. Tech Graphic Typography & HUD Badges
    font_brand = get_font(18, bold=True)
    font_badge = get_font(14, bold=True)

    # Top Brand Pill
    brand_text = f"✦ {brand_label.upper()} ✦"
    draw.text((pad + 18, pad - 2), brand_text, fill=(148, 163, 184), font=font_brand)

    # Tech Status
    draw.text((W - pad - 175, pad - 2), "FLAGSHIP KEYNOTE", fill=laser_c, font=font_brand)

    # Bottom Spec Pill Badge (Glassmorphic)
    badge_w, badge_h = 580, 42
    bx = (W - badge_w) // 2
    by = H - 85

    pill = Image.new('RGBA', (badge_w, badge_h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pill)
    pdraw.rounded_rectangle([0, 0, badge_w, badge_h], radius=21, fill=(15, 23, 42, 220), outline=laser_c, width=1)
    canvas.paste(pill, (bx, by), pill)

    # Badge Text Centered
    spec_clean = spec_badge[:60]
    bbox = font_badge.getbbox(spec_clean)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = bx + max(10, (badge_w - tw) // 2)
    ty = by + (badge_h - th) // 2 - 2
    draw.text((tx, ty), spec_clean, fill=(241, 245, 249), font=font_badge)

    canvas.save(dst_path, 'JPEG', quality=95)

# Brand Palettes
BRAND_PALETTES = {
    "Apple": {
        "glow": (37, 99, 235),
        "bg": (7, 12, 24),
        "label": "APPLE RESELLER VN/A"
    },
    "Samsung": {
        "glow": (37, 99, 235),
        "bg": (6, 12, 28),
        "label": "SAMSUNG GALAXY AI"
    },
    "Sony": {
        "glow": (37, 99, 235),
        "bg": (6, 10, 24),
        "label": "SONY ENTERTAINMENT"
    },
    "Dell": {
        "glow": (14, 165, 233),
        "bg": (8, 14, 24),
        "label": "DELL TECHNOLOGIES"
    },
    "ASUS": {
        "glow": (239, 68, 68),
        "bg": (18, 6, 8),
        "label": "REPUBLIC OF GAMERS"
    },
    "OPPO": {
        "glow": (16, 185, 129),
        "bg": (6, 18, 14),
        "label": "OPPO AI PORTRAIT"
    },
    "Huawei": {
        "glow": (220, 38, 38),
        "bg": (20, 6, 8),
        "label": "HUAWEI HARMONYOS"
    },
    "Realme": {
        "glow": (234, 88, 12),
        "bg": (22, 10, 6),
        "label": "REALME DARE TO LEAP"
    }
}

# Read products/index.html
with open(PROD_HTML, "r", encoding="utf-8") as f:
    text = f.read()

cards = text.split('<div class="product-card')[1:]
print(f"Generating tech graphic posters for all {len(cards)} products...")

updated_cards_html = []
for i, c in enumerate(cards):
    full_card = '<div class="product-card' + c
    brand_m = re.search(r'data-brand="([^"]+)"', full_card[:80])
    brand = brand_m.group(1) if brand_m else 'Apple'
    
    name_m = re.search(r'<h3 class="product-name">(.*?)</h3>', full_card)
    name = name_m.group(1).strip() if name_m else f'Product {i+1}'

    specs_m = re.search(r'<div class="product-specs">(.*?)</div>', full_card)
    raw_specs = specs_m.group(1).strip() if specs_m else ''
    clean_specs = html.unescape(raw_specs).replace('&quot;', '"')
    spec_parts = [p.strip() for p in clean_specs.split('•') if p.strip()]
    spec_badge = " • ".join(spec_parts[:3]).upper() if spec_parts else name.upper()

    img_m = re.search(r'<img[^>]+src="([^"]+)"', full_card)
    current_img = img_m.group(1).strip() if img_m else '/assets/macbook_pro_silver.jpg'

    # Determine base source image for generation
    # If it is already a poster, see if there is an underlying real image
    base_src_filename = os.path.basename(current_img)
    base_src_path = os.path.join(ASSETS_DIR, base_src_filename)

    # Target poster filename
    slug = slugify(f"{brand}_{name}")
    poster_filename = f"poster_{slug}.jpg"
    poster_path = os.path.join(ASSETS_DIR, poster_filename)

    palette = BRAND_PALETTES.get(brand, BRAND_PALETTES["Apple"])

    # Generate tech graphic poster
    create_tech_poster(
        src_path=base_src_path,
        dst_path=poster_path,
        brand_label=palette["label"],
        model_title=name,
        spec_badge=spec_badge,
        glow_color=palette["glow"],
        bg_tint=palette["bg"]
    )

    poster_web_path = f"/assets/{poster_filename}"

    # Replace primary img src in card
    full_card = re.sub(
        r'(<img[^>]+src=")[^"]+(")',
        rf'\g<1>{poster_web_path}\g<2>',
        full_card,
        count=1
    )
    # Replace active variant pill
    full_card = re.sub(
        r'(<button type="button" class="variant-pill active"[^>]+data-img=")[^"]+(")',
        rf'\g<1>{poster_web_path}\g<2>',
        full_card
    )

    updated_cards_html.append(full_card[len('<div class="product-card'):])
    if (i + 1) % 15 == 0 or (i + 1) == len(cards):
        print(f"  Processed {i+1}/{len(cards)} posters...")

new_prod_html = '<div class="product-card'.join([text.split('<div class="product-card')[0]] + updated_cards_html)

with open(PROD_HTML, "w", encoding="utf-8") as f:
    f.write(new_prod_html)

print("Saved updated demo_pages/products/index.html")
