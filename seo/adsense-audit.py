# -*- coding: utf-8 -*-
"""CoinvestAI — AdSense readiness audit. Re-run any time."""
import os, re, glob, json, html as H
from urllib.parse import urlparse, unquote

os.chdir('/home/user/coinvestai')
files = sorted(glob.glob('*.html'))
SKIP = {'404.html', 'blog-article-template.html', 'blog-ai-onchain-crypto-analytics-2026.html',
        'AI-Driven On-Chain Analytics in Crypto Markets (2026).html'}
indexable = [f for f in files if f not in SKIP]

assets = set(os.listdir('.'))
for d in ['css', 'images', 'includes', 'partials', 'seo']:
    if os.path.isdir(d):
        for f in os.listdir(d):
            assets.add(d + '/' + f)

ok, warn, fail = [], [], []

# ---- 1. invalid ad units -------------------------------------------------
fake = [f for f in files if re.search(r'data-ad-slot="(1234567890|0987654321|9876543210|1122334455|REPLACE[^"]*)"', open(f, encoding='utf-8', errors='replace').read())]
ins = [f for f in files if '<ins class="adsbygoogle"' in open(f, encoding='utf-8', errors='replace').read()]
(ok if not fake else fail).append('Fake/placeholder ad-slot IDs: %s' % (fake or 'none'))
(ok if not ins else fail).append('Manual <ins> ad units (Auto Ads strategy): %s' % (ins or 'none'))

# ---- 2. exactly one AdSense loader + verification meta -------------------
multi, nometa = [], []
for f in indexable:
    h = open(f, encoding='utf-8').read()
    if h.count('pagead/js/adsbygoogle.js') != 1: multi.append(f)
    if h.count('google-adsense-account') != 1: nometa.append(f)
(ok if not multi else fail).append('Exactly one adsbygoogle.js loader per indexable page: %s' % (multi or 'OK (%d pages)' % len(indexable)))
(ok if not nometa else fail).append('google-adsense-account meta present: %s' % (nometa or 'OK'))

# ---- 3. ads.txt ----------------------------------------------------------
t = open('ads.txt').read().strip()
(ok if t.startswith('google.com, pub-') and 'DIRECT' in t else fail).append('ads.txt: %r' % t)

# ---- 4. broken internal links -------------------------------------------
broken = []
for f in files:
    h = open(f, encoding='utf-8').read()
    hs = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)   # drop JS + CSS
    hs = re.sub(r'(?i)placeholder="[^"]*"', '', hs)                # drop form placeholders
    for m in re.finditer(r'<a\b[^>]*href="([^"]*)"', hs, re.I):
        href = m.group(1).strip()
        if href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'http')): continue
        p = unquote(urlparse(href).path).lstrip('/')
        if p and p not in assets and p + '.html' not in assets: broken.append((f, href))
    h_np = re.sub(r'(?i)placeholder="[^"]*"', '', h)               # drop form placeholders
    for m in re.finditer(r'"https://coinvestai\.com/([^"#?\s]+)"', h_np):
        p = m.group(1)
        if p.endswith(('.xml', '.txt', '.png', '.jpg', '.ico', '.svg')): continue
        if '$' in p or '{' in p: continue                                  # template tokens
        if p not in assets and p + '.html' not in assets and p != '': broken.append((f, '[schema] ' + p))
    for m in re.finditer(r'<a\b[^>]*href="(https://coinvestai\.com/[^"#?\s]+)"', hs, re.I):
        p = unquote(urlparse(m.group(1)).path).lstrip('/')
        if p and p not in assets and p + '.html' not in assets: broken.append((f, p))
(ok if not broken else fail).append('Broken internal links: %s' % (broken or 'none'))

# ---- 5. scraped third-party artifacts -----------------------------------
arts = [f for f in files if re.search(r'cdn-cgi|__cf_email__|data-cfasync|challenge-platform', open(f, encoding='utf-8').read())]
(ok if not arts else fail).append('Cloudflare scrape artifacts baked into HTML: %s' % (arts or 'none'))

