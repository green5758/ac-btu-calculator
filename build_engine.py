import os
import json
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "BTUSizerPro"
SITE_TAGLINE = "Precision AC, Mini-Split, Heater & Dehumidifier BTU Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d"

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/btusizerpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "btusizerpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

# ==========================================
# AMAZON BEST SELLERS DATABASE (HVAC / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Midea Duo 12,000 BTU (10,000 SACC) Smart Inverter Portable Air Conditioner",
        "category": "Dual-Hose Inverter Portable AC",
        "rating": "4.6 ★ (9,200+ reviews)",
        "badge": "#1 Best Seller in Portable ACs",
        "specs": "Cools up to 550 Sq.Ft | Ultra-Quiet 42dB | 2x Faster Cooling | Wi-Fi Smart Control",
        "keyword": "Midea+Duo+12000+BTU+Smart+Inverter+Portable+Air+Conditioner"
    },
    {
        "title": "Midea 8,000–12,000 BTU U-Shaped Smart Inverter Window Air Conditioner",
        "category": "Ultra-Quiet Window AC",
        "rating": "4.7 ★ (16,400+ reviews)",
        "badge": "Most Energy Efficient",
        "specs": "35% Energy Savings | Open-Window U-Design | Extreme Quiet 32dB | ENERGY STAR",
        "keyword": "Midea+U+Shaped+Inverter+Window+Air+Conditioner+12000+BTU"
    },
    {
        "title": "Senville LETO Series 12,000 BTU Mini Split Air Conditioner & Heat Pump",
        "category": "Ductless Mini-Split HVAC",
        "rating": "4.6 ★ (6,800+ reviews)",
        "badge": "Top All-Season Heat Pump",
        "specs": "AC + Heating + Dehumidifier | SEER2 20+ Inverter | Complete Installation Kit",
        "keyword": "Senville+12000+BTU+Mini+Split+Air+Conditioner+Heat+Pump"
    },
    {
        "title": "BLACK+DECKER 14,000 BTU Portable Air Conditioner with Heat & Remote",
        "category": "4-in-1 Portable Climate Control",
        "rating": "4.5 ★ (28,500+ reviews)",
        "badge": "#1 Most Reviewed Unit",
        "specs": "Cools & Heats up to 700 Sq.Ft | Built-in Dehumidifier | Slide-Out Washable Filter",
        "keyword": "BLACK+DECKER+14000+BTU+Portable+Air+Conditioner+with+Heat"
    },
    {
        "title": "hOmeLabs 50 Pint (4,500 Sq.Ft) Energy Star Dehumidifier for Basements",
        "category": "High-Capacity Dehumidifier",
        "rating": "4.6 ★ (49,000+ reviews)",
        "badge": "#1 Basement Dehumidifier",
        "specs": "Removes 50 Pints/Day | Continuous Drain Hose Outlet | Turbo Fan Mode",
        "keyword": "hOmeLabs+50+Pint+Energy+Star+Dehumidifier+for+Basement"
    },
    {
        "title": "DELLA 18,000 BTU Wifi Ductless Mini Split Inverter AC & Heater 230V",
        "category": "Large Room / Garage Mini Split",
        "rating": "4.6 ★ (5,100+ reviews)",
        "badge": "Best for Garages & Workshops",
        "specs": "Covers up to 1,000 Sq.Ft | Heat Pump down to 5°F | Pre-Charged Line Set",
        "keyword": "DELLA+18000+BTU+Mini+Split+Air+Conditioner+Heat+Pump"
    },
    {
        "title": "Dr. Infrared Heater Portable Space Heater 1500W Dual Heating System",
        "category": "Room & Office Space Heater",
        "rating": "4.7 ★ (31,000+ reviews)",
        "badge": "Top Rated Winter Heater",
        "specs": "5,200 BTU Output | Quartz Infrared + PTC | Tip-Over & Overheat Protection",
        "keyword": "Dr+Infrared+Heater+Portable+Space+Heater+1500+Watt"
    },
    {
        "title": "Coway Airmega AP-1512HH Mighty True HEPA Air Purifier with Eco Mode",
        "category": "HEPA Air Filtration",
        "rating": "4.8 ★ (34,000+ reviews)",
        "badge": "Wirecutter Top Pick",
        "specs": "99.97% True HEPA | Auto Air Quality Sensor | 4-Stage Filtration System",
        "keyword": "Coway+Airmega+AP-1512HH+True+HEPA+Air+Purifier"
    }
]

