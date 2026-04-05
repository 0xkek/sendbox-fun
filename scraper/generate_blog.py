"""
Auto-generate blog posts from the agents database.
Posts:
- Weekly digest: "New AI agents added this week"
- Category spotlights: "Best [category] AI tools (2026)"
"""
import json
import html
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
AGENTS_JSON = ROOT / "agents.json"
BLOG_DIR = ROOT / "blog"
BASE_URL = "https://sendbox.fun"
TODAY = datetime.now(timezone.utc).date()


def esc(s):
    return html.escape(str(s) if s else "", quote=True)


def get_domain(url):
    try:
        from urllib.parse import urlparse
        return (urlparse(url).hostname or "").replace("www.", "")
    except Exception:
        return ""


def logo_img(url):
    d = get_domain(url)
    if not d:
        return ""
    return f'<img src="https://icons.duckduckgo.com/ip3/{d}.ico" alt="" loading="lazy" onerror="this.style.visibility=\'hidden\'">'


CAT_LABELS = {
    "social": "Social Media", "sales": "Sales & CRM", "ecom": "Ecommerce",
    "content": "Content", "email": "Email", "seo": "SEO", "video": "Video",
    "automation": "Automation", "customer-service": "Customer Service",
    "analytics": "Analytics", "ads": "Advertising", "design": "Design",
    "assistant": "AI Assistants", "coding": "AI Coding", "dev-tools": "Dev Tools",
    "productivity": "Productivity", "research": "Research",
}


def shared_css():
    return """
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --bg: #FAFAF9; --card: #FFF; --text: #1A1A2E; --text-light: #6B7280; --accent: #7C3AED; --accent-light: #EDE9FE; --accent-hover: #6D28D9; --border: #E5E7EB; --radius: 16px; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
nav { position: sticky; top: 0; z-index: 100; background: rgba(250,250,249,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); padding: 0 24px; }
.nav-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 72px; }
.logo { font-size: 22px; font-weight: 800; color: var(--accent); display: flex; align-items: center; gap: 10px; text-decoration: none; }
.logo img { height: 48px; width: 48px; border-radius: 10px; }
.nav-links { display: flex; gap: 24px; }
.nav-links a { color: var(--text-light); font-size: 15px; font-weight: 500; text-decoration: none; }
main { max-width: 760px; margin: 0 auto; padding: 48px 24px 80px; }
.breadcrumbs { font-size: 14px; color: var(--text-light); margin-bottom: 24px; }
.breadcrumbs a { color: var(--text-light); }
.breadcrumbs span { margin: 0 8px; }
article h1 { font-size: clamp(32px, 5vw, 44px); font-weight: 800; margin-bottom: 12px; line-height: 1.2; }
.post-meta { color: var(--text-light); font-size: 14px; margin-bottom: 32px; }
article h2 { font-size: 26px; font-weight: 700; margin: 40px 0 16px; }
article p { margin-bottom: 16px; color: var(--text); }
.tool-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; margin-bottom: 20px; }
.tool-card-head { display: flex; gap: 14px; align-items: flex-start; margin-bottom: 12px; }
.tool-card-head img { width: 48px; height: 48px; border-radius: 10px; flex-shrink: 0; background: #F3F4F6; }
.tool-card h3 { font-size: 20px; font-weight: 700; margin-bottom: 2px; }
.tool-card h3 a { color: var(--text); }
.tool-card .cat { font-size: 13px; color: var(--accent); font-weight: 600; }
.tool-card p { font-size: 15px; color: var(--text-light); margin-bottom: 12px; }
.tool-card .meta-row { display: flex; gap: 16px; font-size: 13px; color: var(--text-light); }
.tool-card .meta-row strong { color: var(--text); }
.blog-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 28px; margin-bottom: 16px; text-decoration: none; color: inherit; display: block; transition: all 0.2s; }
.blog-card:hover { border-color: var(--accent); text-decoration: none; }
.blog-card h2 { font-size: 22px; font-weight: 700; margin-bottom: 8px; color: var(--text); }
.blog-card p { font-size: 15px; color: var(--text-light); margin-bottom: 8px; }
.blog-card .date { font-size: 13px; color: var(--text-light); }
footer { border-top: 1px solid var(--border); padding: 32px 24px; max-width: 1200px; margin: 48px auto 0; color: var(--text-light); font-size: 14px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 16px; }
footer a { color: var(--text-light); text-decoration: none; }
@media (max-width: 640px) { .nav-links { display: none; } }
"""


