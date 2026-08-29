# CoinvestAI — Advanced SEO Implementation Guide
**Date:** 2026-08-29
**Keywords Focus:** AI Finance Tools, Algorithmic Analysis, Smart Investing Insights (no stuffing)

## 1. URL Preservation & Redirection (تم التنفيذ)
- **_redirects** (Netlify / Cloudflare Pages): يحتوي على 301 redirects للروابط القديمة ذات المسافات والملفات بدون امتداد.
- **.htaccess** (Apache): نفس القواعد + Security Headers + Compression + Caching.
- **HTML Fallback:** كل صفحة redirect تحتوي:
  - `<link rel="canonical" href="...">`
  - `<meta http-equiv="refresh">`
  - `window.location.replace()`
  - `noindex, follow` لتجنب duplicate content.

### الروابط المحفوظة:
- `AI-Driven On-Chain Analytics in Crypto Markets (2026).html` → `/blog-blockchain-data-analytics-ai.html` 301
- `blog-ai-onchain-crypto-analytics-2026` → `/blog-blockchain-data-analytics-ai.html` 301
- `blog-ai-onchain-crypto-analytics-2026.html` → `/blog-blockchain-data-analytics-ai.html` 301

## 2. Meta Tags Optimization
### Template (includes/seo-head-template.html)
- Title: 50-60 chars, جذاب، يحتوي كلمة مفتاحية واحدة أساسية.
  - مثال: `Explainable AI in Finance: How XAI Improves Algorithmic Transparency (2026) — CoinvestAI`
- Description: 150-160 chars، دقيقة، CTA ضمني، بدون حشو.
- Canonical: مطلق `https://coinvestai.com/...`
- OG & Twitter: 1200x630 image، نفس العنوان والوصف.
- Robots: `index, follow, max-snippet:-1, max-image-preview:large`

### Keyword Strategy (بدون حشو):
- استخدم كل كلمة مفتاحية مرة واحدة في Title، مرة في Description، و2-3 مرات طبيعية في النص.
- مرادفات: `AI-powered investing tools` بدل تكرار `AI Finance Tools`.

## 3. Schema Markup (JSON-LD)
### Organization (كل الصفحات)
```json
{
  "@type":"Organization",
  "name":"CoinvestAI",
  "url":"https://coinvestai.com/",
  "logo":"https://coinvestai.com/logo.png",
  "knowsAbout":["AI Finance Tools","Algorithmic Analysis","Smart Investing Insights"]
}
```

### WebSite (Homepage + Blog)
- يتضمن `SearchAction` للـ Sitelinks Search Box.

### TechArticle / Article (كل مقال)
- استخدم قالب `includes/schema-techarticle-template.json`
- حقول إلزامية: headline, description, author (Person), publisher (Organization), datePublished, dateModified, mainEntityOfPage, keywords, wordCount, timeRequired.

### BreadcrumbList (كل صفحة داخلية)
```json
{
  "@type":"BreadcrumbList",
  "itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://coinvestai.com/"},
    {"@type":"ListItem","position":2,"name":"Blog","item":"https://coinvestai.com/blog.html"},
    {"@type":"ListItem","position":3,"name":"Article Title"}
  ]
}
```

### FAQPage (للصفحات التي تحتوي FAQ)
- يجب أن يطابق النص الظاهر حرفيًا.

## 4. Blog / Knowledge Base Structure
### الملفات الجديدة:
- `/blog.html` — تم تحسينه (search, categories, lazy ads, schema CollectionPage)
- `/blog-ai-explainability-finance-2026.html` — مقال 1 (XAI)
- `/blog-real-time-risk-scoring-ai-2026.html` — مقال 2 (Risk Scoring)

### هيكل المقال الاحترافي (موجود في القالب الجديد):
- Breadcrumbs
- Category tag + Title + Meta (date, author, read time)
- Disclaimer above the fold
- Hero image placeholder (CSS gradient)
- TOC sticky (desktop) + anchor links
- H2 / H3 hierarchy
- Callout boxes, comparison tables
- FAQ with JSON-LD
- References & Data Sources
- Internal links (3-5 per article)
- Related articles grid
- Comments (Cusdis)
- Newsletter block
- Footer disclaimer

### Performance:
- `content-visibility:auto` للـ footer والـ ads
- Lazy-load AdSense (scroll/touch/mousemove + timeout 7s)
- No render-blocking CSS (inline critical CSS)
- Responsive: mobile-first, 1 column <768px

## 5. Sitemap & Robots
- `sitemap.xml` محدث: يتضمن المقالين الجديدين + تاريخ lastmod 2026-08-29 + priority 0.85
- `robots.txt` محدث: Disallow utm_*, fbclid, gclid, Allow /

## 6. Internal Linking Strategy
- كل مقال جديد يربط:
  - إلى 2 مقال قديم ذو صلة (مثلاً blog-ai-fraud-detection-finance.html)
  - إلى 1 أداة (ai-tools-chatgpt.html, ai-tools-tradingview.html)
  - إلى 1 guide (guides.html)
  - إلى About / Editorial Guidelines (E-E-A-T)

## 7. E-E-A-T Signals
- Author: `CoinvestAI Editorial Team` مع رابط لصفحة authors-coinvestai-editorial-team.html
- Reviewed by, Last Updated, Reading time
- References: Investopedia, SEC, BIS, CoinMarketCap
- Methodology link, Disclaimer, Contact

## 8. Checklist قبل النشر
- [ ] Title 50-60 chars, Description 150-160
- [ ] Canonical absolute
- [ ] OG image exists (1200x630)
- [ ] Schema Organization + WebSite + TechArticle + Breadcrumb + FAQ
- [ ] No keyword stuffing (density <2%)
- [ ] Internal links 3-5
- [ ] External authoritative links 2-3 (nofollow if needed)
- [ ] Disclaimer above fold + footer
- [ ] Mobile responsive test
- [ ] Added to sitemap.xml
- [ ] Added to blog.html grid + search index
- [ ] _redirects if URL changed