# ==========================================
# PROGRAMMATIC SEO ROOM & USE-CASE PRESETS
# ==========================================
ROOM_PRESETS = [
    {"slug": "bedroom-ac-btu-calculator", "name": "Master Bedroom", "length": 16, "width": 14, "ceiling": 8, "sun": "1.0", "insulation": "1.0", "occupants": 2, "desc": "Calculate the exact quiet Air Conditioner BTU, inverter window unit size, and HEPA purifier CFM needed for a master bedroom."},
    {"slug": "two-car-garage-btu-calculator", "name": "2-Car Garage & Workshop", "length": 24, "width": 22, "ceiling": 10, "sun": "1.1", "insulation": "1.15", "occupants": 2, "desc": "Size a ductless mini-split heat pump or heavy-duty garage heater BTU required to cool and heat an insulated or uninsulated 2-car garage."},
    {"slug": "basement-dehumidifier-btu-calculator", "name": "Finished & Unfinished Basement", "length": 30, "width": 20, "ceiling": 8, "sun": "0.9", "insulation": "1.0", "occupants": 2, "desc": "Calculate exact dehumidifier pint capacity (pints/day) and HVAC BTU sizing to eliminate dampness and control temperature in basements."},
    {"slug": "living-room-mini-split-btu-calculator", "name": "Open-Concept Living Room", "length": 25, "width": 18, "ceiling": 9, "sun": "1.1", "insulation": "1.0", "occupants": 4, "desc": "Find the right BTU rating for open-concept living rooms, family rooms, and vaulted-ceiling spaces using portable or mini-split ACs."},
    {"slug": "home-office-ac-heater-btu-calculator", "name": "Home Office & Gaming Room", "length": 12, "width": 12, "ceiling": 8, "sun": "1.1", "insulation": "1.0", "occupants": 1, "desc": "Calculate cooling BTUs needed for home offices and PC gaming rooms with high heat-generating monitors and computer equipment."},
    {"slug": "sunroom-patio-btu-calculator", "name": "Glass Sunroom & Enclosed Patio", "length": 18, "width": 14, "ceiling": 9, "sun": "1.2", "insulation": "1.15", "occupants": 3, "desc": "Calculate high-solar-gain BTU requirements for glass sunrooms, Florida rooms, and 3-season enclosed patios."},
    {"slug": "rv-camper-air-conditioner-btu-calculator", "name": "RV, Fifth Wheel & Camper Van", "length": 26, "width": 8, "ceiling": 7, "sun": "1.2", "insulation": "1.15", "occupants": 2, "desc": "Size rooftop 12V/120V RV air conditioners and portable heat pumps for travel trailers, campers, and van conversions."},
    {"slug": "server-room-cooling-btu-calculator", "name": "IT Closet & Home Server Room", "length": 10, "width": 8, "ceiling": 8, "sun": "1.2", "insulation": "1.15", "occupants": 1, "desc": "Calculate 24/7 continuous cooling BTUs required to prevent thermal throttling in server racks, network closets, and mining rooms."},
    {"slug": "studio-apartment-ac-btu-calculator", "name": "Studio Apartment & Loft", "length": 22, "width": 20, "ceiling": 9, "sun": "1.0", "insulation": "1.0", "occupants": 2, "desc": "Calculate single-zone portable AC or window air conditioner BTU capacity for studio apartments and loft living spaces."},
    {"slug": "attic-bonus-room-btu-calculator", "name": "Converted Attic & Bonus Room", "length": 20, "width": 16, "ceiling": 8, "sun": "1.2", "insulation": "1.15", "occupants": 2, "desc": "Calculate cooling and heating BTU load for hot upstairs bonus rooms, FROG rooms, and finished attic bedrooms."},
    {"slug": "kitchen-dining-ac-btu-calculator", "name": "Kitchen & Dining Area", "length": 18, "width": 15, "ceiling": 9, "sun": "1.1", "insulation": "1.15", "occupants": 3, "desc": "Factor in oven and stove heat loads to calculate the proper air conditioner BTU rating for residential kitchens."},
    {"slug": "indoor-grow-tent-room-btu-calculator", "name": "Indoor Grow Room & Greenhouse", "length": 12, "width": 10, "ceiling": 8, "sun": "1.2", "insulation": "1.15", "occupants": 1, "desc": "Calculate cooling BTUs and dehumidifier pints per day required to offset LED grow lights and plant transpiration."},
    {"slug": "tiny-house-cabin-btu-calculator", "name": "Tiny House & Off-Grid Cabin", "length": 24, "width": 12, "ceiling": 10, "sun": "1.1", "insulation": "1.0", "occupants": 2, "desc": "Size high-efficiency 9,000 or 12,000 BTU mini-split heat pumps and space heaters for tiny homes and cabins."},
    {"slug": "home-gym-cooling-btu-calculator", "name": "Home Gym & Fitness Studio", "length": 16, "width": 15, "ceiling": 9, "sun": "1.1", "insulation": "1.0", "occupants": 2, "desc": "Calculate cooling BTUs, dehumidification, and air changes per hour (ACH) needed for a comfortable home workout room."},
    {"slug": "nursery-kids-room-btu-calculator", "name": "Baby Nursery & Kids Bedroom", "length": 12, "width": 11, "ceiling": 8, "sun": "1.0", "insulation": "1.0", "occupants": 2, "desc": "Find the right ultra-quiet (<40dB) inverter AC BTU size and HEPA air purifier rating for a baby nursery."},
    {"slug": "commercial-retail-office-btu-calculator", "name": "Small Retail Shop & Suite", "length": 35, "width": 25, "ceiling": 10, "sun": "1.1", "insulation": "1.0", "occupants": 6, "desc": "Calculate commercial light-duty HVAC and multi-zone mini-split BTU requirements for small storefronts and offices."}
]

