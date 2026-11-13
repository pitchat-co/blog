# 未處理事項

## 主站

- **`https://pitchat.co/robots.txt` 沒有列出部落格 sitemap**，`pitchat.co/sitemap.xml` 也沒有部落格網址。要在 `dudeyee-backend` 加上 `Sitemap: https://pitchat.co/blog/sitemap.xml`。`/blog/robots.txt` 位在子目錄，搜尋引擎不會讀。
  - **不用改主站的替代做法：** 在 Google Search Console 的 `pitchat.co` 資源中，到「索引 → Sitemap」提交 `https://pitchat.co/blog/sitemap.xml`，效果相同。需要有 GSC 權限的人操作。
  - 這批 SEO 修改上線後，同時在 GSC 對標題有修改的 3 篇（threads-scheduler-guide、threads-image-splitter、threads-management）要求重新索引，並在下一次週報追蹤它們的點擊率變化。
- 英文版選單的 Home 連到 `https://pitchat.co`，主站有英文版時再改。

## 內容

- 英文文章：目前只有 1 篇範例（`threads-marketing`）。中英文章不需一一對應，寫法見 `docs/blog-maintenance.md`。

## 主題與版面

- `safari-pinned-tab.svg` 仍是 404：需要單色 SVG 版 logo。這是舊版 Safari 才用的圖示，影響很小。
- LINE 分享按鈕：LINE 文件表示，使用分享連結前需閱讀並同意 LINE Social Plugins 使用規範（https://developers.line.biz/en/docs/line-social-plugins/），請負責人確認。

## 部署

`public/`、`resources/`、`.hugo_build.lock`、`.idea/` 已在 `chore/untrack-build-output` 分支取消追蹤並列入 `.gitignore`。合併上線後要確認：
- `https://pitchat.co/blog/posts/threads-image-splitter/operation.gif` 回 404（舊檔已不在線上）
- 比對 `baseline-live-urls.txt` 與分類、標籤、轉址頁，確認沒有網址消失
- 會消失的只有 build 不再產生的舊檔：已刪除或改名的原圖、舊版 CSS／JS、舊命名的縮圖、15 個舊標籤的 RSS，以及 0 byte 的 `public/posts/threads-`
