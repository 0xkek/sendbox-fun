"""
sendbox.fun Agent Scraper
=========================
Scrapes AI agent directories and outputs to agents.json.
Run manually or on a cron schedule.

Usage:
  python scrape_agents.py                    # Scrape all sources
  python scrape_agents.py --source aiagentstore  # Scrape specific source
  python scrape_agents.py --dry-run          # Preview without saving

Requirements:
  pip install requests beautifulsoup4

NOTE: This scraper is a starting framework. The actual CSS selectors
will need updating as directory sites change their layouts. The core
logic (fetch -> parse -> merge -> save) stays the same.
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install dependencies first: pip install requests beautifulsoup4")
    sys.exit(1)

# ============================================================
# CONFIG
# ============================================================

AGENTS_JSON_PATH = Path(__file__).parent.parent / "agents.json"
USER_AGENT = "sendbox.fun Agent Scraper/1.0 (contact@sendbox.fun)"

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml",
}

# Category mapping keywords
CATEGORY_KEYWORDS = {
    "social": ["social media", "instagram", "tiktok", "twitter", "content", "posting",
               "scheduling", "followers", "engagement", "influencer", "reels", "youtube"],
    "sales": ["sales", "crm", "lead", "pipeline", "outreach", "deal", "revenue",
              "prospecting", "follow-up", "cold email", "b2b"],
    "ecom": ["ecommerce", "e-commerce", "shopify", "woocommerce", "etsy", "retail",
             "inventory", "pricing", "product", "shopping", "store", "cart", "checkout"],
}


# ============================================================
# HELPERS
# ============================================================

def categorize_agent(name, description):
    """Guess category based on name and description."""
    text = f"{name} {description}".lower()
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        scores[cat] = sum(1 for kw in keywords if kw in text)
    best = max(scores, key=scores.get)
    return [best] if scores[best] > 0 else ["general"]


def load_existing_agents():
    """Load the current agents.json file."""
    if AGENTS_JSON_PATH.exists():
        with open(AGENTS_JSON_PATH) as f:
            return json.load(f)
    return {"lastUpdated": None, "agents": []}


def save_agents(data):
    """Save agents data to JSON."""
    data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    with open(AGENTS_JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data['agents'])} agents to {AGENTS_JSON_PATH}")


def merge_agent(existing_agents, new_agent):
    """Merge a new agent into the existing list. Update if exists, add if new."""
    for i, a in enumerate(existing_agents):
        if a["id"] == new_agent["id"]:
            # Preserve our manual reviews and trust scores
            new_agent["ourReview"] = a.get("ourReview", new_agent.get("ourReview", ""))
            new_agent["trustScore"] = a.get("trustScore", new_agent.get("trustScore", 0))
            new_agent["verified"] = a.get("verified", False)
            existing_agents[i] = new_agent
            return "updated"
    existing_agents.append(new_agent)
    return "added"


def make_id(name):
    """Create a URL-safe ID from an agent name."""
    return name.lower().strip().replace(" ", "-").replace(".", "")


def make_agent_template(name, url, description, source):
    """Create a standard agent entry."""
    return {
        "id": make_id(name),
        "name": name,
        "url": url,
        "verified": False,
        "trustScore": 0,
        "description": description,
        "ourReview": "",
        "categories": categorize_agent(name, description),
        "subcategories": [],
        "bestFor": [],
        "platforms": [],
        "pricingModel": "unknown",
        "pricingFrom": "See website",
        "pricingNote": "",
        "stats": {"users": "N/A", "keyMetric": "N/A", "timeSaved": "N/A"},
        "affiliateLink": None,
        "founded": "",
        "addedDate": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "lastChecked": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "source": source,
    }


# ============================================================
# SCRAPERS
# ============================================================

def scrape_aiagentstore():
    """
    Scrape AI Agent Store (aiagentstore.ai).

    NOTE: This scraper uses CSS selectors that may need updating
    if the site changes its layout. Check the site manually and
    update selectors as needed.
    """
    print("Scraping AI Agent Store...")
    agents = []

    # Scrape category pages
    categories_to_scrape = [
        "https://aiagentstore.ai/category/marketing",
        "https://aiagentstore.ai/category/sales",
        "https://aiagentstore.ai/category/customer-support",
        "https://aiagentstore.ai/category/ecommerce",
    ]

    for url in categories_to_scrape:
        try:
            print(f"  Fetching {url}...")
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"  Warning: Got status {resp.status_code} for {url}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            # Look for agent cards — these selectors will need updating
            # based on the actual site structure
            cards = soup.select("article, .agent-card, [data-agent], .card")

            for card in cards:
                # Try to extract name
                name_el = card.select_one("h2, h3, .title, .agent-name")
                if not name_el:
                    continue
                name = name_el.get_text(strip=True)

                # Try to extract link
                link_el = card.select_one("a[href]")
                agent_url = link_el["href"] if link_el else ""
                if agent_url and not agent_url.startswith("http"):
                    agent_url = "https://aiagentstore.ai" + agent_url

                # Try to extract description
                desc_el = card.select_one("p, .description, .summary")
                desc = desc_el.get_text(strip=True) if desc_el else ""

                if name and len(name) > 2:
                    agent = make_agent_template(name, agent_url, desc, "aiagentstore")
                    agents.append(agent)

            print(f"  Found {len(cards)} potential agents on {url}")

        except Exception as e:
            print(f"  Error scraping {url}: {e}")

    print(f"AI Agent Store: {len(agents)} agents found")
    return agents


def scrape_producthunt():
    """
    Scrape Product Hunt AI Agents category.

    NOTE: Product Hunt has anti-scraping measures. For production use,
    consider using their official API (https://api.producthunt.com).
    You'll need a developer token.
    """
    print("Scraping Product Hunt AI Agents category...")
    agents = []

    url = "https://www.producthunt.com/categories/ai-agents"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  Warning: Got status {resp.status_code}")
            print("  Tip: Product Hunt may require API access. Get a token at api.producthunt.com")
            return agents

        soup = BeautifulSoup(resp.text, "html.parser")

        # Product Hunt product cards
        cards = soup.select("[data-test='product-item'], .product-item, article")

        for card in cards:
            name_el = card.select_one("h3, .name, [data-test='product-name']")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)

            desc_el = card.select_one("p, .tagline, [data-test='product-tagline']")
            desc = desc_el.get_text(strip=True) if desc_el else ""

            link_el = card.select_one("a[href*='/posts/']")
            agent_url = ""
            if link_el:
                agent_url = "https://www.producthunt.com" + link_el["href"] if not link_el["href"].startswith("http") else link_el["href"]

            if name:
                agent = make_agent_template(name, agent_url, desc, "producthunt")
                agents.append(agent)

        print(f"  Found {len(cards)} potential agents")

    except Exception as e:
        print(f"  Error: {e}")

    print(f"Product Hunt: {len(agents)} agents found")
    return agents


def scrape_aiagentslist():
    """
    Scrape AI Agents List (aiagentslist.com).
    """
    print("Scraping AI Agents List...")
    agents = []

    url = "https://aiagentslist.com/"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  Warning: Got status {resp.status_code}")
            return agents

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("article, .agent-card, .tool-card, [data-tool]")

        for card in cards:
            name_el = card.select_one("h2, h3, .title")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)

            desc_el = card.select_one("p, .description")
            desc = desc_el.get_text(strip=True) if desc_el else ""

            link_el = card.select_one("a[href]")
            agent_url = link_el["href"] if link_el else ""

            if name:
                agent = make_agent_template(name, agent_url, desc, "aiagentslist")
                agents.append(agent)

    except Exception as e:
        print(f"  Error: {e}")

    print(f"AI Agents List: {len(agents)} agents found")
    return agents


# ============================================================
# MAIN
# ============================================================

SCRAPERS = {
    "aiagentstore": scrape_aiagentstore,
    "producthunt": scrape_producthunt,
    "aiagentslist": scrape_aiagentslist,
}


def main():
    parser = argparse.ArgumentParser(description="sendbox.fun Agent Scraper")
    parser.add_argument("--source", choices=list(SCRAPERS.keys()), help="Scrape a specific source only")
    parser.add_argument("--dry-run", action="store_true", help="Preview results without saving")
    args = parser.parse_args()

    print("=" * 60)
    print("sendbox.fun Agent Scraper")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    # Load existing data
    data = load_existing_agents()
    existing_count = len(data["agents"])
    print(f"Existing agents in database: {existing_count}")
    print()

    # Run scrapers
    new_agents = []
    sources = [args.source] if args.source else list(SCRAPERS.keys())

    for source in sources:
        scraped = SCRAPERS[source]()
        new_agents.extend(scraped)
        print()

    # Merge results
    added = 0
    updated = 0
    for agent in new_agents:
        result = merge_agent(data["agents"], agent)
        if result == "added":
            added += 1
        elif result == "updated":
            updated += 1

    print("=" * 60)
    print(f"Results: {added} new agents added, {updated} existing agents updated")
    print(f"Total agents in database: {len(data['agents'])}")

    if args.dry_run:
        print("\n[DRY RUN] Not saving. New agents found:")
        for a in new_agents[:20]:
            print(f"  - {a['name']} ({a['source']}) -> {a['categories']}")
        if len(new_agents) > 20:
            print(f"  ... and {len(new_agents) - 20} more")
    else:
        save_agents(data)

    print("=" * 60)


if __name__ == "__main__":
    main()
