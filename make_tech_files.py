#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

BASE = "https://ezogear.com/"

# ---- llms.txt (GEO index for AI engines) ----
llms = f"""# EZO Gear
> China cheapest factory for gaming desks and chairs. Direct factory price, OEM/ODM, low MOQ, FOB Ningbo. Based in Yiwu, Zhejiang, China.

## Products
- Gaming Tables (electric / manual height-adjustable, fixed & LED corner desks): {BASE}tables.html
- Gaming Chairs (racing-style & ergonomic mesh chairs): {BASE}chairs.html

## Pages
- Home: {BASE}
- Gaming Tables catalog: {BASE}tables.html
- Gaming Chairs catalog: {BASE}chairs.html
- Request a Quote: {BASE}contact.html

## Company
- Legal entity: Yiwu shanqing E‑commerce Firm
- Location: Yiwu, Zhejiang, China
- Email: jojo@EZOGEAR.com
- Tel / WhatsApp: 0086 15088255784
- Trade term: FOB Ningbo
- Services: wholesale, OEM, ODM

## Sitemap
{BASE}sitemap.xml
"""
open("llms.txt", "w", encoding="utf-8").write(llms)
print("wrote llms.txt")

# ---- sitemap.xml ----
urls = [
    ("", "weekly", "1.0"),
    ("tables.html", "weekly", "0.9"),
    ("chairs.html", "weekly", "0.9"),
    ("contact.html", "monthly", "0.6"),
]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, freq, pri in urls:
    loc = BASE if path == "" else BASE + path
    sitemap.append(f"  <url>\n    <loc>{loc}</loc>\n    <changefreq>{freq}</changefreq>\n"
                   f"    <priority>{pri}</priority>\n  </url>")
sitemap.append("</urlset>\n")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(sitemap))
print("wrote sitemap.xml")

# ---- robots.txt ----
robots = f"""User-agent: *
Allow: /

Sitemap: {BASE}sitemap.xml
# AI crawlers: structured index at {BASE}llms.txt
"""
open("robots.txt", "w", encoding="utf-8").write(robots)
print("wrote robots.txt")
