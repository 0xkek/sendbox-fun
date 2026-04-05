"""
sendbox.fun Static Page Generator
==================================
Generates SEO-friendly static HTML pages from agents.json:
- /tools/<id>.html         (one per tool)
- /category/<cat>.html     (one per category)
- /sitemap.xml
- /robots.txt

Runs after scraper to keep SEO pages in sync with the database.

Usage:
  python scraper/generate_pages.py
"""

import json
import os
import re
import html
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
AGENTS_JSON = ROOT / "agents.json"
TOOLS_DIR = ROOT / "tools"
CATEGORY_DIR = ROOT / "category"
BASE_URL = "https://sendbox.fun"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

CATEGORIES = {
    "social": {"icon": "📱", "label": "Social Media", "desc": "Scheduling, analytics, content creation, and audience growth."},
    "sales": {"icon": "💰", "label": "Sales & CRM", "desc": "Lead generation, outreach, pipeline management, and CRM."},
    "ecom": {"icon": "🛒", "label": "Ecommerce", "desc": "Customer service, pricing, inventory, and conversions."},
    "content": {"icon": "✍️", "label": "Content Creation", "desc": "AI copywriting, blog posts, and product descriptions."},
    "email": {"icon": "📧", "label": "Email Marketing", "desc": "Email marketing, newsletters, and deliverability."},
    "seo": {"icon": "🔍", "label": "SEO", "desc": "Keyword research, site audits, rank tracking, and optimization."},
    "video": {"icon": "🎬", "label": "Video", "desc": "AI video creation, editing, avatars, and repurposing."},
    "automation": {"icon": "⚡", "label": "Automation", "desc": "Workflow automation, integrations, and no-code tools."},
    "customer-service": {"icon": "🎧", "label": "Customer Service", "desc": "Helpdesks, chatbots, live chat, and ticketing."},
    "analytics": {"icon": "📊", "label": "Analytics", "desc": "Web analytics, reporting, heatmaps, and insights."},
    "ads": {"icon": "📣", "label": "Advertising", "desc": "Ad management, optimization, and attribution."},
    "design": {"icon": "🎨", "label": "Design", "desc": "Graphic design, logos, and creative tools."},
    "assistant": {"icon": "🤖", "label": "AI Assistants", "desc": "General-purpose AI chatbots like ChatGPT, Claude, and Gemini."},
    "coding": {"icon": "💻", "label": "AI Coding", "desc": "AI code editors, copilots, and engineering agents."},
    "dev-tools": {"icon": "🛠️", "label": "Developer Tools", "desc": "Agent frameworks, vector DBs, LLM gateways, and observability."},
    "productivity": {"icon": "✅", "label": "Productivity", "desc": "Note-taking, meetings, scheduling, tasks, and email."},
    "research": {"icon": "🔬", "label": "Research", "desc": "Web research, academic search, and data extraction."},
}


def esc(s):
    """HTML escape a string."""
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def get_category_meta(cat):
    return CATEGORIES.get(cat, {"icon": "🤖", "label": cat.title(), "desc": "AI tools."})


def get_domain(url):
    try:
        from urllib.parse import urlparse
        h = urlparse(url).hostname or ""
        return h.replace("www.", "")
    except Exception:
        return ""


def logo_img(url, css_class="card-logo"):
    domain = get_domain(url)
    if not domain:
        return ''
    return f'<img src="https://icons.duckduckgo.com/ip3/{domain}.ico" alt="" class="{css_class}" loading="lazy" onerror="this.style.visibility=\'hidden\'">'


