"""
Generate /compare/X-vs-Y pages for popular tool matchups.
These rank well for "X vs Y" search queries.
"""
import json
import html
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
AGENTS_JSON = ROOT / "agents.json"
COMPARE_DIR = ROOT / "compare"
BASE_URL = "https://sendbox.fun"

# Curated high-value comparisons (pairs of tool IDs)
# These are queries people actually search for
COMPARISONS = [
    # AI Coding
    ("cursor", "github-copilot"),
    ("cursor", "windsurf"),
    ("cursor", "claude-code"),
    ("windsurf", "claude-code"),
    ("github-copilot", "claude-code"),
    ("tabnine", "codeium"),
    ("boltnew", "lovable"),
    ("v0", "boltnew"),
    ("aider", "cline"),
    # AI Assistants
    ("chatgpt", "claude"),
    ("claude", "gemini"),
    ("chatgpt", "gemini"),
    ("chatgpt", "perplexity"),
    ("claude", "perplexity"),
    # Sales
    ("apollo-io", "zoominfo"),
    ("apollo-io", "seamlessai"),
    ("instantly", "lemlist"),
    ("outreach", "salesloft"),
    ("hubspot-crm", "pipedrive"),
    # Social Media
    ("buffer", "hootsuite"),
    ("buffer", "later"),
    ("buffer", "metricool"),
    ("buffer", "feedhive"),
    ("metricool", "hootsuite"),
    # Video
    ("synthesia", "heygen"),
    ("descript", "riverside"),
    ("opus-clip", "descript"),
    # Ecommerce
    ("gorgias", "tidio"),
    ("gorgias", "intercom"),
    ("klaviyo", "privy"),
    # Email
    ("mailchimp", "beehiiv"),
    ("mailchimp", "convertkit"),
    ("convertkit", "beehiiv"),
    # SEO
    ("surfer-seo", "clearscope"),
    ("ahrefs", "semrush"),
    # Automation
    ("zapier", "make"),
    ("zapier", "n8n"),
    ("make", "n8n"),
    # Meetings
    ("otterai", "firefliesai"),
    ("firefliesai", "fathom"),
    # Design
    ("midjourney", "dall-e-3"),
    ("midjourney", "leonardoai"),
    ("runway", "pika"),
    # Dev Tools
    ("langchain", "llamaindex"),
    ("crewai", "autogen"),
    ("openrouter", "litellm"),
    # CRM
    ("hubspot-crm", "attio"),
    ("pipedrive", "freshsales"),
]


def esc(s):
    return html.escape(str(s) if s else "", quote=True)


