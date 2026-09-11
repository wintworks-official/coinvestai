# CoinvestAI — Google AdSense & Financial Content Compliance Checklist
**Last Audit:** 2026-09-11 (full re-audit after «يتطلب عناية» warning)  
**Status:** ✅ Compliant — **24 PASS / 0 WARN / 0 FAIL** via `python3 seo/adsense-audit.py`  
**Report:** `seo/adsense-fix-report-2026-09-11.md` (full before/after)

## 0. Automated Audit Gate (run before every deploy)
```bash
python3 seo/adsense-audit.py
```
The script must report `FAIL 0` and `WARN 0`. It checks 23 policy areas across all HTML
files and prints the offending filename for any failure. Do not push while it fails.

**Current status (2026-09-11):**

| Area | Result |
|---|---|
| Fake/placeholder `ad-slot` IDs | ✅ none |
| Manual `<ins>` ad units (Auto Ads strategy) | ✅ none |
| Exactly one `adsbygoogle.js` loader per indexable page | ✅ 64/64 |
| `google-adsense-account` meta | ✅ all indexable pages |
| `ads.txt` | ✅ correct pub ID, DIRECT |
| Broken internal links (incl. JSON-LD URLs) | ✅ none |
| Cloudflare scrape artifacts | ✅ none |
| Consent Mode v2 default-deny | ✅ all indexable pages |
| Cookie banner + non-personalized-ads fallback | ✅ all indexable pages |
| HTML tag balance (36 tag types, 68 files) | ✅ OK |
| Thin content (<500 words) | ✅ none |
| `<h1>` present | ✅ all |
| `canonical` present | ✅ all |
| Meta description 110–320 chars | ✅ all |
| Title 25–120 chars | ✅ all |
| Disclaimer / disclosure language | ✅ all |
| Prohibited get-rich-quick phrasing (12 patterns) | ✅ none |
| JSON-LD parses | ✅ all blocks |
| `sitemap.xml` matches disk | ✅ 64 URLs |
| Required trust/legal pages (9) | ✅ all present |
| Privacy policy covers advertising & cookies | ✅ |
| 404 page: no ad code, `noindex` | ✅ |
| `og:image` / `twitter:image` files exist on disk | ✅ all resolve |

---

## 1. المحتوى المحظور الذي تم تطهيره
تم فحص جميع ملفات HTML بحثًا عن عبارات تنتهك سياسات المحتوى المالي:

### عبارات تم البحث عنها:
- `guaranteed profit` / `أرباح مضمونة`
- `get rich quick` / `الثراء السريع`
- `make money fast` / `earn $X per day guaranteed`
- `100% win rate` / `risk-free profit`
- `financial advice` بدون إخلاء مسؤولية

### النتائج:
- **لا توجد عبارات ترويجية محظورة.** جميع استخدامات كلمة `guaranteed` موجودة في سياق تحذيري:
  - مثال: `Any platform claiming "95% win rates" or "zero-risk automated income" is deceptive.`
  - مثال: `No. Any platform or vendor claiming guaranteed returns is misleading you.`
- عبارة `risk-free` وجدت مرتين فقط في سياق **paper trading simulation**:
  - `Paper trading mode lets you test strategies risk-free` → تم تحسينها إلى `risk-free simulation environment` لتوضيح أنها بيئة تجريبية وليست ربح بدون مخاطرة.

## 2. تحويل النبرة إلى تقني/تحليلي تعليمي
### المبادئ المطبقة:
1. **لا وعود أرباح:** جميع المقالات تتحدث عن `statistical probabilities` وليس `guaranteed predictions`.
2. **لغة تقنية:** استخدام مصطلحات مثل `algorithmic analysis`, `quantitative research`, `data pipelines`, `backtesting limitations`.
3. **إخلاء مسؤولية في كل مقال:**
   ```html
   <div class="disclaimer-box">
     <strong>Educational Disclosure:</strong> Content is for educational and research purposes only. Not financial advice...
   </div>
   ```

## 3. صفحات السياسات الأساسية — موجودة ومحدثة
| الصفحة | الرابط | الحالة |
|--------|--------|--------|
| Privacy Policy | /privacy-policy.html | ✅ موجودة، GDPR/CCPA |
| Terms of Service | /terms.html | ✅ موجودة |
| Disclaimer / Risk Notice | /disclaimer.html | ✅ مفصلة، CFTC Rule 4.41 |
| Cookie Policy | /cookie-policy.html | ✅ مع Consent Mode v2 |
| Editorial Guidelines | /editorial-guidelines.html | ✅ E-E-A-T |
| Review Methodology | /review-methodology.html | ✅ 7-factor scoring |
| Contact | /contact.html | ✅ |
| ads.txt | /ads.txt | ✅ `google.com, pub-7088247829787060, DIRECT` |

## 4. متطلبات AdSense الإضافية