def shared_css():
    return """
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --bg: #FAFAF9; --card: #FFF; --text: #1A1A2E; --text-light: #6B7280;
  --accent: #7C3AED; --accent-light: #EDE9FE; --accent-hover: #6D28D9;
  --border: #E5E7EB; --radius: 16px;
  --shadow-lg: 0 10px 25px rgba(0,0,0,0.08);
}
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
nav { position: sticky; top: 0; z-index: 100; background: rgba(250,250,249,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); padding: 0 24px; }
.nav-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 72px; }
.logo { font-size: 22px; font-weight: 800; color: var(--accent); text-decoration: none; display: flex; align-items: center; gap: 10px; }
.logo img { height: 48px; width: 48px; border-radius: 10px; }
.nav-links { display: flex; gap: 24px; align-items: center; }
.nav-links a { color: var(--text-light); font-size: 15px; font-weight: 500; text-decoration: none; }
.nav-links a:hover { color: var(--accent); }
main { max-width: 1200px; margin: 0 auto; padding: 48px 24px 80px; }
.breadcrumbs { font-size: 14px; color: var(--text-light); margin-bottom: 24px; }
.breadcrumbs a { color: var(--text-light); }
.breadcrumbs a:hover { color: var(--accent); }
.breadcrumbs span { margin: 0 8px; }
h1 { font-size: clamp(32px, 5vw, 48px); font-weight: 800; margin-bottom: 16px; line-height: 1.2; }
h2 { font-size: 24px; font-weight: 700; margin: 40px 0 20px; }
.tool-header { display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start; margin-bottom: 32px; padding-bottom: 32px; border-bottom: 1px solid var(--border); }
.tool-main { flex: 1; min-width: 280px; }
.tool-desc { font-size: 18px; color: var(--text-light); margin-bottom: 24px; }
.tool-sidebar { min-width: 280px; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; }
.meta-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border); font-size: 14px; }
.meta-row:last-child { border-bottom: none; }
.meta-label { color: var(--text-light); }
.meta-value { font-weight: 600; }
.btn-primary { display: inline-block; background: var(--accent); color: white; padding: 14px 24px; border-radius: 99px; font-weight: 700; text-decoration: none; text-align: center; width: 100%; margin-top: 20px; transition: background 0.2s; }
.btn-primary:hover { background: var(--accent-hover); text-decoration: none; }
.tags { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.tag { font-size: 13px; padding: 4px 12px; border-radius: 99px; background: var(--accent-light); color: var(--accent); font-weight: 600; text-decoration: none; }
.tag:hover { background: var(--accent); color: white; text-decoration: none; }
.platform-list, .bestfor-list { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.chip { font-size: 13px; padding: 4px 10px; border-radius: 99px; background: #F3F4F6; color: var(--text); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 24px; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; transition: all 0.2s; text-decoration: none; color: inherit; display: block; }
.card:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); text-decoration: none; border-color: var(--accent); }
.card h3 { font-size: 17px; font-weight: 700; margin-bottom: 8px; color: var(--text); }
.card p { font-size: 14px; color: var(--text-light); line-height: 1.5; }
.card .card-meta { font-size: 12px; color: var(--text-light); margin-top: 12px; }
.card-head { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 8px; }
.card-logo { width: 40px; height: 40px; border-radius: 8px; flex-shrink: 0; background: #F3F4F6; }
.card-title-wrap { flex: 1; min-width: 0; }
.card-rating { display: inline-block; margin-left: 8px; font-size: 13px; color: #F59E0B; }
.tool-logo-hero { width: 64px; height: 64px; border-radius: 12px; margin-bottom: 16px; background: #F3F4F6; }
.intro-box { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 28px; margin-bottom: 32px; }
.intro-box p { color: var(--text-light); font-size: 16px; line-height: 1.6; }
.reviews-section { margin-top: 48px; padding-top: 32px; border-top: 1px solid var(--border); }
.reviews-section h2 { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
.rating-summary { margin: 12px 0 32px; font-size: 16px; }
.review-box { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; margin-bottom: 24px; }
.review-box h3 { font-size: 18px; font-weight: 700; margin-bottom: 8px; }
.reviews-list { display: flex; flex-direction: column; gap: 16px; }
.review-item { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; }
.review-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 14px; }
.review-stars { color: #F59E0B; font-size: 16px; }
.review-meta { color: var(--text-light); font-size: 13px; }
.review-text { color: var(--text); font-size: 14px; line-height: 1.5; margin: 0; }
footer { border-top: 1px solid var(--border); padding: 32px 24px; max-width: 1200px; margin: 48px auto 0; color: var(--text-light); font-size: 14px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 16px; }
footer a { color: var(--text-light); text-decoration: none; }
footer a:hover { color: var(--accent); }
.footer-links { display: flex; gap: 20px; flex-wrap: wrap; }
@media (max-width: 640px) { .nav-links { display: none; } .tool-header { flex-direction: column; } .tool-sidebar { width: 100%; } }
"""