# ---- 6. consent ----------------------------------------------------------
noconsent, nobanner = [], []
for f in indexable:
    h = open(f, encoding='utf-8').read()
    if not re.search(r"gtag\('consent',\s*'default'|gtag\('consent','default'", h): noconsent.append(f)
    if 'cvaConsentBanner' not in h and 'consentBanner' not in h: nobanner.append(f)
    if 'requestNonPersonalizedAds' not in h: nobanner.append(f + ' (no NPA fallback)')
(ok if not noconsent else fail).append('Consent Mode v2 default block: %s' % (noconsent or 'OK'))
(ok if not nobanner else fail).append('Cookie banner + non-personalized-ads fallback: %s' % (nobanner or 'OK'))

# ---- 7. HTML validity ----------------------------------------------------
tagissues = []
for f in files:
    h = re.sub(r'(?s)<!--.*?-->', '', open(f, encoding='utf-8').read())
    for t_ in ['html','head','body','main','script','style','header','footer','article','section',
               'table','thead','tbody','tr','td','th','div','nav','ul','ol','li','p','h1','h2','h3',
               'h4','a','span','button','details','summary','aside']:
        o = len(re.findall(r'<%s(?=[\s>])' % t_, h, re.I)); c = len(re.findall(r'</%s>' % t_, h, re.I))
        if o != c: tagissues.append('%s <%s> %d/%d' % (f, t_, o, c))
(ok if not tagissues else fail).append('HTML tag balance: %s' % (tagissues or 'OK'))

# ---- 8. per-page SEO / content quality ----------------------------------
thin, noh1, nocanon, nodesc, nodiscl, badtitle = [], [], [], [], [], []
DISCL = re.compile(r'(?i)disclaimer|disclosure|not financial|does not constitute|educational purposes|informational purposes')
for f in indexable:
    raw = open(f, encoding='utf-8').read()
    txt = H.unescape(raw)
    b = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', '', raw)
    words = len(re.sub(r'\s+', ' ', re.sub(r'(?s)<[^>]+>', ' ', b)).split())
    if words < 500: thin.append('%s (%dw)' % (f, words))
    if not re.search(r'(?i)<h1', raw): noh1.append(f)
    if not re.search(r'(?i)rel=["\']canonical["\']', raw): nocanon.append(f)
    m = re.search(r'(?is)<meta[^>]+name=["\']description["\'][^>]*content="([^"]*)"', raw) or \
        re.search(r"(?is)<meta[^>]+name=[\"']description[\"'][^>]*content='([^']*)'", raw)
    d = m.group(1).strip() if m else ''
    if not (110 <= len(d) <= 320): nodesc.append('%s (%d chars)' % (f, len(d)))
    if not DISCL.search(txt): nodiscl.append(f)
    tm = re.search(r'(?is)<title[^>]*>(.*?)</title>', raw)
    tl = len(tm.group(1).strip()) if tm else 0
    if not (25 <= tl <= 120): badtitle.append('%s (%d chars)' % (f, tl))
(ok if not thin else warn).append('Thin content (<500 words): %s' % (thin or 'none'))
(ok if not noh1 else fail).append('Missing <h1>: %s' % (noh1 or 'none'))
(ok if not nocanon else fail).append('Missing canonical: %s' % (nocanon or 'none'))
(ok if not nodesc else warn).append('Meta description length 110-320: %s' % (nodesc or 'OK'))
(ok if not nodiscl else warn).append('Disclaimer / disclosure language: %s' % (nodiscl or 'OK'))
(ok if not badtitle else warn).append('Title length 25-120: %s' % (badtitle or 'OK'))