### سياسة الإعلانات (Auto Ads حصراً — لا وحدات يدوية)
- ❌ **لا تضع `<ins class="adsbygoogle" data-ad-slot="...">` يدوياً.** جميع الوحدات اليدوية حُذفت
  في 2026-09-11 لأن أرقام `ad-slot` كانت وهمية. إن أردت وحدات يدوية لاحقاً، أنشئها من
  **AdSense → Ads → Ad units → Get code** وانسخ الرقم الحقيقي — **لا تخترع أرقاماً أبداً**.
- ✅ محمّل واحد فقط في كل صفحة، مع معرّف الناشر كوسيط استعلام:
  ```html
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7088247829787060" crossorigin="anonymous"></script>
  ```
- ✅ `<meta name="google-adsense-account" content="ca-pub-7088247829787060">` في كل صفحة قابلة للفهرسة.
- ✅ **Auto Ads مفعّل في اللوحة** — بدون تشغيله لن تظهر إعلانات، لأن الوحدات اليدوية لم تعد موجودة.
- ❌ **لا تفعّل الإعلانات ببوابات تفاعل المستخدم** (scroll / mousemove / setTimeout). هذا
  «تسليم غير متسق للمحتوى» (cloaking): بوت جوجل لا يمرّر الصفحة ولا يمرّر الفأرة، فيرى محتوى
  بلا إعلانات بينما يرى المستخدم إعلانات. حُذف هذا النمط من `blog.html` في 2026-09-11.
- ✅ **Ad labeling:** عند إضافة أي وحدة يدوية مستقبلاً، يجب أن تبقى داخل
  `<div class="ad-slot"><div class="ad-label">Advertisement</div>…` — **لا تُظهر تسمية
  «Advertisement» فوق صندوق فارغ** (مخالفة صريحة لسياسة Ad placement).

### الموافقة والخصوصية
- **Consent Mode v2** في كل الصفحات القابلة للفهرسة (64)، بالرفض الافتراضي و`region:['EEA','GB','CH']`.
- **Non-personalized ads fallback:** `requestNonPersonalizedAds=1` عند رفض الكوكيز.
- **بانر كوكيز بأزرار Accept/Reject** في كل صفحة قابلة للفهرسة. الصفحات الـ14 التي كان لها
  بانر أصلي (`.consent-banner`) أُبقيت كما هي — **لا تُضف بانراً ثانياً لها.**
- **No ad on 404 / noindex pages:** `404.html` وصفحتا إعادة التوجيه بلا أي كود إعلاني وتتبع.

## 5. قواعد النشر (طبقها على كل محتوى جديد)

قبل النشر، شغّل:
```bash
python3 seo/adsense-audit.py        # يجب: FAIL 0 · WARN 0
```

**قواعد صارمة:**
1. لا وعود أرباح — `statistical probabilities` وليس `guaranteed predictions`.
2. إخلاء مسؤولية **فوق الطية** في كل مقال، بصيغة مخصّصة للموضوع (لا نسخة لصق).
3. لا تستخدم عبارات مثل `best way to get rich` في Title Tags.
4. `<title>` بين 25-120 حرفاً؛ `<meta description>` بين 110-320 حرفاً.
5. **كل رابط في البطاقات يجب أن يشير إلى ملف موجود فعلاً.** إضافة بطاقة لمقال غير مكتوب
   هي المخالفة التي سببت «يتطلب عناية» — لا تكرر ذلك.
6. عند إضافة مقال جديد، حدّث معاً: `blog.html` (بطاقة + ItemList) · `index.html` (بحث + عدّادات)
   · المحور المناسب · `sitemap.xml` · العدّادات المعلنة في `about.html`.
7. `sitemap.xml` يُولَّد من القرص لا يدوياً — أي ملف `noindex` مستبعد تلقائياً.
8. **العدّادات المعلنة يجب أن تطابق الواقع.** أي رقم («34 Articles», «11 Tools») يُدقَّق آلياً.
9. **لا تحفظ صفحات من المتصفح وتودعها.** آثار Cloudflare (`__CF$cv$params`، `data-cfemail`،
   iframe مخفي) تسبب 404 على غير Cloudflare وتبدو كبصمات برمجيات غير مرغوب فيها.
10. FAQPage JSON-LD يجب أن يطابق نص `<details>` المرئي حرفياً (شرط جوجل).

## 6. ملخص الامتثال
CoinvestAI يلتزم بـ:
- Google Publisher Policies (Financial content)
- AdSense Program Policies (ad placement, ad labeling, traffic quality)
- EU User Consent Policy (Consent Mode v2, default-deny)
- E-E-A-T guidelines (author profiles, methodology, testing protocol, primary sources)
- Spam Policies (no scraped artifacts, no invented structured data, no broken-link hubs)

**68 ملف HTML · 64 صفحة قابلة للفهرسة · 34 مقالة · ~70,000 كلمة · 0 روابط مكسورة · 0 وحدات إعلانية غير صالحة**
