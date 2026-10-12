#!/usr/bin/env python3
"""Generate table placeholder SVGs (white-bg, matching chair photos) + data.js for the EZO Gear catalog.
Prices are intentionally NOT embedded in any rendered output. They live only in back-office data
(the `fob` field) and are never shown on the site (per user instruction: 不显示价格).
"""
import os, json, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
CHAIRS = os.path.join(ROOT, "assets", "chairs")
TABLES_SVG = os.path.join(ROOT, "assets", "tables")
os.makedirs(TABLES_SVG, exist_ok=True)

# --- Table master data (fob kept internally, never displayed) ---
TABLES = [
    {"sku": "GT-14070-E",  "size": "140x70 cm", "adj": "Electric (72-118 cm)", "desc": "Electronic height adjustment for the table", "moq": 400, "fob": 31.6, "accent": "electric"},
    {"sku": "GT-12060-E1", "size": "120x60 cm", "adj": "Electric (72-118 cm)", "desc": "Electronic height adjustment for the table", "moq": 400, "fob": 28.2, "accent": "electric"},
    {"sku": "GT-12060-E2", "size": "120x60 cm", "adj": "Electric (72-118 cm)", "desc": "Electronic height adjustment for the table", "moq": 400, "fob": 26.8, "accent": "electric"},
    {"sku": "GT-12060-M",  "size": "120x60 cm", "adj": "Manual (56-79 cm)",   "desc": "Manual table height adjustment",            "moq": 400, "fob": 25.2, "accent": "manual"},
    {"sku": "GT-10085-F",  "size": "100x85 cm", "adj": "Fixed (85 cm)",        "desc": "No adjustable legs",                       "moq": 400, "fob": 11.6, "accent": "fixed"},
    {"sku": "GT-14060-M",  "size": "140x60 cm", "adj": "Manual (56-79 cm)",   "desc": "Manual table height adjustment",            "moq": 400, "fob": 28.6, "accent": "manual"},
    {"sku": "GT-14060-F",  "size": "140x60 cm", "adj": "Fixed (75 cm)",        "desc": "No adjustable legs",                       "moq": 400, "fob": 27.2, "accent": "fixed"},
    {"sku": "GT-CORNER-LED","size": "Corner",   "adj": "Fixed + LED",          "desc": "Corner desk, LED lights, remote control", "moq": 400, "fob": 29.8, "accent": "led"},
]

def desk_svg(t):
    a = t["accent"]
    W, H = 800, 600
    bg = '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7f8fb"/><stop offset="1" stop-color="#eef1f6"/></linearGradient></defs>'
    # desk top
    top = '<rect x="170" y="250" width="460" height="28" rx="10" fill="#3a3f4b"/>'
    # legs
    leg_l = '<rect x="210" y="278" width="20" height="200" rx="6" fill="#5b6270"/>'
    leg_r = '<rect x="570" y="278" width="20" height="200" rx="6" fill="#5b6270"/>'
    cross = '<rect x="230" y="455" width="330" height="14" rx="6" fill="#6b7280"/>'
    accent_el = ""
    label = ""
    if a == "electric":
        # motor box + up/down arrows
        accent_el = (
            '<rect x="365" y="278" width="70" height="34" rx="8" fill="#1f2937"/>'
            '<path d="M400 286 l-12 14 h8 v8 h8 v-8 h8 z" fill="#22d3ee"/>'
            '<path d="M400 314 l12 -14 h-8 v-8 h-8 v8 h-8 z" fill="#22d3ee"/>'
        )
        label = "Electric Lift"
    elif a == "manual":
        # crank handle on right leg
        accent_el = (
            '<rect x="590" y="330" width="40" height="10" rx="5" fill="#1f2937"/>'
            '<circle cx="640" cy="335" r="16" fill="none" stroke="#22d3ee" stroke-width="6"/>'
        )
        label = "Manual Crank"
    elif a == "led":
        # L-shape corner desk + LED strip + remote
        accent_el = (
            '<rect x="170" y="250" width="200" height="28" rx="10" fill="#3a3f4b"/>'
            '<rect x="170" y="250" width="28" height="200" rx="10" fill="#3a3f4b"/>'
            '<rect x="200" y="252" width="360" height="6" rx="3" fill="#22d3ee"/>'
            '<rect x="200" y="260" width="360" height="4" rx="2" fill="#a855f7"/>'
            '<rect x="610" y="300" width="34" height="60" rx="8" fill="#1f2937"/>'
            '<circle cx="627" cy="320" r="10" fill="#22d3ee"/>'
        )
        top = ""  # replaced by L-shape above
        label = "Corner + LED"
    else:  # fixed
        label = "Fixed Height"
    # glow strip under top for gaming vibe (non-led)
    if a != "led":
        accent_el += '<rect x="170" y="278" width="460" height="5" rx="2" fill="#22d3ee" opacity="0.85"/>'
    text = (
        f'<text x="400" y="520" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#1f2937" text-anchor="middle">{t["sku"]}</text>'
        f'<text x="400" y="555" font-family="Arial, sans-serif" font-size="22" fill="#6b7280" text-anchor="middle">{t["size"]} · {label}</text>'
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
        f'{bg}<rect width="{W}" height="{H}" fill="url(#bg)"/>'
        f'{top}{leg_l}{leg_r}{cross}{accent_el}{text}</svg>'
    )
    return svg

for t in TABLES:
    with open(os.path.join(TABLES_SVG, t["sku"] + ".svg"), "w") as f:
        f.write(desk_svg(t))
    t["img"] = "assets/tables/" + t["sku"] + ".svg"

# --- Chairs ---
COLOR_MAP = {
    "DS5004": "White", "DS5006": "White", "DS5008": "White",
    "DS5011BW": "Black / White", "DS5011PINK": "Black / Pink",
    "DS5011RED": "Black / Red", "DS5017": "Pink / White", "DS5018": "Black / White",
}
chairs = []
for d in sorted(os.listdir(CHAIRS)):
    dp = os.path.join(CHAIRS, d)
    if not os.path.isdir(dp):
        continue
    imgs = sorted([f for f in os.listdir(dp) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
    if not imgs:
        continue
    chairs.append({
        "sku": d,
        "color": COLOR_MAP.get(d, "Multi"),
        "desc": "Ergonomic racing-style gaming chair with adjustable backrest, armrests and lumbar support.",
        "moq": 300,
        "fob": None,
        "cover": f"assets/chairs/{d}/{imgs[0]}",
        "gallery": [f"assets/chairs/{d}/{i}" for i in imgs],
    })

data = {"tables": TABLES, "chairs": chairs}
with open(os.path.join(ROOT, "assets", "js", "data.js"), "w") as f:
    f.write("// Auto-generated by gen_assets.py. Prices (fob) are stored but NEVER rendered on the site.\n")
    f.write("window.PRODUCTS = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n")

print("tables:", len(TABLES), "| chairs:", len(chairs))
print("wrote assets/js/data.js and", len(TABLES), "table SVGs")
