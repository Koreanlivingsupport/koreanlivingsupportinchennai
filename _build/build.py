# -*- coding: utf-8 -*-
"""Builds the static site for koreanlivingsupport.com (GitHub Pages)."""
import json, os, html
from urllib.parse import quote
from content import *

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WA = "https://wa.me/917985040232?text="
E = html.escape
WA_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20.5l1.6-5.4A8.4 8.4 0 1 1 21 11.5z"/></svg>'
MAIL_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>'


def wa(msg):
    return WA + quote(msg)


def rel(from_slug, to_slug):
    depth = from_slug.count("/")
    return ("../" * depth) + to_slug if (("../" * depth) + to_slug) else "./"


def asset(from_slug, path):
    return ("../" * from_slug.count("/")) + path


def head(lang, key, title, desc, schema_list):
    slug = SLUGS[lang][key]
    other = "ko" if lang == "en" else "en"
    a = lambda p: asset(slug, p)
    schemas = "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False) for s in schema_list)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE}{slug}">
<link rel="alternate" hreflang="en" href="{SITE}{SLUGS['en'][key]}">
<link rel="alternate" hreflang="ko" href="{SITE}{SLUGS['ko'][key]}">
<link rel="alternate" hreflang="x-default" href="{SITE}{SLUGS['en'][key]}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{SITE}{slug}">
<meta property="og:image" content="{SITE}assets/img/og-image.jpg">
<meta property="og:locale" content="{'ko_KR' if lang == 'ko' else 'en_IN'}">
<meta name="theme-color" content="#12305C">
<link rel="icon" type="image/png" href="{a('favicon.png')}">
<link rel="apple-touch-icon" href="{a('apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{a('assets/css/site.css')}">
{schemas}
</head>
<body>
'''


def header(lang, key):
    u = UI[lang]
    slug = SLUGS[lang][key]
    other = "ko" if lang == "en" else "en"
    links = "".join(
        f'<a href="{rel(slug, SLUGS[lang][k])}"{" aria-current=\"page\"" if k == key else ""}>{E(u["nav"][k])}</a>' for k in ORDER)
    return f'''<a class="skip" href="#main">{E(u["skip"])}</a>
<header class="site-header">
<div class="wrap nav">
<a class="brand" href="{rel(slug, SLUGS[lang]['home'])}">
<img src="{asset(slug, 'assets/img/kls-logo-96.png')}" alt="" width="44" height="44">
<span><b>Korean Living Support</b><small>{E(u["brand_sub"])}</small></span>
</a>
<nav class="nav-links" aria-label="Main">{links}</nav>
<div class="nav-actions">
<a class="lang" href="{rel(slug, SLUGS[other][key])}" hreflang="{other}" lang="{other}" aria-label="{E(u['other_lang_aria'])}">{E(u["other_lang_label"])}</a>
<a class="btn btn-gold nav-wa" href="{wa(u['general_msg'])}">{WA_SVG}<span>{E(u["wa_btn"])}</span></a>
</div>
</div>
<nav class="subnav" aria-label="Services">{links}</nav>
</header>
'''


def cta_footer(lang, key, msg=None):
    u = UI[lang]
    slug = SLUGS[lang][key]
    msg = msg or u["general_msg"]
    svc_links = "".join(f'<a href="{rel(slug, SLUGS[lang][k])}">{E(TILES[lang][k][1])}</a>' for k in ORDER)
    return f'''<section class="cta">
