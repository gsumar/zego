import asyncio
from client import SessionManager
from parser import extract_links, filter_by_domain
from yarl import URL

async def main(url: str):
    parsed_base = URL(url)
    domain = parsed_base.host
    async with SessionManager(timeout=10) as session_manager:
        html = await session_manager.fetch(url)
        links = extract_links(url, html)
        same_domain_links = filter_by_domain(links, domain)
    print(same_domain_links)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Error: URL parameter is required")
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))

# python3 main.py https://www.bbc.com