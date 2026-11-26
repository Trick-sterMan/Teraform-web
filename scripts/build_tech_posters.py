from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os, math

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

def create_tech_poster(src_path, dst_path, brand_label, model_title, spec_badge, glow_color, bg_tint=(10, 14, 26)):
    W, H = 1024, 1024
    canvas = Image.new('RGB', (W, H), bg_tint)
    draw = ImageDraw.Draw(canvas)

    cx, cy = W // 2, H // 2 - 25

    # 1. Radial Tech Nebula Glow
    max_r = 480
    for r in range(max_r, 0, -8):
        factor = (1.0 - (r / max_r) ** 1.4)
        c = (
            min(255, bg_tint[0] + int(glow_color[0] * factor * 0.95)),
            min(255, bg_tint[1] + int(glow_color[1] * factor * 0.95)),
            min(255, bg_tint[2] + int(glow_color[2] * factor * 0.95))
        )
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    # 2. Concentric Tech Orbit Rings
    for r in [220, 340, 440]:
        ring_color = (
            min(255, glow_color[0] // 3 + 20),
            min(255, glow_color[1] // 3 + 20),
            min(255, glow_color[2] // 3 + 30)
        )
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring_color, width=1)

    # 3. High-Tech Crosshairs and Precision Corner Brackets
    cross_c = (min(255, glow_color[0] // 2), min(255, glow_color[1] // 2), min(255, glow_color[2] // 2))
    draw.line([cx - 460, cy, cx - 430, cy], fill=cross_c, width=2)
    draw.line([cx + 430, cy, cx + 460, cy], fill=cross_c, width=2)
    draw.line([cx, cy - 460, cx, cy - 430], fill=cross_c, width=2)
    draw.line([cx, cy + 430, cx, cy + 460], fill=cross_c, width=2)

    # Corner HUD brackets
    pad = 40
    hud_len = 35
    hud_c = (100, 116, 139)
    # Top-Left
    draw.line([pad, pad, pad + hud_len, pad], fill=hud_c, width=2)
    draw.line([pad, pad, pad, pad + hud_len], fill=hud_c, width=2)
    # Top-Right
    draw.line([W - pad - hud_len, pad, W - pad, pad], fill=hud_c, width=2)
    draw.line([W - pad, pad, W - pad, pad + hud_len], fill=hud_c, width=2)
    # Bottom-Left
    draw.line([pad, H - pad, pad + hud_len, H - pad], fill=hud_c, width=2)
    draw.line([pad, H - pad - hud_len, pad, H - pad], fill=hud_c, width=2)
    # Bottom-Right
    draw.line([W - pad - hud_len, H - pad, W - pad, H - pad], fill=hud_c, width=2)
    draw.line([W - pad, H - pad - hud_len, W - pad, H - pad], fill=hud_c, width=2)

    # 4. Keynote Stage Pedestal & Laser Horizon
    floor_y = H - 200
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
        fg = Image.open(src_path).convert('RGBA')
        fg.thumbnail((700, 680), Image.Resampling.LANCZOS)

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
        fg_y = floor_y - fg.height + 70

        # Cast Floor Reflection
        ref = fg.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        ref_h = 100
        ref = ref.crop((0, 0, ref.width, ref_h))
        ref_datas = ref.getdata()
        ref_new = []
        for idx, itm in enumerate(ref_datas):
            row = idx // ref.width
            f_fade = max(0, 1.0 - (row / ref_h)) * 0.22
            ref_new.append((itm[0], itm[1], itm[2], int(itm[3] * f_fade)))
        ref.putdata(ref_new)
        canvas.paste(ref, (fg_x, floor_y + 1), ref)

        # Drop shadow
        shadow = Image.new('RGBA', (fg.width + 40, 50), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.ellipse([20, 5, fg.width + 20, 45], fill=(0, 0, 0, 190))
        shadow = shadow.filter(ImageFilter.GaussianBlur(15))
        canvas.paste(shadow, (fg_x - 20, floor_y - 25), shadow)

        # Device Paste
        canvas.paste(fg, (fg_x, fg_y), fg)

    # 6. Tech Graphic Typography & HUD Badges
    font_brand = get_font(18, bold=True)
    font_title = get_font(28, bold=True)
    font_badge = get_font(14, bold=True)

    # Top Brand Pill
    brand_text = f"✦ {brand_label.upper()} ✦"
    draw.text((pad + 20, pad - 2), brand_text, fill=(148, 163, 184), font=font_brand)

    # Tech Status
    draw.text((W - pad - 180, pad - 2), "FLAGSHIP KEYNOTE", fill=laser_c, font=font_brand)

    # Bottom Spec Pill Badge (Glassmorphic)
    badge_w, badge_h = 580, 44
    bx = (W - badge_w) // 2
    by = H - 90

    # Draw Badge Background Pill
    pill = Image.new('RGBA', (badge_w, badge_h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pill)
    pdraw.rounded_rectangle([0, 0, badge_w, badge_h], radius=22, fill=(15, 23, 42, 220), outline=laser_c, width=1)
    canvas.paste(pill, (bx, by), pill)

    # Badge Text Centered
    # Using textbbox to center
    bbox = font_badge.getbbox(spec_badge)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = bx + (badge_w - tw) // 2
    ty = by + (badge_h - th) // 2 - 2
    draw.text((tx, ty), spec_badge, fill=(241, 245, 249), font=font_badge)

    canvas.save(dst_path, 'JPEG', quality=95)
    print(f"Created Tech Graphic Banner: {os.path.basename(dst_path)} ({os.path.getsize(dst_path)} bytes)")

posters = [
    # iPhone 17 & 18 Lineup
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/iphone_17_pro_max.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_iphone_17_pro_max.jpg",
        "brand_label": "Apple Next-Gen 2025",
        "model_title": "iPhone 17 Pro Max",
        "spec_badge": "A19 PRO 2NM • TITANIUM CERAMIC • ZOOM 10X • 120HZ PROMOTION",
        "glow_color": (37, 99, 235),  # Electric Sapphire Blue
        "bg_tint": (7, 12, 24)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/iphone_17_pro.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_iphone_17_pro.jpg",
        "brand_label": "Apple Flagship 2025",
        "model_title": "iPhone 17 Pro",
        "spec_badge": "6.3\" PROMOTION • A19 PRO • TETRAPRISM 5X • NATURAL TITANIUM",
        "glow_color": (217, 119, 6),  # Warm Desert Titanium Amber
        "bg_tint": (18, 14, 10)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/iphone_17_air.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_iphone_17_air.jpg",
        "brand_label": "Apple Breakthrough 2025",
        "model_title": "iPhone 17 Air (Slim 5.6mm)",
        "spec_badge": "5.6MM ULTRA SLIM • TITANIUM-ALUMINIUM • 6.6\" PROMOTION 120HZ",
        "glow_color": (14, 165, 233),  # Sky Cyan
        "bg_tint": (8, 16, 26)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/iphone_17_air_white.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_iphone_17_base.jpg",
        "brand_label": "Apple Innovation 2025",
        "model_title": "iPhone 17 Standard",
        "spec_badge": "FIRST-EVER 120HZ PROMOTION • A19 BIONIC • DUAL 48MP FUSION",
        "glow_color": (99, 102, 241),  # Violet Crystal
        "bg_tint": (12, 10, 25)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/iphone_18_pro_max.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_iphone_18_pro_max.jpg",
        "brand_label": "Apple Future Flagship 2026",
        "model_title": "iPhone 18 Pro Max",
        "spec_badge": "UNDER-DISPLAY INVISIBLE FACE ID • A20 PRO 1.8NM • 15X CONTINUOUS ZOOM",
        "glow_color": (168, 85, 247),  # Cosmic Hologram Purple
        "bg_tint": (14, 8, 28)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/iphone_18_duo.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_iphone_18_duo.jpg",
        "brand_label": "Apple Fold Innovation 2026",
        "model_title": "iPhone 18 Fold Duo",
        "spec_badge": "8.1\" DYNAMIC DUO OLED • LIQUID TITANIUM HINGE • APPLE M5 FOLD",
        "glow_color": (6, 182, 212),  # Cyber Neon Cyan
        "bg_tint": (6, 18, 24)
    },
    # Samsung Galaxy S25 & Z Fold Lineup
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/samsung_s25_ultra_render.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_samsung_s25_ultra.jpg",
        "brand_label": "Samsung Galaxy Unpacked 2025",
        "model_title": "Samsung Galaxy S25 Ultra 5G AI",
        "spec_badge": "GALAXY AI 2.0 • SNAPDRAGON 8 ELITE 3NM • 200MP AI SENSOR",
        "glow_color": (37, 99, 235),  # Samsung Galaxy AI Blue
        "bg_tint": (5, 12, 30)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/samsung_s25_plus.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_samsung_s25_plus.jpg",
        "brand_label": "Samsung Galaxy AI 2025",
        "model_title": "Samsung Galaxy S25+ 5G AI",
        "spec_badge": "6.7\" QHD+ 3000 NITS • SNAPDRAGON 8 ELITE • ARMOR ALUMINUM",
        "glow_color": (59, 130, 246),  # Galaxy Blue
        "bg_tint": (8, 14, 28)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/samsung_s25_base.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_samsung_s25_base.jpg",
        "brand_label": "Samsung Galaxy AI 2025",
        "model_title": "Samsung Galaxy S25 5G AI",
        "spec_badge": "COMPACT 6.2\" DYNAMIC AMOLED 2X • ON-DEVICE GALAXY AI 2.0",
        "glow_color": (96, 165, 250),  # Ice Blue
        "bg_tint": (8, 15, 25)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/samsung_zfold_se.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_samsung_zfold_se.jpg",
        "brand_label": "Samsung Special Edition",
        "model_title": "Galaxy Z Fold Special Edition",
        "spec_badge": "10.6MM ULTRA SLIM • 8.0\" DUAL AMOLED • 200MP FOLD CAMERA",
        "glow_color": (217, 119, 6),  # Luxury Titanium Gold
        "bg_tint": (20, 14, 8)
    },
    # Contemporary Other Brands Flagships
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/realme_gt_7_pro.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_realme_gt7_pro.jpg",
        "brand_label": "Realme Dare To Leap 2025",
        "model_title": "Realme GT 7 Pro 5G",
        "spec_badge": "SNAPDRAGON 8 ELITE • 6500MAH TITAN BATTERY • IP69 UNDERWATER",
        "glow_color": (234, 88, 12),  # Mars Orange
        "bg_tint": (25, 10, 5)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/huawei_mate_70_pro.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_huawei_mate70_pro.jpg",
        "brand_label": "Huawei HarmonyOS NEXT 2025",
        "model_title": "Huawei Mate 70 Pro+",
        "spec_badge": "HARMONYOS NEXT 100% PURE • KIRIN 9020 • BEIDOU SATELLITE 3",
        "glow_color": (220, 38, 38),  # Huawei Red & Gold
        "bg_tint": (22, 6, 8)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/oppo_find_n5.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_oppo_find_n5.jpg",
        "brand_label": "OPPO Innovation 2025",
        "model_title": "OPPO Find N5 5G",
        "spec_badge": "ULTRA-FLAT TITANIUM HINGE • SNAPDRAGON 8 ELITE • HASSELBLAD",
        "glow_color": (16, 185, 129),  # OPPO Emerald Green
        "bg_tint": (6, 20, 14)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/rog_phone_9_pro.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_rog_phone_9_pro.jpg",
        "brand_label": "ASUS Republic of Gamers",
        "model_title": "ASUS ROG Phone 9 Pro 5G",
        "spec_badge": "SNAPDRAGON 8 ELITE • 185HZ AMOLED • ANIME VISION LED MATRIX",
        "glow_color": (239, 68, 68),  # ROG Cyber Red
        "bg_tint": (20, 4, 6)
    }
]

for p in posters:
    create_tech_poster(**p)

print("\nAll 14 Tech Graphic Poster Banners successfully built!")

additional_posters = [
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/real_iphone_16_pro_max.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_iphone_16_pro_max.jpg",
        "brand_label": "Apple Retail Flagship 2024",
        "model_title": "iPhone 16 Pro Max",
        "spec_badge": "A18 PRO 3NM • CAMERA CONTROL • 5X TETRAPRISM • NATURAL TITANIUM",
        "glow_color": (217, 119, 6),
        "bg_tint": (18, 14, 10)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/real_samsung_s24_ultra.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_samsung_s24_ultra.jpg",
        "brand_label": "Samsung Galaxy AI Store",
        "model_title": "Samsung Galaxy S24 Ultra 5G AI",
        "spec_badge": "GALAXY AI BUILT-IN • TITANIUM FRAME • S PEN • 200MP QUAD-TELE",
        "glow_color": (99, 102, 241),
        "bg_tint": (10, 12, 28)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/ps5_pro.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_ps5_pro.jpg",
        "brand_label": "Sony PlayStation Gaming",
        "model_title": "PlayStation 5 Pro 2TB",
        "spec_badge": "ADVANCED RAY TRACING • PSSR AI UPSCALING • 2TB SSD • 120FPS 4K",
        "glow_color": (37, 99, 235),
        "bg_tint": (6, 12, 26)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/dell_xps.png",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_dell_xps16.jpg",
        "brand_label": "Dell Technologies Premium",
        "model_title": "Dell XPS 16 9640 Core Ultra",
        "spec_badge": "INTEL CORE ULTRA 7 • RTX 4070 • 4K+ OLED INFINITYEDGE TOUCH",
        "glow_color": (14, 165, 233),
        "bg_tint": (8, 16, 26)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/apple_watch_ultra2.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_apple_watch_ultra2.jpg",
        "brand_label": "Apple Watch Extreme",
        "model_title": "Apple Watch Ultra 2 49mm",
        "spec_badge": "3000 NITS DISPLAY • SIP S9 DUAL-CORE • PRECISION DUAL-GPS • 100M",
        "glow_color": (234, 88, 12),
        "bg_tint": (24, 10, 6)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/ipad_pro_13_m4.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_ipad_pro_13.jpg",
        "brand_label": "Apple Pro Tablet",
        "model_title": "iPad Pro 13\" M4 OLED",
        "spec_badge": "APPLE M4 3NM • ULTRA RETINA XDR TANDEM OLED • 5.1MM THIN",
        "glow_color": (168, 85, 247),
        "bg_tint": (16, 8, 26)
    },
    {
        "src_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/macbook_pro_m3_space_gray.jpg",
        "dst_path": "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/assets/poster_macbook_pro_16.jpg",
        "brand_label": "Apple Silicon Studio",
        "model_title": "MacBook Pro 16\" M3 Max",
        "spec_badge": "M3 MAX 16-CORE CPU • 40-CORE GPU • LIQUID RETINA XDR • 128GB UNIFIED",
        "glow_color": (100, 116, 139),
        "bg_tint": (12, 14, 20)
    }
]

for p in additional_posters:
    create_tech_poster(**p)

print("\nAll 21 Tech Graphic Posters created!")
