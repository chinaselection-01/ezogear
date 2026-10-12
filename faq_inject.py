#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json

BASE = "https://ezogear.com/"
SITE = "EZO Gear"

# 1) hero keyword tagline (after the hero <p>)
hero_tag = ('    <p class="seo-tag">🏭 China cheapest factory &nbsp;·&nbsp; 💰 Direct factory price '
            '— wholesale gaming desks &amp; chairs, OEM/ODM.</p>\n')

# 2) FAQ section + FAQPage JSON-LD, inserted before footer
faq_items = [
    ("Are you a direct factory or a trading company?",
     "We are a China factory-direct supplier (Yiwu shanqing E‑commerce Firm). You get a direct factory price with no trading middlemen — lower cost and faster lead times."),
    ("Are you the cheapest gaming chair factory in China?",
     "As a China cheapest factory for gaming desks and chairs, we keep our direct factory price low through vertical production and OEM/ODM volume. Request a quote to compare against your current supplier."),
    ("What is your minimum order quantity (MOQ)?",
     "400 pcs per desk model. Gaming chairs support flexible mixed-container MOQ. All pricing is quoted on inquiry."),
    ("Do you provide OEM / ODM customization?",
     "Yes. Logo, colorway, fabric and packaging can be customized to your brand and target market."),
    ("Which port do you ship from and what is the trade term?",
     "FOB Ningbo. We ship worldwide for distributors, e-commerce sellers and OEM brands."),
    ("Can I get a public price list?",
     "No public price list — we quote a direct factory price per inquiry so it stays tied to your quantity, model mix and destination. Contact us for FOB pricing and lead time."),
]

faq_html = ['<section class="section soft" id="faq">', '  <div class="wrap">',
            '    <h2>Frequently asked questions</h2>',
            '    <p class="lead">Common questions from distributors and OEM buyers about our direct factory price and supply.</p>',
            '    <div class="faq">']
for q, a in faq_items:
    faq_html.append(f'      <div class="faq-item"><h4>{q}</h4><p>{a}</p></div>')
faq_html += ['    </div>', '  </div>', '</section>']

faq_ld = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faq_items
    ],
}
faq_html.append('<script type="application/ld+json">\n' + json.dumps(faq_ld, ensure_ascii=False, indent=2) + '\n</script>')
faq_block = "\n".join(faq_html) + "\n"

fn = "index.html"
t = open(fn, encoding="utf-8").read()

# inject hero tagline
t = t.replace(
    '    <p>We design and manufacture height-adjustable gaming desks and ergonomic gaming chairs for distributors, e-commerce and OEM brands worldwide. Request a quote — pricing shared on inquiry.</p>\n',
    '    <p>We design and manufacture height-adjustable gaming desks and ergonomic gaming chairs for distributors, e-commerce and OEM brands worldwide. Request a quote — pricing shared on inquiry.</p>\n' + hero_tag,
    1)

# inject FAQ before footer
marker = '<footer class="site-footer">'
assert marker in t, "footer marker missing"
t = t.replace(marker, faq_block + "\n" + marker, 1)

# 3) footer first column: weave keywords
t = t.replace(
    '<p style="font-size:14px;max-width:320px">Zhejiang Yiwu-based manufacturer of gaming desks and chairs. Wholesale, OEM and ODM for global buyers.</p>',
    '<p style="font-size:14px;max-width:340px">China cheapest factory for gaming desks &amp; chairs. Direct factory price, wholesale, OEM and ODM for global buyers. Based in Yiwu, Zhejiang.</p>',
    1)

open(fn, "w", encoding="utf-8").write(t)
print("index FAQ + keywords injected")
