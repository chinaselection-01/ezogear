#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""0-dependency SEO/GEO validator for ezogear.com static site."""
import os, re, json, glob

ROOT = os.getcwd()
errors, warns = [], []

def check(fn):
    html = open(fn, encoding="utf-8").read()
    rel = os.path.relpath(fn, ROOT)
    # 1) unique H1
    h1 = re.findall(r'<h1\b', html)
    if len(h1) != 1:
        errors.append(f"{rel}: found {len(h1)} <h1> (expected 1)")
    # 2) meta description + canonical + og + twitter
    if 'name="description"' not in html:
        errors.append(f"{rel}: missing meta description")
    if 'rel="canonical"' not in html:
        errors.append(f"{rel}: missing canonical")
    if 'property="og:title"' not in html:
        errors.append(f"{rel}: missing og:title")
    if 'name="twitter:title"' not in html:
        errors.append(f"{rel}: missing twitter:title (note: twitter uses name=, not property=)")
    # 3) JSON-LD parseable
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(m)
        except Exception as e:
            errors.append(f"{rel}: JSON-LD parse error: {e}")
    # 4) img alt
    for src, alt in re.findall(r'<img[^>]+src="([^"]+)"[^>]*?alt="([^"]*)"', html):
        if alt.strip() == "":
            warns.append(f"{rel}: <img src={src}> has empty alt")
    # 5) broken local images
    for src in re.findall(r'<img[^>]+src="([^"]+)"', html):
        if src.startswith("http") or src.startswith("data:"):
            continue
        if not os.path.exists(src):
            errors.append(f"{rel}: broken image {src}")
    # 6) internal link reachable
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http", "mailto:", "tel:", "#")):
            continue
        target = href.split("#")[0]
        if target == "":
            continue
        if not os.path.exists(target):
            errors.append(f"{rel}: broken internal link {href}")

for fn in sorted(glob.glob("*.html")):
    check(fn)

print(f"Validated {len(glob.glob('*.html'))} HTML pages.")
print(f"ERRORS: {len(errors)}")
for e in errors:
    print("  ✗", e)
print(f"WARNINGS: {len(warns)}")
for w in warns[:10]:
    print("  ⚠", w)
print("RESULT:", "PASS ✅" if not errors else "FAIL ❌")
