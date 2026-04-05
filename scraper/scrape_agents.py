"""
sendbox.fun Agent Scraper
=========================
Scrapes AI agent directories from GitHub awesome-lists (curated markdown lists)
and adds new agents to agents.json. Runs every 6 hours via GitHub Actions.

Sources:
- e2b-dev/awesome-ai-agents       (400+ agents, updated weekly)
- jim-schwoebel/awesome_ai_agents (1500+ resources)
- kyrolabs/awesome-agents          (framework-focused)
- slavakurilyak/awesome-ai-agents  (general)

These are markdown files on GitHub that are actively maintained. They're
stable, don't require API keys, and structure changes are rare.

Usage:
  python scraper/scrape_agents.py                 # Scrape all sources, save
  python scraper/scrape_agents.py --dry-run       # Preview without saving
  python scraper/scrape_agents.py --source e2b    # One source only

Requirements:
  pip install requests
"""

import json
import os
import re
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install dependencies first: pip install requests")
    sys.exit(1)

# ============================================================
# CONFIG
# ============================================================

AGENTS_JSON_PATH = Path(__file__).parent.parent / "agents.json"
USER_AGENT = "sendbox.fun Agent Scraper/2.0 (contact@sendbox.fun)"
HEADERS = {"User-Agent": USER_AGENT}
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Awesome-list sources on GitHub (raw markdown)
SOURCES = {
    "e2b": {
        "url": "https://raw.githubusercontent.com/e2b-dev/awesome-ai-agents/main/README.md",
        "name": "e2b-dev/awesome-ai-agents",
    },
    "jim": {
        "url": "https://raw.githubusercontent.com/jim-schwoebel/awesome_ai_agents/main/README.md",
        "name": "jim-schwoebel/awesome_ai_agents",
    },
    "kyrolabs": {
        "url": "https://raw.githubusercontent.com/kyrolabs/awesome-agents/main/README.md",
        "name": "kyrolabs/awesome-agents",
    },
    "slava": {
        "url": "https://raw.githubusercontent.com/slavakurilyak/awesome-ai-agents/main/README.md",
        "name": "slavakurilyak/awesome-ai-agents",
    },
}

# Category guessing keywords
CATEGORY_KEYWORDS = {
    "social": ["social media", "instagram", "tiktok", "twitter", "linkedin", "content scheduling", "followers", "posting"],
    "sales": ["sales", "crm", "lead", "pipeline", "outreach", "deal", "prospecting", "cold email", "b2b"],
    "ecom": ["ecommerce", "e-commerce", "shopify", "woocommerce", "etsy", "retail", "inventory", "product descriptions", "cart"],
    "content": ["copywriting", "blog post", "article writing", "content generation", "writing assistant", "text generation"],
    "email": ["email marketing", "newsletter", "cold email", "email automation", "email sequence"],
    "seo": ["seo", "keyword", "search engine", "rank tracking", "backlink"],
    "video": ["video editor", "video generation", "avatar video", "text-to-video", "video editing", "viral video"],
    "automation": ["workflow automation", "zapier alternative", "no-code", "low-code", "integration platform"],
    "customer-service": ["customer support", "helpdesk", "ticketing", "live chat", "customer service"],
    "analytics": ["analytics", "dashboard", "reporting", "metrics", "data visualization"],
    "ads": ["advertising", "ad campaign", "paid media", "google ads", "facebook ads"],
    "design": ["graphic design", "logo", "image generation", "illustration", "creative suite"],
    "assistant": ["general-purpose", "chatbot", "ai assistant", "chatgpt alternative"],
    "coding": ["code editor", "pair programming", "ai coding", "github copilot", "code completion", "autocomplete"],
    "dev-tools": ["framework", "sdk", "api", "vector database", "rag", "llm gateway", "observability"],
    "productivity": ["note-taking", "meeting notes", "calendar", "scheduling", "task management", "project management"],
    "research": ["research assistant", "academic", "literature", "web search", "semantic search"],
}


def make_id(name):
    """Create a URL-safe ID from a name."""
    s = name.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[-\s]+', '-', s)
    return s.strip('-')


