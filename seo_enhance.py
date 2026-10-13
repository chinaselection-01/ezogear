#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GEO + SEO enhancement for ezogear.com (single-brand B2B factory catalog)."""
import os, json, re

BASE = "https://ezogear.com/"
SITE = "EZO Gear"
CO = "Yiwu shanqing E‑commerce Firm"

# ---- per-page SEO metadata ----
PAGES = {
    "index.html": {
        "title": "EZO Gear — China's Cheapest Factory for Gaming Desks & Chairs | Direct Factory Price",
        "desc": "China cheapest factory for gaming desks and chairs. Direct factory price, OEM/ODM, low MOQ 400 pcs. Wholesale gaming tables & ergonomic gaming chairs from Yiwu, Zhejiang.",
    },
    "tables.html": {
        "title": "Wholesale Gaming Desks — China Cheapest Factory | Direct Factory Price | EZO Gear",
        "desc": "Buy gaming desks direct from China's cheapest factory. Electric & manual height-adjustable, fixed and LED corner desks. Direct factory price, MOQ 400, OEM/ODM, FOB Ningbo.",
    },
    "chairs.html": {
        "title": "Wholesale Gaming Chairs — China Cheapest Factory | Direct Factory Price | EZO Gear",
        "desc": "Buy gaming chairs direct from China's cheapest factory. Racing-style and ergonomic mesh chairs. Direct factory price, OEM/ODM, mixed-container MOQ, FOB Ningbo.",
    },
    "contact.html": {
        "title": "Request a Quote — Direct Factory Price | EZO Gear",
        "desc": "Request direct factory price and FOB quote for gaming desks and chairs. China cheapest factory, MOQ 400 pcs, OEM/ODM. Reply within 24h.",
    },
}

def head_block(fn):
    md = PAGES[fn]
    url = BASE if fn == "index.html" else BASE + fn
    return (
        f'<title>{md["title"]}</title>\n'
        f'<meta name="description" content="{md["desc"]}">\n'
        f'<link rel="canonical" href="{url}">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:title" content="{md["title"]}">\n'
        f'<meta property="og:description" content="{md["desc"]}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:site_name" content="{SITE}">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{md["title"]}">\n'
        f'<meta name="twitter:description" content="{md["desc"]}">\n'
    )

def org_jsonld(fn):
    url = BASE if fn == "index.html" else BASE + fn
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": BASE + "#organization",
                "name": CO,
                "url": BASE,
                "logo": BASE + "assets/chairs/GC6111RED/GC6111-BLA-RED-2.jpg",
                "description": ("China cheapest factory for gaming desks and chairs. "
                                "We supply direct factory price wholesale gaming furniture with OEM/ODM, "
                                "low MOQ and FOB Ningbo shipping from Yiwu, Zhejiang."),
                "email": "jojo@EZOGEAR.com",
                "telephone": "+86 15088255784",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Yiwu",
                    "addressRegion": "Zhejiang",
                    "addressCountry": "CN",
                },
                "areaServed": "Worldwide",
                "sameAs": [BASE],
            },
            {
                "@type": "Brand",
                "@id": BASE + "#brand",
                "name": SITE,
                "url": BASE,
                "description": ("Direct factory price gaming desk & chair brand. China cheapest factory for "
                                "wholesale gaming furniture, OEM/ODM."),
                "logo": BASE + "assets/chairs/GC6111RED/GC6111-BLA-RED-2.jpg",
                "sameAs": [BASE],
                "areaServed": "Worldwide",
                "category": "Gaming furniture",
                "mainEntityOfPage": BASE,
            },
            {
                "@type": "WebSite",
                "@id": BASE + "#website",
                "url": BASE,
                "name": SITE,
                "publisher": {"@id": BASE + "#organization"},
                "inLanguage": "en",
            },
        ]
    }
    return json.dumps(data, ensure_ascii=False, indent=2)

# breadcrumb JSON-LD for sub-pages
def crumb_jsonld(fn, label):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": label, "item": BASE + fn},
        ]
    }, ensure_ascii=False, indent=2)

for fn, md in PAGES.items():
    p = fn
    t = open(p, encoding="utf-8").read()
    # 1) replace title + meta description lines
    t = re.sub(r'<title>.*?</title>\s*\n\s*<meta name="description" content=".*?">',
               head_block(fn).rstrip("\n"), t, count=1, flags=re.S)
    # 2) inject JSON-LD after stylesheet link (before </head>)
    ld = ('<script type="application/ld+json">\n' + org_jsonld(fn) + '\n</script>\n')
    if fn in ("tables.html", "chairs.html", "contact.html"):
        label = {"tables.html": "Gaming Tables", "chairs.html": "Gaming Chairs",
                 "contact.html": "Request a Quote"}[fn]
        ld += ('<script type="application/ld+json">\n' + crumb_jsonld(fn, label) + '\n</script>\n')
    t = t.replace('<link rel="stylesheet" href="assets/css/style.css">\n</head>',
                  '<link rel="stylesheet" href="assets/css/style.css">\n' + ld + '</head>', 1)
    open(p, "w", encoding="utf-8").write(t)
    print("SEO head updated:", fn)

print("HEADS DONE")
