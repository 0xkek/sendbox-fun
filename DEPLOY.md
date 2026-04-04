# Sendbox.fun — Deployment Guide

## Quick Start (5 minutes)

### Option A: Vercel (Recommended)

1. **Create a GitHub repo**
   ```bash
   # In the sendbox-fun folder
   git init
   git add index.html agents.json
   git commit -m "Initial sendbox.fun site"
   ```

2. **Push to GitHub**
   - Create a new repo at github.com/new (name it "sendbox-fun")
   - Follow the instructions to push your local repo

3. **Deploy on Vercel**
   - Go to vercel.com and sign up with your GitHub account
   - Click "Import Project" and select your sendbox-fun repo
   - Click "Deploy" — that's it
   - Your site is live at sendbox-fun.vercel.app

4. **Connect your domain**
   - In Vercel dashboard → Settings → Domains
   - Add "sendbox.fun"
   - Update your DNS records as Vercel instructs (usually just an A record and CNAME)
   - SSL is automatic

### Option B: Netlify (Alternative)

Same process but at netlify.com. Drag and drop the folder, or connect via GitHub.

### Option C: GitHub Pages (Free, simplest)

1. Push to GitHub
2. Settings → Pages → Deploy from main branch
3. Custom domain: add sendbox.fun in the settings

---

## Updating Agent Data

### Manual Update
Edit `agents.json` directly, commit, and push. Vercel auto-deploys.

### Using the Scraper
```bash
cd scraper

# Install dependencies
pip install requests beautifulsoup4

# Run all scrapers
python scrape_agents.py

# Run a specific source
python scrape_agents.py --source aiagentstore

# Preview without saving
python scrape_agents.py --dry-run
```

After running the scraper, commit and push the updated `agents.json`.

### Automated Updates (GitHub Actions)

Create `.github/workflows/scrape.yml`:

```yaml
name: Scrape Agents

on:
  schedule:
    # Run every 6 hours
    - cron: '0 */6 * * *'
  workflow_dispatch: # Allow manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Run scraper
        run: python scraper/scrape_agents.py

      - name: Commit and push if changed
        run: |
          git config user.name "sendbox-bot"
          git config user.email "bot@sendbox.fun"
          git add agents.json
          git diff --staged --quiet || git commit -m "Auto-update agent data $(date -u +%Y-%m-%dT%H:%M:%SZ)"
          git push
```

This runs the scraper every 6 hours, and if there are new agents, it commits and pushes automatically. Vercel detects the push and redeploys.

---

## File Structure

```
sendbox-fun/
├── index.html          # Main website (single page app)
├── agents.json         # Agent database (loaded by the site)
├── scraper/
│   └── scrape_agents.py  # Agent discovery scraper
├── DEPLOY.md           # This file
├── STRATEGY-Data-Sourcing.md
├── STRATEGY-Agent-Outreach.md
└── STRATEGY-Marketing-Launch.md
```

---

## Newsletter Setup

For the automated newsletter ("The Agent Brief"):

1. **Sign up for Beehiiv** (beehiiv.com) — free tier supports 2,500 subscribers
2. **Connect your waitlist** — Replace the email form action in index.html with your Beehiiv form endpoint
3. **Weekly workflow:**
   - Review newly scraped agents
   - Pick "Agent of the Week"
   - Write 3-4 paragraphs about new finds
   - Send via Beehiiv every Tuesday morning

---

## Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| Vercel hosting | Free | Up to 100GB bandwidth/mo |
| Domain (sendbox.fun) | ~$10/yr | If not already owned |
| GitHub | Free | Public or private repo |
| GitHub Actions | Free | 2,000 min/mo on free tier |
| Beehiiv newsletter | Free → $39/mo | Free up to 2,500 subscribers |
| **Total to launch** | **$0-10** | Just the domain cost |
