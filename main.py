import asyncio
from client import SessionManager
from helper import LinksExtractor, LinksDomainFilter
from yarl import URL

async def main(url: str):
    parsed_base = URL(url)
    domain = parsed_base.host

    extractor = LinksExtractor()
    domain_filter = LinksDomainFilter(domain)

    async with SessionManager(timeout=10) as session_manager:
        html = await session_manager.fetch(url)
        links = extractor.extract(url, html)
        same_domain_links = domain_filter.filter(links)

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