def categorize(name, desc):
    """Guess category from name+description."""
    text = f"{name} {desc}".lower()
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        scores[cat] = sum(1 for kw in keywords if kw in text)
    best_cat = max(scores, key=scores.get)
    return [best_cat] if scores[best_cat] > 0 else ["dev-tools"]  # default


def make_entry(name, url, desc, source):
    """Create a standard agent entry for agents.json."""
    return {
        "id": make_id(name),
        "name": name.strip(),
        "url": url,
        "verified": False,
        "trustScore": 0,
        "description": desc.strip() or f"{name} — AI tool discovered from {source}.",
        "ourReview": "",
        "categories": categorize(name, desc),
        "subcategories": [],
        "bestFor": [],
        "platforms": [],
        "pricingModel": "unknown",
        "pricingFrom": "See website",
        "pricingNote": "",
        "stats": {"users": "N/A", "keyMetric": "N/A", "timeSaved": "N/A"},
        "affiliateLink": None,
        "founded": "",
        "addedDate": TODAY,
        "lastChecked": TODAY,
        "source": f"scraper-{source}",
    }


# ============================================================
# MARKDOWN PARSING
# ============================================================

# Match markdown links: [name](url) followed by optional description
# Pattern: "- [name](url) - description" or "* [name](url): description"
LINK_PATTERN = re.compile(
    r'[-*]\s+\[([^\]]+)\]\((https?://[^\s\)]+)\)(?:[:\s\-—]+(.+))?',
    re.MULTILINE
)


