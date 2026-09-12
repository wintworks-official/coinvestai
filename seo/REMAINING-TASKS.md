# المهام المتبقية — coinvestai.com («يتطلب عناية» من AdSense)

**التاريخ:** 2026-09-12
**الفرع المنفِّذ:** `arena/01a095a8-coinvestai` → PR إلى `main`
**المرجع:** `seo/adsense-fix-report-2026-09-11.md` (تقرير الإصلاح الكامل، المدمج في `main` عبر PR #2)
**بوابة النشر:** `python3 seo/adsense-audit.py` → `PASS 24 · WARN 0 · FAIL 0`

> **قاعدة هذا الملف:** البنود الثلاثة أدناه **«لا يتغير»** — صيغت في جلسة سابقة واستُقرّ عليها،
> ولا تُعاد صياغتها عند كل جلسة. التنفيذ هو ما يتغيّر، لا البند نفسه.
> أي تعديل على نص بند يتطلب قرارًا صريحًا من صاحب الموقع، لا اجتهادًا من الجلسة.

---

## البند 1 — نشر التغييرات وفتح PR إلى `main` «لا يتغير»

**من ينفّذه:** الجلسة (لها وصول GitHub).
**الحالة:** ⏳ يُنفَّذ في هذه الجلسة.

```bash
git push origin arena/01a095a8-coinvestai
gh pr create --base main --head arena/01a095a8-coinvestai
```

ثم **ادمج** — «الموقع الحي هو ما يفحصه جوجل، لا الفرع.» أي طلب مراجعة على فرع غير منشور
يُسجَّل كإخفاق جديد، لأن المراجع يزور `coinvestai.com` لا الفرع.

**شرط الدمج:** `python3 seo/adsense-audit.py` يُرجع `PASS 24 · WARN 0 · FAIL 0`. إن فشل أي بند،
لا يُدمج — البوابة قبل النشر، وليست بعده.

---

## البند 2 — تفعيل Auto Ads «لا يتغير»

**من ينفّذه:** صاحب الموقع في لوحة AdSense. **بعد** دمج البند 1.
**الحالة:** ⬜ لم يُنفَّذ.

AdSense → **Ads** → اختر `coinvestai.com` → **Auto ads: ON** → Save.

هذا البند **إلزامي وليس اختياريًا**: كل الوحدات اليدوية الـ71 حُذفت لأنها كانت بأرقام `ad-slot`
مخترعة، فـAuto Ads صار المصدر الوحيد للإعلانات. بدون تشغيله لن تظهر إعلانات إطلاقًا،
وسيبدو الموقع للمراجع بلا إعلانات رغم وجود المحمّل.

> ⚠️ **لا تُضف وحدة يدوية واحدة.** إن أردت وحدات يدوية لاحقًا: **Ads → Ad units → Get code**،
> انسخ الرقم الحقيقي (10 أرقام غير متسلسلة، يبدأ عادةً بـ`8` أو `9`)، ثم ألصق الكتلة.
> اختراع رقم — حتى لو بدا صالحًا — هو السبب الجذري الأصلي لحالة «يتطلب عناية».

---

## البند 3 — طلب إعادة الزحف وإعادة المراجعة «لا يتغير»

**من ينفّذه:** صاحب الموقع. **بعد** دمج البند 1.
**الحالة:** ⬜ لم يُنفَّذ.

### 3.1 عشرة روابط للصق في Search Console

Google Search Console → **URL Inspection** → اطلب الفهرسة لكل رابط:

```text
https://coinvestai.com/
https://coinvestai.com/blog.html
https://coinvestai.com/guides.html
https://coinvestai.com/news.html
https://coinvestai.com/sitemap.xml
https://coinvestai.com/blog-ai-regulatory-compliance-finance.html
https://coinvestai.com/blog-backtesting-ai-trading-strategies.html
https://coinvestai.com/blog-ai-fraud-detection-banking.html
https://coinvestai.com/blog-smart-contract-security-ai.html
https://coinvestai.com/blog-ai-credit-underwriting.html
```

ثم **Sitemaps** → أرسل `sitemap.xml` مجددًا (تغيّر من 49 إلى 64 URL).

### 3.2 في لوحة AdSense

- **Sites → coinvestai.com:** إن ظهر زر **Request review** / **I fixed my site** فاضغطه.
  إن لم يظهر، أعد إرسال الموقع من **Sites → Add site**.
- **Policy center:** إن كانت هناك مخالفة مسجّلة باسمها، أرسلها لمعالجتها تحديدًا.
- تحقّق: **ads.txt = Authorized** · **Site verification = Verified**.

### 3.3 نص المراجعة — 938 حرفًا، جاهز للصق

يُستخدم في حقل الطلب عند الضغط على **Request review**، أو كرسالة appeal:

```text
Hello AdSense team, the "Needs attention" status on coinvestai.com has been remediated; all fixes are live as of 2026-09-11. 1) 71 placeholder ad units with invented ad-slot IDs were removed - the site now runs Auto Ads with one adsbygoogle.js loader per indexable page. 2) Nine articles promoted across guides, news, crypto-ai, fintech and the homepage but never written have been published (29,633 words), removing ~30 broken links and every structured-data reference to a missing URL. 3) Cloudflare challenge scripts baked into 14 saved pages were deleted, and the obfuscated email decoded. 4) Consent Mode v2, a cookie banner with accept/reject, and a non-personalized ads fallback now cover all 64 indexable pages. 5) sitemap.xml was regenerated from disk, growing from 49 to 64 URLs, no entry pointing to a missing file. Automated audit: 24 checks passing, 0 warnings, 0 failures. ads.txt is authorized. Please re-review. Thank you.
```

> **مهم:** لا تُرسل هذا النص قبل أن يصبح الموقع الحي محدَّثًا بالفعل (بعد دمج البند 1).

### 3.4 إضافة معلومات الدفع

الرسالة في أعلى لوحة AdSense تطلب أمرين منفصلين، والثاني ليس تقنيًا:
**Payments → Add payment method** (حساب بنكي) + **تحقيق الحد الأدنى للدفع**.
ربط الموقع وحده لا يبدأ الأرباح.

---

## ثوابت دائمة (تفحصها البوابة آليًا)

| الثابت | لماذا |
|--------|-------|
| محمّل `adsbygoogle.js` **واحد** لكل صفحة قابلة للفهرسة | محمّل ثانٍ أو تحميل كسول خلف تفاعل المستخدم = cloaking |
| `404.html` وصفحتا إعادة التوجيه **بلا أي كود إعلاني أو تتبّع** | مطلوب لصفحات `noindex` |
| Consent Mode v2 + بانر بقبول/رفض + `requestNonPersonalizedAds` في **كل** صفحة قابلة للفهرسة | سياسة موافقة مستخدمي الاتحاد الأوروبي |
| لا رقم `ad-slot` إلا منسوخًا من لوحة AdSense | السبب الجذري الأصلي |

**إعادة الفحص ليست فورية:** Googlebot يحتاج أيامًا إلى أسابيع، وAdSense يعيد الفحص تلقائيًا
كل 2-3 أسابيع. لا تُكرَّر الطلبات قبل مرور هذه المدة.
