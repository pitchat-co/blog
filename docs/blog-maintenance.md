# 部落格維護說明

## 本機預覽

```bash
HUGO_RESOURCEDIR="$TMPDIR/pitchat-resources" hugo server --renderToMemory
```

- `--renderToMemory`：不把輸出寫進 `public/`。少了這個參數，`hugo server` 會改動 `public/` 裡幾百個檔案，還會帶入 livereload 腳本；萬一被 commit，就會部署上線。
- `HUGO_RESOURCEDIR`：處理過的圖片寫到暫存資料夾，不會在 `resources/_gen` 產生大量新檔。
- 預覽網址：`http://localhost:1313/blog/`

上線由 Cloudflare Pages 負責：push 到 `main` 後自動執行 `hugo --minify`，不需要在本機 build `public/`。

## 新增文章

文章是 page bundle：`content/posts/<網址名稱>/index.md`，圖片放在同一個資料夾。

- 資料夾名稱就是網址，例如 `content/posts/threads-marketing/` → `/posts/threads-marketing/`。不要用空格或中文。
- front matter 範例（TOML）：

  ```toml
  +++
  title = '文章標題'
  date = 2026-11-12T10:00:00+08:00
  # lastmod = 2026-12-01T10:00:00+08:00   # 大幅改寫時才填，見下方說明
  draft = false
  categories = ["抽獎工具"]   # 抽獎工具、Threads、科技趨勢、使用教學 擇一
  tags = ["Threads"]          # 從下方「標籤清單」挑選
  description = '搜尋結果與分享預覽顯示的摘要，中文 80～110 字（也會顯示在文章標題下方）'
  cover = { image = "cover.png", alt = "描述封面畫面的文字" }   # 檔名對應資料夾裡的圖片
  +++
  ```

- 標題層級：內文不要用 `#`（文章標題已經是 H1），段落用 `##`、子段落用 `###`。目錄只顯示每篇最上層的標題，所以段落如果都寫成 `###`、只有一個 `##`，目錄就只會剩一項。
- `description`：每篇都要寫。寫出讀者能得到什麼，不重複標題；不寫具體成效數字、價格，也不宣稱和 Meta 官方合作。主要曝光落在主站或 `/app` 工具頁的查詢（例如 ig抽獎、threads抽獎、抽獎系統），文章不要拿來當主要關鍵字，改用教學或比較的角度，並連到該工具頁（詳見 seo-workspace 的 seo-context、blog-profile）。
- `cover.alt`：描述封面畫面，例如「Pitchat 預約發文編輯畫面截圖：…」，搜尋引擎和螢幕閱讀器都會用到。
- 文章之間的連結：寫成 `[文字]({{< ref "/posts/<資料夾名稱>" >}})`，目標文章不存在時 build 會報錯；網址特殊的文章（例如結尾有 `-` 的那篇）也會自動解析成正確網址。每篇新文章至少連到 2 篇相關文章，也回頭在 2 篇舊文章中加上連到新文章的連結。提到工具時連到主站或 `/app` 的工具頁（只帶 `?r=blog`，不加 `utm_*`）。
- `lastmod`：內容有實質更新（改寫段落、更新資訊）時才填。日期晚於 `date` 時，標題下方會顯示「更新於 …」，結構化資料的 `dateModified` 和 sitemap 的 `<lastmod>` 也會跟著更新。修錯字、改連結不用填。
- 標籤清單（每個標籤至少要有 2 篇文章，新文章優先從這裡挑；沒有合適的就不加，靠分類歸類）：Threads、Instagram、社群媒體、演算法、數據分析、自動回覆、發文工具、免費工具。要新增標籤時，至少要有 2 篇文章適用，並在 `content/tags/<標籤>/_index.md` 寫一段描述。
- 移除或改名標籤時，用 `aliases` 把舊標籤頁 `/tags/<舊標籤小寫>/` 轉到最接近的頁面，避免搜尋結果出現 404。目前的轉址寫在 `content/tags/*/_index.md`、`content/categories/抽獎工具/_index.md`，以及 line-bots-recommendation、threads-ig-cross-platform-lottery 兩篇文章。
- 內文圖片照常放 PNG 或 JPEG 即可，build 時會自動產生縮小的 WebP（`render-image.html`），不需要自己壓縮或縮圖。原圖寬度建議至少 1440px，高解析螢幕才會清楚。
- 動畫圖片用動態 WebP，不要用 GIF（同樣的畫面通常小 50～75%）。轉檔：`gif2webp -lossy -q 75 -m 6 -mt 原檔.gif -o 新檔.webp`（`brew install webp`），轉完和原檔比對畫質。
- 文章改名或搬移時，在新文章加 `aliases = ["/posts/舊網址/"]`，讓舊網址轉到新網址。

## 英文文章

中英文章不需要一一對應：

| 情況 | 做法 | 結果 |
|---|---|---|
| 中文文章的英文翻譯 | 在中文文章的資料夾加 `index.en.md` | 兩篇自動互相連結，頁面顯示「Translations」，並輸出 hreflang |
| 只有英文的文章 | 建立新資料夾，只放 `index.en.md` | 只出現在 `/en/` |
| 只有中文的文章 | 照舊只放 `index.md` | 只出現在中文版 |

不相關的中英文章不要放在同一個資料夾，否則會被當成翻譯。

英文的分類、標籤是獨立的；英文文章的 `categories` 用英文名稱即可，例如 `["Threads"]`。

## 主題覆寫

PaperMod 是 git submodule（`themes/PaperMod`，目前釘在 `1181196`）。下列檔案是從主題複製後修改的，**更新主題時要檢查主題是否也改了這些檔案**：

