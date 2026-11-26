for path in [
    "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/products/index.html",
    "/Users/huynhnhathoa/.gemini/antigravity/scratch/Teraform-web/demo_pages/frontend/index.html"
]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    old_css = ".product-img-box { height: 190px; display: flex; align-items: center; justify-content: center; margin-bottom: 0.75rem; background: #f8fafc; border-radius: 14px; overflow: hidden; position: relative; padding: 12px; }"
    new_css = ".product-img-box { height: 215px; display: flex; align-items: center; justify-content: center; margin-bottom: 0.75rem; background: #070b14; border-radius: 14px; overflow: hidden; position: relative; padding: 2px; border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: inset 0 0 25px rgba(0, 0, 0, 0.5); }"
    
    if old_css in text:
        text = text.replace(old_css, new_css)
    else:
        # For frontend if slightly different height
        old_css2 = ".product-img-box { height: 190px; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem; background: #f8fafc; border-radius: 14px; overflow: hidden; position: relative; padding: 12px; }"
        new_css2 = ".product-img-box { height: 215px; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem; background: #070b14; border-radius: 14px; overflow: hidden; position: relative; padding: 2px; border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: inset 0 0 25px rgba(0, 0, 0, 0.5); }"
        text = text.replace(old_css2, new_css2)

    # Make product-img fill and scale cleanly
    text = text.replace(
        ".product-img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; transition: transform 0.3s ease; display: block; }",
        ".product-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.35s ease; display: block; border-radius: 12px; }"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Updated poster box styling in {path}")
