# -*- coding: utf-8 -*-
"""
CoinvestAI — idempotent social-meta injector (og:* + twitter:*).

Contract (site format, per owner):
  * og:image   comes BEFORE og:site_name
  * twitter:image comes AFTER twitter:description
  * Runs on ANY page without pre-checking (upsert, never duplicate)
  * Idempotent: running twice yields byte-identical output.

What it does, per indexable page:
  1. Preserves every existing og:/twitter:/article: value verbatim.
  2. Fills the gaps with deterministic fallbacks (title/description/canonical/
     JSON-LD dates / per-page image map).
  3. Re-emits the full social block in canonical order, immediately after the
     <link rel="canonical"> line (site convention), one tag per line.
"""
import os, re, glob, sys, json, html as H

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SKIP = {'404.html', 'blog-article-template.html',
        'blog-ai-onchain-crypto-analytics-2026.html',
        'AI-Driven On-Chain Analytics in Crypto Markets (2026).html'}

SITE = 'https://coinvestai.com'
SITE_NAME = 'CoinvestAI'
AUTHOR = 'CoinvestAI Editorial Team'
TW_SITE = '@CoinvestAI_HQ'

# Pages that currently ship NO og:image get one of these (all exist on disk).
IMAGE_MAP = {
    'about.html': 'og-home-2026.jpg',
    'ai-tools.html': 'reviews-og-2026.jpg',
    'ai-tools-claude.html': 'reviews-og-2026.jpg',
    'ai-tools-liquid-coinvest.html': 'reviews-og-2026.jpg',
    'ai-tools-macroaxis.html': 'reviews-og-2026.jpg',
    'ai-tools-manus-ai.html': 'reviews-og-2026.jpg',
    'ai-tools-trade-ideas.html': 'reviews-og-2026.jpg',
    'ai-tools-tradingview.html': 'reviews-og-2026.jpg',
    'ai-tools-trendspider.html': 'reviews-og-2026.jpg',
    'authors-coinvestai-editorial-team.html': 'og-home-2026.jpg',
    'authors.html': 'og-home-2026.jpg',
    'best-ai-trading-platforms-compared-2026.html': 'reviews-og-2026.jpg',
    'blog-ai-crypto-trading-2026.html': 'crypto-ai-og-2026.jpg',
    'blog-ai-crypto-trading-algorithms.html': 'crypto-ai-og-2026.jpg',
    'blog-ai-digital-banking-automation.html': 'fintech-og-2026.jpg',
    'blog-ai-driven-crypto-insights.html': 'crypto-ai-og-2026.jpg',
    'blog-ai-fraud-detection-finance.html': 'fintech-og-2026.jpg',
    'blog-ai-native-financial-services.html': 'fintech-og-2026.jpg',
    'blog-ai-risk-management-defi-2026.html': 'crypto-ai-og-2026.jpg',
    'blog-blockchain-data-analytics-ai.html': 'crypto-ai-og-2026.jpg',
    'blog-deepseek-ai-finance-2026.html': 'deepseek-review-2026.jpg',
    'blog-draftbit-review-2026.html': 'reviews-og-2026.jpg',
    'blog-generative-ai-corporate-financial-auditing.html': 'fintech-og-2026.jpg',
    'blog-ml-crypto-market-analysis.html': 'crypto-ai-og-2026.jpg',
    'blog-ml-portfolio-management.html': 'guides-og-2026.jpg',
    'blog-nlp-financial-document-analysis.html': 'guides-og-2026.jpg',
    'blog-openai-gpt-5-6-cyber-launch.html': 'news-og-2026.jpg',
    'blog-psychology-long-term-investing.html': 'guides-og-2026.jpg',
    'blog-robo-advisors-ai-investment.html': 'fintech-og-2026.jpg',
    'blog-stablecoins-business-ledgers.html': 'crypto-ai-og-2026.jpg',
    'contact.html': 'og-home-2026.jpg',
    'cookie-policy.html': 'og-home-2026.jpg',
    'editorial-guidelines.html': 'og-home-2026.jpg',
    'magnifi-ai-review-2026.html': 'reviews-og-2026.jpg',
    'privacy-policy.html': 'og-home-2026.jpg',
    'review-methodology.html': 'og-home-2026.jpg',
    'terms.html': 'og-home-2026.jpg',
}