<div class="wrap">
<div class="stack" style="flex:1 1 460px">
<h2>{E(u["cta_title"])}</h2>
<p>{E(u["cta_sub"])}</p>
</div>
<div class="cta-btns">
<a class="btn btn-cobalt" href="{wa(msg)}">{WA_SVG}{E(PHONE_DISPLAY)}</a>
<a class="btn btn-outline-dark" href="mailto:{EMAIL}">{MAIL_SVG}{EMAIL}</a>
</div>
</div>
</section>
<footer class="site-footer">
<div class="wrap">
<div class="foot-grid">
<div>
<b>Korean Living Support</b>
<p>{E(u["address"])}</p>
</div>
<div><b>{E(u["foot_services"])}</b>{svc_links}</div>
<div><b>{E(u["foot_contact"])}</b>
<a href="{wa(u['general_msg'])}">WhatsApp {E(PHONE_DISPLAY)}</a>
<a href="tel:+917985040232">{E(PHONE_DISPLAY)}</a>
<a href="mailto:{EMAIL}">{EMAIL}</a>
</div>
<div><b>{E(u["foot_area"])}</b><p>{E(u["foot_areas"])}</p></div>
</div>
<p class="note">{E(u["concept_note"])}</p>
<div class="foot-bottom">
<span>© 2026 Korean Living Support, Chennai · <a href="{rel(slug, SLUGS[lang]['privacy'])}">{E(u["privacy_link"])}</a></span>
<span class="formerly"><img src="{asset(slug, 'assets/img/mastermind-logo.jpg')}" alt="Mastermind IT Security Solutions logo" width="36" height="36" loading="lazy">{E(u["formerly"])}</span>
</div>
</div>
</footer>
<a class="wa-float" href="{wa(msg)}" aria-label="WhatsApp {E(PHONE_DISPLAY)}">{WA_SVG}</a>
<script src="{asset(slug, 'assets/js/site.js')}" defer></script>
</body>
</html>
'''


def org_schema(lang):
    return {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "@id": SITE + "#business",
        "name": "Korean Living Support", "alternateName": ["KLS", "코리안 리빙 서포트", "Mastermind IT Security Solutions"],
        "url": SITE, "logo": SITE + "assets/img/kls-logo-512.png", "image": SITE + "assets/img/og-image.jpg",
        "telephone": "+91-79850-40232", "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS["street"], "addressLocality": ADDRESS["city"],
                    "postalCode": ADDRESS["zip"], "addressRegion": ADDRESS["region"], "addressCountry": "IN"},
        "areaServed": ["Chennai", "Anna Nagar", "Kilpauk", "Sriperumbudur", "Oragadam", "Irungattukottai"],
        "knowsLanguage": ["ko", "en", "ta"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services for Korean expats and companies",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": SERVICES[k]["en"]["service_name"]}} for k in ORDER]},
    }


def map_svg(h):
    return f'''<svg viewBox="0 0 640 360" role="img" aria-label="{E(h['map_aria'])}" style="width:100%;height:auto;display:block;font-family:'IBM Plex Sans KR',sans-serif">
<path d="M560 0 C548 60 572 120 556 180 C542 240 566 300 552 360 L640 360 L640 0 Z" fill="#E4EFEB"/>
<text x="600" y="60" font-size="13" fill="#2F6B5E" text-anchor="middle">Bay of</text><text x="600" y="76" font-size="13" fill="#2F6B5E" text-anchor="middle">Bengal</text>
<path d="M548 168 C470 172 400 168 330 176 C260 184 190 178 60 186" stroke="#C9D2DC" stroke-width="10" fill="none" stroke-linecap="round"/>
<text x="110" y="214" font-size="12" fill="#6B7787">NH48 → Bengaluru</text>
<path d="M300 178 C292 220 270 250 250 272" stroke="#C9D2DC" stroke-width="6" fill="none" stroke-linecap="round"/>
<ellipse cx="490" cy="150" rx="70" ry="52" fill="rgba(242,167,59,0.14)"/><ellipse cx="225" cy="215" rx="125" ry="88" fill="rgba(47,107,94,0.10)"/>
<circle cx="468" cy="128" r="8" fill="#F2A73B" stroke="#fff" stroke-width="2"/><text x="468" y="108" font-size="14" font-weight="600" fill="#16202E" text-anchor="middle">Anna Nagar</text><text x="468" y="94" font-size="12" fill="#4B5768" text-anchor="middle">안나 나가르</text>
<circle cx="512" cy="160" r="8" fill="#F2A73B" stroke="#fff" stroke-width="2"/><text x="512" y="190" font-size="14" font-weight="600" fill="#16202E" text-anchor="middle">Kilpauk</text><text x="512" y="206" font-size="12" fill="#4B5768" text-anchor="middle">킬파욱</text>
<circle cx="168" cy="180" r="8" fill="#2F6B5E" stroke="#fff" stroke-width="2"/><text x="168" y="160" font-size="14" font-weight="600" fill="#16202E" text-anchor="middle">Sriperumbudur</text><text x="168" y="146" font-size="12" fill="#4B5768" text-anchor="middle">스리페룸부두르</text>
<circle cx="292" cy="176" r="8" fill="#2F6B5E" stroke="#fff" stroke-width="2"/><text x="300" y="156" font-size="14" font-weight="600" fill="#16202E" text-anchor="middle">Irungattukottai</text><text x="300" y="142" font-size="12" fill="#4B5768" text-anchor="middle">이룽가투코타이</text>
<circle cx="250" cy="272" r="8" fill="#2F6B5E" stroke="#fff" stroke-width="2"/><text x="250" y="300" font-size="14" font-weight="600" fill="#16202E" text-anchor="middle">Oragadam</text><text x="250" y="316" font-size="12" fill="#4B5768" text-anchor="middle">오라가담</text>
<text x="490" y="250" font-size="13" fill="#6B7787" text-anchor="middle">{E(h['map_note'])}</text>
</svg>'''


def tiles(lang, slug):
    out = []
    for k in ORDER:
        badge, title, desc, more = TILES[lang][k]
        out.append(f'<a class="tile{" featured" if k == "housing" else ""}" href="{rel(slug, SLUGS[lang][k])}"><span class="badge">{badge}</span><b>{E(title)}</b><span class="d">{E(desc)}</span><span class="more">{E(more)}</span></a>')
    return "".join(out)


def build_home(lang):
    h = HOME[lang]; u = UI[lang]; slug = SLUGS[lang]["home"]
    A = lambda p: asset(slug, p)
    # finder tabs and panels
    tabbtns, panels = [], []
    for i, k in enumerate(ORDER):
        on = i == 0
        tabbtns.append(f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if on else "false"}" tabindex="{0 if on else -1}">{E(h["tabs"][k])}</button>')
    fields = []
    lines = [h["home_intro"]]
    for label, opts, default in h["fields"]:
        chips = "".join(f'<button type="button" class="chip" aria-pressed="{"true" if j == default else "false"}">{E(o)}</button>' for j, o in enumerate(opts))
        fields.append(f'<div data-field data-label="{E(label)}"><div class="field-label">{E(label)}</div><div class="chips">{chips}</div></div>')
        lines.append(f"- {label}: {opts[default]}")
    panels.append(f'''<div class="finder-panel" id="panel-housing" role="tabpanel" aria-labelledby="tab-housing" data-home-finder data-intro="{E(h['home_intro'])}">
{''.join(fields)}
<div class="finder-foot"><a class="btn btn-gold" data-home-link href="{wa(chr(10).join(lines))}">{WA_SVG}{E(h["home_cta"])}</a><small>{E(h["home_note"])}</small></div>
</div>''')
    for k in ORDER[1:]:
        title, cta, msg, items = h["panels"][k]
        lis = "".join(f"<li>{E(x)}</li>" for x in items)
        panels.append(f'''<div class="finder-panel" id="panel-{k}" role="tabpanel" aria-labelledby="tab-{k}" hidden>