def shared_nav():
    return """<nav>
  <div class="nav-inner">
    <a href="/" class="logo"><img src="/logo.png" alt="sendbox"> sendbox.fun</a>
    <div class="nav-links">
      <a href="/#categories">Categories</a>
      <a href="/#agents">All Tools</a>
      <a href="/compare/">Compare</a>
      <a href="/blog/">Blog</a>
    </div>
  </div>
</nav>"""


def shared_footer():
    return """<footer>
  <div>© 2026 sendbox.fun — The search engine for AI agents</div>
  <div><a href="/">Home</a> · <a href="/blog/">Blog</a></div>
</footer>"""


def tool_card_html(agent):
    cat = agent["categories"][0] if agent["categories"] else "dev-tools"
    cat_label = CAT_LABELS.get(cat, "AI tool")
    return f"""<div class="tool-card">
  <div class="tool-card-head">{logo_img(agent['url'])}<div style="flex:1;min-width:0;"><h3><a href="/tools/{esc(agent['id'])}">{esc(agent['name'])}</a></h3><div class="cat">{esc(cat_label)}</div></div></div>
  <p>{esc(agent['description'][:200])}{"..." if len(agent['description']) > 200 else ""}</p>
  <div class="meta-row">
    <span><strong>{esc(agent.get('pricingFrom', 'See website'))}</strong></span>
    {f"<span>{esc(agent.get('pricingNote', ''))}</span>" if agent.get('pricingNote') else ''}
  </div>
</div>"""


def render_post(title, slug, meta_desc, body_html, date_str):
    canonical = f"{BASE_URL}/blog/{slug}"
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": meta_desc,
        "datePublished": date_str,
        "author": {"@type": "Organization", "name": "sendbox.fun"},
        "publisher": {"@type": "Organization", "name": "sendbox.fun", "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/logo.png"}},
        "url": canonical,
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} | sendbox.fun</title>
<meta name="description" content="{esc(meta_desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta_desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://sendbox.fun/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://sendbox.fun/og-image.png">
<script type="application/ld+json">{json.dumps(schema)}</script>
<style>{shared_css()}</style>
</head>
<body>
{shared_nav()}
<main>
  <div class="breadcrumbs"><a href="/">Home</a><span>›</span><a href="/blog">Blog</a><span>›</span><span>{esc(title)}</span></div>
  <article>
    <h1>{esc(title)}</h1>
    <div class="post-meta">Published {esc(date_str)} · sendbox.fun</div>
    {body_html}
  </article>
</main>
{shared_footer()}
</body>
</html>"""


def render_blog_index(posts):
    title = "Blog — New AI tools every week | sendbox.fun"
    meta_desc = "Weekly posts on the newest AI agents and tools. Comparisons, deep-dives, and curated picks across 17 categories."

    cards = []
    for p in posts:
        cards.append(f"""<a href="/blog/{esc(p['slug'])}" class="blog-card">
  <h2>{esc(p['title'])}</h2>
  <p>{esc(p['excerpt'])}</p>
  <div class="date">{esc(p['date'])}</div>
</a>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta_desc)}">
<link rel="canonical" href="{BASE_URL}/blog/">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta_desc)}">
<meta property="og:url" content="{BASE_URL}/blog/">
<meta property="og:image" content="https://sendbox.fun/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://sendbox.fun/og-image.png">
<style>{shared_css()}</style>
</head>
<body>
{shared_nav()}
<main>
  <div class="breadcrumbs"><a href="/">Home</a><span>›</span><span>Blog</span></div>
  <article>
    <h1>Blog</h1>
    <div class="post-meta">Weekly picks and digests from the world of AI tools.</div>
    {"".join(cards) if cards else '<p>No posts yet.</p>'}
  </article>
</main>
{shared_footer()}
</body>
</html>"""


def weekly_digest(agents):
    """Generate a weekly digest post of newest agents."""
    # Find agents added in the last 7 days
    cutoff = TODAY - timedelta(days=7)
    recent = []
    for a in agents:
        added = a.get("addedDate", "")
        try:
            d = datetime.strptime(added, "%Y-%m-%d").date()
            if d >= cutoff:
                recent.append((d, a))
        except Exception:
            pass

    # Sort newest first, limit to 15
    recent.sort(key=lambda x: x[0], reverse=True)
    recent = [a for _, a in recent[:15]]

    if len(recent) < 3:
        # Fallback: use most recently added overall
        all_with_dates = []
        for a in agents:
            try:
                d = datetime.strptime(a.get("addedDate", ""), "%Y-%m-%d").date()
                all_with_dates.append((d, a))
            except Exception:
                pass
        all_with_dates.sort(key=lambda x: x[0], reverse=True)
        recent = [a for _, a in all_with_dates[:10]]

    if not recent:
        return None

    date_str = TODAY.strftime("%B %d, %Y")
    year, week, _ = TODAY.isocalendar()
    slug = f"new-ai-tools-week-{year}-{week}"
    title = f"{len(recent)} new AI tools we added this week"
    meta_desc = f"The latest AI agents added to sendbox.fun — {len(recent)} new tools across categories including {', '.join(CAT_LABELS.get(recent[0]['categories'][0], 'various').lower() for _ in range(1))}. Discover what's new in AI this week."

    intro = f"""<p>We added <strong>{len(recent)} new AI tools</strong> to sendbox.fun this week. Here's what's worth your attention:</p>"""

    cards_html = "\n".join(tool_card_html(a) for a in recent)

    outro = f"""<h2>Discover more</h2>
