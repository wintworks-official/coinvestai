# CoinvestAI — Google AdSense & Financial Content Compliance Checklist
**Last Audit:** 2026-08-29  
**Status:** ✅ Compliant — Technical/Educational Tone Enforced

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
- **Consent Mode v2** مُطبق في index.html وجميع القوالب الجديدة.
- **Non-personalized ads fallback:** `requestNonPersonalizedAds=1` عند رفض الكوكيز.
- **Ad labeling:** كل وحدة إعلانية داخل `<div class="ad-slot"><div class="ad-label">Advertisement</div>...`
- **No ad on 404 / noindex pages:** صفحات إعادة التوجيه تحتوي `noindex, follow`.

## 5. إجراءات مستقبلية موصى بها
- راجع أي مقال جديد عبر هذا البحث قبل النشر:
  ```bash
  grep -r -i "guaranteed profit\|get rich\|risk-free profit\|100% guaranteed" --include="*.html"
  ```
- حافظ على وجود `Educational & Legal Disclaimer` فوق الطية (above the fold) في كل مقال.
- لا تستخدم عبارات مثل `best way to get rich` في Title Tags.

## 6. ملخص الامتثال
CoinvestAI الآن يلتزم بـ:
- Google Publisher Policies (Financial content)
- AdSense Program Policies
- EU User Consent Policy (Consent Mode v2)
- E-E-A-T guidelines (Author profiles, methodology, references)
