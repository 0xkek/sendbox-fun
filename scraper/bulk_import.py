"""
sendbox.fun Bulk Agent Import
==============================
Seeds agents.json with 100+ verified AI tools from web research.
Preserves existing entries (reviews, trust scores) and adds new ones.

Usage:
  python scraper/bulk_import.py              # Import and save
  python scraper/bulk_import.py --dry-run    # Preview without saving
"""

import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

AGENTS_JSON_PATH = Path(__file__).parent.parent / "agents.json"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

def make_id(name):
    return name.lower().strip().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "")

def make_entry(name, url, desc, categories, pricing_from="See website", pricing_note="", pricing_model="unknown", platforms=None, best_for=None, subcategories=None, founded=""):
    return {
        "id": make_id(name),
        "name": name,
        "url": url,
        "verified": False,
        "trustScore": 0,
        "description": desc,
        "ourReview": "",
        "categories": categories if isinstance(categories, list) else [categories],
        "subcategories": subcategories or [],
        "bestFor": best_for or [],
        "platforms": platforms or [],
        "pricingModel": pricing_model,
        "pricingFrom": pricing_from,
        "pricingNote": pricing_note,
        "stats": {"users": "N/A", "keyMetric": "N/A", "timeSaved": "N/A"},
        "affiliateLink": None,
        "founded": founded,
        "addedDate": TODAY,
        "lastChecked": TODAY,
        "source": "bulk-import",
    }

# ============================================================
# VERIFIED TOOL DATA — All URLs confirmed real via web research
# ============================================================