| 覆寫檔 | 主題原檔 | 修改內容 |
|---|---|---|
| `layouts/baseof.html` | `layouts/baseof.html` | `<html lang>` 改用 locale（`zh-TW`／`en`） |
| `layouts/partials/share_icons.html` | `layouts/_partials/share_icons.html` | 開頭加「分享至：」與複製連結按鈕；新增 LINE、Threads 分享按鈕；按鈕依 `ShareButtons` 設定的順序顯示（主題原本是固定順序） |
| `layouts/partials/post_meta.html` | `layouts/_partials/post_meta.html` | 日期後面加上「更新於」（`lastmod` 晚於 `date` 才顯示）和分類連結（首頁卡片也會顯示，但卡片整塊是文章連結，只有文章頁能點進分類） |
| `layouts/_markup/render-image.html` | `layouts/_markup/render-image.html` | 內文 PNG／JPEG 自動轉成 480～1440px 的 WebP 並輸出 `srcset`；所有點陣圖加上 `width`、`height`、`decoding="async"`。GIF 和 WebP（可能是動畫）照原檔輸出 |
| `layouts/partials/templates/opengraph.html` | `layouts/_partials/templates/opengraph.html` | `og:image` 改用 `cover-url.html`；加上 `og:image:alt`（取自 `cover.alt`，沒有封面時用 `params.imagesAlt`） |
| `layouts/partials/templates/twitter_cards.html` | `layouts/_partials/templates/twitter_cards.html` | `twitter:image` 改用 `cover-url.html`；加上 `twitter:image:alt`（同上） |
| `layouts/partials/templates/schema_json.html` | `layouts/_partials/templates/schema_json.html` | JSON-LD 圖片改用 `cover-url.html`；logo 改讀 `params.schema.logo`（`pitchat.png`），沒設才用 favicon；作者改由 `schema-author.html` 產生 |

以下是本站自己的檔案，不是複製來的，更新主題時不用比對：
- `layouts/partials/cover-url.html`：封面圖的實際網址
- `layouts/partials/schema-author.html`：結構化資料的作者。作者名稱是「Pitchat」時輸出 Organization，其他名稱輸出 Person
- `layouts/partials/extend_head.html`：`x-default` hreflang（PaperMod 的擴充點）
- `layouts/partials/google_analytics.html`：GA4
- `assets/css/extended/share.css`：分享區塊的標籤與複製連結按鈕樣式（PaperMod 的 CSS 擴充點）
- `layouts/partials/extend_post_content.html`：文章結尾的「相關文章」（PaperMod 的擴充點）。排序規則在 `hugo.yaml` 的 `related`：同分類優先，其次共同標籤，再依日期遠近，最多 3 篇；沒有相關文章時不顯示
- `assets/css/extended/related.css`：相關文章的樣式
- `assets/css/extended/post-meta.css`：文章 meta 列的分類連結樣式
- `assets/css/extended/images.css`：有寬高的內文圖片維持比例（`height: auto`），和 `render-image.html` 搭配
- `assets/css/extended/toc.css`：目錄只顯示最上層標題（目錄預設展開，避免長文章的目錄太長）
- `layouts/404.html`、`assets/css/extended/404.css`：404 頁（說明，以及回首頁／搜尋／分類按鈕），取代 PaperMod 只有「404」三個字的頁面。文字在 `i18n/*.yaml` 的 `not_found_*`
- `layouts/partials/clauses.html`：把中文句子依「，」拆成不斷行的片段，窄螢幕時在逗號後換行（404 頁使用）
- `i18n/zh-tw.yaml`、`i18n/en.yaml`：本站新增的介面文字，會和主題的翻譯檔合併

分享區塊的文字在 `hugo.yaml` 的 `shareLabel`、`copyLinkLabel`、`copiedLabel`（中文在 `params`，英文在 `languages.en.params`）。按鈕順序也在 `hugo.yaml` 的 `ShareButtons`：中文依台灣常用程度（LINE、Facebook、Threads、X、LinkedIn），英文版不放 LINE（Facebook、X、LinkedIn、Threads）。複製連結固定在最前面。

### 更新主題的步驟

```bash
git -C themes/PaperMod fetch origin master
git -C themes/PaperMod log --oneline HEAD..origin/master
```

列出上面 7 個主題原檔在新版本中的變動：

```bash
git -C themes/PaperMod diff HEAD origin/master -- layouts/baseof.html layouts/_markup/render-image.html layouts/_partials/share_icons.html layouts/_partials/post_meta.html layouts/_partials/templates/opengraph.html layouts/_partials/templates/twitter_cards.html layouts/_partials/templates/schema_json.html
```

- 沒有輸出：直接更新即可。
- 有變動：把變動合併進對應的覆寫檔，並保留本站的修改。

```bash
git -C themes/PaperMod checkout origin/master
```

更新後用 `docs/migration/baseline-clean-html.txt` 比對頁面清單，確認網址沒有變。PaperMod 的 `hugo.Version` 下限要和 Cloudflare Pages 的 `HUGO_VERSION` 一起檢查。

## 已知的特殊設定

- `content/posts/how-pitchat-makes-lottery-transparent/`：網址固定為 `/posts/how-pitchat-makes-lottery-transparent-/`（結尾有 `-`，是舊資料夾名稱留下的），由 front matter 的 `url` 指定，請勿移除。
- 英文選單使用相對網址（`search/` 等），不用 `pageRef`：PaperMod 會再加一次語言前綴，變成 `/en/blog/en/...`。
- `static/og-image.png`（1200×630）：沒有封面圖的頁面（首頁、分類、標籤、彙整、搜尋）的分享預覽圖，由 `hugo.yaml` 的 `params.images` 指定。來源是主站 `pitchat-frontend/public/opengraph-image.png`，四周裁掉 32px 後置中，兩側延伸背景色。主站換圖時要一起更新。