<span class="panel-title">{E(title)}</span><ul class="checks">{lis}</ul>
<div class="finder-foot"><a class="btn btn-cobalt" href="{wa(msg)}">{WA_SVG}{E(cta)}</a><a href="{rel(slug, SLUGS[lang][k])}">{E(TILES[lang][k][3])}</a></div>
</div>''')

    types = "".join(f'<div class="type"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in h["types"])
    why = "".join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in h["why"])
    steps = "".join(f'<li><div><b>{E(a)}</b><span>{E(b)}</span></div></li>' for a, b in h["steps"])
    journey = "".join(f'<li><b>{E(a)}</b><span>{E(b)}</span></li>' for a, b in h["journey"])
    corp = "".join(f'<div><span class="ic">{E(t)}</span><div><h3><a href="{rel(slug, SLUGS[lang][link])}" style="text-decoration:none">{E(a)}</a></h3><p>{E(b)}</p></div></div>' for t, a, b, link in h["corp"])
    team = "".join(f'<div class="member"><span class="av" aria-hidden="true">{E(i)}</span><div><b>{E(n)}</b><em>{E(r)}</em><p>{E(d)}</p></div></div>' for i, n, r, d in h["team"])
    road = "".join(f'<li><b>{E(w)}</b>' + "".join(f"<span>{E(x)}</span>" for x in items) + "</li>" for w, items in h["road"])
    trust = "".join(f"<li>{E(t)}</li>" for t in h["trust"])

    body = f'''<main id="main">
<section class="hero">
<img class="hero-bg" src="{A('assets/img/housing.jpg')}" alt="" fetchpriority="high">
<div class="hero-shade"></div>
<span class="tag">{E(u["concept"])}</span>
<div class="wrap hero-inner">
<h1>{E(h["h1"])}</h1>
<p class="lead">{E(h["lead"])}</p>
<div class="finder">
<div class="finder-tabs" role="tablist" aria-label="{E(h['finder_aria'])}">{''.join(tabbtns)}</div>
<div class="finder-card">{''.join(panels)}</div>
</div>
</div>
</section>
<section class="trust" aria-label="Why KLS"><ul>{trust}</ul></section>

<section class="section" id="services"><div class="wrap stack-lg">
<h2 style="max-width:20em">{E(h["svc_title"])}</h2>
<div class="tiles">{tiles(lang, slug)}</div>
</div></section>