TOOLS = [
    # ── SOCIAL MEDIA ──────────────────────────────────────
    make_entry("Buffer", "https://buffer.com", "Social media management platform with AI-powered content suggestions, scheduling, and analytics across all major platforms.", ["social"], "$5/channel/mo", "Free plan for 3 channels", "freemium", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "YouTube", "Pinterest", "Threads", "Bluesky"], ["solopreneurs", "small-teams", "beginners"], ["scheduling", "analytics", "content-creation"], "2010"),
    make_entry("FeedHive", "https://www.feedhive.com", "AI-powered social media management with content creation at scale, performance predictions, hashtag generation, and a social inbox.", ["social"], "$19/mo", "7-day free trial", "subscription", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "YouTube", "Pinterest"], ["content-creators", "small-teams", "agencies"], ["content-creation", "scheduling", "analytics", "hashtags"], "2021"),
    make_entry("Metricool", "https://metricool.com", "All-in-one social media management with AI-powered content suggestions, optimal timing, hashtag research, and competitor analysis.", ["social"], "$20/mo", "Free plan available", "freemium", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "YouTube"], ["solopreneurs", "budget-conscious", "beginners"], ["scheduling", "analytics", "hashtags", "competitor-analysis"], "2016"),
    make_entry("SocialBee", "https://socialbee.com", "Social media management platform with AI Copilot that builds strategies and generates custom content for all channels.", ["social"], "$24/mo", "14-day free trial", "subscription", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "Pinterest"], ["solopreneurs", "small-teams"], ["scheduling", "content-creation", "analytics"], "2016"),
    make_entry("Agorapulse", "https://www.agorapulse.com", "Social media management with scheduling, social inbox, analytics, and ROI tracking. Built for teams and agencies.", ["social"], "$49/mo", "Free plan available", "freemium", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "YouTube"], ["agencies", "small-teams"], ["scheduling", "analytics", "social-inbox"], "2011"),
    make_entry("Postwise", "https://postwise.ai", "AI-powered tool that converts ideas into viral social media posts with smart scheduling and growth tools.", ["social"], "$29/mo", "Free trial", "subscription", ["X/Twitter", "LinkedIn", "Instagram"], ["content-creators", "solopreneurs"], ["content-creation", "scheduling"], "2022"),
    make_entry("Brandwatch", "https://www.brandwatch.com", "AI-powered social media analytics, listening, and management platform for understanding audiences and trends.", ["social", "analytics"], "$108/mo", "Demo available", "subscription", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "YouTube", "Reddit"], ["agencies", "enterprises"], ["social-listening", "analytics", "competitor-analysis"], "2007"),
    make_entry("Brand24", "https://brand24.com", "Social listening tool that monitors online mentions across social media, news, blogs, and forums in real-time.", ["social", "analytics"], "$49/mo", "14-day free trial", "subscription", ["Instagram", "X/Twitter", "Facebook", "Reddit", "YouTube"], ["small-teams", "agencies"], ["social-listening", "analytics"], "2011"),
    make_entry("Hootsuite", "https://www.hootsuite.com", "Enterprise social media management platform with scheduling, analytics, social listening, and team collaboration.", ["social"], "$99/mo", "30-day free trial", "subscription", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "YouTube", "Pinterest"], ["enterprises", "agencies"], ["scheduling", "analytics", "social-listening"], "2008"),
    make_entry("Sprout Social", "https://sproutsocial.com", "All-in-one social media management with publishing, analytics, engagement, and social listening powered by AI.", ["social"], "$199/mo", "30-day free trial", "subscription", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "YouTube", "Pinterest"], ["enterprises", "agencies"], ["scheduling", "analytics", "social-listening", "engagement"], "2010"),
    make_entry("Later", "https://later.com", "Visual social media marketing platform focused on Instagram, TikTok, and Pinterest with AI-powered scheduling.", ["social"], "$16.67/mo", "14-day free trial", "subscription", ["Instagram", "TikTok", "Facebook", "LinkedIn", "Pinterest"], ["content-creators", "solopreneurs"], ["scheduling", "visual-planning"], "2014"),
    make_entry("ContentIn", "https://contentin.io", "AI-powered LinkedIn content creation and scheduling tool that helps generate professional post ideas.", ["social"], "$25/mo", "Free trial", "subscription", ["LinkedIn"], ["b2b-professionals", "solopreneurs"], ["content-creation", "scheduling"], "2023"),
    make_entry("Snowball", "https://snowball.club", "AI tool that grows, schedules, and automates X (Twitter) content for audience growth.", ["social"], "$29/mo", "Free trial", "subscription", ["X/Twitter"], ["content-creators", "solopreneurs"], ["scheduling", "content-creation", "growth"], "2023"),

    # ── SALES & CRM ───────────────────────────────────────
    make_entry("Apollo.io", "https://www.apollo.io", "AI sales intelligence platform with a 210M+ contact database, email outreach sequences, lead scoring, and CRM integration.", ["sales"], "$49/user/mo", "Free tier available", "freemium", ["Gmail", "HubSpot", "Salesforce", "LinkedIn"], ["solopreneurs", "small-teams", "b2b-sales"], ["lead-gen", "outreach", "crm-integration"], "2015"),
    make_entry("Lindy.ai", "https://www.lindy.ai", "Build custom AI workflows without code. Automate follow-ups, CRM updates, meeting scheduling, and pipeline management.", ["sales", "automation"], "$49.99/mo", "Free plan with 400 credits", "freemium", ["Gmail", "Slack", "HubSpot", "Salesforce", "Zoom", "Calendly"], ["small-teams", "agencies", "power-users"], ["workflow-automation", "follow-ups", "crm-integration", "scheduling"], "2023"),
    make_entry("Freshsales", "https://www.freshworks.com/crm/sales/", "AI-powered CRM by Freshworks with lead scoring, auto-enrichment, built-in phone, email, and chat.", ["sales"], "$9/user/mo", "Free plan for up to 3 users", "freemium", ["Gmail", "Outlook", "Slack", "Zoom"], ["small-teams", "budget-conscious", "growing-teams"], ["crm-integration", "deal-tracking", "lead-gen", "workflow-automation"], "2016"),
    make_entry("Clay", "https://www.clay.com", "Data enrichment and outbound automation platform. Access 100+ data sources and AI agents for go-to-market workflows.", ["sales"], "$149/mo", "Free tier available", "freemium", ["HubSpot", "Salesforce", "Gmail"], ["growth-teams", "agencies", "b2b-sales"], ["lead-gen", "data-enrichment", "outreach"], "2017"),
    make_entry("Instantly", "https://instantly.ai", "Cold email platform with unlimited sending accounts, AI personalization, warmup, and deliverability tools.", ["sales", "email"], "$30/mo", "Free trial", "subscription", ["Gmail", "Outlook"], ["solopreneurs", "agencies", "b2b-sales"], ["cold-email", "outreach", "deliverability"], "2021"),
    make_entry("Lemlist", "https://www.lemlist.com", "Cold outreach automation platform with AI-powered email personalization, multichannel sequences, and deliverability.", ["sales", "email"], "$32/mo", "14-day free trial", "subscription", ["Gmail", "Outlook", "LinkedIn"], ["solopreneurs", "small-teams", "agencies"], ["cold-email", "outreach", "personalization"], "2018"),
    make_entry("Attio", "https://attio.com", "AI-native CRM that automatically enriches contacts, syncs communications, and automates sales workflows.", ["sales"], "$29/seat/mo", "Free plan available", "freemium", ["Gmail", "Outlook", "Slack"], ["startups", "small-teams"], ["crm-integration", "workflow-automation"], "2019"),
    make_entry("Attention", "https://www.attention.tech", "AI that joins sales calls, takes notes, generates follow-ups, and provides coaching insights automatically.", ["sales"], "Custom pricing", "Demo available", "subscription", ["Zoom", "Google Meet", "HubSpot", "Salesforce"], ["sales-teams", "growing-teams"], ["call-intelligence", "coaching", "follow-ups"], "2022"),
    make_entry("HubSpot CRM", "https://www.hubspot.com/products/crm", "All-in-one CRM platform with AI-powered sales, marketing, and customer service tools. Free forever plan.", ["sales"], "$15/user/mo", "Free plan available", "freemium", ["Gmail", "Outlook", "Slack", "Zoom"], ["solopreneurs", "small-teams", "enterprises"], ["crm-integration", "deal-tracking", "workflow-automation"], "2006"),
    make_entry("Pipedrive", "https://www.pipedrive.com", "Sales-focused CRM with AI sales assistant, pipeline management, email tracking, and workflow automation.", ["sales"], "$14/user/mo", "14-day free trial", "subscription", ["Gmail", "Outlook", "Slack", "Zoom"], ["solopreneurs", "small-teams"], ["crm-integration", "pipeline-management", "email-tracking"], "2010"),
    make_entry("Salesforce Einstein", "https://www.salesforce.com/products/einstein-ai-solutions/", "AI layer for Salesforce CRM providing predictive lead scoring, opportunity insights, and automated recommendations.", ["sales"], "$25/user/mo", "Free trial available", "subscription", ["Salesforce"], ["enterprises", "growing-teams"], ["crm-integration", "lead-scoring", "forecasting"], "1999"),
    make_entry("PhantomBuster", "https://phantombuster.com", "Automates lead generation and data enrichment from LinkedIn, Sales Navigator, and other platforms.", ["sales"], "$56/mo", "14-day free trial", "subscription", ["LinkedIn", "Sales Navigator", "Google Maps"], ["solopreneurs", "agencies", "growth-teams"], ["lead-gen", "data-enrichment", "automation"], "2016"),
    make_entry("Seamless.AI", "https://www.seamless.ai", "Real-time B2B search engine that finds verified contact information including emails and phone numbers.", ["sales"], "$147/mo", "Free credits available", "subscription", ["Salesforce", "HubSpot", "LinkedIn"], ["b2b-sales", "agencies"], ["lead-gen", "data-enrichment"], "2018"),
    make_entry("Growbots", "https://www.growbots.com", "Outbound sales automation platform that finds prospects, creates campaigns, and automates follow-ups.", ["sales"], "$49/mo", "Free trial", "subscription", ["Gmail", "Outlook", "Salesforce", "HubSpot"], ["solopreneurs", "small-teams"], ["lead-gen", "outreach", "automation"], "2014"),

    # ── ECOMMERCE ─────────────────────────────────────────
    make_entry("Gorgias", "https://www.gorgias.com", "Ecommerce helpdesk built for Shopify, BigCommerce, and Magento. AI agent handles up to 60% of support tickets.", ["ecom", "customer-service"], "$10/mo", "7-day free trial", "subscription", ["Shopify", "BigCommerce", "Magento", "WooCommerce"], ["ecommerce-sellers", "small-ecommerce", "shopify-stores"], ["customer-service", "returns", "order-management"], "2015"),
    make_entry("Tidio", "https://www.tidio.com", "Live chat and AI chatbot platform for ecommerce. Lyro AI handles product questions, recommends items, and checks order status.", ["ecom", "customer-service"], "$29/mo", "Free plan available", "freemium", ["Shopify", "WooCommerce", "WordPress", "Wix"], ["small-ecommerce", "solopreneurs", "budget-conscious"], ["customer-service", "recommendations", "chatbot"], "2013"),
    make_entry("Privy", "https://www.privy.com", "Ecommerce-focused email and SMS marketing with popups, cart abandonment flows, and conversion optimization.", ["ecom", "email"], "$24/mo", "15-day free trial", "subscription", ["Shopify", "BigCommerce", "Wix", "Squarespace"], ["small-ecommerce", "solopreneurs", "beginners"], ["email-marketing", "conversion", "popups", "sms"], "2011"),
    make_entry("Klaviyo", "https://www.klaviyo.com", "Email and SMS marketing platform built for ecommerce with AI-powered segmentation, predictive analytics, and automation.", ["ecom", "email"], "$20/mo", "Free plan for 250 contacts", "freemium", ["Shopify", "BigCommerce", "WooCommerce", "Magento"], ["ecommerce-sellers", "growing-teams"], ["email-marketing", "sms", "segmentation", "analytics"], "2012"),
    make_entry("Nosto", "https://www.nosto.com", "Ecommerce personalization platform delivering AI-powered product recommendations, content personalization, and merchandising.", ["ecom"], "Custom pricing", "Demo available", "subscription", ["Shopify", "BigCommerce", "Magento"], ["ecommerce-sellers", "enterprises"], ["personalization", "recommendations", "merchandising"], "2011"),
    make_entry("Prisync", "https://prisync.com", "Competitor price tracking and dynamic repricing engine for ecommerce stores that syncs prices automatically.", ["ecom"], "$99/mo", "14-day free trial", "subscription", ["Shopify", "WooCommerce", "Magento", "BigCommerce"], ["ecommerce-sellers", "multi-product-stores"], ["pricing", "competitor-monitoring"], "2013"),
    make_entry("Growave", "https://growave.io", "Shopify marketing app combining loyalty programs, reviews, wishlists, and social proof in one platform.", ["ecom"], "$49/mo", "14-day free trial", "subscription", ["Shopify"], ["shopify-stores", "small-ecommerce"], ["loyalty", "reviews", "social-proof"], "2016"),
    make_entry("Riskified", "https://www.riskified.com", "AI-powered fraud prevention and chargeback protection for ecommerce with guaranteed approval decisions.", ["ecom"], "Custom pricing", "Demo available", "subscription", ["Shopify", "BigCommerce", "Magento", "WooCommerce"], ["ecommerce-sellers", "enterprises"], ["fraud-prevention", "chargeback-protection"], "2013"),
    make_entry("OptiMonk AI", "https://www.optimonk.com", "AI-powered popup and personalization platform that understands visitor behavior for real-time targeted offers.", ["ecom"], "$39/mo", "Free plan available", "freemium", ["Shopify", "WooCommerce", "WordPress"], ["ecommerce-sellers", "solopreneurs"], ["popups", "personalization", "conversion"], "2014"),
    make_entry("ReelUp", "https://www.reelup.co", "Shoppable video platform that boosts ecommerce engagement and conversions with interactive product videos.", ["ecom", "video"], "Custom pricing", "Demo available", "subscription", ["Shopify", "WooCommerce"], ["ecommerce-sellers"], ["shoppable-video", "engagement"], "2022"),

    # ── CONTENT CREATION ──────────────────────────────────
    make_entry("Jasper", "https://www.jasper.ai", "AI marketing assistant that generates blog posts, ad copy, product descriptions, and social media content at scale.", ["content"], "$39/mo", "7-day free trial", "subscription", [], ["marketers", "agencies", "content-teams"], ["copywriting", "blog-posts", "ad-copy"], "2021"),
    make_entry("Copy.ai", "https://www.copy.ai", "AI-powered platform for go-to-market automation including content generation, outbound prospecting, and lead research.", ["content", "sales"], "$36/mo", "Free plan available", "freemium", [], ["marketers", "sales-teams", "agencies"], ["copywriting", "outreach", "automation"], "2020"),
    make_entry("Writesonic", "https://writesonic.com", "Full-stack AI marketing platform for researching, creating, optimizing, and publishing content at scale.", ["content"], "$16/mo", "Free plan available", "freemium", [], ["solopreneurs", "marketers", "content-teams"], ["copywriting", "seo-content", "blog-posts"], "2021"),
    make_entry("Grammarly", "https://www.grammarly.com", "AI writing assistant that improves clarity, tone, grammar, and consistency across all written communication.", ["content"], "$12/mo", "Free plan available", "freemium", ["Chrome", "Gmail", "Google Docs", "Microsoft Office"], ["everyone", "teams", "enterprises"], ["writing", "grammar", "tone"], "2009"),
    make_entry("Hypotenuse AI", "https://www.hypotenuse.ai", "Ecommerce-trained AI for bulk generation of product descriptions, blog posts, and marketing copy with brand consistency.", ["content", "ecom"], "$56/mo", "Free trial", "subscription", ["Shopify", "WooCommerce"], ["ecommerce-sellers", "content-teams"], ["product-descriptions", "bulk-content"], "2020"),
    make_entry("Frase", "https://www.frase.io", "AI content research and writing platform that generates SEO-optimized content with competitor analysis built in.", ["content", "seo"], "$15/mo", "5-day trial for $1", "subscription", [], ["content-teams", "seo-professionals"], ["seo-content", "research", "optimization"], "2016"),
    make_entry("Castmagic", "https://www.castmagic.io", "AI transcription platform that turns audio and video content into blog posts, social media content, and newsletters.", ["content"], "$23/mo", "Free trial", "subscription", [], ["podcasters", "content-creators"], ["transcription", "repurposing"], "2022"),

    # ── EMAIL MARKETING ───────────────────────────────────
    make_entry("Mailchimp", "https://mailchimp.com", "All-in-one email marketing platform with AI-powered content suggestions, automation, and audience segmentation.", ["email"], "$13/mo", "Free plan for 500 contacts", "freemium", ["Shopify", "WooCommerce", "WordPress"], ["solopreneurs", "small-teams"], ["email-marketing", "automation", "segmentation"], "2001"),
    make_entry("ConvertKit", "https://convertkit.com", "Email marketing platform built for creators with visual automations, landing pages, and subscriber tagging.", ["email"], "$9/mo", "Free plan for 1,000 subscribers", "freemium", ["Shopify", "WordPress"], ["content-creators", "solopreneurs"], ["email-marketing", "automation", "landing-pages"], "2013"),
    make_entry("Beehiiv", "https://www.beehiiv.com", "Newsletter platform with built-in growth tools, monetization, and AI writing assistant for creators and publishers.", ["email"], "$39/mo", "Free plan for 2,500 subscribers", "freemium", [], ["content-creators", "publishers", "solopreneurs"], ["newsletters", "monetization", "growth"], "2021"),
    make_entry("ActiveCampaign", "https://www.activecampaign.com", "Email marketing and CRM platform with AI-powered automation, predictive sending, and customer journey mapping.", ["email", "sales"], "$15/mo", "14-day free trial", "subscription", ["Shopify", "WooCommerce", "Salesforce"], ["small-teams", "ecommerce-sellers"], ["email-marketing", "automation", "crm"], "2003"),
    make_entry("Brevo", "https://www.brevo.com", "All-in-one marketing platform with email, SMS, WhatsApp, chat, and CRM. Formerly Sendinblue.", ["email"], "$8.08/mo", "Free plan for 300 emails/day", "freemium", ["Shopify", "WooCommerce", "WordPress"], ["solopreneurs", "small-teams", "budget-conscious"], ["email-marketing", "sms", "crm"], "2012"),

    # ── SEO ────────────────────────────────────────────────
    make_entry("Surfer SEO", "https://surferseo.com", "AI-powered SEO tool that analyzes top-performing pages and generates optimized content outlines and articles.", ["seo", "content"], "$79/mo", "Free trial", "subscription", ["Google Docs", "WordPress"], ["seo-professionals", "content-teams"], ["seo-optimization", "content-creation"], "2017"),
    make_entry("Clearscope", "https://www.clearscope.io", "AI content optimization platform that helps create high-ranking content by analyzing top search results.", ["seo", "content"], "$170/mo", "Demo available", "subscription", ["Google Docs", "WordPress"], ["content-teams", "seo-professionals"], ["seo-optimization", "content-grading"], "2016"),
    make_entry("Semrush", "https://www.semrush.com", "All-in-one SEO and marketing toolkit with keyword research, site audits, rank tracking, and competitor analysis.", ["seo", "analytics"], "$119.95/mo", "Free plan available", "freemium", [], ["marketers", "seo-professionals", "agencies"], ["keyword-research", "site-audit", "rank-tracking"], "2008"),
    make_entry("Ahrefs", "https://ahrefs.com", "SEO toolset for backlink analysis, keyword research, site audits, and rank tracking used by top marketers.", ["seo"], "$99/mo", "Free webmaster tools", "subscription", [], ["seo-professionals", "agencies", "content-teams"], ["backlink-analysis", "keyword-research", "site-audit"], "2011"),
    make_entry("Sitechecker", "https://sitechecker.pro", "AI-powered platform for technical SEO audits, rank tracking, and website monitoring with actionable recommendations.", ["seo"], "$59/mo", "Free trial", "subscription", [], ["solopreneurs", "small-teams"], ["site-audit", "rank-tracking", "monitoring"], "2018"),
    make_entry("Alli AI", "https://www.alliai.com", "AI SEO automation tool that optimizes on-page elements, creates content, and manages technical SEO at scale.", ["seo"], "$249/mo", "10-day free trial", "subscription", ["WordPress", "Shopify"], ["agencies", "seo-professionals"], ["seo-automation", "on-page-optimization"], "2019"),

    # ── VIDEO ─────────────────────────────────────────────
    make_entry("Synthesia", "https://www.synthesia.io", "AI video generator that creates studio-quality videos from text with realistic AI avatars in 120+ languages.", ["video"], "$22/mo", "Free demo video", "subscription", [], ["marketers", "trainers", "enterprises"], ["video-creation", "avatars", "localization"], "2017"),
    make_entry("Descript", "https://www.descript.com", "All-in-one video and podcast editor that makes editing as easy as editing a document. AI-powered transcription.", ["video"], "$24/mo", "Free plan available", "freemium", [], ["content-creators", "podcasters", "marketers"], ["video-editing", "podcast-editing", "transcription"], "2017"),
    make_entry("Opus Clip", "https://www.opus.pro", "AI-powered tool that turns long videos into viral short clips with smart scene detection and captioning.", ["video"], "$15/mo", "Free plan available", "freemium", [], ["content-creators", "agencies", "marketers"], ["video-clipping", "repurposing", "captions"], "2022"),
    make_entry("HeyGen", "https://www.heygen.com", "AI video creation platform with customizable avatars, text-to-video, and video translation in 40+ languages.", ["video"], "$24/mo", "Free credits available", "freemium", [], ["marketers", "enterprises", "trainers"], ["video-creation", "avatars", "translation"], "2020"),
    make_entry("VEED", "https://www.veed.io", "Online AI video editor with auto-subtitles, text-to-speech, background removal, and one-click social media formatting.", ["video"], "$18/mo", "Free plan available", "freemium", [], ["content-creators", "solopreneurs", "marketers"], ["video-editing", "subtitles", "social-formatting"], "2018"),
    make_entry("Fliki", "https://fliki.ai", "Turn text into videos with AI voices, stock media, and branded templates in minutes.", ["video"], "$21/mo", "Free plan available", "freemium", [], ["content-creators", "marketers"], ["text-to-video", "ai-voices"], "2022"),
    make_entry("ElevenLabs", "https://elevenlabs.io", "AI voice generator with ultra-realistic text-to-speech, voice cloning, and dubbing in 29 languages.", ["video"], "$5/mo", "Free plan available", "freemium", [], ["content-creators", "developers", "enterprises"], ["text-to-speech", "voice-cloning", "dubbing"], "2022"),
    make_entry("Vidyard", "https://www.vidyard.com", "Video platform for sales and marketing teams with AI-generated scripts, personalized videos, and analytics.", ["video", "sales"], "$19/mo", "Free plan available", "freemium", ["HubSpot", "Salesforce", "Gmail", "Outlook"], ["sales-teams", "marketers"], ["video-messaging", "analytics", "personalization"], "2011"),

    # ── AUTOMATION & WORKFLOW ─────────────────────────────
    make_entry("Zapier", "https://zapier.com", "Connect 6,000+ apps and automate workflows without code. The most popular workflow automation platform.", ["automation"], "$19.99/mo", "Free plan for 100 tasks/mo", "freemium", [], ["everyone", "solopreneurs", "small-teams"], ["workflow-automation", "integrations"], "2011"),
    make_entry("Make", "https://www.make.com", "Visual workflow automation platform (formerly Integromat) connecting apps with powerful logic and data transformation.", ["automation"], "$9/mo", "Free plan available", "freemium", [], ["power-users", "agencies", "developers"], ["workflow-automation", "integrations", "data-transformation"], "2012"),
    make_entry("n8n", "https://n8n.io", "Open-source workflow automation tool with 400+ integrations, AI capabilities, and self-hosting option.", ["automation"], "$20/mo", "Free self-hosted option", "freemium", [], ["developers", "power-users", "small-teams"], ["workflow-automation", "integrations", "self-hosted"], "2019"),
    make_entry("Axiom", "https://axiom.ai", "No-code browser automation that records and replays web actions for scraping, form filling, and repetitive tasks.", ["automation"], "$15/mo", "Free plan available", "freemium", ["Chrome"], ["solopreneurs", "small-teams"], ["browser-automation", "scraping", "no-code"], "2020"),
    make_entry("Bardeen", "https://www.bardeen.ai", "AI-powered browser automation that connects apps, scrapes data, and automates repetitive tasks from any website.", ["automation"], "$10/mo", "Free plan available", "freemium", ["Chrome"], ["solopreneurs", "sales-teams"], ["browser-automation", "scraping", "integrations"], "2020"),
    make_entry("Retool", "https://retool.com", "Build internal tools remarkably fast with drag-and-drop components, AI, and connections to any database or API.", ["automation"], "$10/user/mo", "Free plan for 5 users", "freemium", [], ["developers", "enterprises"], ["internal-tools", "dashboards", "database"], "2017"),

    # ── CUSTOMER SERVICE ──────────────────────────────────
    make_entry("Intercom", "https://www.intercom.com", "AI-first customer service platform with Fin AI agent that resolves 50%+ of queries, plus live chat and helpdesk.", ["customer-service"], "$29/seat/mo", "14-day free trial", "subscription", ["Shopify", "Salesforce", "HubSpot", "Slack"], ["startups", "growing-teams", "enterprises"], ["ai-chatbot", "live-chat", "helpdesk", "ticketing"], "2011"),
    make_entry("Zendesk", "https://www.zendesk.com", "Complete customer service platform with AI-powered bots, ticketing, live chat, and omnichannel support.", ["customer-service"], "$19/agent/mo", "Free trial available", "subscription", ["Shopify", "Salesforce", "Slack"], ["enterprises", "growing-teams"], ["helpdesk", "ticketing", "ai-chatbot", "omnichannel"], "2007"),
    make_entry("Freshdesk", "https://www.freshworks.com/freshdesk/", "AI-powered helpdesk with ticketing, automation, self-service, and Freddy AI for instant customer resolutions.", ["customer-service"], "$15/agent/mo", "Free plan for 10 agents", "freemium", ["Shopify", "Slack", "Salesforce"], ["small-teams", "growing-teams"], ["helpdesk", "ticketing", "ai-chatbot"], "2010"),
    make_entry("Drift", "https://www.salesloft.com/platform/drift/", "Conversational AI platform for website chat, lead qualification, and meeting scheduling powered by AI.", ["customer-service", "sales"], "$2,500/mo", "Demo available", "subscription", ["Salesforce", "HubSpot", "Marketo"], ["enterprises", "b2b-sales"], ["conversational-ai", "lead-qualification", "scheduling"], "2015"),
    make_entry("Crisp", "https://crisp.chat", "All-in-one customer messaging platform with live chat, chatbot, knowledge base, and shared inbox.", ["customer-service"], "$25/mo", "Free plan available", "freemium", ["Shopify", "WordPress", "WooCommerce"], ["startups", "small-teams"], ["live-chat", "chatbot", "knowledge-base"], "2015"),
    make_entry("Help Scout", "https://www.helpscout.com", "Customer support platform with shared inbox, knowledge base, and AI features for small businesses.", ["customer-service"], "$20/user/mo", "Free plan for 1 user", "freemium", ["Shopify", "HubSpot", "Slack"], ["small-teams", "solopreneurs"], ["helpdesk", "shared-inbox", "knowledge-base"], "2011"),

    # ── ANALYTICS & REPORTING ─────────────────────────────
    make_entry("Google Analytics", "https://analytics.google.com", "Free web analytics platform with AI-powered insights, audience analysis, and conversion tracking.", ["analytics"], "Free", "Enterprise version available", "free", [], ["everyone"], ["web-analytics", "conversion-tracking", "audience-insights"], "2005"),
    make_entry("Hotjar", "https://www.hotjar.com", "Behavior analytics platform with heatmaps, session recordings, and AI-powered surveys for understanding users.", ["analytics"], "$32/mo", "Free plan available", "freemium", ["Shopify", "WordPress"], ["product-teams", "marketers", "ux-designers"], ["heatmaps", "session-recording", "surveys"], "2014"),
    make_entry("Mixpanel", "https://mixpanel.com", "Product analytics platform with AI-powered insights, funnel analysis, and user segmentation.", ["analytics"], "$20/mo", "Free plan available", "freemium", [], ["product-teams", "developers", "startups"], ["product-analytics", "funnel-analysis", "segmentation"], "2009"),
    make_entry("Plausible", "https://plausible.io", "Privacy-friendly, lightweight web analytics — an ethical alternative to Google Analytics with no cookies.", ["analytics"], "$9/mo", "30-day free trial", "subscription", [], ["solopreneurs", "privacy-conscious"], ["web-analytics", "privacy-friendly"], "2019"),
    make_entry("Socialinsider", "https://www.socialinsider.io", "Social media analytics and competitive benchmarking platform for agencies and brands.", ["analytics", "social"], "$82/mo", "14-day free trial", "subscription", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "YouTube"], ["agencies", "brands"], ["social-analytics", "benchmarking", "reporting"], "2015"),

    # ── ADVERTISING ────────────────────────────────────────
    make_entry("AdEspresso", "https://adespresso.com", "Facebook, Instagram, and Google Ads management platform with AI optimization and A/B testing.", ["ads"], "$49/mo", "14-day free trial", "subscription", ["Facebook", "Instagram", "Google Ads"], ["solopreneurs", "small-teams", "agencies"], ["ad-management", "optimization", "ab-testing"], "2013"),
    make_entry("Madgicx", "https://madgicx.com", "AI-powered ad optimization platform for Meta and Google Ads with automated bidding and creative insights.", ["ads"], "$31/mo", "7-day free trial", "subscription", ["Facebook", "Instagram", "Google Ads"], ["ecommerce-sellers", "agencies"], ["ad-optimization", "creative-insights", "automation"], "2018"),
    make_entry("Albert AI", "https://albert.ai", "Autonomous AI platform that runs and optimizes digital ad campaigns across Google, Facebook, and more.", ["ads"], "Custom pricing", "Demo available", "subscription", ["Google Ads", "Facebook", "Instagram", "YouTube"], ["enterprises", "agencies"], ["ad-automation", "optimization", "cross-channel"], "2014"),
    make_entry("Revealbot", "https://revealbot.com", "Ad automation platform for Facebook, Google, TikTok, and Snapchat with rule-based optimization and reporting.", ["ads"], "$99/mo", "14-day free trial", "subscription", ["Facebook", "Google Ads", "TikTok", "Snapchat"], ["agencies", "ecommerce-sellers"], ["ad-automation", "rules-based", "reporting"], "2016"),

    # ── DESIGN ─────────────────────────────────────────────
    make_entry("Canva", "https://www.canva.com", "Visual design platform with AI-powered tools for creating social media graphics, presentations, videos, and more.", ["design"], "$12.99/mo", "Free plan available", "freemium", [], ["everyone", "solopreneurs", "small-teams"], ["graphic-design", "social-media", "presentations"], "2013"),
    make_entry("Figma", "https://www.figma.com", "Collaborative design platform with AI features for interface design, prototyping, and design systems.", ["design"], "$12/editor/mo", "Free plan available", "freemium", [], ["designers", "developers", "product-teams"], ["ui-design", "prototyping", "collaboration"], "2012"),
    make_entry("Looka", "https://looka.com", "AI-powered logo and brand identity designer that creates professional logos, business cards, and brand kits.", ["design"], "$20 one-time", "Free to design", "one-time", [], ["solopreneurs", "startups", "small-businesses"], ["logo-design", "brand-identity"], "2016"),
    make_entry("Designs.ai", "https://designs.ai", "All-in-one AI creative suite for logos, videos, mockups, and social media graphics generation.", ["design"], "$19/mo", "Free trial", "subscription", [], ["solopreneurs", "small-teams", "marketers"], ["logo-design", "video", "mockups"], "2018"),
    make_entry("Adobe Firefly", "https://www.adobe.com/products/firefly.html", "Adobe's generative AI for creating images, text effects, and graphics integrated with Creative Cloud.", ["design"], "$4.99/mo", "Free credits monthly", "freemium", ["Photoshop", "Illustrator", "Express"], ["designers", "marketers"], ["image-generation", "text-effects"], "2023"),
    make_entry("Midjourney", "https://www.midjourney.com", "AI image generator known for artistic, high-quality visuals via Discord and web interface.", ["design"], "$10/mo", "Paid only", "subscription", ["Discord"], ["designers", "artists", "marketers"], ["image-generation", "ai-art"], "2022"),
    make_entry("DALL-E 3", "https://openai.com/dall-e-3", "OpenAI's image generation model integrated into ChatGPT for creating images from text prompts.", ["design"], "$20/mo", "Via ChatGPT Plus", "subscription", ["ChatGPT"], ["everyone"], ["image-generation"], "2023"),
    make_entry("Leonardo.Ai", "https://leonardo.ai", "AI image generator for production-quality visual assets, game assets, and concept art.", ["design"], "$12/mo", "Free plan available", "freemium", [], ["designers", "game-developers"], ["image-generation", "game-assets"], "2022"),
    make_entry("Runway", "https://runwayml.com", "AI video generation and editing platform with text-to-video, image-to-video, and creative tools.", ["video", "design"], "$15/mo", "Free plan available", "freemium", [], ["filmmakers", "designers", "creators"], ["video-generation", "ai-video"], "2018"),
    make_entry("Pika", "https://pika.art", "AI video generator creating short clips from text prompts or images with simple controls.", ["video"], "$10/mo", "Free plan available", "freemium", [], ["creators", "marketers"], ["video-generation"], "2023"),
    make_entry("Luma Dream Machine", "https://lumalabs.ai/dream-machine", "AI video generation model creating realistic cinematic clips from text or image prompts.", ["video"], "$29.99/mo", "Free tier available", "freemium", [], ["creators", "filmmakers"], ["video-generation"], "2023"),

    # ── AI CHAT & ASSISTANTS ──────────────────────────────
    make_entry("ChatGPT", "https://chat.openai.com", "OpenAI's flagship conversational AI for writing, coding, analysis, and creative tasks.", ["assistant"], "$20/mo", "Free plan available", "freemium", [], ["everyone"], ["chatbot", "writing", "analysis"], "2022"),
    make_entry("Claude", "https://claude.ai", "Anthropic's AI assistant with long context, strong reasoning, and artifacts for creating content.", ["assistant"], "$20/mo", "Free plan available", "freemium", [], ["everyone", "developers"], ["chatbot", "writing", "coding"], "2023"),
    make_entry("Gemini", "https://gemini.google.com", "Google's AI assistant integrated with Workspace, search, and multimodal capabilities.", ["assistant"], "$19.99/mo", "Free plan available", "freemium", ["Google Workspace"], ["everyone"], ["chatbot", "multimodal"], "2023"),
    make_entry("Perplexity", "https://www.perplexity.ai", "AI-powered search engine that answers questions with cited sources and follow-up queries.", ["assistant", "research"], "$20/mo", "Free plan available", "freemium", [], ["researchers", "everyone"], ["search", "research", "citations"], "2022"),
    make_entry("Poe", "https://poe.com", "Quora's multi-model AI chat platform with access to GPT-4, Claude, Gemini, and more in one place.", ["assistant"], "$19.99/mo", "Free plan available", "freemium", [], ["power-users"], ["chatbot", "multi-model"], "2023"),
    make_entry("Mistral Le Chat", "https://chat.mistral.ai", "European AI assistant from Mistral with strong reasoning, coding, and multilingual capabilities.", ["assistant"], "Free", "Free tier", "freemium", [], ["everyone"], ["chatbot", "multilingual"], "2024"),
    make_entry("Grok", "https://grok.com", "xAI's chatbot with real-time X/Twitter access and a conversational personality.", ["assistant"], "$30/mo", "Via X Premium", "subscription", ["X/Twitter"], ["everyone"], ["chatbot", "real-time"], "2023"),
    make_entry("HuggingChat", "https://huggingface.co/chat/", "Open-source AI chat from Hugging Face with multiple open models and tool use.", ["assistant"], "Free", "Completely free", "free", [], ["developers", "researchers"], ["chatbot", "open-source"], "2023"),

    # ── AI CODING & DEVELOPMENT ───────────────────────────
    make_entry("Cursor", "https://cursor.com", "AI-powered code editor built on VS Code with inline editing, codebase understanding, and agent mode.", ["coding"], "$20/mo", "Free plan available", "freemium", ["VS Code"], ["developers"], ["ai-coding", "ide"], "2023"),
    make_entry("GitHub Copilot", "https://github.com/features/copilot", "AI pair programmer from GitHub offering code completions, chat, and PR reviews in your editor.", ["coding"], "$10/mo", "Free for students", "subscription", ["VS Code", "JetBrains", "Neovim"], ["developers"], ["ai-coding", "completions"], "2021"),
    make_entry("Windsurf", "https://windsurf.com", "AI IDE with Cascade agent that understands your entire codebase and makes multi-file edits.", ["coding"], "$15/mo", "Free plan available", "freemium", [], ["developers"], ["ai-coding", "ide", "agent"], "2024"),
    make_entry("Claude Code", "https://www.anthropic.com/claude-code", "Anthropic's CLI coding agent that runs in your terminal with access to your full codebase.", ["coding"], "$20/mo", "Via Claude Pro", "subscription", ["Terminal"], ["developers"], ["ai-coding", "cli", "agent"], "2024"),
    make_entry("Aider", "https://aider.chat", "Open-source AI pair programming tool that edits code in your terminal with git integration.", ["coding"], "Free (API costs)", "Open source", "free", ["Terminal", "Git"], ["developers"], ["ai-coding", "cli", "open-source"], "2023"),
    make_entry("Bolt.new", "https://bolt.new", "StackBlitz AI full-stack web development in the browser — describe an app and see it built live.", ["coding"], "$20/mo", "Free plan available", "freemium", [], ["developers", "solopreneurs"], ["ai-coding", "web-dev"], "2024"),
    make_entry("Lovable", "https://lovable.dev", "AI app builder that generates full-stack applications from natural language prompts.", ["coding"], "$20/mo", "Free plan available", "freemium", [], ["founders", "solopreneurs"], ["ai-coding", "app-builder"], "2024"),
    make_entry("v0", "https://v0.dev", "Vercel's AI tool for generating React components and UI from text prompts and screenshots.", ["coding", "design"], "$20/mo", "Free plan available", "freemium", ["React", "Next.js"], ["developers", "designers"], ["ui-generation", "react"], "2023"),
    make_entry("Replit Agent", "https://replit.com", "Cloud IDE with AI agent that builds full applications from your description in the browser.", ["coding"], "$25/mo", "Free tier available", "freemium", [], ["developers", "students"], ["ai-coding", "cloud-ide"], "2016"),
    make_entry("Tabnine", "https://www.tabnine.com", "AI code completion tool with privacy-focused, team-trained models for enterprise developers.", ["coding"], "$9/mo", "Free plan available", "freemium", ["VS Code", "JetBrains"], ["developers", "enterprises"], ["ai-coding", "completions"], "2013"),
    make_entry("Codeium", "https://codeium.com", "Free AI code autocomplete, chat, and search across 70+ languages and all major IDEs.", ["coding"], "Free", "Free for individuals", "freemium", ["VS Code", "JetBrains", "Neovim"], ["developers"], ["ai-coding", "completions"], "2022"),
    make_entry("Sourcegraph Cody", "https://sourcegraph.com/cody", "AI coding assistant that reads your entire codebase for context-aware completions and chat.", ["coding"], "$9/mo", "Free plan available", "freemium", ["VS Code", "JetBrains"], ["developers", "enterprises"], ["ai-coding", "codebase-aware"], "2023"),
    make_entry("Supermaven", "https://supermaven.com", "Ultra-fast AI code completion with 300K+ token context window and sub-second latency.", ["coding"], "$10/mo", "Free plan available", "freemium", ["VS Code", "JetBrains", "Neovim"], ["developers"], ["ai-coding", "completions"], "2024"),
    make_entry("Devin", "https://devin.ai", "Cognition's autonomous AI software engineer that plans, codes, and debugs full projects.", ["coding"], "$500/mo", "Team plans", "subscription", [], ["enterprises", "teams"], ["autonomous-agent", "ai-engineer"], "2024"),

    # ── AI AGENT PLATFORMS & INFRASTRUCTURE ───────────────
    make_entry("LangChain", "https://www.langchain.com", "Framework for building LLM-powered applications with chains, agents, and memory. Python and JS.", ["dev-tools"], "Free (open source)", "Paid LangSmith", "freemium", ["Python", "JavaScript"], ["developers"], ["framework", "llm-apps"], "2022"),
    make_entry("LlamaIndex", "https://www.llamaindex.ai", "Data framework for building LLM applications with RAG, structured data, and agents.", ["dev-tools"], "Free (open source)", "Paid cloud", "freemium", ["Python", "TypeScript"], ["developers"], ["rag", "framework"], "2022"),
    make_entry("CrewAI", "https://www.crewai.com", "Framework for orchestrating role-playing autonomous AI agents to tackle complex tasks together.", ["dev-tools", "automation"], "Free (open source)", "Paid enterprise", "freemium", ["Python"], ["developers"], ["multi-agent", "framework"], "2023"),
    make_entry("AutoGen", "https://microsoft.github.io/autogen/", "Microsoft's framework for building multi-agent AI applications with conversation patterns.", ["dev-tools"], "Free", "Open source", "free", ["Python", ".NET"], ["developers", "researchers"], ["multi-agent", "framework"], "2023"),
    make_entry("LangGraph", "https://www.langchain.com/langgraph", "LangChain's framework for building stateful, multi-actor agent workflows with graphs.", ["dev-tools"], "Free (open source)", "Paid cloud", "freemium", ["Python", "JavaScript"], ["developers"], ["graph-agents", "framework"], "2024"),
    make_entry("OpenAI Assistants API", "https://platform.openai.com/docs/assistants/overview", "OpenAI's API for building AI assistants with tools, code interpreter, and file search.", ["dev-tools"], "Pay-as-you-go", "API pricing", "usage-based", [], ["developers"], ["api", "assistants"], "2023"),
    make_entry("Vercel AI SDK", "https://sdk.vercel.ai", "TypeScript toolkit for building AI-powered streaming UIs and agents with any model provider.", ["dev-tools"], "Free (open source)", "Open source", "free", ["Next.js", "React", "Svelte"], ["developers"], ["sdk", "streaming-ui"], "2023"),
    make_entry("Mastra", "https://mastra.ai", "TypeScript AI framework for building agents, workflows, RAG, and evals quickly.", ["dev-tools"], "Free (open source)", "Open source", "free", ["TypeScript"], ["developers"], ["typescript", "framework"], "2024"),
    make_entry("Haystack", "https://haystack.deepset.ai", "Open-source Python framework for building production-ready LLM applications and RAG pipelines.", ["dev-tools"], "Free (open source)", "Paid cloud", "freemium", ["Python"], ["developers"], ["rag", "framework"], "2020"),
    make_entry("Relevance AI", "https://relevanceai.com", "No-code platform for building AI agents that automate tasks across sales, marketing, and ops.", ["dev-tools", "automation"], "$19/mo", "Free plan available", "freemium", [], ["business-users", "developers"], ["no-code", "agents"], "2020"),
    make_entry("Dify", "https://dify.ai", "Open-source LLM app development platform with visual workflow builder, RAG, and agent orchestration.", ["dev-tools"], "$59/mo", "Free self-hosted", "freemium", [], ["developers"], ["visual-builder", "rag"], "2023"),
    make_entry("Flowise", "https://flowiseai.com", "Open-source low-code tool to build LLM apps with drag-and-drop visual interface.", ["dev-tools"], "$35/mo", "Free self-hosted", "freemium", [], ["developers"], ["visual-builder", "low-code"], "2023"),

    # ── VECTOR DBS & RAG INFRASTRUCTURE ───────────────────
    make_entry("Pinecone", "https://www.pinecone.io", "Managed vector database purpose-built for AI applications with similarity search at scale.", ["dev-tools"], "$70/mo", "Free tier available", "freemium", [], ["developers"], ["vector-db", "rag"], "2019"),
    make_entry("Weaviate", "https://weaviate.io", "Open-source vector database with built-in ML models and hybrid search capabilities.", ["dev-tools"], "$25/mo", "Free sandbox", "freemium", [], ["developers"], ["vector-db", "open-source"], "2019"),
    make_entry("Chroma", "https://www.trychroma.com", "Open-source embedding database designed for AI applications. Python and JavaScript.", ["dev-tools"], "Free (open source)", "Paid cloud", "freemium", ["Python", "JavaScript"], ["developers"], ["vector-db", "open-source"], "2023"),
    make_entry("Qdrant", "https://qdrant.tech", "High-performance vector similarity search engine with Rust-based architecture.", ["dev-tools"], "$25/mo", "Free tier available", "freemium", [], ["developers"], ["vector-db", "search"], "2021"),

    # ── LLM API GATEWAYS & OBSERVABILITY ──────────────────
    make_entry("OpenRouter", "https://openrouter.ai", "Unified API for 300+ AI models with automatic failover, cost optimization, and analytics.", ["dev-tools"], "Pay-as-you-go", "Free to start", "usage-based", [], ["developers"], ["api-gateway", "multi-model"], "2023"),
    make_entry("LiteLLM", "https://www.litellm.ai", "Open-source proxy to call 100+ LLM APIs in OpenAI format with load balancing and logging.", ["dev-tools"], "Free (open source)", "Paid cloud", "freemium", ["Python"], ["developers"], ["api-gateway", "open-source"], "2023"),
    make_entry("LangSmith", "https://smith.langchain.com", "LangChain's platform for debugging, testing, and monitoring LLM applications.", ["dev-tools"], "$39/user/mo", "Free tier available", "freemium", [], ["developers"], ["observability", "evals"], "2023"),
    make_entry("Langfuse", "https://langfuse.com", "Open-source LLM engineering platform for observability, analytics, and prompt management.", ["dev-tools"], "$29/mo", "Free self-hosted", "freemium", [], ["developers"], ["observability", "open-source"], "2023"),
    make_entry("Helicone", "https://www.helicone.ai", "Open-source observability and gateway for LLMs with logging, caching, and rate limiting.", ["dev-tools"], "$50/mo", "Free tier available", "freemium", [], ["developers"], ["observability", "api-gateway"], "2023"),
    make_entry("Portkey", "https://portkey.ai", "AI gateway with 1600+ model integrations, observability, prompt management, and guardrails.", ["dev-tools"], "$49/mo", "Free tier available", "freemium", [], ["developers"], ["api-gateway", "observability"], "2023"),

    # ── WRITING & PRODUCTIVITY ────────────────────────────
    make_entry("Notion AI", "https://www.notion.so/product/ai", "AI writing assistant built into Notion for drafting, summarizing, and transforming content.", ["content", "productivity"], "$10/member/mo", "Add-on to Notion", "subscription", ["Notion"], ["knowledge-workers", "teams"], ["writing", "summarization"], "2023"),
    make_entry("Anyword", "https://anyword.com", "AI copywriting platform with predictive performance scores for marketing content.", ["content"], "$49/mo", "Free trial", "subscription", [], ["marketers"], ["copywriting", "performance"], "2013"),
    make_entry("Rytr", "https://rytr.me", "AI writing assistant with 40+ use cases and 30+ languages at affordable pricing.", ["content"], "$9/mo", "Free plan available", "freemium", [], ["solopreneurs", "budget-conscious"], ["copywriting"], "2021"),
    make_entry("Sudowrite", "https://www.sudowrite.com", "AI writing assistant built specifically for fiction authors with story development tools.", ["content"], "$19/mo", "Free trial", "subscription", [], ["fiction-writers", "authors"], ["fiction-writing"], "2020"),
    make_entry("QuillBot", "https://quillbot.com", "AI paraphrasing tool with grammar checker, summarizer, and citation generator.", ["content"], "$9.95/mo", "Free plan available", "freemium", [], ["students", "writers"], ["paraphrasing", "grammar"], "2017"),

    # ── MEETING & PRODUCTIVITY ────────────────────────────
    make_entry("Otter.ai", "https://otter.ai", "AI meeting transcription with summaries, action items, and integrations with Zoom, Meet, and Teams.", ["productivity"], "$8.33/mo", "Free plan available", "freemium", ["Zoom", "Google Meet", "Teams"], ["remote-teams", "solopreneurs"], ["transcription", "meetings"], "2016"),
    make_entry("Fireflies.ai", "https://fireflies.ai", "AI meeting assistant that records, transcribes, summarizes, and analyzes your meetings.", ["productivity"], "$10/user/mo", "Free plan available", "freemium", ["Zoom", "Google Meet", "Teams", "Webex"], ["remote-teams", "sales-teams"], ["meetings", "transcription"], "2016"),
    make_entry("Fathom", "https://fathom.video", "AI meeting assistant that records, transcribes, and summarizes calls with free forever plan.", ["productivity"], "Free", "Paid team plans", "freemium", ["Zoom", "Google Meet", "Teams"], ["remote-teams", "solopreneurs"], ["meetings", "transcription"], "2020"),
    make_entry("Granola", "https://www.granola.ai", "AI note-taker that enhances your raw meeting notes with context and summaries. Mac-first.", ["productivity"], "$10/mo", "Free 25 notes", "freemium", ["macOS"], ["knowledge-workers"], ["meetings", "notes"], "2023"),
    make_entry("tl;dv", "https://tldv.io", "AI meeting recorder for Zoom, Meet, and Teams with transcripts, summaries, and timestamps.", ["productivity"], "$18/user/mo", "Free plan available", "freemium", ["Zoom", "Google Meet", "Teams"], ["remote-teams"], ["meetings", "transcription"], "2020"),
    make_entry("Reclaim.ai", "https://reclaim.ai", "AI calendar assistant that automatically schedules tasks, habits, and meetings around priorities.", ["productivity"], "$10/user/mo", "Free plan available", "freemium", ["Google Calendar", "Outlook"], ["knowledge-workers"], ["calendar", "scheduling"], "2019"),
    make_entry("Motion", "https://www.usemotion.com", "AI task manager and calendar that automatically plans your day based on deadlines and meetings.", ["productivity"], "$19/user/mo", "7-day free trial", "subscription", ["Google Calendar", "Outlook"], ["solopreneurs", "small-teams"], ["calendar", "task-management"], "2019"),
    make_entry("Superhuman", "https://superhuman.com", "Fastest email experience with AI triage, instant replies, and productivity shortcuts.", ["productivity", "email"], "$30/mo", "30-day free trial", "subscription", ["Gmail", "Outlook"], ["executives", "power-users"], ["email", "productivity"], "2017"),

    # ── RESEARCH & DATA ───────────────────────────────────
    make_entry("Elicit", "https://elicit.com", "AI research assistant that finds, summarizes, and extracts data from academic papers.", ["research"], "$12/mo", "Free plan available", "freemium", [], ["researchers", "academics"], ["academic-research", "literature-review"], "2021"),
    make_entry("Consensus", "https://consensus.app", "AI-powered search engine for scientific research with evidence-backed answers from papers.", ["research"], "$9/mo", "Free plan available", "freemium", [], ["researchers", "students"], ["scientific-search"], "2022"),
    make_entry("Exa", "https://exa.ai", "AI search engine and API designed for finding specific web content by meaning, not keywords.", ["research", "dev-tools"], "Free tier", "Pay-as-you-go", "freemium", [], ["developers", "researchers"], ["search-api", "semantic-search"], "2023"),
    make_entry("Tavily", "https://tavily.com", "Search API optimized for AI agents with real-time web data, summaries, and citations.", ["research", "dev-tools"], "Pay-as-you-go", "Free tier available", "freemium", [], ["developers"], ["search-api", "agents"], "2023"),
    make_entry("Browse AI", "https://www.browse.ai", "No-code web scraping and monitoring tool that extracts data from any website.", ["research", "automation"], "$48.75/mo", "Free plan available", "freemium", [], ["solopreneurs", "analysts"], ["web-scraping", "monitoring"], "2021"),
    make_entry("Apify", "https://apify.com", "Web scraping and automation platform with 2,000+ ready-made actors and custom scraper development.", ["research", "automation", "dev-tools"], "$49/mo", "Free plan available", "freemium", [], ["developers", "data-teams"], ["web-scraping", "automation"], "2015"),
    make_entry("Firecrawl", "https://www.firecrawl.dev", "API that turns websites into LLM-ready markdown data for AI applications.", ["research", "dev-tools"], "$19/mo", "Free tier available", "freemium", [], ["developers"], ["web-scraping", "llm-data"], "2024"),

    # ── IMAGE & PHOTO EDITING ─────────────────────────────
    make_entry("Remove.bg", "https://www.remove.bg", "AI tool that removes image backgrounds automatically in 5 seconds with high quality.", ["design"], "$9/mo", "Free for low-res", "freemium", [], ["everyone"], ["background-removal"], "2018"),
    make_entry("Photoroom", "https://www.photoroom.com", "AI photo editor for ecommerce and social with background removal, shadows, and templates.", ["design", "ecom"], "$9.99/mo", "Free plan available", "freemium", [], ["ecommerce-sellers", "content-creators"], ["photo-editing", "product-photos"], "2019"),
    make_entry("Cleanup.pictures", "https://cleanup.pictures", "AI tool to remove objects, people, text, or defects from photos automatically.", ["design"], "$5/mo", "Free for low-res", "freemium", [], ["everyone"], ["photo-editing", "object-removal"], "2022"),
    make_entry("Upscale.media", "https://www.upscale.media", "AI image upscaler that enhances resolution up to 4x without losing quality.", ["design"], "Free", "Paid bulk", "freemium", [], ["everyone", "ecommerce-sellers"], ["image-upscaling"], "2022"),
    make_entry("Topaz Labs", "https://www.topazlabs.com", "Professional AI image and video enhancement for upscaling, denoising, and sharpening.", ["design", "video"], "$99 one-time", "Free trial", "one-time", [], ["photographers", "designers"], ["image-enhancement", "video-enhancement"], "2005"),

    # ── PRESENTATION & SLIDES ─────────────────────────────
    make_entry("Gamma", "https://gamma.app", "AI presentation generator that creates beautiful slide decks, docs, and webpages from prompts.", ["content", "design"], "$8/mo", "Free plan available", "freemium", [], ["solopreneurs", "small-teams"], ["presentations", "docs"], "2022"),
    make_entry("Tome", "https://tome.app", "AI-powered storytelling platform for generating presentations and pitches from a prompt.", ["content"], "$20/mo", "Free plan available", "freemium", [], ["founders", "marketers"], ["presentations", "storytelling"], "2022"),
    make_entry("Beautiful.ai", "https://www.beautiful.ai", "AI-powered presentation software with smart templates and design assistance.", ["design"], "$12/mo", "Free trial", "subscription", [], ["business-users"], ["presentations"], "2016"),
    make_entry("Pitch", "https://pitch.com", "Collaborative presentation software with AI slide generation and modern templates.", ["design"], "$10/user/mo", "Free plan available", "freemium", [], ["startups", "teams"], ["presentations", "collaboration"], "2018"),

    # ── FORMS & SURVEYS ───────────────────────────────────
    make_entry("Typeform", "https://www.typeform.com", "Conversational forms and surveys with AI-powered question suggestions and logic.", ["productivity"], "$25/mo", "Free plan available", "freemium", [], ["marketers", "small-teams"], ["forms", "surveys"], "2012"),
    make_entry("Tally", "https://tally.so", "Free form builder with unlimited forms, responses, and AI integration.", ["productivity"], "$29/mo", "Free unlimited plan", "freemium", [], ["solopreneurs", "budget-conscious"], ["forms", "surveys"], "2020"),
    make_entry("Fillout", "https://www.fillout.com", "Powerful form builder with conditional logic, payments, and AI-assisted form generation.", ["productivity"], "$19/mo", "Free plan available", "freemium", [], ["small-teams"], ["forms", "surveys"], "2022"),

    # ── TRANSLATION & LOCALIZATION ────────────────────────
    make_entry("DeepL", "https://www.deepl.com", "AI translation service known for higher accuracy than Google Translate across 31 languages.", ["content"], "$10.49/mo", "Free plan available", "freemium", [], ["everyone", "translators"], ["translation"], "2017"),
    make_entry("Lokalise", "https://lokalise.com", "Translation management platform with AI-powered suggestions for software and app localization.", ["content", "dev-tools"], "$140/mo", "14-day free trial", "subscription", [], ["developers", "product-teams"], ["localization", "translation"], "2017"),

    # ── LEGAL & COMPLIANCE ────────────────────────────────
    make_entry("DoNotPay", "https://donotpay.com", "AI lawyer helping consumers fight corporations, cancel subscriptions, and draft legal documents.", ["productivity"], "$36 every 3 months", "Paid only", "subscription", [], ["consumers"], ["legal", "consumer-rights"], "2015"),
    make_entry("Spellbook", "https://www.spellbook.legal", "AI contract drafting and review for lawyers built on GPT-4 with Word integration.", ["productivity"], "Custom pricing", "Demo available", "subscription", ["Microsoft Word"], ["lawyers"], ["legal", "contracts"], "2022"),
    make_entry("Harvey", "https://www.harvey.ai", "AI platform for elite law firms with research, drafting, and analysis tailored for legal work.", ["productivity"], "Custom pricing", "Enterprise only", "subscription", [], ["law-firms", "enterprises"], ["legal", "research"], "2022"),

    # ── HR & RECRUITING ───────────────────────────────────
    make_entry("HireVue", "https://www.hirevue.com", "AI-powered video interviewing and hiring platform with assessments and scheduling.", ["productivity"], "Custom pricing", "Demo available", "subscription", [], ["enterprises", "recruiters"], ["recruiting", "interviews"], "2004"),
    make_entry("Paradox Olivia", "https://www.paradox.ai", "Conversational AI recruiter that screens candidates, schedules interviews, and answers questions.", ["productivity", "customer-service"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["recruiting", "chatbot"], "2016"),

    # ── FINANCE & ACCOUNTING ──────────────────────────────
    make_entry("Ramp", "https://ramp.com", "Corporate card and spend management with AI expense categorization and reporting.", ["productivity"], "Free", "Paid Plus plan", "freemium", [], ["startups", "small-teams"], ["expense-management", "corporate-cards"], "2019"),
    make_entry("Brex", "https://www.brex.com", "AI-powered spend management platform with cards, expenses, and accounting automation.", ["productivity"], "Free", "Paid plans available", "freemium", [], ["startups", "enterprises"], ["spend-management"], "2017"),

    # ── MORE SOCIAL MEDIA ─────────────────────────────────
    make_entry("Typefully", "https://typefully.com", "AI-powered writing and scheduling tool for X/Twitter and LinkedIn with analytics.", ["social"], "$12/mo", "Free plan available", "freemium", ["X/Twitter", "LinkedIn"], ["content-creators", "solopreneurs"], ["writing", "scheduling"], "2021"),
    make_entry("Hypefury", "https://hypefury.com", "X/Twitter and LinkedIn growth tool with auto-scheduling, threads, and AI content generation.", ["social"], "$19/mo", "Free trial", "subscription", ["X/Twitter", "LinkedIn"], ["content-creators"], ["growth", "scheduling"], "2020"),
    make_entry("Tweet Hunter", "https://tweethunter.io", "X/Twitter growth platform with content ideas, scheduling, and AI tweet generation.", ["social"], "$49/mo", "Free trial", "subscription", ["X/Twitter"], ["content-creators"], ["twitter", "growth"], "2021"),
    make_entry("Publer", "https://publer.com", "Social media scheduling tool for 13+ networks with AI caption generation.", ["social"], "$9.60/mo", "Free plan available", "freemium", ["Instagram", "TikTok", "X/Twitter", "Facebook", "LinkedIn", "YouTube", "Pinterest", "Threads"], ["solopreneurs", "small-teams"], ["scheduling", "analytics"], "2016"),
    make_entry("Taplio", "https://taplio.com", "LinkedIn growth tool with viral post library, AI content generation, and scheduling.", ["social"], "$49/mo", "Free trial", "subscription", ["LinkedIn"], ["b2b-professionals", "solopreneurs"], ["linkedin", "growth"], "2022"),

    # ── MORE SALES & CRM ──────────────────────────────────
    make_entry("Outreach", "https://www.outreach.io", "Sales execution platform with AI-powered sequences, forecasting, and deal intelligence.", ["sales"], "Custom pricing", "Demo available", "subscription", ["Salesforce", "HubSpot"], ["enterprises", "growing-teams"], ["outreach", "forecasting"], "2011"),
    make_entry("Salesloft", "https://salesloft.com", "AI sales engagement platform with cadences, conversation intelligence, and forecasting.", ["sales"], "Custom pricing", "Demo available", "subscription", ["Salesforce", "HubSpot"], ["enterprises"], ["sales-engagement", "cadences"], "2011"),
    make_entry("Gong", "https://www.gong.io", "Revenue intelligence platform that captures and analyzes sales calls with AI insights.", ["sales"], "Custom pricing", "Demo available", "subscription", ["Salesforce", "HubSpot"], ["enterprises", "growing-teams"], ["conversation-intelligence"], "2015"),
    make_entry("Chorus", "https://www.zoominfo.com/chorus", "Conversation intelligence from ZoomInfo for recording and analyzing sales calls.", ["sales"], "Custom pricing", "Demo available", "subscription", ["Salesforce"], ["enterprises"], ["conversation-intelligence"], "2015"),
    make_entry("Cognism", "https://www.cognism.com", "B2B sales intelligence with GDPR-compliant contact data and AI prospecting tools.", ["sales"], "Custom pricing", "Demo available", "subscription", ["Salesforce", "HubSpot"], ["b2b-sales", "enterprises"], ["lead-gen", "data"], "2015"),
    make_entry("ZoomInfo", "https://www.zoominfo.com", "B2B contact database and sales intelligence platform with 100M+ professional profiles.", ["sales"], "Custom pricing", "Demo available", "subscription", ["Salesforce", "HubSpot"], ["enterprises", "b2b-sales"], ["lead-gen", "data"], "2007"),
    make_entry("Lavender", "https://www.lavender.ai", "AI email coach that scores your sales emails and suggests improvements in real-time.", ["sales", "email"], "$29/user/mo", "7-day free trial", "subscription", ["Gmail", "Outlook"], ["sales-teams"], ["email-coaching"], "2020"),
    make_entry("Regie.ai", "https://www.regie.ai", "AI sales sequence generator creating personalized multi-channel outbound campaigns.", ["sales", "email"], "Custom pricing", "Demo available", "subscription", ["Salesforce", "Outreach"], ["sales-teams"], ["sequences", "personalization"], "2020"),

    # ── MORE ECOMMERCE ────────────────────────────────────
    make_entry("Shopify Magic", "https://www.shopify.com/magic", "Shopify's built-in AI for product descriptions, email subject lines, and customer support.", ["ecom", "content"], "Included with Shopify", "Free with plan", "included", ["Shopify"], ["shopify-stores"], ["product-descriptions", "ai-assistant"], "2023"),
    make_entry("Vendoo", "https://vendoo.co", "Multi-channel crosslisting tool for resellers with AI descriptions and inventory sync.", ["ecom"], "$9.99/mo", "Free plan available", "freemium", ["eBay", "Poshmark", "Mercari", "Depop", "Etsy"], ["resellers", "solopreneurs"], ["crosslisting", "inventory"], "2019"),
    make_entry("Triple Whale", "https://www.triplewhale.com", "Ecommerce analytics and AI-powered insights for Shopify stores across ads, CAC, and LTV.", ["ecom", "analytics"], "$150/mo", "15-day free trial", "subscription", ["Shopify"], ["ecommerce-sellers"], ["ecom-analytics", "attribution"], "2021"),
    make_entry("Octane AI", "https://www.octaneai.com", "Shopify quiz and AI personalization platform for product recommendations and email capture.", ["ecom"], "$50/mo", "Free trial", "subscription", ["Shopify"], ["shopify-stores"], ["quizzes", "personalization"], "2018"),

    # ── CHATBOT BUILDERS ──────────────────────────────────
    make_entry("ManyChat", "https://manychat.com", "Chat marketing platform for Instagram, WhatsApp, Messenger with AI automation flows.", ["customer-service", "social"], "$15/mo", "Free plan available", "freemium", ["Instagram", "WhatsApp", "Facebook Messenger", "SMS"], ["small-businesses", "ecommerce-sellers"], ["chatbot", "marketing"], "2015"),
    make_entry("Chatfuel", "https://chatfuel.com", "No-code AI chatbot builder for WhatsApp, Instagram, and Facebook with GPT-powered responses.", ["customer-service"], "$29.99/mo", "Free plan available", "freemium", ["WhatsApp", "Instagram", "Facebook"], ["small-businesses"], ["chatbot", "no-code"], "2015"),
    make_entry("Botpress", "https://botpress.com", "Open-source AI chatbot platform with visual flow builder and LLM integration.", ["customer-service", "dev-tools"], "$89/mo", "Free tier available", "freemium", ["WhatsApp", "Slack", "Telegram", "Web"], ["developers", "small-teams"], ["chatbot", "open-source"], "2017"),
    make_entry("Voiceflow", "https://www.voiceflow.com", "AI agent and chatbot platform for collaborative design and deployment at scale.", ["customer-service", "dev-tools"], "$50/mo", "Free plan available", "freemium", [], ["product-teams", "developers"], ["chatbot", "voice"], "2018"),

    # ── MORE CUSTOMER SERVICE ─────────────────────────────
    make_entry("Ada", "https://www.ada.cx", "AI customer service platform that automates up to 83% of support interactions.", ["customer-service"], "Custom pricing", "Demo available", "subscription", ["Shopify", "Salesforce", "Zendesk"], ["enterprises"], ["ai-chatbot", "automation"], "2016"),
    make_entry("Forethought", "https://forethought.ai", "Generative AI customer support platform with intent prediction and agent assistance.", ["customer-service"], "Custom pricing", "Demo available", "subscription", ["Zendesk", "Salesforce", "Intercom"], ["enterprises"], ["ai-support", "agent-assist"], "2017"),

    # ── MORE ANALYTICS ────────────────────────────────────
    make_entry("Amplitude", "https://amplitude.com", "Product analytics with AI-powered insights, experimentation, and customer data platform.", ["analytics"], "$61/mo", "Free plan available", "freemium", [], ["product-teams", "growth-teams"], ["product-analytics", "experimentation"], "2012"),
    make_entry("Heap", "https://heap.io", "Digital insights platform with autocapture and AI-powered session replay analysis.", ["analytics"], "Custom pricing", "Free plan available", "freemium", [], ["product-teams"], ["product-analytics", "autocapture"], "2013"),
    make_entry("PostHog", "https://posthog.com", "Open-source product analytics, feature flags, session replay, and A/B testing platform.", ["analytics", "dev-tools"], "$0 (usage-based)", "Free 1M events/mo", "freemium", [], ["developers", "product-teams"], ["product-analytics", "open-source"], "2020"),
    make_entry("FullStory", "https://www.fullstory.com", "Digital experience intelligence with AI-powered session replay and friction analysis.", ["analytics"], "Custom pricing", "14-day free trial", "subscription", [], ["product-teams", "enterprises"], ["session-replay", "experience"], "2014"),

    # ── ENTERPRISE AI AGENT PLATFORMS ─────────────────────
    make_entry("Salesforce Agentforce", "https://www.salesforce.com/agentforce/", "Salesforce's autonomous AI agent platform managing customer lifecycle across service, sales, and marketing.", ["assistant", "customer-service", "sales"], "$2/conversation", "Demo available", "usage-based", ["Salesforce"], ["enterprises"], ["autonomous-agent", "enterprise"], "2024"),
    make_entry("Microsoft Copilot", "https://copilot.microsoft.com", "Microsoft's AI assistant integrated across Microsoft 365, Windows, and enterprise tools.", ["assistant", "productivity"], "$30/user/mo", "Free version available", "freemium", ["Microsoft 365", "Windows", "Teams", "Outlook"], ["enterprises", "everyone"], ["ai-assistant", "enterprise"], "2023"),
    make_entry("Glean", "https://www.glean.com", "Enterprise AI search and work assistant that finds information across all your company's apps.", ["assistant", "research"], "Custom pricing", "Demo available", "subscription", ["Slack", "Google Drive", "Notion", "Jira", "Salesforce"], ["enterprises"], ["enterprise-search", "rag"], "2019"),
    make_entry("Moveworks", "https://www.moveworks.com", "AI assistant for enterprise employees handling IT, HR, and operations support conversationally.", ["assistant", "customer-service"], "Custom pricing", "Demo available", "subscription", ["Slack", "Teams"], ["enterprises"], ["employee-support", "enterprise"], "2016"),
    make_entry("Sierra AI", "https://sierra.ai", "AI customer experience platform with conversational agents for enterprise support.", ["customer-service"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["ai-agent", "customer-experience"], "2023"),
    make_entry("Decagon", "https://decagon.ai", "AI customer service agents with human-level reasoning for enterprise support automation.", ["customer-service"], "Custom pricing", "Demo available", "subscription", ["Zendesk", "Salesforce"], ["enterprises"], ["ai-agent", "customer-service"], "2023"),
    make_entry("Cognigy", "https://www.cognigy.com", "Enterprise conversational AI platform for voice and chat customer service agents.", ["customer-service"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["voice-ai", "chatbot"], "2016"),
    make_entry("Aisera", "https://aisera.com", "Agentic AI platform for IT, HR, sales, and customer service automation at enterprise scale.", ["customer-service", "assistant"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["enterprise-ai", "automation"], "2017"),
    make_entry("Kore.ai", "https://kore.ai", "Enterprise conversational AI platform for deploying agents across voice, chat, and workflows.", ["customer-service", "assistant"], "Custom pricing", "Free tier available", "freemium", [], ["enterprises"], ["conversational-ai", "voice"], "2014"),

    # ── NEW AI AGENT BUILDERS ─────────────────────────────
    make_entry("Gumloop", "https://www.gumloop.com", "Visual no-code AI agent builder for automating workflows with drag-and-drop nodes.", ["automation", "dev-tools"], "$24/mo", "Free plan available", "freemium", [], ["business-users", "solopreneurs"], ["no-code", "visual-builder"], "2024"),
    make_entry("Relay.app", "https://www.relay.app", "Human-in-the-loop AI workflow automation with visual builder and app integrations.", ["automation"], "$9/user/mo", "Free plan available", "freemium", [], ["small-teams", "solopreneurs"], ["no-code", "workflow"], "2022"),
    make_entry("StackAI", "https://www.stack-ai.com", "No-code AI agent platform for building knowledge-based assistants and back-office automations.", ["automation", "dev-tools"], "$199/mo", "Free trial", "subscription", [], ["enterprises", "agencies"], ["no-code", "rag"], "2023"),
    make_entry("Beam AI", "https://beam.ai", "Agentic AI platform with pre-built agents and custom agent builder for enterprise operations.", ["automation"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["agents", "operations"], "2024"),
    make_entry("n8n", "https://n8n.io", "Open-source workflow automation with AI nodes, 400+ integrations, and self-hosting option.", ["automation"], "$20/mo", "Free self-hosted", "freemium", [], ["developers", "power-users"], ["workflow-automation", "open-source"], "2019"),
    make_entry("Tasklet", "https://tasklet.ai", "AI agent that connects to every tool you use and takes real actions — pulling reports, updating CRMs, triaging emails.", ["automation", "productivity"], "Contact sales", "Demo available", "subscription", [], ["small-teams", "solopreneurs"], ["agent", "integrations"], "2024"),
    make_entry("Userlens", "https://www.userlens.ai", "AI agents monitoring user behavior to catch churn signals months early in SaaS products.", ["analytics", "customer-service"], "Custom pricing", "Demo available", "subscription", [], ["saas-teams"], ["churn-prediction", "analytics"], "2024"),
    make_entry("Arzule", "https://arzule.com", "Partnership intelligence platform using AI agents to monitor SaaS ecosystem for opportunities.", ["sales"], "Custom pricing", "Demo available", "subscription", [], ["saas-teams"], ["partnerships", "intelligence"], "2024"),

    # ── AUTONOMOUS AGENTS ─────────────────────────────────
    make_entry("AgentGPT", "https://agentgpt.reworkd.ai", "Browser-based no-code platform for assembling, configuring, and deploying autonomous AI agents.", ["dev-tools"], "$40/mo", "Free tier available", "freemium", [], ["developers", "hobbyists"], ["autonomous-agent", "no-code"], "2023"),
    make_entry("AutoGPT", "https://agpt.co", "Open-source autonomous AI agent attempting complex goals by breaking them into sub-tasks.", ["dev-tools"], "Free (API costs)", "Open source", "free", ["Python"], ["developers"], ["autonomous-agent", "open-source"], "2023"),
    make_entry("BabyAGI", "https://github.com/yoheinakajima/babyagi", "Autonomous task management AI that creates, prioritizes, and executes tasks toward objectives.", ["dev-tools"], "Free", "Open source", "free", ["Python"], ["developers"], ["autonomous-agent", "open-source"], "2023"),
    make_entry("Superagent", "https://www.superagent.sh", "Open-source framework and cloud platform for building AI assistants and agents.", ["dev-tools"], "$20/mo", "Free self-hosted", "freemium", [], ["developers"], ["framework", "open-source"], "2023"),
    make_entry("Open Interpreter", "https://openinterpreter.com", "Code interpreter letting LLMs execute code locally on your computer for any task.", ["dev-tools", "productivity"], "Free", "Open source", "free", [], ["developers", "power-users"], ["code-interpreter", "open-source"], "2023"),
    make_entry("HyperWrite Self-Operating Computer", "https://www.hyperwriteai.com/self-operating-computer", "AI agent that operates a computer using mouse and keyboard to complete tasks.", ["dev-tools"], "$19/mo", "Free plan available", "freemium", [], ["developers", "power-users"], ["computer-use", "agent"], "2023"),

    # ── BROWSER & WEB AUTOMATION AGENTS ───────────────────
    make_entry("Browser Use", "https://browser-use.com", "Open-source library enabling AI to control browsers for web automation tasks.", ["dev-tools", "automation"], "Free", "Open source + cloud", "freemium", ["Playwright"], ["developers"], ["browser-automation", "open-source"], "2024"),
    make_entry("Skyvern", "https://www.skyvern.com", "AI browser automation using computer vision to understand and interact with any website.", ["automation", "dev-tools"], "$99/mo", "Free tier available", "freemium", [], ["developers", "businesses"], ["browser-automation", "vision"], "2024"),
    make_entry("Multi-On", "https://www.multion.ai", "Personal AI agent that browses the web and completes tasks on your behalf.", ["productivity"], "$20/mo", "Free trial", "subscription", [], ["consumers", "power-users"], ["browser-agent", "personal-ai"], "2023"),
    make_entry("Adept ACT-1", "https://www.adept.ai", "AI foundation models for actions that use software like a human would.", ["dev-tools"], "Custom pricing", "Enterprise only", "subscription", [], ["enterprises"], ["action-models", "enterprise"], "2022"),
    make_entry("Induced AI", "https://www.induced.ai", "AI agent that uses a real browser to automate repetitive workflows for businesses.", ["automation"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["browser-automation"], "2023"),

    # ── VOICE AI AGENTS ───────────────────────────────────
    make_entry("Vapi", "https://vapi.ai", "Developer platform for building voice AI agents with low-latency speech and any LLM.", ["dev-tools"], "Pay-as-you-go", "Free credits to start", "usage-based", [], ["developers"], ["voice-ai", "api"], "2023"),
    make_entry("Retell AI", "https://www.retellai.com", "Voice AI platform for building human-like conversational agents for phone calls.", ["dev-tools", "customer-service"], "$0.07/min", "Free credits", "usage-based", [], ["developers", "businesses"], ["voice-ai", "phone"], "2023"),
    make_entry("Bland AI", "https://www.bland.ai", "AI phone calling platform for building agents that handle inbound and outbound calls.", ["sales", "customer-service"], "$0.09/min", "Free trial", "usage-based", [], ["businesses", "sales-teams"], ["voice-ai", "phone-agents"], "2023"),
    make_entry("Air AI", "https://www.air.ai", "AI phone agents that hold 10-40 minute conversations for sales and customer service.", ["sales", "customer-service"], "Custom pricing", "Demo available", "subscription", [], ["enterprises", "sales-teams"], ["voice-ai", "phone"], "2023"),
    make_entry("PolyAI", "https://poly.ai", "Enterprise voice AI platform for customer-led conversations across industries.", ["customer-service"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["voice-ai", "enterprise"], "2017"),

    # ── SEARCH & DISCOVERY ────────────────────────────────
    make_entry("You.com", "https://you.com", "AI-powered search engine with conversational answers, citations, and customizable modes.", ["assistant", "research"], "$15/mo", "Free plan available", "freemium", [], ["everyone"], ["ai-search"], "2020"),
    make_entry("Andi Search", "https://andisearch.com", "Ad-free AI search engine that shows answers instead of links with visual results.", ["research"], "Free", "Completely free", "free", [], ["everyone"], ["ai-search"], "2021"),
    make_entry("Phind", "https://www.phind.com", "AI search engine for developers with code-aware answers and technical documentation.", ["coding", "research"], "$17/mo", "Free plan available", "freemium", [], ["developers"], ["developer-search"], "2022"),
    make_entry("Metaphor", "https://metaphor.systems", "Neural search engine that finds content by meaning and intent rather than keywords.", ["research", "dev-tools"], "API pricing", "Free credits", "usage-based", [], ["developers", "researchers"], ["semantic-search"], "2022"),
    make_entry("Kagi", "https://kagi.com", "Premium ad-free search engine with AI assistant integration and customizable results.", ["research"], "$10/mo", "Free trial", "subscription", [], ["power-users"], ["privacy-search"], "2022"),

    # ── PERSONAL KNOWLEDGE & NOTES ────────────────────────
    make_entry("Mem", "https://get.mem.ai", "AI-powered note-taking app that organizes thoughts, meetings, and ideas automatically.", ["productivity"], "$14.99/mo", "Free trial", "subscription", [], ["knowledge-workers"], ["notes", "ai-organization"], "2019"),
    make_entry("Reflect Notes", "https://reflect.app", "Note-taking app with GPT-4 integration for backlinking and generating ideas.", ["productivity"], "$10/mo", "Free trial", "subscription", [], ["knowledge-workers"], ["notes", "networked-thought"], "2021"),
    make_entry("Mymind", "https://mymind.com", "AI-powered bookmark and notes organizer that auto-categorizes everything you save.", ["productivity"], "$12.99/mo", "Free trial", "subscription", [], ["creatives", "researchers"], ["bookmarks", "notes"], "2020"),
    make_entry("Obsidian", "https://obsidian.md", "Knowledge base on local markdown files with AI plugins for search and generation.", ["productivity"], "$8/mo", "Free for personal use", "freemium", [], ["researchers", "writers"], ["notes", "local-first"], "2020"),
    make_entry("Supermemory", "https://supermemory.ai", "Your personal AI memory that remembers everything you read, save, or write.", ["productivity", "research"], "$10/mo", "Free tier available", "freemium", [], ["knowledge-workers"], ["personal-memory", "second-brain"], "2024"),

    # ── PROJECT MANAGEMENT ────────────────────────────────
    make_entry("Asana", "https://asana.com", "Project management platform with AI features for workload prediction, summaries, and automation.", ["productivity"], "$10.99/user/mo", "Free plan available", "freemium", [], ["teams", "enterprises"], ["project-management"], "2008"),
    make_entry("ClickUp", "https://clickup.com", "All-in-one project management with ClickUp AI for writing, summarizing, and automations.", ["productivity"], "$7/user/mo", "Free plan available", "freemium", [], ["teams"], ["project-management", "all-in-one"], "2017"),
    make_entry("Linear", "https://linear.app", "Modern issue tracking and project management with AI-powered summaries and automation.", ["productivity"], "$8/user/mo", "Free plan available", "freemium", [], ["software-teams"], ["issue-tracking"], "2019"),
    make_entry("monday.com", "https://monday.com", "Work management platform with AI assistant for summaries, formulas, and automations.", ["productivity"], "$9/user/mo", "Free plan available", "freemium", [], ["teams", "enterprises"], ["project-management"], "2012"),
    make_entry("Trello", "https://trello.com", "Visual project management with Butler automation and AI-powered features.", ["productivity"], "$5/user/mo", "Free plan available", "freemium", [], ["small-teams"], ["kanban"], "2011"),
    make_entry("Height", "https://height.app", "AI-native project management tool that automates task management and standup reports.", ["productivity"], "$6.99/user/mo", "Free plan available", "freemium", [], ["software-teams"], ["project-management", "ai-native"], "2019"),

    # ── DOCUMENT & PDF ────────────────────────────────────
    make_entry("ChatPDF", "https://www.chatpdf.com", "Chat with any PDF document — ask questions and get instant answers with citations.", ["productivity", "research"], "$5/mo", "Free for small PDFs", "freemium", [], ["students", "researchers"], ["pdf", "chat-with-docs"], "2023"),
    make_entry("PDF.ai", "https://pdf.ai", "AI tool to chat with PDFs, summarize documents, and extract insights.", ["productivity"], "$15/mo", "Free plan available", "freemium", [], ["researchers", "students"], ["pdf", "document-ai"], "2023"),
    make_entry("Humata", "https://www.humata.ai", "AI for professional documents — ask questions across multiple PDFs with citations.", ["productivity", "research"], "$9.99/mo", "Free plan available", "freemium", [], ["lawyers", "researchers"], ["document-ai", "citations"], "2022"),
    make_entry("LightPDF", "https://lightpdf.com/chatdoc", "AI chat tool for PDFs and documents with translation and summarization.", ["productivity"], "$5.99/mo", "Free trial", "subscription", [], ["everyone"], ["pdf", "document-chat"], "2018"),

    # ── DATA & SPREADSHEETS ───────────────────────────────
    make_entry("Rows", "https://rows.com", "AI-powered spreadsheet with ChatGPT integrated for data analysis and automation.", ["productivity", "analytics"], "$59/mo", "Free plan available", "freemium", [], ["analysts", "business-users"], ["spreadsheets", "ai-data"], "2018"),
    make_entry("Equals", "https://equals.com", "AI-native spreadsheet with built-in SQL, live data connections, and ChatGPT.", ["productivity", "analytics"], "$99/mo", "Free plan available", "freemium", [], ["analysts", "finance-teams"], ["spreadsheets", "sql"], "2021"),
    make_entry("Airtable", "https://www.airtable.com", "No-code database platform with AI features for automations and content generation.", ["productivity", "automation"], "$20/user/mo", "Free plan available", "freemium", [], ["teams"], ["database", "no-code"], "2012"),
    make_entry("Coda", "https://coda.io", "All-in-one doc with tables, AI writing, formulas, and integrations for teams.", ["productivity"], "$10/user/mo", "Free plan available", "freemium", [], ["teams"], ["docs", "database"], "2014"),
    make_entry("Numerous AI", "https://numerous.ai", "AI for Google Sheets and Excel with writing, classification, and data extraction.", ["productivity"], "$10/mo", "Free trial", "subscription", ["Google Sheets", "Excel"], ["analysts", "business-users"], ["spreadsheets", "ai-formulas"], "2023"),
    make_entry("Julius AI", "https://julius.ai", "AI data analyst that analyzes your files, creates visualizations, and answers questions.", ["analytics", "research"], "$17.99/mo", "Free plan available", "freemium", [], ["analysts", "researchers"], ["data-analysis", "visualization"], "2023"),

    # ── RECRUITING & HR ───────────────────────────────────
    make_entry("Ashby", "https://www.ashbyhq.com", "All-in-one recruiting platform with AI sourcing, scheduling, and analytics.", ["productivity"], "Custom pricing", "Demo available", "subscription", [], ["startups", "growing-teams"], ["recruiting", "ats"], "2020"),
    make_entry("Gem", "https://www.gem.com", "Recruiting CRM with AI sourcing and candidate engagement for talent teams.", ["productivity"], "Custom pricing", "Demo available", "subscription", ["LinkedIn", "Greenhouse"], ["recruiters", "enterprises"], ["recruiting", "sourcing"], "2017"),
    make_entry("Eightfold AI", "https://eightfold.ai", "Talent intelligence platform using AI for recruiting, retention, and career paths.", ["productivity"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["talent-intelligence"], "2016"),
    make_entry("Lever", "https://www.lever.co", "ATS and CRM with AI matching, nurture campaigns, and pipeline analytics.", ["productivity"], "Custom pricing", "Demo available", "subscription", [], ["growing-teams", "enterprises"], ["ats", "recruiting-crm"], "2012"),

    # ── FINANCE & ANALYTICS ───────────────────────────────
    make_entry("Mercury", "https://mercury.com", "Banking for startups with AI insights, spend controls, and automated bookkeeping.", ["productivity"], "Free", "Startup banking", "free", [], ["startups", "founders"], ["banking", "startup-tools"], "2019"),
    make_entry("Pilot", "https://pilot.com", "Bookkeeping, tax, and CFO services powered by AI for startups and small businesses.", ["productivity"], "$499/mo", "Demo available", "subscription", [], ["startups", "small-businesses"], ["bookkeeping", "accounting"], "2017"),
    make_entry("Puzzle", "https://puzzle.io", "AI-first accounting software for startups with real-time bookkeeping and insights.", ["productivity", "analytics"], "$200/mo", "Free tier available", "freemium", [], ["startups"], ["accounting", "bookkeeping"], "2020"),
    make_entry("Bench", "https://bench.co", "Online bookkeeping with AI-assisted categorization and monthly financial reports.", ["productivity"], "$299/mo", "1-month free trial", "subscription", [], ["small-businesses", "solopreneurs"], ["bookkeeping"], "2012"),

    # ── LEGAL ─────────────────────────────────────────────
    make_entry("Ironclad", "https://ironcladapp.com", "AI contract lifecycle management for legal teams with drafting, negotiation, and signing.", ["productivity"], "Custom pricing", "Demo available", "subscription", [], ["legal-teams", "enterprises"], ["contracts", "legal-ai"], "2014"),
    make_entry("Lawgeex", "https://www.lawgeex.com", "AI contract review platform that automates approvals for NDAs and sales agreements.", ["productivity"], "Custom pricing", "Demo available", "subscription", [], ["legal-teams", "enterprises"], ["contract-review"], "2014"),

    # ── HEALTHCARE & WELLNESS ─────────────────────────────
    make_entry("Abridge", "https://www.abridge.com", "AI medical scribe that generates clinical notes from patient conversations.", ["productivity", "customer-service"], "Custom pricing", "Demo available", "subscription", ["Epic", "Cerner"], ["healthcare"], ["medical-scribe", "healthcare-ai"], "2018"),
    make_entry("Nuance DAX", "https://www.nuance.com/healthcare/ambient-clinical-intelligence.html", "AI ambient clinical documentation from Microsoft that creates notes from conversations.", ["productivity"], "Custom pricing", "Demo available", "subscription", ["Epic", "Cerner"], ["healthcare"], ["medical-scribe", "healthcare-ai"], "2020"),

    # ── EDUCATION ─────────────────────────────────────────
    make_entry("Khanmigo", "https://www.khanmigo.ai", "AI tutor from Khan Academy for students, teachers, and parents.", ["productivity"], "$4/mo", "Free for teachers", "freemium", [], ["students", "teachers"], ["education", "tutoring"], "2023"),
    make_entry("Synthesis Tutor", "https://www.synthesis.com/tutor", "AI math tutor for kids that adapts to each student's pace and learning style.", ["productivity"], "$29/mo", "Free trial", "subscription", [], ["parents", "students"], ["education", "math"], "2023"),
    make_entry("Duolingo Max", "https://www.duolingo.com/max", "AI-powered language learning with Roleplay and Explain My Answer features.", ["productivity"], "$30/mo", "Free tier available", "freemium", [], ["language-learners"], ["language-learning"], "2023"),

    # ── MORE CODING & DEV ─────────────────────────────────
    make_entry("Warp", "https://www.warp.dev", "AI-powered terminal with natural language commands, autocomplete, and team collaboration.", ["coding", "productivity"], "$15/user/mo", "Free plan available", "freemium", [], ["developers"], ["terminal", "ai-cli"], "2020"),
    make_entry("Fig", "https://fig.io", "Terminal autocomplete and AI assistant now part of Amazon Q Developer.", ["coding"], "Free", "Part of Amazon Q", "free", [], ["developers"], ["terminal", "autocomplete"], "2020"),
    make_entry("Zed", "https://zed.dev", "High-performance collaborative code editor with AI assistant from the creators of Atom.", ["coding"], "Free", "Paid team plans", "freemium", [], ["developers"], ["code-editor", "collaboration"], "2021"),
    make_entry("Cline", "https://cline.bot", "Autonomous coding agent inside VS Code that can create, edit, and execute code.", ["coding"], "Free (API costs)", "Open source", "free", ["VS Code"], ["developers"], ["ai-coding", "autonomous"], "2024"),
    make_entry("Continue.dev", "https://www.continue.dev", "Open-source AI code assistant for VS Code and JetBrains with customizable models.", ["coding"], "Free (open source)", "Open source", "free", ["VS Code", "JetBrains"], ["developers"], ["ai-coding", "open-source"], "2023"),
    make_entry("Builder.io", "https://www.builder.io", "Visual development platform with AI that converts Figma designs to production code.", ["coding", "design"], "$19/user/mo", "Free plan available", "freemium", ["Figma"], ["developers", "designers"], ["design-to-code"], "2018"),
    make_entry("Locofy", "https://www.locofy.ai", "AI tool that converts Figma, Adobe XD, and Sketch designs to React, Next.js, HTML code.", ["coding", "design"], "$24/mo", "Free plan available", "freemium", ["Figma", "Adobe XD"], ["developers", "designers"], ["design-to-code"], "2021"),
    make_entry("Anima", "https://www.animaapp.com", "Design-to-code platform turning Figma designs into React, Vue, and HTML code.", ["coding", "design"], "$39/mo", "Free plan available", "freemium", ["Figma", "Sketch", "Adobe XD"], ["developers", "designers"], ["design-to-code"], "2017"),

    # ── PROMPT ENGINEERING ────────────────────────────────
    make_entry("PromptLayer", "https://promptlayer.com", "Prompt management, version control, and analytics for LLM applications.", ["dev-tools"], "$50/mo", "Free tier available", "freemium", [], ["developers"], ["prompt-management"], "2023"),
    make_entry("PromptPerfect", "https://promptperfect.jina.ai", "AI tool that optimizes your prompts for better results across different models.", ["dev-tools", "productivity"], "$9.99/mo", "Free tier available", "freemium", [], ["developers", "power-users"], ["prompt-optimization"], "2023"),
    make_entry("Agenta", "https://agenta.ai", "Open-source LLM development platform for prompt engineering, evaluation, and deployment.", ["dev-tools"], "$49/mo", "Free self-hosted", "freemium", [], ["developers"], ["prompt-engineering", "open-source"], "2023"),

    # ── DATA LABELING & TRAINING ──────────────────────────
    make_entry("Label Studio", "https://labelstud.io", "Open-source data labeling platform for machine learning with multi-type annotation support.", ["dev-tools"], "Free (open source)", "Paid enterprise", "freemium", [], ["ml-teams"], ["data-labeling", "open-source"], "2019"),
    make_entry("Scale AI", "https://scale.com", "Data platform for AI with labeling, RLHF, and model evaluation services.", ["dev-tools"], "Custom pricing", "Enterprise only", "subscription", [], ["enterprises", "ml-teams"], ["data-labeling", "rlhf"], "2016"),
    make_entry("Labelbox", "https://labelbox.com", "Training data platform with AI-assisted labeling and model evaluation workflows.", ["dev-tools"], "Custom pricing", "Free tier available", "freemium", [], ["ml-teams", "enterprises"], ["data-labeling"], "2018"),

    # ── MARKETING AUTOMATION ──────────────────────────────
    make_entry("Marketo", "https://www.marketo.com", "Adobe's marketing automation platform with AI for lead scoring, email, and campaigns.", ["email", "sales"], "Custom pricing", "Demo available", "subscription", ["Salesforce"], ["enterprises", "b2b"], ["marketing-automation"], "2006"),
    make_entry("Customer.io", "https://customer.io", "Messaging platform for sending personalized emails, push, SMS based on user behavior.", ["email"], "$100/mo", "Free trial", "subscription", [], ["saas-teams"], ["behavioral-messaging"], "2012"),
    make_entry("Iterable", "https://iterable.com", "Cross-channel marketing automation with AI-powered personalization and send time optimization.", ["email"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["cross-channel", "marketing-automation"], "2013"),
    make_entry("Braze", "https://www.braze.com", "Customer engagement platform with AI for cross-channel messaging and personalization.", ["email"], "Custom pricing", "Demo available", "subscription", [], ["enterprises"], ["customer-engagement"], "2011"),

    # ── REPUTATION & REVIEWS ──────────────────────────────
    make_entry("Trustpilot", "https://business.trustpilot.com", "Review management platform with AI-powered sentiment analysis and response tools.", ["customer-service"], "Custom pricing", "Free plan available", "freemium", [], ["businesses", "ecommerce-sellers"], ["reviews", "reputation"], "2007"),
    make_entry("Birdeye", "https://birdeye.com", "AI-powered reputation, reviews, and customer experience platform for multi-location businesses.", ["customer-service"], "Custom pricing", "Demo available", "subscription", [], ["multi-location"], ["reviews", "reputation"], "2012"),
    make_entry("Podium", "https://www.podium.com", "Customer interaction platform with AI for reviews, messaging, and payments for local businesses.", ["customer-service"], "$399/mo", "Demo available", "subscription", [], ["local-businesses"], ["messaging", "reviews"], "2014"),

    # ── LANDING PAGE & WEBSITE BUILDERS ───────────────────
    make_entry("Framer", "https://www.framer.com", "AI website builder that generates sites from prompts with CMS and responsive design.", ["design"], "$5/mo", "Free plan available", "freemium", [], ["designers", "founders"], ["website-builder", "ai-design"], "2014"),
    make_entry("Webflow", "https://webflow.com", "Visual web design platform with AI content generation and no-code publishing.", ["design"], "$14/mo", "Free plan available", "freemium", [], ["designers", "businesses"], ["website-builder", "no-code"], "2013"),
    make_entry("Durable", "https://durable.co", "AI website builder that creates a business website in 30 seconds with hosting and CRM.", ["design"], "$15/mo", "Free 30-day trial", "subscription", [], ["solopreneurs", "small-businesses"], ["website-builder", "ai"], "2021"),
    make_entry("10Web", "https://10web.io", "AI website builder powered by WordPress with automatic generation and optimization.", ["design"], "$10/mo", "Free trial", "subscription", ["WordPress"], ["solopreneurs", "small-businesses"], ["wordpress", "ai-builder"], "2017"),
    make_entry("Wix", "https://www.wix.com", "Website builder with AI Website Builder (ADI) that creates sites from answers to questions.", ["design"], "$17/mo", "Free plan available", "freemium", [], ["solopreneurs", "small-businesses"], ["website-builder"], "2006"),

    # ── PODCASTING ────────────────────────────────────────
    make_entry("Riverside", "https://riverside.fm", "Remote podcast and video recording with AI transcription, editing, and show notes.", ["video", "productivity"], "$15/mo", "Free plan available", "freemium", [], ["podcasters", "creators"], ["podcasting", "recording"], "2019"),
    make_entry("Descript Overdub", "https://www.descript.com/overdub", "AI voice cloning feature in Descript for seamlessly editing podcast audio.", ["video", "content"], "$24/mo", "Part of Descript", "subscription", [], ["podcasters"], ["voice-cloning"], "2020"),
    make_entry("Podcastle", "https://podcastle.ai", "AI-powered audio recording and editing platform for podcasters with voice cloning.", ["video"], "$14.99/mo", "Free plan available", "freemium", [], ["podcasters"], ["podcasting", "audio-editing"], "2020"),

    # ── COMMUNITY ─────────────────────────────────────────
    make_entry("Circle", "https://circle.so", "Community platform with AI-powered insights, personalization, and automation.", ["customer-service"], "$49/mo", "14-day free trial", "subscription", [], ["creators", "businesses"], ["community"], "2020"),
    make_entry("Mighty Networks", "https://www.mightynetworks.com", "Community platform with AI host that guides members to content and connections.", ["customer-service"], "$41/mo", "Free trial", "subscription", [], ["creators"], ["community"], "2017"),

    # ── SUPPORT & TICKETING (MORE) ────────────────────────
    make_entry("Kustomer", "https://www.kustomer.com", "Customer service CRM with AI for unified customer view and automation.", ["customer-service"], "$89/user/mo", "Demo available", "subscription", [], ["enterprises"], ["crm", "customer-service"], "2015"),
    make_entry("Front", "https://front.com", "Customer communication platform with AI assist, shared inboxes, and team collaboration.", ["customer-service", "email"], "$19/user/mo", "7-day free trial", "subscription", ["Gmail", "Outlook", "Slack"], ["small-teams"], ["shared-inbox", "email"], "2013"),
    make_entry("Dixa", "https://www.dixa.com", "Conversational customer service platform with AI agents for voice, chat, and email.", ["customer-service"], "$39/user/mo", "Demo available", "subscription", [], ["growing-teams"], ["conversational-cs"], "2015"),

    # ── PERSONAL FINANCE ──────────────────────────────────
    make_entry("Copilot Money", "https://copilot.money", "AI personal finance app that categorizes transactions and provides spending insights.", ["productivity"], "$13/mo", "Free trial", "subscription", [], ["consumers"], ["personal-finance"], "2020"),
    make_entry("Monarch Money", "https://www.monarchmoney.com", "Personal finance platform with AI-powered budgeting and net worth tracking.", ["productivity"], "$14.99/mo", "7-day free trial", "subscription", [], ["consumers"], ["personal-finance"], "2018"),

    # ── MORE PRODUCTIVITY AI TOOLS ────────────────────────
    make_entry("Shortwave", "https://www.shortwave.com", "Modern AI email client with inbox zero, smart summaries, and AI assistant.", ["email", "productivity"], "$9/mo", "Free plan available", "freemium", ["Gmail"], ["knowledge-workers"], ["email", "ai-client"], "2020"),
    make_entry("Spike", "https://www.spikenow.com", "Conversational email with AI writing, scheduling, and team collaboration features.", ["email", "productivity"], "$5/user/mo", "Free plan available", "freemium", ["Gmail", "Outlook"], ["teams", "solopreneurs"], ["email", "conversational"], "2014"),
    make_entry("Krisp", "https://krisp.ai", "AI noise cancellation app for calls with meeting assistant and transcription.", ["productivity"], "$8/mo", "Free plan available", "freemium", ["Zoom", "Google Meet", "Teams"], ["remote-workers"], ["noise-cancellation", "meetings"], "2017"),
    make_entry("Loom", "https://www.loom.com", "Async video messaging with AI transcripts, chapters, and automated summaries.", ["productivity", "video"], "$15/user/mo", "Free plan available", "freemium", [], ["remote-teams"], ["video-messaging"], "2015"),
    make_entry("Scribe", "https://scribehow.com", "AI tool that automatically creates step-by-step guides from any web-based process.", ["productivity"], "$29/user/mo", "Free plan available", "freemium", [], ["teams", "operations"], ["documentation", "sop"], "2019"),
    make_entry("Guidde", "https://www.guidde.com", "AI video documentation tool that creates how-to videos and knowledge bases automatically.", ["productivity", "video"], "$20/user/mo", "Free plan available", "freemium", [], ["teams"], ["video-documentation"], "2021"),
    make_entry("Read AI", "https://www.read.ai", "AI meeting assistant with engagement scores, summaries, and action items.", ["productivity"], "$19.75/user/mo", "Free plan available", "freemium", ["Zoom", "Google Meet", "Teams"], ["teams"], ["meetings", "engagement"], "2021"),

    # ── AI WRITING TOOLS (MORE) ───────────────────────────
    make_entry("WriteSmart", "https://writesmart.ai", "AI copywriting assistant for ads, emails, and landing pages with performance tracking.", ["content"], "$19/mo", "Free trial", "subscription", [], ["marketers"], ["copywriting"], "2023"),
    make_entry("Lex", "https://lex.page", "AI-native writing assistant for long-form content with collaboration and voice dictation.", ["content"], "$12/mo", "Free plan available", "freemium", [], ["writers"], ["long-form-writing"], "2022"),
    make_entry("AI Writer", "https://ai-writer.com", "AI content generation with accurate citations and research for article drafting.", ["content"], "$29/mo", "Free trial", "subscription", [], ["content-writers"], ["research-writing"], "2020"),

    # ── DATA VISUALIZATION ────────────────────────────────
    make_entry("Flourish", "https://flourish.studio", "Data visualization and storytelling tool with templates and AI-assisted insights.", ["analytics", "design"], "$69/mo", "Free plan available", "freemium", [], ["journalists", "analysts"], ["data-viz"], "2016"),
    make_entry("Datawrapper", "https://www.datawrapper.de", "Chart, map, and table builder used by newsrooms and researchers worldwide.", ["analytics"], "$599/mo", "Free plan available", "freemium", [], ["journalists", "analysts"], ["data-viz"], "2012"),
    make_entry("Observable", "https://observablehq.com", "Collaborative data visualization platform with AI assistance for analysts.", ["analytics", "dev-tools"], "$15/user/mo", "Free plan available", "freemium", [], ["data-teams"], ["data-viz", "notebooks"], "2017"),
]

def main():
    parser = argparse.ArgumentParser(description="sendbox.fun Bulk Agent Import")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    args = parser.parse_args()

    # Load existing
    if AGENTS_JSON_PATH.exists():
        with open(AGENTS_JSON_PATH) as f:
            data = json.load(f)
    else:
        data = {"lastUpdated": None, "agents": []}

    existing_ids = {a["id"] for a in data["agents"]}
    print(f"Existing agents: {len(data['agents'])}")

    added = 0
    skipped = 0
    for tool in TOOLS:
        if tool["id"] in existing_ids:
            skipped += 1
        else:
            data["agents"].append(tool)
            existing_ids.add(tool["id"])
            added += 1

    # Count per category
    cats = {}
    for a in data["agents"]:
        for c in a["categories"]:
            cats[c] = cats.get(c, 0) + 1

    print(f"\nNew agents added: {added}")
    print(f"Skipped (already exist): {skipped}")
    print(f"Total agents: {len(data['agents'])}")
    print(f"\nCategories breakdown:")
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")

    if args.dry_run:
        print("\n[DRY RUN] Not saving.")
    else:
        data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
        with open(AGENTS_JSON_PATH, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nSaved to {AGENTS_JSON_PATH}")

if __name__ == "__main__":
    main()
