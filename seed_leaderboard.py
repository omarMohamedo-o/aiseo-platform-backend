"""
Seed Leaderboard Script
Fetches a list of real, well-known top global domains and submits each one
to the local AISEO crawl-and-analyze endpoint so that the leaderboard
gets populated with authentic, real-world audit data.
"""
import asyncio
import httpx
import sys

# Real top global domains sourced from publicly known rankings.
# These are NOT fake — they are actual websites that will be crawled live.
TOP_DOMAINS = [
    ("google.com", "Google"),
    ("youtube.com", "YouTube"),
    ("facebook.com", "Facebook"),
    ("amazon.com", "Amazon"),
    ("wikipedia.org", "Wikipedia"),
    ("twitter.com", "Twitter"),
    ("instagram.com", "Instagram"),
    ("linkedin.com", "LinkedIn"),
    ("reddit.com", "Reddit"),
    ("netflix.com", "Netflix"),
    ("microsoft.com", "Microsoft"),
    ("apple.com", "Apple"),
    ("github.com", "GitHub"),
    ("stackoverflow.com", "StackOverflow"),
    ("medium.com", "Medium"),
    ("openai.com", "OpenAI"),
    ("shopify.com", "Shopify"),
    ("cloudflare.com", "Cloudflare"),
    ("stripe.com", "Stripe"),
    ("notion.so", "Notion"),
    ("figma.com", "Figma"),
    ("vercel.com", "Vercel"),
    ("docker.com", "Docker"),
    ("slack.com", "Slack"),
    ("zoom.us", "Zoom"),
]

API_URL = "http://localhost:8000/api/v1/websites/crawl-and-analyze"


async def crawl_domain(client: httpx.AsyncClient, domain: str, brand_name: str) -> bool:
    """Submit a single domain to the crawl-and-analyze endpoint."""
    print(f"  -> Crawling {domain} ({brand_name})...")
    payload = {
        "url": f"https://{domain}",
        "brand_name": brand_name,
        "max_pages": 1,
        "target_audience": "General",
        "focus_keywords": [],
    }
    try:
        response = await client.post(API_URL, json=payload, timeout=120.0)
        if response.status_code == 200:
            data = response.json()
            vis = data.get("visibility_score", 0)
            opp = data.get("opportunity_score", 0)
            print(f"  [OK] {domain} — visibility={vis}, opportunity={opp}")
            return True
        else:
            print(f"  [FAIL] {domain} — HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"  [FAIL] {domain} — {e}")
        return False


async def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    domains = TOP_DOMAINS[:limit]

    print(f"=== AISEO Leaderboard Seeder ===")
    print(f"Will crawl {len(domains)} real domains via {API_URL}\n")

    success = 0
    failed = 0

    async with httpx.AsyncClient() as client:
        for domain, brand in domains:
            ok = await crawl_domain(client, domain, brand)
            if ok:
                success += 1
            else:
                failed += 1
            # Small delay between requests to avoid overwhelming the server
            await asyncio.sleep(2)

    print(f"\n=== Done! {success} succeeded, {failed} failed ===")


if __name__ == "__main__":
    asyncio.run(main())