# True pixel dimensions of every share image on disk (measured from files).
DIMS = {
    'ai-credit-underwriting-2026.jpg': (1200, 630),
    'ai-fraud-detection-banking-2026.jpg': (1200, 630),
    'ai-investment-research-2026.jpg': (1408, 768),
    'ai-regulatory-compliance-finance-2026.jpg': (1200, 630),
    'alphasense-review-2026.jpg': (1408, 768),
    'backtesting-ai-trading-strategies-2026.jpg': (1200, 630),
    'beginners-guide-ai-investing-2026.jpg': (1408, 768),
    'chatgpt-review-2026.jpg': (1408, 768),
    'crypto-ai-og-2026.jpg': (1408, 768),
    'deepseek-review-2026.jpg': (1408, 768),
    'disclaimer-og-2026.jpg': (1536, 1024),
    'evaluate-ai-trading-platforms-2026.jpg': (1408, 768),
    'fintech-og-2026.jpg': (1408, 768),
    'guides-og-2026.jpg': (1408, 768),
    'kavout-review-2026.jpg': (1536, 1024),
    'news-og-2026.jpg': (1408, 768),
    'og-home-2026.jpg': (1408, 768),
    'open-source-financial-ai-qlib-finrl-2026.jpg': (1408, 768),
    'reviews-og-2026.jpg': (1408, 768),
    'smart-contract-security-ai-2026.jpg': (1200, 630),
}

SOCIAL_TAG_RE = re.compile(
    r'<meta\s[^>]*?(?:property="(?:og|article):[^"]*"|name="twitter:[^"]*")[^>]*>')

META_ATTR_RE = re.compile(
    r'<meta\s([^>]*)>')


def attrs(tag_text):
    out = {}
    for m in re.finditer(r'(property|name|content)="([^"]*)"', tag_text):
        out[m.group(1)] = m.group(2)
    return out


def parse_head_meta(head):
    """Return {canonical_key: value} for every social field present."""
    found = {}
    for m in META_ATTR_RE.finditer(head):
        a = attrs(m.group(1))
        key = a.get('property') or a.get('name')
        if key and (key.startswith('og:') or key.startswith('twitter:') or key.startswith('article:')):
            found[key] = a.get('content', '')
    return found


def strip_site_suffix(title):
    t = title.strip()
    t2 = re.sub(r'\s*[—–\-|]\s*CoinvestAI\s*(?:20\d{2})?\s*$', '', t)
    if t2.strip():
        return t2.strip()
    return t


def clean_section(cat):
    s = re.sub(r'<[^>]+>', '', cat)
    s = re.sub(r'^[^\w\s&()-]+', '', s)  # drop leading emoji/symbols
    return s.strip()


def is_article(filename, existing_type):
    if existing_type:
        return existing_type == 'article'
    if filename.startswith('blog-') and filename != 'blog.html':
        return True
    if filename.startswith('ai-tools-'):
        return True
    if filename in ('best-ai-trading-platforms-compared-2026.html', 'magnifi-ai-review-2026.html'):
        return True
    return False


def build_block(fname, found, title, meta_desc, canon):
    ogt = found.get('og:title') or strip_site_suffix(title)
    ogd = found.get('og:description') or meta_desc
    ogu = found.get('og:url') or canon or (SITE + '/' + fname)
    og_type = found.get('og:type') or ('article' if is_article(fname, None) else 'website')
    oimg = found.get('og:image') or (SITE + '/images/' + IMAGE_MAP[fname] if fname in IMAGE_MAP else None)

    img_name = oimg.rsplit('/', 1)[-1] if oimg else ''
    w = found.get('og:image:width') or (str(DIMS[img_name][0]) if img_name in DIMS else None)
    h = found.get('og:image:height') or (str(DIMS[img_name][1]) if img_name in DIMS else None)
    alt = found.get('og:image:alt') or ogt
    site_name = found.get('og:site_name') or SITE_NAME

    tcard = found.get('twitter:card') or 'summary_large_image'
    tt = found.get('twitter:title') or ogt
    td = found.get('twitter:description') or ogd
    timg = found.get('twitter:image') or oimg
    tsite = found.get('twitter:site') or TW_SITE

    lines = []
    lines.append('<meta property="og:type" content="%s">' % og_type)
    lines.append('<meta property="og:title" content="%s">' % ogt)
    lines.append('<meta property="og:description" content="%s">' % ogd)
    lines.append('<meta property="og:url" content="%s">' % ogu)
    if oimg:
        lines.append('<meta property="og:image" content="%s">' % oimg)
        if w:
            lines.append('<meta property="og:image:width" content="%s">' % w)
        if h:
            lines.append('<meta property="og:image:height" content="%s">' % h)
        if alt:
            lines.append('<meta property="og:image:alt" content="%s">' % alt)
    lines.append('<meta property="og:site_name" content="%s">' % site_name)

    if og_type == 'article':
        pub = found.get('article:published_time')
        mod = found.get('article:modified_time')
        sec = found.get('article:section')
        aut = found.get('article:author') or AUTHOR
        if pub:
            lines.append('<meta property="article:published_time" content="%s">' % pub)
        if mod:
            lines.append('<meta property="article:modified_time" content="%s">' % mod)
        if sec:
            lines.append('<meta property="article:section" content="%s">' % sec)
        lines.append('<meta property="article:author" content="%s">' % aut)

    lines.append('<meta name="twitter:card" content="%s">' % tcard)
    lines.append('<meta name="twitter:title" content="%s">' % tt)
    lines.append('<meta name="twitter:description" content="%s">' % td)
    if timg:
        lines.append('<meta name="twitter:image" content="%s">' % timg)
    lines.append('<meta name="twitter:site" content="%s">' % tsite)
    return lines