def shared_nav(base_path=""):
    return f"""<nav>
  <div class="nav-inner">
    <a href="{base_path}/" class="logo"><img src="{base_path}/logo.png" alt="sendbox"> sendbox.fun</a>
    <div class="nav-links">
      <a href="{base_path}/#categories">Categories</a>
      <a href="{base_path}/#agents">All Tools</a>
      <a href="{base_path}/#how">How It Works</a>
    </div>
  </div>
</nav>"""


def shared_footer():
    return """<footer>
  <div>© 2026 sendbox.fun — The search engine for AI agents</div>
  <div class="footer-links">
    <a href="/">Home</a>
    <a href="/#agents">All Tools</a>
    <a href="/sitemap.xml">Sitemap</a>
  </div>
</footer>"""


def related_tools(agent, all_agents, limit=6):
    """Find up to `limit` other tools sharing a category."""
    tags = set(agent["categories"])
    related = []
    for a in all_agents:
        if a["id"] == agent["id"]:
            continue
        if tags & set(a["categories"]):
            related.append(a)
        if len(related) >= limit:
            break
    return related


def tool_page_html(agent, all_agents):
    """Generate HTML for a single tool page."""
    name = esc(agent["name"])
    desc = esc(agent["description"])
    url = esc(agent["url"])
    cats = agent["categories"]
    primary_cat = cats[0] if cats else "dev-tools"
    cat_meta = get_category_meta(primary_cat)

    title = f"{name} — {cat_meta['label']} AI Tool | sendbox.fun"
    meta_desc = desc[:155] + ("..." if len(desc) > 155 else "")
    canonical = f"{BASE_URL}/tools/{agent['id']}"

    # Sidebar info
    platforms = agent.get("platforms", []) or []
    best_for = agent.get("bestFor", []) or []
    pricing = esc(agent.get("pricingFrom", "See website"))
    pricing_note = esc(agent.get("pricingNote", ""))
    founded = esc(agent.get("founded", ""))

    # Structured data
    structured = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": agent["name"],
        "description": agent["description"],
        "applicationCategory": "BusinessApplication",
        "url": agent["url"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"} if "free" in pricing.lower() else None,
    }
    structured = {k: v for k, v in structured.items() if v is not None}

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": cat_meta["label"], "item": f"{BASE_URL}/category/{primary_cat}"},
            {"@type": "ListItem", "position": 3, "name": agent["name"], "item": canonical},
        ],
    }

    # Related tools
    related = related_tools(agent, all_agents)
    related_html = ""
    if related:
        cards = []
        for r in related:
            r_cat = r["categories"][0] if r["categories"] else "dev-tools"
            r_cat_label = get_category_meta(r_cat)["label"]
            cards.append(f"""<a href="/tools/{esc(r['id'])}" class="card">
  <div class="card-head">{logo_img(r['url'])}<div class="card-title-wrap"><h3>{esc(r['name'])}</h3></div></div>
  <p>{esc(r['description'][:120])}{"..." if len(r['description']) > 120 else ""}</p>
  <div class="card-meta">{esc(r_cat_label)} · {esc(r.get('pricingFrom', 'See website'))}</div>
</a>""")
        related_html = f"""<h2>Related tools</h2>
<div class="grid">{"".join(cards)}</div>"""

    # Platforms/best-for chips
    platforms_html = ""
    if platforms:
        chips = "".join(f'<span class="chip">{esc(p)}</span>' for p in platforms)
        platforms_html = f'<div class="meta-row"><span class="meta-label">Integrations</span></div><div class="platform-list">{chips}</div>'

    bestfor_html = ""
    if best_for:
        chips = "".join(f'<span class="chip">{esc(b)}</span>' for b in best_for)
        bestfor_html = f'<div class="meta-row"><span class="meta-label">Best for</span></div><div class="bestfor-list">{chips}</div>'

    founded_html = f'<div class="meta-row"><span class="meta-label">Founded</span><span class="meta-value">{founded}</span></div>' if founded else ""

    # Category tags with links
    cat_tags = "".join(f'<a href="/category/{esc(c)}" class="tag">{get_category_meta(c)["icon"]} {esc(get_category_meta(c)["label"])}</a>' for c in cats)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta_desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta_desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="sendbox.fun">
