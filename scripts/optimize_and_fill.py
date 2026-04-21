"""
1) Resize all existing product images to max 720px (long edge), save as JPEG q=82 (keeps alpha -> PNG if needed).
2) Generate top-view flat-lay style placeholder images for missing AUS GARDEN products (720x720).
3) Update products.json to include the new placeholders.
"""
import os, json, re, math, random, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PRODUCTS_JSON = r"D:\專案經理全自動AI\aus-garden\web\lib\products.json"
IMG_DIR = r"D:\專案經理全自動AI\aus-garden\web\public\products"
MISSING_JSON = r"D:\專案經理全自動AI\aus-garden\scripts\missing.json"

MAX_SIDE = 720
JPEG_Q = 82

# -------- 1) Resize existing images --------
print("== Resizing existing images ==")
total_before = 0
total_after = 0
with open(PRODUCTS_JSON, encoding="utf-8") as f:
    products = json.load(f)

corrupt_codes = set()
for p in products:
    if not p.get("image"): continue
    fname = os.path.basename(p["image"])
    src = os.path.join(IMG_DIR, fname)
    if not os.path.exists(src): continue
    before = os.path.getsize(src)
    total_before += before
    try:
        im = Image.open(src)
        im.load()
    except Exception as e:
        print(f"  corrupt {fname}: {e} — will generate placeholder")
        corrupt_codes.add(p["code"])
        try: os.remove(src)
        except: pass
        p["image"] = None
        continue
    # resize long edge to MAX_SIDE
    w, h = im.size
    if max(w, h) > MAX_SIDE:
        if w >= h:
            nw, nh = MAX_SIDE, int(h * MAX_SIDE / w)
        else:
            nw, nh = int(w * MAX_SIDE / h), MAX_SIDE
        im = im.resize((nw, nh), Image.LANCZOS)

    # flatten alpha onto cream background (matches site bg)
    bg = Image.new("RGB", im.size, (250, 246, 239))
    if im.mode in ("RGBA", "LA"):
        bg.paste(im, mask=im.split()[-1])
    elif im.mode == "P":
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
    else:
        bg.paste(im.convert("RGB"))

    # always output jpg
    newname = re.sub(r"\.\w+$", ".jpg", fname)
    dst = os.path.join(IMG_DIR, newname)
    bg.save(dst, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    if newname != fname:
        os.remove(src)
    after = os.path.getsize(dst)
    total_after += after
    p["image"] = f"products/{newname}"

print(f"  {total_before/1024/1024:.1f} MB -> {total_after/1024/1024:.1f} MB")

# -------- 2) Generate top-view placeholders for missing products --------
print("\n== Generating top-view placeholders for missing products ==")
with open(MISSING_JSON, encoding="utf-8") as f:
    missing = json.load(f)

# existing codes
existing_codes = {p["code"] for p in products}
existing_bases = {re.match(r"^(A\d+)", c).group(1) for c in existing_codes if re.match(r"^(A\d+)", c)}

# font - try to find a Chinese-capable font on Windows
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msjh.ttc",  # Microsoft JhengHei
    r"C:\Windows\Fonts\msjhbd.ttc",
    r"C:\Windows\Fonts\mingliu.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]
def get_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try: return ImageFont.truetype(path, size)
            except: pass
    return ImageFont.load_default()

# AUS GARDEN palette
CREAM  = (250, 246, 239)
SAND   = (241, 233, 217)
MOSS   = (107, 122, 79)
FOREST = (63, 74, 46)
CLAY   = (200, 155, 107)
INK    = (42, 42, 40)

def draw_leaf(draw, cx, cy, length, angle_deg, color):
    """Draw a simple leaf shape."""
    import math
    pts = []
    # parametric leaf (vesica-ish)
    for t in [i/24 for i in range(25)]:
        # half-leaf x(t) and y(t)
        x = t * length
        y = math.sin(math.pi * t) * length * 0.28
        pts.append((x, y))
    for t in [i/24 for i in range(24, -1, -1)]:
        x = t * length
        y = -math.sin(math.pi * t) * length * 0.28
        pts.append((x, y))
    # rotate
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    rot = [(cx + x*ca - y*sa, cy + x*sa + y*ca) for x, y in pts]
    draw.polygon(rot, fill=color)
    # mid-rib
    x2 = cx + length*ca
    y2 = cy + length*sa
    draw.line([(cx, cy), (x2, y2)], fill=(FOREST[0], FOREST[1], FOREST[2], 120), width=2)

def make_placeholder(code, title, subtitle, dst):
    size = 720
    im = Image.new("RGB", (size, size), CREAM)
    draw = ImageDraw.Draw(im, "RGBA")

    # soft radial sand wash in center
    overlay = Image.new("RGBA", (size, size), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    for r in range(360, 120, -4):
        alpha = int((360 - r) / 240 * 50)
        odraw.ellipse([size/2 - r, size/2 - r, size/2 + r, size/2 + r],
                      fill=(SAND[0], SAND[1], SAND[2], alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(20))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(im, "RGBA")

    # scatter leaves (deterministic by code)
    rng = random.Random(hash(code) & 0xffffffff)
    leaf_palette = [
        (*MOSS, 180),
        (*FOREST, 150),
        (107, 130, 85, 160),
        (140, 155, 100, 150),
    ]
    for _ in range(14):
        cx = rng.randint(40, size-40)
        cy = rng.randint(40, size-40)
        # avoid strong overlap with the central bottle area
        if (cx-size/2)**2 + (cy-size/2)**2 < 180**2:
            # push outward
            dx = cx - size/2
            dy = cy - size/2
            d = max((dx*dx+dy*dy)**0.5, 1)
            cx = int(size/2 + dx/d * 220)
            cy = int(size/2 + dy/d * 220)
        length = rng.randint(50, 110)
        angle = rng.randint(0, 359)
        color = rng.choice(leaf_palette)
        draw_leaf(draw, cx, cy, length, angle, color)

    # central "bottle top-down" — concentric circles
    cx, cy = size//2, size//2 - 20
    # outer shadow
    shadow = Image.new("RGBA", (size, size), (0,0,0,0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([cx-130, cy-110, cx+130, cy+150], fill=(0,0,0,60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    im = Image.alpha_composite(im.convert("RGBA"), shadow).convert("RGB")
    draw = ImageDraw.Draw(im, "RGBA")

    # bottle body (from top view: circle)
    for r, col in [(120, FOREST), (110, MOSS), (90, (140, 155, 100)), (70, SAND)]:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col)
    # cap / dropper center
    draw.ellipse([cx-32, cy-32, cx+32, cy+32], fill=CLAY)
    draw.ellipse([cx-16, cy-16, cx+16, cy+16], fill=FOREST)

    # subtle highlight
    hl = Image.new("RGBA", (size, size), (0,0,0,0))
    hdraw = ImageDraw.Draw(hl)
    hdraw.ellipse([cx-100, cy-100, cx-20, cy-40], fill=(255,255,255,40))
    hl = hl.filter(ImageFilter.GaussianBlur(12))
    im = Image.alpha_composite(im.convert("RGBA"), hl).convert("RGB")
    draw = ImageDraw.Draw(im, "RGBA")

    # brand mark top-left
    f_brand = get_font(22)
    f_sub = get_font(13)
    draw.text((34, 28), "AUS GARDEN", fill=FOREST, font=f_brand)
    draw.text((34, 56), "澳維花園 · From the Garden", fill=MOSS, font=f_sub)

    # code top-right
    f_code = get_font(14)
    draw.text((size-34, 28), code, fill=CLAY, font=f_code, anchor="rt")

    # title at bottom
    f_title = get_font(36)
    f_caption = get_font(16)
    title_text = title or code
    # center text; truncate if too long
    if len(title_text) > 16:
        title_text = title_text[:15] + "…"
    draw.text((size//2, size-110), title_text, fill=FOREST, font=f_title, anchor="mm")
    if subtitle:
        sub = subtitle
        if len(sub) > 28: sub = sub[:27] + "…"
        draw.text((size//2, size-70), sub, fill=INK, font=f_caption, anchor="mm")
    # bottom rule
    draw.rectangle([size//2 - 40, size-42, size//2 + 40, size-40], fill=CLAY)

    im.save(dst, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)

# clean product name: drop 【】 prefix and size suffix
def clean_name(full):
    if not full: return ""
    s = re.sub(r"【[^】]*】\s*", "", str(full)).strip()
    s = re.sub(r"\s*\d+\s*(ml|ML|g|G|L)\s*$", "", s).strip()
    return s

# First: generate placeholders for corrupt-source products still in products list
for p in products:
    if p.get("image"): continue
    code = p["code"]
    title = clean_name(p.get("shortName") or p.get("fullName"))
    subtitle = p.get("series") or p.get("category") or ""
    fname = f"{code}.jpg"
    dst = os.path.join(IMG_DIR, fname)
    make_placeholder(code, title, subtitle, dst)
    p["image"] = f"products/{fname}"
    print(f"  * {code}  {title}  (corrupt-source placeholder)")

added = 0
# Map every existing image file basename (without ext) to its product
existing_image_basenames = {
    os.path.splitext(os.path.basename(p["image"]))[0]
    for p in products if p.get("image")
}
for m in missing:
    code = m["code"]
    # skip if a file already exists for this code (either exact or as any SKU variant)
    if code in existing_image_basenames:
        continue
    # also check: is there an existing file whose name starts with this code
    # (handles xlsx A33050 vs image A330) or vice-versa
    if any(b.startswith(code) or code.startswith(b) for b in existing_image_basenames):
        continue
    dst_check = os.path.join(IMG_DIR, f"{code}.jpg")
    if os.path.exists(dst_check):
        continue
    title = clean_name(m.get("shortName") or m.get("fullName"))
    subtitle = m.get("series") or ""
    fname = f"{code}.jpg"
    dst = os.path.join(IMG_DIR, fname)
    make_placeholder(code, title, subtitle, dst)
    products.append({
        "code": code,
        "series": m.get("series"),
        "fullName": m.get("fullName"),
        "shortName": m.get("shortName"),
        "price": m.get("price"),
        "benefits": m.get("benefits"),
        "audience": m.get("audience"),
        "ingredients": m.get("ingredients"),
        "usage": m.get("usage"),
        "usp": m.get("usp"),
        "notes": m.get("notes"),
        "category": "其他",
        "folder": "",
        "image": f"products/{fname}",
    })
    added += 1
    print(f"  + {code}  {title}")

print(f"\nAdded {added} placeholders. Total products: {len(products)}")

with open(PRODUCTS_JSON, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

# final folder size
total = sum(os.path.getsize(os.path.join(IMG_DIR, x)) for x in os.listdir(IMG_DIR))
print(f"Final folder size: {total/1024/1024:.1f} MB ({len(os.listdir(IMG_DIR))} files)")
