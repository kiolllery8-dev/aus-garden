import openpyxl, json, os, re, shutil, sys

XLSX = r"N:\商品資料庫AI專用-開放\商品優化原文件\澳思萊_產品資料庫_162款_完整版.xlsx"
IMG_ROOT = r"\\Auslife\Public\商品資料庫AI專用-開放\商品優化原文件\商品圖\澳維花園"
OUT_DIR = r"D:\專案經理全自動AI\aus-garden\web\public\products"
DATA_OUT = r"D:\專案經理全自動AI\aus-garden\web\lib\products.json"

os.makedirs(OUT_DIR, exist_ok=True)

# 1) scan image folders; key = product code prefix (A\d+)
folder_map = {}  # code -> (category, folder_path, folder_name)
for cat in os.listdir(IMG_ROOT):
    cat_path = os.path.join(IMG_ROOT, cat)
    if not os.path.isdir(cat_path): continue
    for pf in os.listdir(cat_path):
        pf_path = os.path.join(cat_path, pf)
        if not os.path.isdir(pf_path): continue
        m = re.match(r"^(A\d+)", pf)
        if m:
            folder_map[m.group(1)] = (cat, pf_path, pf)

print(f"Found {len(folder_map)} image folders")

# 2) read xlsx
wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb['🌿 產品資料庫(162款)']
headers = None
products = []
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 2:
        headers = row
        continue
    if i < 3: continue
    if not row or not row[4]: continue  # 品號
    code = str(row[4]).strip()
    m = re.match(r"^(A\d+)", code)
    if not m: continue
    base_code = m.group(1)
    # match — try full code, then base
    key = code if code in folder_map else base_code
    # also scan for any folder that starts with this code
    if key not in folder_map:
        for fc in folder_map:
            if fc.startswith(base_code) or base_code.startswith(fc):
                key = fc; break
    if key not in folder_map:
        continue
    cat, path, folder_name = folder_map[key]
    products.append({
        "code": code,
        "series": row[1],
        "fullName": row[2],
        "shortName": row[3],
        "price": row[5],
        "benefits": row[6],
        "audience": row[7],
        "ingredients": row[8],
        "usage": row[9],
        "usp": row[10],
        "notes": row[11],
        "category": cat,
        "folder": folder_name,
        "_key": key,
    })

print(f"Matched {len(products)} products from xlsx")

# 3) also include folders that had no xlsx match
matched_keys = {p["_key"] for p in products}
for key, (cat, path, folder_name) in folder_map.items():
    if key in matched_keys: continue
    # infer name from folder: "A2013_玫瑰果油" -> "玫瑰果油"
    nm = folder_name.split("_", 1)[1] if "_" in folder_name else folder_name
    products.append({
        "code": key,
        "series": cat,
        "fullName": nm,
        "shortName": nm,
        "price": None,
        "benefits": None, "audience": None, "ingredients": None,
        "usage": None, "usp": None, "notes": None,
        "category": cat,
        "folder": folder_name,
        "_key": key,
    })

# dedupe by _key, prefer entries WITH xlsx data (have price or benefits)
seen = {}
for p in products:
    k = p["_key"]
    if k not in seen:
        seen[k] = p
    else:
        # prefer row with more xlsx data
        has_now = any(seen[k].get(f) for f in ("price","benefits","ingredients"))
        has_new = any(p.get(f) for f in ("price","benefits","ingredients"))
        if has_new and not has_now:
            seen[k] = p
products = list(seen.values())
print(f"Total products: {len(products)}")

# 4) pick one "hero" image per product and copy to public/products/<code>.<ext>
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")
def pick_hero(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(IMG_EXTS)]
    if not files: return None
    # prefer files NOT containing 說明/SKU labels; prefer 新版/IMG/1/主
    def score(f):
        low = f.lower()
        s = 0
        if "說明" in f: s -= 50
        if "01" in f or "1." in f or "-1" in f: s += 10
        if "新版" in f: s += 8
        if "img" in low: s += 5
        if "主" in f: s += 20
        # prefer png > jpg (usually higher quality product shots)
        if low.endswith(".png"): s += 3
        # prefer smaller filenames (usually main product)
        s -= len(f) * 0.01
        return s
    files.sort(key=score, reverse=True)
    return os.path.join(folder, files[0])

for p in products:
    _, path, _ = folder_map[p["_key"]]
    hero = pick_hero(path)
    if not hero:
        p["image"] = None
        continue
    ext = os.path.splitext(hero)[1].lower()
    dest = os.path.join(OUT_DIR, f"{p['_key']}{ext}")
    shutil.copy2(hero, dest)
    p["image"] = f"products/{p['_key']}{ext}"

# cleanup private field
for p in products: p.pop("_key", None)

with open(DATA_OUT, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"Wrote {DATA_OUT}")
print(f"Copied images to {OUT_DIR}")