# ---- 9. prohibited financial language ------------------------------------
BAD = re.compile(r'(?i)\b(guaranteed (profit|returns?|income|wins?)|get rich quick|100% (win rate|guaranteed|profit|safe)|'
                 r'risk[- ]free (profit|income|returns|money|trading)|double your (money|investment)|'
                 r'no[- ]loss|never lose money|surefire|foolproof (profit|system|strategy)|'
                 r'make \$?\d+ (a|per) day (guaranteed|easy))\b')
hits = []
for f in files:
    txt = H.unescape(re.sub(r'(?s)<[^>]+>', ' ', open(f, encoding='utf-8', errors='replace').read()))
    for m in BAD.finditer(txt):
        ctx = txt[max(0, m.start()-900):m.end()+130].replace('\n', ' ')
        low = ctx.lower()
        # legitimate critical / prohibitive context — not a policy violation
        if any(k in low for k in ['never publish', 'we do not use', 'banned', 'prohibit', 'claiming',
                                  'is misleading', 'is deceptive', 'red flag', 'no claim implies',
                                  'do not use', 'language we do not', 'scam', 'not a defense', 'any multiplier promise', 'loss-prevention guarantees']):
            continue
        hits.append((f, m.group(0), ctx))
(ok if not hits else warn).append('Prohibited get-rich-quick phrasing: %s' % (hits or 'none'))

# ---- 10. JSON-LD parses --------------------------------------------------
badjson = []
for f in files:
    h = open(f, encoding='utf-8').read()
    for i, m in enumerate(re.finditer(r'(?is)<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h)):
        try: json.loads(m.group(1).strip())
        except Exception as e: badjson.append('%s block#%d: %s' % (f, i, e))
(ok if not badjson else fail).append('JSON-LD validity: %s' % (badjson or 'OK'))

# ---- 11. sitemap <-> disk consistency -----------------------------------
sm = open('sitemap.xml').read()
locs = re.findall(r'<loc>(?:https://coinvestai\.com/)([^<]*)</loc>', sm)
sm_files = {l if l else 'index.html' for l in locs}
on_disk = set(indexable)
(ok if sm_files == on_disk else warn).append(
    'Sitemap matches indexable pages: %s' % (
        'OK (%d URLs)' % len(sm_files) if sm_files == on_disk else
        'in sitemap only=%s / on disk only=%s' % (sorted(sm_files - on_disk), sorted(on_disk - sm_files))))

# ---- 12. policy pages ----------------------------------------------------
need = ['privacy-policy.html','terms.html','disclaimer.html','cookie-policy.html',
        'editorial-guidelines.html','review-methodology.html','contact.html','about.html','authors.html']
miss = [p for p in need if not os.path.exists(p)]
(ok if not miss else fail).append('Required trust/legal pages: %s' % (miss or 'all present'))
pp = H.unescape(open('privacy-policy.html').read())
adv = [k for k in ['AdSense','Google','third-party','cookie','advertis'] if k.lower() in pp.lower()]
(ok if len(adv) >= 4 else warn).append('Privacy policy covers advertising/cookies (%s)' % ', '.join(adv))

# ---- 13. 404 must carry no ads -----------------------------------------
h404 = open('404.html').read()
(ok if 'adsbygoogle' not in h404 else fail).append('404 page carries no ad code')
(ok if 'noindex' in h404 else warn).append('404 page is noindex')

print('=' * 78)
print(' COINVESTAI \u2014 ADSENSE READINESS AUDIT')
print('=' * 78)
for label, items in (('PASS', ok), ('WARN', warn), ('FAIL', fail)):
    print('\n--- %s (%d) ---' % (label, len(items)))
    for i in items: print('  ' + ('\u2713 ' if label == 'PASS' else '\u26A0 ' if label == 'WARN' else '\u2717 ') + i)
print('\n' + '=' * 78)
print(' PASS %d   WARN %d   FAIL %d' % (len(ok), len(warn), len(fail)))
print('=' * 78)