def extract_head_meta_values(raw):
    """title, meta description, canonical, JSON-LD dates, cat-tag."""
    title_m = re.search(r'(?is)<title[^>]*>(.*?)</title>', raw)
    title = title_m.group(1).strip() if title_m else ''  # keep HTML-escaped
    desc_m = re.search(r'(?is)<meta\s[^>]*name="description"\s[^>]*content="([^"]*)"', raw)
    desc = desc_m.group(1) if desc_m else ''
    canon_m = re.search(r'<link\s[^>]*rel="canonical"\s[^>]*href="([^"]*)"', raw)
    canon = canon_m.group(1) if canon_m else ''
    dp = re.search(r'"datePublished"\s*:\s*"([^"]+)"', raw)
    dm = re.search(r'"dateModified"\s*:\s*"([^"]+)"', raw)
    cat_m = re.search(r'(?is)class="cat-tag"[^>]*>(.*?)<', raw)
    cat = clean_section(cat_m.group(1)) if cat_m else ''
    return title, desc, canon, (dp.group(1) if dp else None), (dm.group(1) if dm else None), cat


def collapse_blanks(lines):
    out = []
    blank = False
    for l in lines:
        if not l.strip():
            if not blank:
                out.append(l)
            blank = True
        else:
            out.append(l)
            blank = False
    return out


def process(fname):
    raw = open(fname, encoding='utf-8').read()
    title, desc, canon, dp, dm, cat = extract_head_meta_values(raw)

    found = parse_head_meta(raw)
    # JSON-LD dates feed article:published/modified when the page lacks them
    if 'article:published_time' not in found and dp:
        found['article:published_time'] = dp
    if 'article:modified_time' not in found and dm:
        found['article:modified_time'] = dm
    if 'article:section' not in found and cat and cat != '$$$CATEGORY$$$':
        found['article:section'] = cat

    block = build_block(fname, found, title, desc, canon)

    lines = raw.split('\n')
    head_end = next((i for i, l in enumerate(lines) if '</head>' in l), len(lines))
    head = lines[:head_end]
    tail = lines[head_end:]

    new_head = []
    for l in head:
        had_social = SOCIAL_TAG_RE.search(l)
        stripped = SOCIAL_TAG_RE.sub('', l)
        if had_social:
            # a line that was only social tags disappears entirely;
            # a mixed line keeps its non-social remainder
            if stripped.strip():
                new_head.append(stripped)
        else:
            new_head.append(l)  # untouched (blank lines preserved)

    # insert canonical block after the canonical link, with a single blank
    # line on each side, then collapse blank runs once -> true fixed point.
    canon_idx = next((i for i, l in enumerate(new_head) if 'rel="canonical"' in l), None)
    if canon_idx is not None:
        new_head[canon_idx + 1:canon_idx + 1] = [''] + block + ['']
    else:
        new_head.extend([''] + block + [''])
    out = collapse_blanks(new_head)

    result = '\n'.join(out + tail)
    return result, raw


def main():
    files = [f for f in sorted(glob.glob('*.html')) if f not in SKIP]
    changed, identical = [], []
    for f in files:
        result, raw = process(f)
        if result != raw:
            open(f, 'w', encoding='utf-8').write(result)
            changed.append(f)
        else:
            identical.append(f)
    print('processed %d indexable pages' % len(files))
    print('changed : %d' % len(changed))
    print('identical (no-op): %d' % len(identical))
    for f in changed:
        print('  + ' + f)


if __name__ == '__main__':
    main()
