# 驗證紀錄：PaperMod 調整設定 + 更新主題 + 英文語系

- 分支：`feat/papermod-tuning-i18n`（從 `main` 的 `3ac2f30` 建立）
- 日期：2026-11-12
- Hugo：v0.169.0+extended（本機）；Cloudflare Pages 也是 0.169.0
- PaperMod：`1cf5327` → `1181196`（官方 master，2026-10-25）

所有 build 都輸出到暫存目錄，並用 `HUGO_RESOURCEDIR` 指到暫存目錄，`public/` 和 `resources/` 都沒有變動。旗標與線上相同（`--minify`）。

## 自動檢查

| # | 項目 | 結果 |
|---|---|---|
| 1 | `hugo --minify --panicOnWarning --printI18nWarnings --printPathWarnings` | 通過，0 個 WARN / ERROR（更新前有 2 個 PaperMod 棄用警告） |
| 2 | 基準 64 個中文 HTML 路徑（`baseline-clean-html.txt`） | 全部存在，缺少 0 個 |
| 3 | 線上 sitemap 的 42 個 URL（`baseline-live-urls.txt`） | 全部在新的 `/zh/sitemap.xml` 內 |
| 4 | RSS 與搜尋索引 | `index.xml`、`posts/index.xml`、`tags/index.xml`、`categories/index.xml`、`index.json`、`en/index.xml`、`en/index.json` 都存在 |
| 5 | 非 HTML 檔案 | 與基準相比沒有任何檔案被移除（只有主題 CSS／JS 的 fingerprint 改變） |
| 6 | 內部連結 | 277 個 `/blog/` 開頭的連結全部存在；絕對網址中只有 `safari-pinned-tab.svg` 404（封面圖 404 已修正，見下方） |
| 7 | 冷快取 build 時間 | 約 5 秒（本機） |

新增的頁面：`archives/`、`zh/index.html`（Hugo 自動產生，從 `/zh/` 轉到中文首頁），以及英文版 11 頁（`en/`、`en/posts/threads-marketing/`、`en/search/`、`en/archives/`、`en/tags/` 等）。

## 功能檢查

| 項目 | 結果 |
|---|---|
| 文章閱讀 | 目錄（預設收合）、閱讀時間、麵包屑（首頁 › 文章）、上一篇／下一篇、程式碼複製都有輸出 |
| 選單 | 中文：搜尋、標籤、彙整、首頁；英文：Search、Tags、Archives、Home（「首頁」連到 pitchat.co，放最後；部落格首頁由左上角 Pitchat 標誌連結）。連結正確，目前頁面有標示 |
| 彙整頁 | `/archives/` 依年、月列出 22 篇；`/en/archives/` 列出 1 篇 |
| 分享按鈕 | Facebook、X、LinkedIn |
| RSS | 首頁社群圖示有 RSS（中文 `/index.xml`、英文 `/en/index.xml`）；文章列表和單一標籤頁有 RSS 按鈕 |
| SEO | 首頁 meta description 已設定；搜尋頁、彙整頁有正式 description；`favicon-16x16.png`、`favicon-32x32.png`、`apple-touch-icon.png` 已存在 |
| 多語系 | 頁首有語言切換（中文 ⇄ English）；翻譯文章顯示「Translations: 中文」 |
| hreflang | 首頁與範例文章：`zh`、`en` 互指，加上指向中文版的 `x-default`；未翻譯的文章只有自身的 `zh` |
| sitemap | `/sitemap.xml` 為 sitemap index → `/zh/sitemap.xml`（43 個 URL，含 zh-TW／en alternate）、`/en/sitemap.xml`（7 個 URL） |
| `<html lang>` | 中文 `zh`、英文 `en` |
| 介面語言 | 中文為繁體（上一頁、下一頁、目錄、分鐘、分享、標籤、首頁）；英文為英文 |
| 搜尋 | 中文查「抽獎」得 13 筆；英文查「algorithm」得 1 筆 |
| 深淺色 | 切換正常（light → dark，背景變為 rgb(29, 30, 32)），預設 light |
| GA | `G-0XK2GTG7KT` 仍在 production build 的 HTML 中 |
| Gallery | `line-bots-recommendation` 的 9 個 gallery 排版正常、捲動後 lazy load 正常、swipebox 燈箱可開啟；沒有 JavaScript 錯誤 |

## 分享預覽封面圖（已修正）

線上原本所有文章的 `og:image`、`twitter:image` 和 JSON-LD 圖片都指向不存在的網址（例如 `https://pitchat.co/blog/cover.jpg`），社群分享預覽不會顯示封面。原因是文章用 page bundle，但 PaperMod 只在 `cover.relative = true` 時才以文章路徑解析封面。

修法：新增 `layouts/partials/cover-url.html`，用 PaperMod `cover.html` 相同的方式先找 page bundle 裡的圖片，取它實際發佈的網址；並覆寫 `templates/opengraph.html`、`twitter_cards.html`、`schema_json.html`，只把封面那一行改成呼叫這個 partial。文章 front matter 不用改。

驗證：23 篇文章（中文 22 篇、英文 1 篇）各有 1 個 `og:image`、1 個 `twitter:image`、1 個 JSON-LD 圖片，全部指向存在的檔案；英文文章使用中文 bundle 的同一張圖。與前一次 build 相比，只有這 23 個文章頁改變。

## 已知問題

1. **`safari-pinned-tab.svg` 404。** 需要單色 SVG 版 logo。

## 截圖

更新前（線上）與更新後（本機 `hugo server`）的截圖未放進 repo，已另外提供：中文首頁、中文文章、英文首頁的桌面版（1440×900）與手機版（375×812），以及一張深色模式。

## 第二階段改善（2026-11-12）

| 項目 | 結果 |
|---|---|
| 舊網域連結 | 6 處 `blog.pitchat.co` 改為 `pitchat.co/blog`，`content/` 中已無舊網域 |
| 結尾空格資料夾 | 改名為 `how-pitchat-makes-lottery-transparent`，以 `url` 固定原網址；頁面輸出與改名前完全相同 |
| 分類 | 抽獎工具 9、Threads 8、科技趨勢 3、使用教學 2；英文範例文章為 Threads |
| 殘留網址（12 個） | `/categories/threads/`、`/categories/科技趨勢/`、`/tags/threads/`、`/tags/數據分析/`、`/tags/社群媒體/` 恢復為真實頁面（各自的 `page/1/` 為 Hugo 轉址頁）；`/posts/2025-line-bots-recommendation/` → `line-bots-recommendation`、`/posts/my-first-post/` → `how-to-register-pithcat`。`public/` 中已沒有 build 不會產生的 HTML |
| 分享按鈕 | X、LinkedIn、Facebook、LINE、Threads；LINE、Threads 連結的標題與網址都有 percent-encode，中英文版各自帶正確網址 |
| `<html lang>` | 中文頁 `zh-TW`、英文頁 `en`（含轉址頁） |
| 嚴格 build | `--panicOnWarning --printI18nWarnings --printPathWarnings` 通過，0 個 WARN／ERROR，冷快取約 5 秒 |
| 基準頁面 | 64 個中文 HTML 全部存在；線上 sitemap 42 個 URL 全部在 `/zh/sitemap.xml` |
| 內部連結 | 檢查 1714 個，只剩 `safari-pinned-tab.svg` 404 |
