import openpyxl, re, json

XLSX = r"N:\商品資料庫AI專用-開放\商品優化原文件\澳思萊_產品資料庫_162款_完整版.xlsx"

with open(r"D:\專案經理全自動AI\aus-garden\web\lib\products.json", encoding="utf-8") as f:
    existing = {p["code"] for p in json.load(f)}
    existing_bases = {re.match(r"^(A\d+)", c).group(1) for c in existing if re.match(r"^(A\d+)", c)}

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb['🌿 產品資料庫(162款)']
missing = []
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i < 3: continue
    if not row or not row[4]: continue
    code = str(row[4]).strip()
    name = str(row[2] or "")
    # only AUS GARDEN products: full name contains 澳維花園 or Aus Garden
    if "澳維花園" not in name and "Aus Garden" not in name.lower().replace(" ", ""):
        if "aus garden" not in name.lower(): continue
    m = re.match(r"^(A\d+)", code)
    if not m: continue
    base = m.group(1)
    if base in existing_bases or code in existing: continue
    missing.append({
        "code": code,
        "fullName": row[2],
        "shortName": row[3],
        "series": row[1],
        "price": row[5],
        "benefits": row[6],
        "audience": row[7],
        "ingredients": row[8],
        "usage": row[9],
        "usp": row[10],
        "notes": row[11],
    })

print(f"Missing AUS GARDEN products: {len(missing)}")
for m in missing[:50]:
    print(f"  {m['code']}  {m['shortName']}  ({m['fullName'][:40] if m['fullName'] else ''})")

with open(r"D:\專案經理全自動AI\aus-garden\scripts\missing.json", "w", encoding="utf-8") as f:
    json.dump(missing, f, ensure_ascii=False, indent=2)