<meta property="og:image" content="https://sendbox.fun/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://sendbox.fun/og-image.png">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(meta_desc)}">
<script type="application/ld+json">{json.dumps(structured)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb_schema)}</script>
<style>{shared_css()}</style>
</head>
<body>
{shared_nav()}
<main>
  <div class="breadcrumbs">
    <a href="/">Home</a><span>›</span>
    <a href="/category/{esc(primary_cat)}">{esc(cat_meta['label'])}</a><span>›</span>
    <span>{name}</span>
  </div>
  <div class="tool-header">
    <div class="tool-main">
      {logo_img(agent['url'], 'tool-logo-hero')}
      <h1>{name}</h1>
      <div class="tags">{cat_tags}</div>
      <p class="tool-desc">{desc}</p>
      <a href="{url}" target="_blank" rel="noopener nofollow" class="btn-primary" style="max-width:240px;">Visit {name} →</a>
    </div>
    <aside class="tool-sidebar">
      <div class="meta-row"><span class="meta-label">Pricing</span><span class="meta-value">{pricing}</span></div>
      {f'<div class="meta-row"><span class="meta-label">Plan</span><span class="meta-value">{pricing_note}</span></div>' if pricing_note else ''}
      {founded_html}
      {platforms_html}
      {bestfor_html}
      <a href="{url}" target="_blank" rel="noopener nofollow" class="btn-primary">Visit website →</a>
    </aside>
  </div>
  <section class="reviews-section">
    <h2>Ratings & Reviews</h2>
    <div id="rating-summary" class="rating-summary"><span style="color:var(--text-light);font-size:14px;">Loading...</span></div>
    <div id="review-box" class="review-box"></div>
    <div id="reviews-list" class="reviews-list"></div>
  </section>
  {related_html}
</main>
{shared_footer()}
<script src="/reviews.js"></script>
</body>
</html>"""


def category_page_html(cat, agents_in_cat):
    """Generate HTML for a category listing page."""
    meta = get_category_meta(cat)
    label = meta["label"]
    icon = meta["icon"]
    desc = meta["desc"]
    count = len(agents_in_cat)

    title = f"{count} Best {label} AI Tools (2026) | sendbox.fun"
    meta_desc = f"{count} curated {label.lower()} AI tools — compare pricing, integrations, and features. {desc}"
    canonical = f"{BASE_URL}/category/{cat}"

    # Structured data
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": label, "item": canonical},
        ],
    }

    itemlist_schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{label} AI Tools",
        "numberOfItems": count,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "url": f"{BASE_URL}/tools/{a['id']}",
                "name": a["name"],
            }
            for i, a in enumerate(agents_in_cat[:50])
        ],
    }

    # Cards
    cards = []
    for a in agents_in_cat:
        cards.append(f"""<a href="/tools/{esc(a['id'])}" class="card">
  <div class="card-head">{logo_img(a['url'])}<div class="card-title-wrap"><h3>{esc(a['name'])}</h3></div></div>
  <p>{esc(a['description'][:140])}{"..." if len(a['description']) > 140 else ""}</p>
  <div class="card-meta">{esc(a.get('pricingFrom', 'See website'))}{' · ' + esc(a.get('pricingNote', '')) if a.get('pricingNote') else ''}</div>
</a>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta_desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta_desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="sendbox.fun">
<meta property="og:image" content="https://sendbox.fun/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://sendbox.fun/og-image.png">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(meta_desc)}">
<script type="application/ld+json">{json.dumps(breadcrumb_schema)}</script>
<script type="application/ld+json">{json.dumps(itemlist_schema)}</script>
<style>{shared_css()}</style>
</head>
<body>
{shared_nav()}
<main>
  <div class="breadcrumbs">
    <a href="/">Home</a><span>›</span>
    <span>{esc(label)}</span>
  </div>
  <h1>{icon} {count} Best {esc(label)} AI Tools</h1>
  <div class="intro-box">
    <p>{esc(desc)} Browse our curated list of {count} {esc(label.lower())} AI tools — every entry includes pricing, integrations, and a direct link to the product. Updated continuously as new tools launch.</p>
  </div>
  <div class="grid">{"".join(cards)}</div>