def extract_links_from_markdown(markdown_text, source_name):
    """Extract (name, url, description) tuples from markdown awesome-list format."""
    results = []
    seen_urls = set()

    # Domains/patterns to reject — these are supporting links, not products
    BLOCKED_DOMAINS = {
        'discord.com', 'discord.gg', 'twitter.com', 'x.com', 't.co',
        'facebook.com', 'instagram.com', 'linkedin.com', 'reddit.com',
        'youtube.com', 'youtu.be', 'twitch.tv', 'tiktok.com',
        'medium.com', 'substack.com', 'dev.to', 'hashnode.dev',
        'arxiv.org', 'aclanthology.org', 'openreview.net', 'acm.org',
        'wikipedia.org', 'wikidata.org',
        'huggingface.co/spaces', 'huggingface.co/datasets', 'huggingface.co/papers',
        'hub.docker.com', 'marketplace.visualstudio.com',
        'colab.research.google.com', 'colab.google.com',
        'replit.com/@', 'codesandbox.io', 'codepen.io', 'stackblitz.com/edit',
        'reworkd.ai/blog', 'producthunt.com/products',
        'news.ycombinator.com', 'ycombinator.com/companies',
        'e2b.dev/blog', '/blog/', '/posts/', '/post/', '/news/',
        'pypi.org/project', 'npmjs.com/package', 'crates.io',
        'semanticscholar.org', 'scholar.google', 'researchgate.net',
        'sites.google.com', 'docs.google.com', 'forms.gle',
        'neurips.cc', 'iclr.cc', 'icml.cc', 'aclweb.org', 'kaggle.com/datasets',
        'towardsdatascience.com', 'towardsai.net',
        '.edu/', '.ac.uk/', '.ac.jp/', 'umich.edu', 'mit.edu', 'stanford.edu',
        'github.io/courses', 'github.io/lecture', 'github.io/syllabus',
    }

    # Name prefixes/patterns that indicate a supporting link, not a product
    BLOCKED_NAME_PREFIXES = (
        'blog post', 'blog:', 'post:', 'article:', 'interview:', 'tutorial:',
        'guide:', 'video:', 'talk:', 'podcast:', 'webinar:', 'workshop:',
        'launch post', 'launch:', 'announcement:', 'introducing',
        'how to', 'how we', 'why ', 'what is', 'what are', 'the story',
        'behind the', 'deep dive', 'review:', 'reviewed:', 'compared:',
        'thread:', 'tweet:', 'video demo', 'demo video', 'live demo',
        'research paper', 'paper:', 'citation', 'case study', 'case studies',
        'features', 'docs:', 'documentation:', 'api docs', 'getting started',
        'quickstart', 'quick start', 'installation', 'changelog', 'roadmap',
        'ai features', 'ai-features', 'pricing', 'playground', 'example',
        'examples', 'samples', 'templates', 'showcase', 'gallery',
        'creator website', 'creator\'s', 'founder\'s', 'founder profile',
        'ycombinator profile', 'yc profile', 'company profile', 'profile of',
        'javascript version', 'python version', 'typescript version',
        'github repository', 'git repository', 'hackernews', 'hacker news',
        'community', 'discussions', 'meme', 'launch',
    )

    # Generic names to reject (these are link-label words, not product names)
    BLOCKED_NAMES = {
        'link', 'here', 'github', 'gitlab', 'docs', 'documentation', 'website',
        'web', 'paper', 'papers', 'demo', 'demos', 'blog', 'twitter', 'x',
        'discord', 'discord invite', 'facebook', 'instagram', 'linkedin',
        'youtube', 'youtube demo', 'video', 'videos', 'tweet', 'thread',
        'announcement', 'launch', 'post', 'article', 'homepage', 'home',
        'landing page', 'repo', 'repository', 'source', 'source code',
        'colab', 'colab demo', 'notebook', 'jupyter', 'replit',
        'vscode extension', 'extension', 'plugin', 'download', 'install',
        'hugging face', 'hugging face datasets', 'hf', 'hf hub', 'hf space',
        'docker', 'docker image', 'pypi', 'npm', 'cargo', 'gem',
        'author', "author's twitter", 'founder', "founder's twitter",
        'linkedin post', 'research paper', 'arxiv', 'citation', 'license',
        'roadmap', 'changelog', 'slack', 'telegram', 'wechat', 'kakao',
        'newsletter', 'rss', 'subscribe', 'contact', 'email',
        'original', 'archived', 'mirror', 'fork', 'preview',
        'apps', 'app store', 'play store', 'chrome extension',
        'bloop apps', 'releases', 'milestone',
    }

    for match in LINK_PATTERN.finditer(markdown_text):
        name = match.group(1).strip()
        url = match.group(2).strip().rstrip('.,;:')
        desc = (match.group(3) or "").strip()

        # Skip junk names
        name_lower = name.lower()
        if len(name) < 2 or len(name) > 60 or name_lower in BLOCKED_NAMES:
            continue
        if any(name_lower.startswith(p) for p in BLOCKED_NAME_PREFIXES):
            continue
        # Names that are just URLs/punctuation
        if name.startswith(('http://', 'https://', '@', '#')):
            continue
        # Sentence-like names = not a product
        if name.count(' ') > 5:
            continue
        # Academic/research/paper/dataset detection
        academic_terms = ['dataset', 'benchmark', 'paper', 'arxiv', 'ethics of', 'survey of',
                          'analysis of', 'towards', 'introduction to', 'lecture', 'course',
                          'thesis', 'dissertation', 'research paper', 'conference',
                          'workshop', 'symposium', 'journal', 'proceedings',
                          'simulation', 'evaluation of', 'case study', 'white paper',
                          'ai ethics', 'ai safety', 'xai ', 'explainable ai',
                          'chapter', 'part 1', 'part 2', 'module', 'curriculum',
                          'homework', 'assignment', 'tutorial series']
        if any(term in name_lower for term in academic_terms):
            continue
        # IDs that are pure technical identifiers (all lowercase with underscores, long)
        if '_' in name and name.islower() and len(name) > 25:
            continue
        # Names with dataset/research-style formatting (underscores + dashes + numbers)
        if re.search(r'\d{4}', name) and ('-' in name or '_' in name):
            continue

        # Skip blocked domains (social media, academic, dev infra links)
        url_lower = url.lower()
        if any(blocked in url_lower for blocked in BLOCKED_DOMAINS):
            continue

        # Skip image/file extensions
        if url_lower.endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.mp4', '.mp3', '.zip', '.tar.gz')):
            continue

        # Skip anchor/fragment URLs
        if url_lower.startswith('#') or '/blob/' in url_lower or '/tree/' in url_lower or '/wiki/' in url_lower:
            continue

        # Clean description
        desc = re.sub(r'!\[[^\]]*\]\([^\)]*\)', '', desc)
        desc = re.sub(r'\[[^\]]*\]\([^\)]*\)', '', desc)
        desc = re.sub(r'<[^>]+>', '', desc)  # strip HTML tags
        desc = desc.strip(' -.,;:*"')
        if len(desc) > 300:
            desc = desc[:297] + "..."

        # Normalize URL for dedup
        norm_url = url.lower().rstrip('/')
        if norm_url in seen_urls:
            continue
        seen_urls.add(norm_url)

        results.append((name, url, desc))

    return results


