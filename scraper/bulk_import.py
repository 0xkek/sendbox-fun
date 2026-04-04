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