<section class="section dark" id="homes"><div class="wrap stack-lg">
<div class="stack" style="max-width:720px"><h2>{E(h["homes_title"])}</h2><p class="lead">{E(h["homes_lead"])}</p>
<a class="btn btn-gold" style="align-self:flex-start" href="{rel(slug, SLUGS[lang]['housing'])}">{E(h["homes_cta"])}</a></div>
<div class="types">{types}</div>
<div class="two">
<div class="stack"><h3 style="font-size:24px">{E(h["why_title"])}</h3><div class="why">{why}</div></div>
<div class="stack"><h3 style="font-size:24px">{E(h["steps_title"])}</h3><ol class="steps">{steps}</ol></div>
</div>
</div></section>

<section class="section" id="areas"><div class="wrap two" style="align-items:center">
<div class="stack" style="flex:1 1 340px"><h2>{E(h["area_title"])}</h2><p class="lead">{E(h["area_lead"])}</p>
<div class="legend"><span><i style="background:#F2A73B"></i>{E(h["area_city"])}</span><span><i style="background:#2F6B5E"></i>{E(h["area_belt"])}</span></div></div>
<div class="mapcard" style="flex:1 1 540px">{map_svg(h)}</div>
</div></section>

<section class="section cobalt"><div class="wrap two" style="align-items:center">
<div style="flex:1 1 340px"><div class="globe"><canvas data-globe role="img" aria-label="{E(h['globe_aria'])}"></canvas></div></div>
<div class="stack" style="flex:1 1 520px;gap:22px"><h2>{E(h["j_title"])}</h2><p class="lead">{E(h["j_lead"])}</p><ol class="journey">{journey}</ol></div>
</div></section>

<section class="section white" id="company"><div class="wrap two">
<div class="stack"><h2>{E(h["c_title"])}</h2><p class="lead">{E(h["c_lead"])}</p>
<div class="photo" style="aspect-ratio:16/10"><img src="{A('assets/img/business-800.jpg')}" alt="{E(h['c_alt'])}" loading="lazy" width="800" height="533"><span class="tag left">{E(u["concept"])}</span></div></div>
<div><div class="rows">{corp}</div>
<a class="btn btn-outline" style="margin-top:18px" href="{wa(h['c_msg'])}">{E(h["c_cta"])}</a></div>
</div></section>

<section class="section"><div class="wrap stack-lg"><h2>{E(h["team_title"])}</h2><div class="team">{team}</div></div></section>

<section class="dark" id="vision" style="background:#0A1A33;color:#F4F6F5">
<div class="vision-hero"><img src="{A('assets/img/vision-office.jpg')}" alt="{E(h['vis_alts'][0])}" loading="lazy">
<div class="wrap"><span class="pill">{E(u["concept"])}</span><h2>{E(h["vis_title"])}</h2><p class="lead" style="color:#CFDAE6">{E(h["vis_lead"])}</p></div></div>
<div class="wrap stack-lg" style="padding-top:24px;padding-bottom:88px">
<ol class="road">{road}</ol>
<div class="gallery">
<div class="photo"><img src="{A('assets/img/vision-team-800.jpg')}" alt="{E(h['vis_alts'][1])}" loading="lazy" width="800" height="533"></div>
<div class="photo"><img src="{A('assets/img/vision-md-800.jpg')}" alt="{E(h['vis_alts'][2])}" loading="lazy" width="800" height="533" style="object-position:center 30%"></div>
</div>
</div>
</section>
</main>
'''
    return head(lang, "home", h["title"], h["desc"], [org_schema(lang)]) + header(lang, "home") + body + cta_footer(lang, "home")


def build_service(lang, key):
    s = SERVICES[key][lang]; u = UI[lang]; slug = SLUGS[lang][key]
    img = SERVICES[key]["img"]
    A = lambda p: asset(slug, p)
    parts = []
    for h2, kind, content in s["sections"]:
        parts.append(f"<h2>{E(h2)}</h2>")
        if kind == "p":
            parts += [f"<p>{E(p)}</p>" for p in content]
        elif kind == "ul":
            parts.append('<ul class="bul">' + "".join(f"<li><strong>{E(a)}</strong> {E(b)}</li>" for a, b in content) + "</ul>")
        elif kind == "steps":
            parts.append('<ol class="steps light">' + "".join(f"<li><div><b>{E(a)}</b><span>{E(b)}</span></div></li>" for a, b in content) + "</ol>")
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in s["faq"])
    related = "".join(
        f'<a class="tile{" featured" if k == "housing" else ""}" href="{rel(slug, SLUGS[lang][k])}"><span class="badge">{TILES[lang][k][0]}</span><b>{E(TILES[lang][k][1])}</b><span class="d">{E(TILES[lang][k][2])}</span></a>'
        for k in ORDER if k != key)
    schemas = [
        {"@context": "https://schema.org", "@type": "Service", "name": s["service_name"], "serviceType": s["service_name"],
         "provider": {"@id": SITE + "#business"}, "areaServed": "Chennai", "url": SITE + slug, "inLanguage": lang},
        {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Korean Living Support", "item": SITE + SLUGS[lang]["home"]},
            {"@type": "ListItem", "position": 2, "name": TILES[lang][key][1], "item": SITE + slug}]},
        org_schema(lang),
    ]
    body = f'''<main id="main">