<p>Browse the full directory of <a href="/#agents">{len(agents):,} AI tools</a> or filter by <a href="/#categories">category</a> to find exactly what you need.</p>"""

    body = f"{intro}\n{cards_html}\n{outro}"

    return {
        "slug": slug,
        "title": title,
        "meta_desc": meta_desc,
        "body": body,
        "date": date_str,
        "excerpt": f"{len(recent)} fresh AI tools added this week across {len(set(a['categories'][0] for a in recent if a['categories']))} categories. See what's new.",
    }


def category_spotlight(agents, cat):
    """Generate a category best-of post."""
    cat_tools = [a for a in agents if cat in a.get("categories", [])]
    if len(cat_tools) < 5:
        return None

    # Pick top 10 (for now: first 10 by name; later: by rating when reviews grow)
    cat_tools.sort(key=lambda a: a["name"].lower())
    featured = cat_tools[:10]

    cat_label = CAT_LABELS.get(cat, cat.title())
    year = TODAY.year
    slug = f"best-{cat}-ai-tools-{year}"
    title = f"10 best {cat_label.lower()} AI tools for 2026"
    meta_desc = f"The top {cat_label.lower()} AI tools in 2026 — {', '.join(a['name'] for a in featured[:3])}, and more. Pricing, features, and integrations compared."
    date_str = TODAY.strftime("%B %d, %Y")

    intro = f"""<p>Looking for the best {cat_label.lower()} AI tools? We've curated {len(cat_tools)} options across the sendbox.fun directory. Here are 10 worth your attention — each with pricing, integrations, and what they're built for.</p>"""

    cards_html = "\n".join(tool_card_html(a) for a in featured)

    outro = f"""<h2>See the full list</h2>
<p>There are <a href="/category/{cat}">{len(cat_tools)} {cat_label.lower()} tools</a> in the sendbox.fun directory. Filter by price, popularity, or recency to find the right one.</p>"""

    body = f"{intro}\n{cards_html}\n{outro}"

    return {
        "slug": slug,
        "title": title,
        "meta_desc": meta_desc,
        "body": body,
        "date": date_str,
        "excerpt": f"The top 10 {cat_label.lower()} AI tools worth your attention in 2026.",
    }


def main():
    with open(AGENTS_JSON) as f:
        data = json.load(f)
    agents = data["agents"]

    BLOG_DIR.mkdir(exist_ok=True)

    posts = []

    # 1. Weekly digest
    weekly = weekly_digest(agents)
    if weekly:
        page = render_post(weekly["title"], weekly["slug"], weekly["meta_desc"], weekly["body"], weekly["date"])
        (BLOG_DIR / f"{weekly['slug']}.html").write_text(page, encoding="utf-8")
        posts.append(weekly)
        print(f"Wrote: {weekly['slug']}")

    # 2. Category spotlights (one per category, only generates new ones)
    for cat in CAT_LABELS.keys():
        post = category_spotlight(agents, cat)
        if post:
            out = BLOG_DIR / f"{post['slug']}.html"
            if not out.exists():  # don't regenerate if already exists
                page = render_post(post["title"], post["slug"], post["meta_desc"], post["body"], post["date"])
                out.write_text(page, encoding="utf-8")
                posts.append(post)
                print(f"Wrote: {post['slug']}")
            else:
                # Still include in index
                posts.append(post)

    # Sort posts: newest first (weekly digests first, then category spotlights)
    posts.sort(key=lambda p: (p["slug"].startswith("new-"), p["date"]), reverse=True)

    # 3. Blog index
    index_html = render_blog_index(posts)
    (BLOG_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"Wrote: blog/index.html with {len(posts)} posts")

    return posts


if __name__ == "__main__":
    main()