def shared_css():
    return """
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --bg: #FAFAF9; --card: #FFF; --text: #1A1A2E; --text-light: #6B7280; --accent: #7C3AED; --accent-light: #EDE9FE; --accent-hover: #6D28D9; --border: #E5E7EB; --radius: 16px; --shadow-lg: 0 10px 25px rgba(0,0,0,0.08); }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
nav { position: sticky; top: 0; z-index: 100; background: rgba(250,250,249,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); padding: 0 24px; }
.nav-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 72px; }
.logo { font-size: 22px; font-weight: 800; color: var(--accent); display: flex; align-items: center; gap: 10px; text-decoration: none; }
.logo img { height: 48px; width: 48px; border-radius: 10px; }
.nav-links { display: flex; gap: 24px; }
.nav-links a { color: var(--text-light); font-size: 15px; font-weight: 500; text-decoration: none; }
main { max-width: 1100px; margin: 0 auto; padding: 48px 24px 80px; }
.breadcrumbs { font-size: 14px; color: var(--text-light); margin-bottom: 24px; }
.breadcrumbs a { color: var(--text-light); }
.breadcrumbs span { margin: 0 8px; }
h1 { font-size: clamp(32px, 5vw, 48px); font-weight: 800; margin-bottom: 16px; line-height: 1.2; }
.intro { font-size: 18px; color: var(--text-light); margin-bottom: 48px; max-width: 720px; }
.vs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 48px; }
.tool-col { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; }
.tool-col-head { display: flex; gap: 16px; align-items: center; margin-bottom: 16px; }
.tool-col-head img { width: 56px; height: 56px; border-radius: 12px; background: #F3F4F6; }
.tool-col h2 { font-size: 26px; font-weight: 800; margin-bottom: 4px; }
.tool-col h2 a { color: var(--text); }
.tool-col .cat { font-size: 13px; color: var(--accent); font-weight: 600; }
.tool-col .desc { font-size: 15px; color: var(--text-light); margin-bottom: 20px; }
.tool-col .stat-row { display: flex; justify-content: space-between; padding: 10px 0; border-top: 1px solid var(--border); font-size: 14px; }
.tool-col .stat-label { color: var(--text-light); }
.tool-col .stat-value { font-weight: 600; }
.tool-col .chip-list { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; }
.tool-col .chip { font-size: 12px; padding: 3px 10px; border-radius: 99px; background: #F3F4F6; }
.tool-col .visit-btn { display: inline-block; margin-top: 20px; padding: 12px 24px; background: var(--accent); color: white; border-radius: 99px; font-weight: 700; font-size: 14px; text-decoration: none; }
.tool-col .visit-btn:hover { background: var(--accent-hover); text-decoration: none; }
.summary { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; margin-bottom: 32px; }
.summary h2 { font-size: 24px; font-weight: 700; margin-bottom: 12px; }
.summary p { color: var(--text-light); font-size: 16px; }
.related { margin-top: 48px; }
.related h2 { font-size: 22px; font-weight: 700; margin-bottom: 16px; }
.related-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }
.related-link { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 14px 18px; text-decoration: none; color: var(--text); font-weight: 500; font-size: 14px; transition: all 0.2s; }
.related-link:hover { border-color: var(--accent); color: var(--accent); text-decoration: none; }
footer { border-top: 1px solid var(--border); padding: 32px 24px; max-width: 1200px; margin: 48px auto 0; color: var(--text-light); font-size: 14px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 16px; }
footer a { color: var(--text-light); text-decoration: none; }
@media (max-width: 720px) { .vs-grid { grid-template-columns: 1fr; } .nav-links { display: none; } }
"""


def shared_nav():
    return """<nav>
  <div class="nav-inner">
    <a href="/" class="logo"><img src="/logo.png" alt="sendbox"> sendbox.fun</a>
    <div class="nav-links">
      <a href="/#categories">Categories</a>
      <a href="/#agents">All Tools</a>
      <a href="/compare/">Compare</a>
    </div>
  </div>
</nav>"""


def shared_footer():
    return """<footer>
  <div>© 2026 sendbox.fun — The search engine for AI agents</div>
  <div><a href="/">Home</a></div>
</footer>"""


def get_domain(url):
    try:
        from urllib.parse import urlparse
        return (urlparse(url).hostname or "").replace("www.", "")
    except Exception:
        return ""


def logo_img(url, size=56):
    d = get_domain(url)
    if not d:
        return ""
    return f'<img src="https://icons.duckduckgo.com/ip3/{d}.ico" alt="" loading="lazy" onerror="this.style.visibility=\'hidden\'">'


CAT_LABELS = {
    "social": "Social Media", "sales": "Sales & CRM", "ecom": "Ecommerce",
    "content": "Content", "email": "Email", "seo": "SEO", "video": "Video",
    "automation": "Automation", "customer-service": "Customer Service",
    "analytics": "Analytics", "ads": "Advertising", "design": "Design",
    "assistant": "AI Assistant", "coding": "AI Coding", "dev-tools": "Dev Tools",
    "productivity": "Productivity", "research": "Research",
}