<section class="page-hero"><div class="wrap">
<div class="txt">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{rel(slug, SLUGS[lang]['home'])}">{E(u["home_crumb"])}</a> / {E(TILES[lang][key][1])}</nav>
<h1>{E(s["h1"])}</h1>
<p class="lead">{E(s["lead"])}</p>
<a class="btn btn-gold" style="align-self:flex-start" href="{wa(s['wa'])}">{WA_SVG}{E(s["cta"])}</a>
</div>
<div class="photo"><img src="{A('assets/img/' + img + '-800.jpg')}" alt="{E(s['alt'])}" width="800" height="533" fetchpriority="high"><span class="tag">{E(u["concept"])}</span></div>
</div></section>
<section class="section white"><div class="wrap"><article class="article">
{''.join(parts)}
<h2>{E(u["faq"])}</h2>
<div class="faq">{faq}</div>
<p style="margin-top:28px"><a class="btn btn-gold" href="{wa(s['wa'])}">{WA_SVG}{E(s["cta"])}</a></p>
</article></div></section>
<section class="section"><div class="wrap stack-lg"><h2>{E(u["related"])}</h2><div class="related">{related}</div></div></section>
</main>
'''
    return head(lang, key, s["title"], s["desc"], schemas) + header(lang, key) + body + cta_footer(lang, key, s["wa"])


def build_privacy(lang):
    p = PRIVACY[lang]; u = UI[lang]; slug = SLUGS[lang]["privacy"]
    ids = {6: ' id="delete"', 7: ' id="contact"'}
    parts = []
    for i, (h, blocks) in enumerate(p["sections"]):
        parts.append(f'<h2{ids.get(i, "")}>{E(h)}</h2>')
        for b in blocks:
            if isinstance(b, list):
                parts.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in b) + "</ul>")
            else:
                parts.append(f"<p>{E(b)}</p>")
        if i == 7:
            parts.append(f'<p><a href="{wa(u["general_msg"])}">WhatsApp {E(PHONE_DISPLAY)}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>')
    body = f'''<main id="main">
<section class="page-hero"><div class="wrap">
<div class="txt">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{rel(slug, SLUGS[lang]['home'])}">{E(u["home_crumb"])}</a> / {E(p["h1"])}</nav>
<h1>{E(p["h1"])}</h1>
<p class="lead">{E(p["lead"])}</p>
<p class="note">{E(p["updated"])}</p>
</div>
</div></section>
<section class="section white"><div class="wrap"><article class="article">
{''.join(parts)}
</article></div></section>
</main>
'''
    return head(lang, "privacy", p["title"], p["desc"], [org_schema(lang)]) + header(lang, "privacy") + body + cta_footer(lang, "privacy")


def write(slug, html_text):
    path = os.path.join(OUT, slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_text)
    return path


pages = []
for lang in ("en", "ko"):
    pages.append(write(SLUGS[lang]["home"], build_home(lang)))
    for k in ORDER:
        pages.append(write(SLUGS[lang][k], build_service(lang, k)))
    pages.append(write(SLUGS[lang]["privacy"], build_privacy(lang)))

# sitemap with hreflang pairs
urls = []
for lang in ("en", "ko"):
    for k in ["home"] + ORDER + ["privacy"]:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{SLUGS[l][k]}"/>' for l in ("en", "ko"))
        urls.append(f"<url><loc>{SITE}{SLUGS[lang][k]}</loc>{alts}<lastmod>2026-10-14</lastmod></url>")
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
    f.write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Korean Living Support</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/css/site.css"></head><body><main class="section"><div class="wrap stack"><h1 style="color:#12305C">Page not found · 페이지를 찾을 수 없습니다</h1><p class="lead">The page may have moved. 페이지가 이동되었을 수 있습니다.</p><p><a class="btn btn-gold" href="/">Home</a> <a class="btn btn-outline" href="/ko/">한국어 홈</a></p></div></main></body></html>')
print("\n".join(os.path.relpath(p, OUT) for p in pages))