def get_dynamic_sqft_pages():
    sqft_tiers = [
        (100, 10, 10), (150, 15, 10), (200, 20, 10), (250, 25, 10),
        (300, 20, 15), (350, 20, 17.5), (400, 20, 20), (450, 25, 18),
        (500, 25, 20), (600, 30, 20), (700, 35, 20), (800, 40, 20),
        (900, 30, 30), (1000, 40, 25), (1200, 40, 30), (1500, 50, 30)
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(sqft_tiers), 10 + (day_of_year % 7))
    pages = []
    for sqft, l, w in sqft_tiers[:active_count]:
        pages.append({
            "slug": f"{sqft}-sq-ft-ac-btu-calculator",
            "name": f"{sqft} Sq. Ft. Room",
            "length": l,
            "width": w,
            "ceiling": 8,
            "sun": "1.0",
            "insulation": "1.0",
            "occupants": 2,
            "desc": f"Calculate the exact Air Conditioner BTU, Heater Wattage, and Dehumidifier Pint rating required for a {sqft} square foot room."
        })
    return pages

ALL_PAGES = ROOM_PRESETS + get_dynamic_sqft_pages()

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

def generate_faq_data(room_name, length, width, ceiling):
    sqft = int(length * width)
    base_btu = int(round((sqft * 25) / 500.0) * 500)
    base_btu = max(5000, base_btu)
    heater_watts = min(1500, int(sqft * 10))
    return [
        {
            "q": f"How many BTUs do I need to cool a {room_name} ({sqft} sq. ft.)?",
            "a": f"For a {sqft} sq. ft. {room_name} with {ceiling}-foot ceilings, you need approximately {base_btu:,} BTU/hr of cooling capacity. If the room has poor insulation, high ceilings, or direct afternoon sunlight, step up to {base_btu + 2000:,} BTUs."
        },
        {
            "q": "What is the difference between ASHRAE BTU and DOE SACC BTU on portable air conditioners?",
            "a": "ASHRAE BTU measures cooling under steady ideal conditions, while SACC (Seasonally Adjusted Cooling Capacity) accounts for heat loss through the exhaust hose. Always choose a Dual-Hose Inverter Portable AC to maximize real-world SACC efficiency."
        },
        {
            "q": f"What size space heater or heat pump is needed for {sqft} square feet?",
            "a": f"Standard winter heating requires 10 watts (or 30–35 BTUs) per square foot. A {sqft} sq. ft. space needs roughly {sqft * 32:,} BTUs of heating—which corresponds to a {heater_watts}W electric heater for supplemental warmth or a {base_btu:,} BTU mini-split heat pump for primary heating."
        },
        {
            "q": "What happens if I buy an air conditioner with too many BTUs for my room?",
            "a": "An oversized standard AC cools the air too rapidly and shuts off before removing humidity, leaving the room feeling cold and clammy. Choosing a variable-speed Inverter AC solves this by automatically throttling down its compressor to match the exact room load."
        },
        {
            "q": "How do I size a dehumidifier in Pints per Day?",
            "a": f"For a {sqft} sq. ft. room or basement, a 30-to-50 Pint Energy Star dehumidifier is recommended for moderate dampness, while very wet basements over 500 sq. ft. should use a 50-Pint unit with a continuous drain hose."
        }
    ]

