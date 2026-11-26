with open("/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Fix iPhone 17 Pro variant pill pointing to 17 pro max
text = text.replace(
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_17_pro_max.jpg">Titan Bạc Ánh Kim</button>',
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_17_pro.jpg">Titan Bạc Ánh Kim</button>'
)

# Fix iPhone 17 base variant pill pointing to 17 air
text = text.replace(
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_17_air.jpg">Xanh Lam Tinh Khiết</button>',
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_17_air_white.jpg">Xanh Lam Tinh Khiết</button>'
)

# Fix iPhone 18 Pro Max variant pill pointing to 17 pro max
text = text.replace(
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_17_pro_max.jpg">Titan Hologram Tự Nhiên</button>',
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_18_pro_max.jpg">Titan Hologram Tự Nhiên</button>'
)

# Fix iPhone 18 Fold Duo variant pill pointing to 17 pro max
text = text.replace(
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_17_pro_max.jpg">Titan Bạc Siêu Nhẹ</button>',
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/iphone_18_duo.jpg">Titan Bạc Siêu Nhẹ</button>'
)

# Fix Samsung S25 base variant pill pointing to s25 plus
text = text.replace(
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s25_plus.jpg">Bạc Ánh Xanh Tinh Khiết</button>',
    '<button type="button" class="variant-pill" onclick="selectColor(this)" data-img="/assets/samsung_s25_base.jpg">Bạc Ánh Xanh Tinh Khiết</button>'
)

# Fix Samsung S24 base variant pill pointing to s24 ultra
text = text.replace(
    '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_samsung_s24_ultra.jpg">Xám Titan (Titanium Gray)</button>',
    '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_samsung_s24.jpg">Xám Titan (Titanium Gray)</button>'
)

# Fix iPhone 15 base variant pill pointing to 15 pro max
text = text.replace(
    '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_15_pro_max.jpg">Titan Tự Nhiên (Natural)</button>',
    '<button type="button" class="variant-pill active" onclick="selectColor(this)" data-img="/assets/real_iphone_15.jpg">Xanh Pastel (Blue)</button>'
)

with open("/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaned cross-linked variant pills successfully.")
