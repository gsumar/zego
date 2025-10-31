import asyncio
from client import SessionManager
from helper import LinksExtractor, LinksDomainFilter, LinksPrinter
from yarl import URL

MAX_CONCURRENT_REQUESTS = 10

async def main(url: str):
    parsed_base = URL(url)
    domain = parsed_base.host

    extractor = LinksExtractor()
    domain_filter = LinksDomainFilter(domain)
    printer = LinksPrinter()

    sem = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with SessionManager(timeout=10) as session_manager:

        async with sem:
            html = await session_manager.fetch(url)
            links = extractor.extract(url, html)
            same_domain_links = domain_filter.filter(links)
            printer.print(url, same_domain_links)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Error: URL parameter is required")
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))

# python3 main.py https://www.bbc.com