def render_html_page(page_data, is_home=False):
    sqft_val = int(page_data["length"] * page_data["width"])
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} AC & Heater BTU Calculator ({sqft_val} Sq Ft) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], page_data["length"], page_data["width"], page_data["ceiling"])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]}
            } for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-blue-100 text-blue-900 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-600">{prod['rating']}</span>
                </div>
                <span class="text-xs text-slate-500 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-slate-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-slate-600 mb-4 bg-slate-50 p-2.5 rounded-lg border border-slate-100">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_PAGES:
        p_sqft = int(p["length"] * p["width"])
        active_cls = "bg-blue-50 border-blue-500 text-blue-900 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-white border-slate-200 text-slate-700 hover:border-blue-500 hover:text-slate-900"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-slate-400 font-mono shrink-0">{p_sqft} sq.ft</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5">
            <h3 class="text-base font-bold text-slate-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-slate-600 leading-relaxed">{item['a']}</p>
        </div>
        """

    top_banner_link = amz_url("Inverter+Portable+Air+Conditioner+Mini+Split+Deals")
    mid_banner_link = amz_url("Ductless+Mini+Split+Air+Conditioner+Heat+Pump+12000+18000+BTU")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    google-site-verification: google8748763e68b6545e.html
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased selection:bg-blue-100 selection:text-slate-900">

    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-blue-950 text-white py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-blue-900">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-slate-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Seasonal Deals</span>
            <span>Save up to 30% on Energy Star Inverter Window ACs, Dual-Hose Portable ACs & Mini-Split Heat Pumps on Amazon.</span>
            <a href="{top_banner_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                Shop Today's HVAC Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY WHITE HEADER -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white font-black text-lg shadow-sm">B</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-slate-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-slate-500 font-medium">HVAC, BTU & Humidity Sizing Engine</span>
                </div>
            </a>
            <nav class="flex items-center gap-5 text-sm font-semibold text-slate-700">
                <a href="#calculator" class="hover:text-blue-600 transition">BTU Calculator</a>
                <a href="#product-search" class="hover:text-blue-600 transition">Product Search</a>
                <a href="#best-sellers" class="hover:text-blue-600 transition">Best Sellers</a>
                <a href="#presets" class="hover:text-blue-600 transition">Room Guides</a>
                <a href="#faq" class="hover:text-blue-600 transition">FAQ</a>
            </nav>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700">
                <span>❄️ ASHRAE & ACCA Manual-J Inspired Room Load Calculator</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                { "AC, Mini-Split, Heater & Dehumidifier BTU Calculator" if is_home else f"{page_data['name']} BTU & HVAC Sizing Calculator ({sqft_val} Sq. Ft.)" }
            </h1>
            <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-slate-900">1. Enter Room Dimensions & Conditions</h2>
                        <p class="text-xs text-slate-500">Calculates cooling BTUs, winter heating watts, and dehumidifier capacity</p>
                    </div>
                    <span class="text-xs font-mono bg-blue-50 text-blue-700 px-2.5 py-1 rounded font-semibold">Instant Sizing</span>
                </div>

                <div>
                    <label for="quickRoomPreset" class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">Quick Select Room Type</label>
                    <select id="quickRoomPreset" onchange="applyRoomPreset(this.value)" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-medium text-slate-900 focus:ring-2 focus:ring-blue-600 focus:border-blue-600">
                        <option value="{page_data['length']},{page_data['width']},{page_data['ceiling']},{page_data['sun']},{page_data['insulation']},{page_data['occupants']}">Current: {page_data['name']} ({sqft_val} Sq. Ft.)</option>
                        <option value="16,14,8,1.0,1.0,2">Master Bedroom (224 Sq. Ft.)</option>
                        <option value="24,22,10,1.1,1.15,2">2-Car Garage / Workshop (528 Sq. Ft.)</option>
                        <option value="30,20,8,0.9,1.0,2">Finished / Unfinished Basement (600 Sq. Ft.)</option>
                        <option value="25,18,9,1.1,1.0,4">Open Living Room (450 Sq. Ft.)</option>
                        <option value="12,12,8,1.1,1.0,1">Home Office / Gaming Room (144 Sq. Ft.)</option>
                        <option value="18,14,9,1.2,1.15,3">Glass Sunroom / Patio (252 Sq. Ft.)</option>
                        <option value="10,8,8,1.2,1.15,1">Server Closet / IT Room (80 Sq. Ft. High Heat)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="lengthInput" class="block text-sm font-bold text-slate-800 mb-1">Room Length (Ft)</label>
                        <input type="number" id="lengthInput" value="{page_data['length']}" min="4" max="200" step="0.5" oninput="calculateHVAC()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-blue-600">
                    </div>
                    <div>
                        <label for="widthInput" class="block text-sm font-bold text-slate-800 mb-1">Room Width (Ft)</label>
                        <input type="number" id="widthInput" value="{page_data['width']}" min="4" max="200" step="0.5" oninput="calculateHVAC()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-blue-600">
                    </div>
                    <div>
                        <label for="ceilingInput" class="block text-sm font-bold text-slate-800 mb-1">Ceiling Height (Ft)</label>
                        <input type="number" id="ceilingInput" value="{page_data['ceiling']}" min="6" max="25" step="0.5" oninput="calculateHVAC()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-blue-600">
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="sunInput" class="block text-sm font-bold text-slate-800 mb-1">Sun Exposure</label>
                        <select id="sunInput" onchange="calculateHVAC()" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2.5 text-sm font-semibold text-slate-900">
                            <option value="0.9" {"selected" if page_data['sun'] == "0.9" else ""}>Shaded / North Window (-10%)</option>
                            <option value="1.0" {"selected" if page_data['sun'] == "1.0" else ""}>Average Sunlight (Standard)</option>
                            <option value="1.1" {"selected" if page_data['sun'] == "1.1" else ""}>Sunny / South-West (+10%)</option>
                            <option value="1.2" {"selected" if page_data['sun'] == "1.2" else ""}>Sunroom / High Heat (+20%)</option>
                        </select>
                    </div>
                    <div>
                        <label for="insulationInput" class="block text-sm font-bold text-slate-800 mb-1">Insulation Quality</label>
                        <select id="insulationInput" onchange="calculateHVAC()" class="w-full bg-white border border-slate-300 rounded-lg px-3 py-2.5 text-sm font-semibold text-slate-900">
                            <option value="0.9">Well Insulated / New Build</option>
                            <option value="1.0" {"selected" if page_data['insulation'] == "1.0" else ""}>Average Home Insulation</option>
                            <option value="1.15" {"selected" if page_data['insulation'] == "1.15" else ""}>Poor / Garage / Attic (+15%)</option>
                        </select>
                    </div>
                    <div>
                        <label for="occupantsInput" class="block text-sm font-bold text-slate-800 mb-1">Occupants in Room</label>
                        <input type="number" id="occupantsInput" value="{page_data['occupants']}" min="1" max="50" oninput="calculateHVAC()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-blue-600">
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Affiliate Hardware Matcher (5 Cols) -->
            <div class="lg:col-span-5 bg-white border-2 border-blue-600 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-slate-100 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-600">2. Engineered Climate Specs</span>
                    <h2 class="text-xl font-extrabold text-slate-900">Your Required Room Capacity</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-blue-50 border border-blue-200 rounded-xl p-3.5">
                        <span class="text-xs text-blue-900 font-semibold block">Cooling Needed (AC)</span>
                        <span id="resCoolingBTU" class="text-2xl font-black text-blue-700">0 BTU</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Room Area & Volume</span>
                        <span id="resAreaVol" class="text-lg font-extrabold text-slate-900">0 Sq.Ft</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Heating Requirement</span>
                        <span id="resHeating" class="text-lg font-extrabold text-amber-700">0 Watts</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Dehumidifier Size</span>
                        <span id="resDehum" class="text-lg font-extrabold text-emerald-700">0 Pints/Day</span>
                    </div>
                </div>

                <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-700">Air Purifier Clean Air Rate (4.8 ACH):</span>
                    <span id="resCADR" class="text-sm font-black text-slate-900 bg-white px-2.5 py-1 rounded border border-slate-200">0 CFM CADR</span>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-blue-50/60 border-2 border-blue-300 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-blue-600 text-white px-2 py-0.5 rounded">Exact Hardware Match</span>
                        <span class="text-xs font-bold text-slate-600">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recUnitTitle" class="text-base font-extrabold text-slate-900 leading-snug">Calculating Best Unit...</h3>
                    <p id="recUnitDesc" class="text-xs text-slate-600"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           View Recommended AC on Amazon &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 font-bold text-xs py-3 px-3 rounded-lg transition">
                           Compare Dehumidifier / Heater
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-slate-900">Search Air Conditioners, Mini-Splits, Heaters & Dehumidifiers</h2>
                <p class="text-sm text-slate-600">Enter any BTU rating, brand (Midea, Senville, LG, Frigidaire, DELLA, hOmeLabs), or room appliance to compare live prices on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. 12000 BTU Dual Hose Inverter Portable AC, 18000 BTU Mini Split, 50 Pint Dehumidifier..."
                           class="flex-1 bg-white border-2 border-slate-300 rounded-xl px-4 py-3 text-sm font-medium text-slate-900 focus:outline-none focus:border-blue-600" required>
                    <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-slate-400 font-semibold">Quick Filters:</span>
                    <a href="{amz_url('Midea U Shaped Window Air Conditioner 8000 12000 BTU')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-blue-100 text-slate-700 rounded-full transition">U-Shaped Window AC</a>
                    <a href="{amz_url('Dual Hose Inverter Portable Air Conditioner 12000 14000 BTU')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-blue-100 text-slate-700 rounded-full transition">Dual-Hose Portable AC</a>
                    <a href="{amz_url('12000 BTU Mini Split Air Conditioner Heat Pump')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-blue-100 text-slate-700 rounded-full transition">12,000 BTU Mini-Split</a>
                    <a href="{amz_url('50 Pint Energy Star Dehumidifier with Pump')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-blue-100 text-slate-700 rounded-full transition">50-Pint Dehumidifier</a>
                    <a href="{amz_url('1500W Infrared Space Heater Thermostat')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-blue-100 text-slate-700 rounded-full transition">1500W Space Heater</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-600">Top Rated Climate Hardware</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">Best-Selling Air Conditioners, Mini-Splits & Dehumidifiers</h2>
                </div>
                <a href="{amz_url('Best Selling Air Conditioners Heaters and Dehumidifiers')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-blue-600 hover:text-blue-700">
                    View Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-slate-50 border-2 border-blue-600 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-600 text-white px-2.5 py-1 rounded">All-Season Efficiency Upgrade</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900">Upgrading a Garage, Sunroom, or Master Suite?</h2>
                <p class="text-sm text-slate-600">SEER2 20+ Ductless Mini-Split Inverter Heat Pumps cut cooling & winter heating bills by up to 40% compared to traditional baseboard heaters and loud window units.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Compare Mini-Split Kits on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-slate-200 pb-3">
                <h2 class="text-xl font-extrabold text-slate-900">Room & Square-Footage BTU Calculators</h2>
                <p class="text-xs text-slate-500">Select your room type or square footage below for pre-calculated cooling, heating, and dehumidification specs.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-slate-200 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-600">HVAC Sizing Guide</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex gap-4 font-medium text-slate-600">
                <a href="{BASE_URL}/" class="hover:text-slate-900">Home</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-slate-900">Sitemap</a>
                <a href="#calculator" class="hover:text-slate-900">Calculator</a>
                <a href="#faq" class="hover:text-slate-900">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyRoomPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 6) {{
                document.getElementById("lengthInput").value = parts[0];
                document.getElementById("widthInput").value = parts[1];
                document.getElementById("ceilingInput").value = parts[2];
                document.getElementById("sunInput").value = parts[3];
                document.getElementById("insulationInput").value = parts[4];
                document.getElementById("occupantsInput").value = parts[5];
                calculateHVAC();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateHVAC() {{
            const length = parseFloat(document.getElementById("lengthInput").value) || 0;
            const width = parseFloat(document.getElementById("widthInput").value) || 0;
            const ceiling = parseFloat(document.getElementById("ceilingInput").value) || 8;
            const sunFactor = parseFloat(document.getElementById("sunInput").value) || 1.0;
            const insulFactor = parseFloat(document.getElementById("insulationInput").value) || 1.0;
            const occupants = parseInt(document.getElementById("occupantsInput").value) || 1;

            const sqft = Math.round(length * width);
            const cubicFt = Math.round(sqft * ceiling);
            const ceilingFactor = ceiling > 8 ? (1 + ((ceiling - 8) * 0.08)) : 1.0;
            const occupantBTU = occupants > 2 ? (occupants - 2) * 600 : 0;

            let rawBTU = (sqft * 25 * ceilingFactor * sunFactor * insulFactor) + occupantBTU;
            let coolingBTU = Math.max(5000, Math.ceil(rawBTU / 500) * 500);

            const heatingWatts = Math.min(3000, Math.ceil((sqft * 10 * insulFactor) / 50) * 50);
            const heatingBTU = Math.ceil((sqft * 32 * insulFactor) / 500) * 500;
            const dehumPints = sqft <= 300 ? 22 : (sqft <= 500 ? 35 : 50);
            const cadrCFM = Math.ceil((cubicFt * 4.8) / 60);

            document.getElementById("resCoolingBTU").textContent = coolingBTU.toLocaleString() + " BTU";
            document.getElementById("resAreaVol").textContent = sqft.toLocaleString() + " Sq.Ft (" + cubicFt.toLocaleString() + " ft³)";
            document.getElementById("resHeating").textContent = heatingWatts.toLocaleString() + "W / " + heatingBTU.toLocaleString() + " BTU";
            document.getElementById("resDehum").textContent = dehumPints + " Pints/Day";
            document.getElementById("resCADR").textContent = cadrCFM + " CFM Minimum";

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "";

            if (coolingBTU <= 8500) {{
                recTitle = "6,000–8,000 BTU Quiet Inverter Window or Compact Portable AC";
                recDesc = "Ideal for bedrooms, home offices, nurseries, and rooms up to 350 sq. ft.";
                primaryQuery = "8000 BTU Inverter Window Air Conditioner Quiet Midea";
                secondaryQuery = "1500W Infrared Space Heater and 30 Pint Dehumidifier";
            }} else if (coolingBTU <= 12500) {{
                recTitle = "10,000–12,000 BTU Dual-Hose Inverter Portable AC or U-Shaped Window AC";
                recDesc = "Best-selling capacity for master bedrooms, living rooms, and studios up to 550 sq. ft.";
                primaryQuery = "12000 BTU Dual Hose Inverter Portable Air Conditioner Midea Duo";
                secondaryQuery = "12000 BTU Mini Split Air Conditioner Heat Pump Senville";
            }} else if (coolingBTU <= 15500) {{
                recTitle = "14,000 BTU Heavy-Duty Portable AC with Heat or 12K/18K Mini-Split";
                recDesc = "Engineered for large living areas, sunrooms, and 1-to-2 car garages up to 700 sq. ft.";
                primaryQuery = "14000 BTU Portable Air Conditioner with Heat Dual Hose";
                secondaryQuery = "50 Pint Energy Star Dehumidifier for Basement hOmeLabs";
            }} else {{
                recTitle = "18,000–24,000 BTU Ductless Mini-Split Inverter AC & Heat Pump System";
                recDesc = "High-output climate control for large open layouts, workshops, basements, and multi-room zones.";
                primaryQuery = "18000 24000 BTU Mini Split Air Conditioner Heat Pump Senville Della";
                secondaryQuery = "Commercial 50 Pint Dehumidifier with Continuous Drain Pump";
            }}

            document.getElementById("recUnitTitle").textContent = recTitle;
            document.getElementById("recUnitDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateHVAC);
    </script>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.8"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow ping notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    home_preset = {
        "slug": "index",
        "name": "Room & Home Space",
        "length": 20,
        "width": 16,
        "ceiling": 8,
        "sun": "1.0",
        "insulation": "1.0",
        "occupants": 2,
        "desc": "Calculate exact Air Conditioner BTU, Mini-Split Heat Pump size, Space Heater wattage, and Dehumidifier pints/day for any room size—plus compare top-rated Amazon HVAC units."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_html_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    for page in ALL_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_html_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Generated {len(generated_urls)} programmatic HVAC calculator pages in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
