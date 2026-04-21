"""Fill AUS GARDEN products from xlsx that have no product code (—)."""
import openpyxl, json, re, os, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

XLSX = r"N:\商品資料庫AI專用-開放\商品優化原文件\澳思萊_產品資料庫_162款_完整版.xlsx"
PRODUCTS_JSON = r"D:\專案經理全自動AI\aus-garden\web\lib\products.json"
IMG_DIR = r"D:\專案經理全自動AI\aus-garden\web\public\products"

CREAM = (250,246,239); SAND = (241,233,217); MOSS = (107,122,79)
FOREST = (63,74,46); CLAY = (200,155,107); INK = (42,42,40)

FONT_CANDIDATES = [r"C:\Windows\Fonts\msjh.ttc", r"C:\Windows\Fonts\msjhbd.ttc",
                   r"C:\Windows\Fonts\mingliu.ttc", r"C:\Windows\Fonts\simhei.ttf",
                   r"C:\Windows\Fonts\arial.ttf"]
def get_font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def draw_leaf(d, cx, cy, length, angle_deg, color):
    pts = []
    for t in [i/24 for i in range(25)]:
        pts.append((t*length, math.sin(math.pi*t)*length*0.28))
    for t in [i/24 for i in range(24,-1,-1)]:
        pts.append((t*length, -math.sin(math.pi*t)*length*0.28))
    a = math.radians(angle_deg); ca, sa = math.cos(a), math.sin(a)
    rot = [(cx+x*ca-y*sa, cy+x*sa+y*ca) for x,y in pts]
    d.polygon(rot, fill=color)

def clean_name(full):
    if not full: return ""
    s = re.sub(r"【[^】]*】\s*", "", str(full)).strip()
    s = re.sub(r"\s*\d+\s*(ml|ML|g|G|L)\s*$", "", s).strip()
    return s

def make_placeholder(code, title, subtitle, dst):
    size = 720
    im = Image.new("RGB", (size, size), CREAM)
    overlay = Image.new("RGBA", (size, size), (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    for r in range(360, 120, -4):
        a = int((360-r)/240*50)
        od.ellipse([size/2-r,size/2-r,size/2+r,size/2+r], fill=(SAND[0],SAND[1],SAND[2],a))
    overlay = overlay.filter(ImageFilter.GaussianBlur(20))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(im, "RGBA")

    rng = random.Random(hash(code) & 0xffffffff)
    palette = [(*MOSS,180), (*FOREST,150), (107,130,85,160), (140,155,100,150)]
    for _ in range(14):
        cx = rng.randint(40, size-40); cy = rng.randint(40, size-40)
        if (cx-size/2)**2 + (cy-size/2)**2 < 180**2:
            dx, dy = cx-size/2, cy-size/2
            dd = max((dx*dx+dy*dy)**0.5, 1)
            cx = int(size/2 + dx/dd*220); cy = int(size/2 + dy/dd*220)
        draw_leaf(d, cx, cy, rng.randint(50,110), rng.randint(0,359), rng.choice(palette))

    cx, cy = size//2, size//2-20
    shadow = Image.new("RGBA", (size,size), (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([cx-130,cy-110,cx+130,cy+150], fill=(0,0,0,60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    im = Image.alpha_composite(im.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(im, "RGBA")

    for r, col in [(120,FOREST),(110,MOSS),(90,(140,155,100)),(70,SAND)]:
        d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=col)
    d.ellipse([cx-32,cy-32,cx+32,cy+32], fill=CLAY)
    d.ellipse([cx-16,cy-16,cx+16,cy+16], fill=FOREST)
    hl = Image.new("RGBA",(size,size),(0,0,0,0))
    hd = ImageDraw.Draw(hl)
    hd.ellipse([cx-100,cy-100,cx-20,cy-40], fill=(255,255,255,40))
    hl = hl.filter(ImageFilter.GaussianBlur(12))
    im = Image.alpha_composite(im.convert("RGBA"), hl).convert("RGB")
    d = ImageDraw.Draw(im, "RGBA")

    d.text((34,28), "AUS GARDEN", fill=FOREST, font=get_font(22))
    d.text((34,56), "澳維花園 · From the Garden", fill=MOSS, font=get_font(13))
    d.text((size-34,28), code, fill=CLAY, font=get_font(14), anchor="rt")

    t = title or code
    if len(t) > 16: t = t[:15] + "…"
    d.text((size//2, size-110), t, fill=FOREST, font=get_font(36), anchor="mm")
    if subtitle:
        s = subtitle if len(subtitle) <= 28 else subtitle[:27]+"…"
        d.text((size//2, size-70), s, fill=INK, font=get_font(16), anchor="mm")
    d.rectangle([size//2-40, size-42, size//2+40, size-40], fill=CLAY)
    im.save(dst, "JPEG", quality=82, optimize=True, progressive=True)

with open(PRODUCTS_JSON, encoding="utf-8") as f:
    products = json.load(f)
existing_short = {p.get("shortName") for p in products}
existing_codes = {p["code"] for p in products}

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb['🌿 產品資料庫(162款)']
added = 0
counter = 1
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i < 3 or not row or not row[4]: continue
    name = str(row[2] or "")
    if "澳維花園" not in name and "aus garden" not in name.lower().replace(" ", ""):
        continue
    code = str(row[4]).strip()
    sn = str(row[3] or "")
    if code not in ("—","–","-","") and not code.startswith("—"): continue
    if sn in existing_short: continue

    synthetic = f"AG{counter:03d}"
    while synthetic in existing_codes:
        counter += 1
        synthetic = f"AG{counter:03d}"
    existing_codes.add(synthetic)

    title = clean_name(sn or name)
    subtitle = str(row[1] or "")
    fname = f"{synthetic}.jpg"
    make_placeholder(synthetic, title, subtitle, os.path.join(IMG_DIR, fname))
    cat = "精油類" if "精油" in sn else ("臉部保養" if "霜" in sn or "乳" in sn else "其他")
    products.append({
        "code": synthetic, "series": row[1], "fullName": row[2], "shortName": sn,
        "price": row[5], "benefits": row[6], "audience": row[7],
        "ingredients": row[8], "usage": row[9], "usp": row[10], "notes": row[11],
        "category": cat, "folder": "", "image": f"products/{fname}",
    })
    print(f"  + {synthetic}  {title}  [{cat}]")
    added += 1
    counter += 1

print(f"Added {added}. Total products: {len(products)}")
with open(PRODUCTS_JSON, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