</main>
{shared_footer()}
</body>
</html>"""


def generate_sitemap(agents):
    """Generate sitemap.xml listing all pages."""
    urls = [
        {"loc": f"{BASE_URL}/", "changefreq": "daily", "priority": "1.0"},
        {"loc": f"{BASE_URL}/compare/", "changefreq": "weekly", "priority": "0.7"},
    ]
    # Category pages
    cats_seen = set()
    for a in agents:
        for c in a["categories"]:
            cats_seen.add(c)
    for c in sorted(cats_seen):
        urls.append({"loc": f"{BASE_URL}/category/{c}", "changefreq": "daily", "priority": "0.8"})
    # Tool pages
    for a in agents:
        urls.append({"loc": f"{BASE_URL}/tools/{a['id']}", "changefreq": "weekly", "priority": "0.6", "lastmod": a.get("lastChecked", TODAY)})
    # Comparison pages
    compare_dir = ROOT / "compare"
    if compare_dir.exists():
        for f in compare_dir.glob("*.html"):
            if f.stem == "index":
                continue
            urls.append({"loc": f"{BASE_URL}/compare/{f.stem}", "changefreq": "monthly", "priority": "0.7"})

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{u['loc']}</loc>")
        if "lastmod" in u:
            xml_lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        xml_lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{u['priority']}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")
    return "\n".join(xml_lines)


def generate_robots():
    return f"""User-agent: *
Allow: /
Disallow: /.vercel/
Disallow: /.git/
Disallow: /.github/
Disallow: /scraper/

Sitemap: {BASE_URL}/sitemap.xml
"""


def main():
    print("=" * 60)
    print("sendbox.fun Static Page Generator")
    print("=" * 60)

    # Load data
    with open(AGENTS_JSON) as f:
        data = json.load(f)
    agents = data["agents"]
    print(f"Loaded {len(agents)} agents from agents.json")

    # Create dirs
    TOOLS_DIR.mkdir(exist_ok=True)
    CATEGORY_DIR.mkdir(exist_ok=True)

    # Remove orphaned tool pages (agents that no longer exist)
    valid_ids = {a['id'] for a in agents}
    deleted = 0
    if TOOLS_DIR.exists():
        for f in TOOLS_DIR.glob('*.html'):
            if f.stem not in valid_ids:
                f.unlink()
                deleted += 1
    if deleted:
        print(f"Removed {deleted} orphaned tool pages")

    # Generate tool pages
    print(f"\nGenerating tool pages in {TOOLS_DIR}/...")
    for a in agents:
        page = tool_page_html(a, agents)
        out = TOOLS_DIR / f"{a['id']}.html"
        out.write_text(page, encoding="utf-8")
    print(f"  Wrote {len(agents)} tool pages")

    # Generate category pages
    print(f"\nGenerating category pages in {CATEGORY_DIR}/...")
    cats = {}
    for a in agents:
        for c in a["categories"]:
            cats.setdefault(c, []).append(a)
    for c, tools in cats.items():
        page = category_page_html(c, tools)
        out = CATEGORY_DIR / f"{c}.html"
        out.write_text(page, encoding="utf-8")
    print(f"  Wrote {len(cats)} category pages")

    # Generate comparison pages
    print("\nRunning comparison page generator...")
    try:
        import generate_compare
        generate_compare.main()
    except Exception as e:
        print(f"  (skipped: {e})")

    # Generate sitemap.xml
    print("\nGenerating sitemap.xml...")
    sitemap = generate_sitemap(agents)
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  Wrote sitemap with {len(agents) + len(cats) + 1} URLs")

    # Generate robots.txt
    print("\nGenerating robots.txt...")
    (ROOT / "robots.txt").write_text(generate_robots(), encoding="utf-8")
    print(f"  Wrote robots.txt")

    print("\n" + "=" * 60)
    print(f"Done! Total: {len(agents)} tool pages + {len(cats)} category pages + sitemap + robots")
    print("=" * 60)


if __name__ == "__main__":
    main()