def generate_summary(a, b):
    """Generate a short comparison summary."""
    a_price = a.get("pricingFrom", "See website")
    b_price = b.get("pricingFrom", "See website")
    a_cat = CAT_LABELS.get(a["categories"][0] if a["categories"] else "", "AI tool")
    b_cat = CAT_LABELS.get(b["categories"][0] if b["categories"] else "", "AI tool")

    # Detect same or different category
    if set(a["categories"]) & set(b["categories"]):
        main_point = f"Both are {a_cat.lower()} tools that target similar use cases."
    else:
        main_point = f"{a['name']} is a {a_cat.lower()} tool, while {b['name']} focuses on {b_cat.lower()}."

    # Price comparison
    price_line = f"Pricing: {a['name']} starts at {a_price}, {b['name']} starts at {b_price}."

    return f"{main_point} {price_line}"


def render_tool_col(agent):
    name = esc(agent["name"])
    cat = CAT_LABELS.get(agent["categories"][0] if agent["categories"] else "", "AI tool")
    desc = esc(agent["description"])
    pricing = esc(agent.get("pricingFrom", "See website"))
    pricing_note = esc(agent.get("pricingNote", ""))
    founded = esc(agent.get("founded", "—") or "—")
    platforms = agent.get("platforms", []) or []
    best_for = agent.get("bestFor", []) or []
    url = esc(agent["url"])

    platforms_html = ""
    if platforms:
        chips = "".join(f'<span class="chip">{esc(p)}</span>' for p in platforms[:6])
        platforms_html = f'<div class="stat-row"><span class="stat-label">Works with</span></div><div class="chip-list">{chips}</div>'

    bestfor_html = ""
    if best_for:
        chips = "".join(f'<span class="chip">{esc(b)}</span>' for b in best_for[:4])
        bestfor_html = f'<div class="stat-row"><span class="stat-label">Best for</span></div><div class="chip-list">{chips}</div>'

    return f"""<div class="tool-col">
  <div class="tool-col-head">{logo_img(agent['url'])}<div><h2><a href="/tools/{esc(agent['id'])}">{name}</a></h2><div class="cat">{esc(cat)}</div></div></div>
  <p class="desc">{desc}</p>
  <div class="stat-row"><span class="stat-label">Pricing</span><span class="stat-value">{pricing}</span></div>
  {f'<div class="stat-row"><span class="stat-label">Plan</span><span class="stat-value">{pricing_note}</span></div>' if pricing_note else ''}
  <div class="stat-row"><span class="stat-label">Founded</span><span class="stat-value">{founded}</span></div>
  {platforms_html}
  {bestfor_html}
  <a href="{url}" target="_blank" rel="noopener nofollow" class="visit-btn">Visit {name} →</a>
</div>"""


def render_comparison(a, b, all_agents):
    title = f"{a['name']} vs {b['name']}: Which AI Tool Is Better? (2026)"
    meta_desc = f"Compare {a['name']} and {b['name']} side by side. See pricing, features, integrations, and which one fits your business. Updated for 2026."
    canonical = f"{BASE_URL}/compare/{a['id']}-vs-{b['id']}"
    summary = generate_summary(a, b)

    # Related comparisons: other pairs involving either tool
    related = []
    seen = {f"{a['id']}-{b['id']}", f"{b['id']}-{a['id']}"}
    for x, y in COMPARISONS:
        key = f"{x}-{y}"
        if key in seen:
            continue
        if x in (a["id"], b["id"]) or y in (a["id"], b["id"]):
            related.append((x, y))
            seen.add(key)
            if len(related) >= 6:
                break

    related_html = ""
    agents_by_id = {ag["id"]: ag for ag in all_agents}
    if related:
        links = []
        for x, y in related:
            if x in agents_by_id and y in agents_by_id:
                links.append(f'<a href="/compare/{x}-vs-{y}" class="related-link">{esc(agents_by_id[x]["name"])} vs {esc(agents_by_id[y]["name"])}</a>')
        if links:
            related_html = f"""<div class="related"><h2>More comparisons</h2><div class="related-grid">{"".join(links)}</div></div>"""

    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": "Compare", "item": f"{BASE_URL}/compare"},
            {"@type": "ListItem", "position": 3, "name": f"{a['name']} vs {b['name']}", "item": canonical},
        ],
    }

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
<script type="application/ld+json">{json.dumps(breadcrumb)}</script>
<style>{shared_css()}</style>
</head>
<body>
{shared_nav()}
<main>
  <div class="breadcrumbs"><a href="/">Home</a><span>›</span><a href="/compare">Compare</a><span>›</span><span>{esc(a['name'])} vs {esc(b['name'])}</span></div>
  <h1>{esc(a['name'])} vs {esc(b['name'])}</h1>
  <p class="intro">A side-by-side comparison of {esc(a['name'])} and {esc(b['name'])} — pricing, features, integrations, and which one is right for your business.</p>
  <div class="summary">
    <h2>Quick take</h2>
    <p>{esc(summary)}</p>
  </div>
  <div class="vs-grid">
    {render_tool_col(a)}
    {render_tool_col(b)}
  </div>
  {related_html}