def scrape_source(source_key):
    """Fetch and parse a single GitHub awesome-list source."""
    source = SOURCES[source_key]
    print(f"\nScraping {source['name']}...")
    print(f"  URL: {source['url']}")

    try:
        resp = requests.get(source['url'], headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            print(f"  ERROR: Got status {resp.status_code}")
            return []

        links = extract_links_from_markdown(resp.text, source['name'])
        print(f"  Found {len(links)} links")

        agents = [make_entry(name, url, desc, source_key) for name, url, desc in links]
        return agents

    except requests.Timeout:
        print(f"  ERROR: Timeout")
        return []
    except Exception as e:
        print(f"  ERROR: {e}")
        return []


# ============================================================
# MAIN
# ============================================================

def load_existing():
    if AGENTS_JSON_PATH.exists():
        with open(AGENTS_JSON_PATH) as f:
            return json.load(f)
    return {"lastUpdated": None, "agents": []}


def save_agents(data):
    data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    with open(AGENTS_JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nSaved {len(data['agents'])} agents to {AGENTS_JSON_PATH}")


def merge_agent(existing_list, existing_ids, existing_urls, new_agent):
    """Add agent if new, skip if already exists. Preserves manual reviews."""
    nid = new_agent["id"]
    nurl = new_agent["url"].lower().rstrip('/')

    if nid in existing_ids or nurl in existing_urls:
        return "skipped"

    existing_list.append(new_agent)
    existing_ids.add(nid)
    existing_urls.add(nurl)
    return "added"


def main():
    parser = argparse.ArgumentParser(description="sendbox.fun Agent Scraper")
    parser.add_argument("--source", choices=list(SOURCES.keys()), help="Scrape one source only")
    parser.add_argument("--dry-run", action="store_true", help="Preview results without saving")
    parser.add_argument("--max-new", type=int, default=500, help="Max new agents to add per run (default 500)")
    args = parser.parse_args()

    print("=" * 60)
    print("sendbox.fun Agent Scraper v2.0")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    # Load existing data
    data = load_existing()
    existing_ids = {a["id"] for a in data["agents"]}
    existing_urls = {a["url"].lower().rstrip('/') for a in data["agents"]}
    print(f"Existing agents: {len(data['agents'])}")

    # Run scrapers
    sources = [args.source] if args.source else list(SOURCES.keys())
    all_scraped = []
    for src in sources:
        scraped = scrape_source(src)
        all_scraped.extend(scraped)

    # Merge (preserve existing entries)
    added = 0
    skipped = 0
    for agent in all_scraped:
        if added >= args.max_new:
            break
        result = merge_agent(data["agents"], existing_ids, existing_urls, agent)
        if result == "added":
            added += 1
        else:
            skipped += 1

    print("\n" + "=" * 60)
    print(f"Results: {added} new agents added, {skipped} skipped (duplicates)")
    print(f"Total agents in database: {len(data['agents'])}")

    if args.dry_run:
        print("\n[DRY RUN] Not saving. Sample of new agents:")
        new_ones = [a for a in data["agents"] if a["addedDate"] == TODAY and a["source"].startswith("scraper")][:20]
        for a in new_ones:
            print(f"  - {a['name']} ({a['categories'][0]}) -> {a['url']}")
    else:
        save_agents(data)

    print("=" * 60)


if __name__ == "__main__":
    main()
