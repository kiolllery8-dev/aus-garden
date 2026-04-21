# AUS GARDEN 澳維花園 · Website

Next.js 14 (App Router) + Tailwind CSS，靜態匯出部署至 GitHub Pages。

## 本地開發

```bash
cd web
npm install
npm run dev
# http://localhost:3000
```

## 本地建置靜態檔

```bash
npm run build
# 產生 web/out/ 靜態檔
```

## 部署到 GitHub Pages

1. 將整個 `aus-garden/` 目錄推上 GitHub（建議 repo 名稱：`aus-garden`）。
2. 在 GitHub → Settings → Pages → Source 選擇 **GitHub Actions**。
3. Push 到 `main` 分支，`.github/workflows/deploy.yml` 會自動：
   - 以 `NEXT_PUBLIC_BASE_PATH=/<repo-name>` 建置
   - 上傳 `web/out/` 為 Pages artifact
   - 發佈至 `https://<user>.github.io/<repo-name>/`

### 若使用自訂網域（CNAME）
將 workflow 中的 `NEXT_PUBLIC_BASE_PATH` 改為空字串，
並在 `web/public/` 放一個 `CNAME` 檔（內容為網域）。

## 技術棧

- Next.js 14（App Router、`output: 'export'`）
- React 18 + TypeScript
- Tailwind CSS
- Noto Serif / Sans TC（Google Fonts）

## 頁面

- `/` 首頁（Hero、三支柱、精選課程、精選商品、品牌故事、CTA）
- `/courses` 手作課程（依 A/B/C/D 分類）
- `/products` 香氛商品
- `/about` 品牌故事
- `/contact` 聯絡我們（含詢問表單）

## 品牌設計

色彩：`cream` / `sand` / `moss` / `forest` / `clay` / `ink`
字體：Noto Serif TC（標題）+ Noto Sans TC（內文）

所有內容依 `aus-garden/CLAUDE.md` 品牌核心事實撰寫。