</main>
{shared_footer()}
</body>
</html>"""


def render_compare_index(pairs, agents_by_id):
    """Generate /compare/ index page listing all comparisons."""
    title = "Compare AI Tools — Side-by-Side Comparisons | sendbox.fun"
    meta_desc = f"Compare {len(pairs)} pairs of AI tools side by side. See pricing, features, and integrations. Free comparisons updated for 2026."
    canonical = f"{BASE_URL}/compare/"

    groups = {}
    for a_id, b_id in pairs:
        if a_id not in agents_by_id or b_id not in agents_by_id:
            continue
        a = agents_by_id[a_id]
        b = agents_by_id[b_id]
        cat = a["categories"][0] if a["categories"] else "other"
        label = CAT_LABELS.get(cat, cat.title())
        groups.setdefault(label, []).append((a, b))

    sections = []
    for label in sorted(groups.keys()):
        items = groups[label]
        cards = []
        for a, b in items:
            cards.append(f'<a href="/compare/{esc(a["id"])}-vs-{esc(b["id"])}" class="related-link">{esc(a["name"])} vs {esc(b["name"])}</a>')
        sections.append(f'<div class="related"><h2>{esc(label)}</h2><div class="related-grid">{"".join(cards)}</div></div>')

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
<meta property="og:image" content="https://sendbox.fun/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://sendbox.fun/og-image.png">
<style>{shared_css()}</style>
</head>
<body>
{shared_nav()}
<main>
  <div class="breadcrumbs"><a href="/">Home</a><span>›</span><span>Compare</span></div>
  <h1>Compare AI Tools</h1>
  <p class="intro">Side-by-side comparisons of popular AI tools. See pricing, features, integrations, and which one fits your business better.</p>
  {"".join(sections)}
</main>
{shared_footer()}
</body>
</html>"""


def main():
    with open(AGENTS_JSON) as f:
        data = json.load(f)
    agents = data["agents"]
    by_id = {a["id"]: a for a in agents}

    COMPARE_DIR.mkdir(exist_ok=True)

    print(f"Loaded {len(agents)} agents")
    print(f"Generating comparison pages in {COMPARE_DIR}/...")

    generated = 0
    missing = []
    for a_id, b_id in COMPARISONS:
        if a_id not in by_id:
            missing.append(a_id)
            continue
        if b_id not in by_id:
            missing.append(b_id)
            continue
        page = render_comparison(by_id[a_id], by_id[b_id], agents)
        out = COMPARE_DIR / f"{a_id}-vs-{b_id}.html"
        out.write_text(page, encoding="utf-8")
        generated += 1

    # Index page
    index = render_compare_index(COMPARISONS, by_id)
    (COMPARE_DIR / "index.html").write_text(index, encoding="utf-8")

    print(f"  Wrote {generated} comparison pages + index")
    if missing:
        print(f"\nMissing tool IDs (skipped): {set(missing)}")

    return generated


if __name__ == "__main__":
    main()
