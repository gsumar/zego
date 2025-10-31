import asyncio
from client import SessionManager
from helper import LinksExtractor, LinksDomainFilter, LinksPrinter, QueueManager
from yarl import URL

MAX_CONCURRENT_REQUESTS = 10

async def main(base_url: str):
    parsed_base = URL(base_url)
    domain = parsed_base.host

    extractor = LinksExtractor()
    domain_filter = LinksDomainFilter(domain)
    printer = LinksPrinter()
    queue_manager = QueueManager()

    visited = set()
    await queue_manager.add(base_url)
    sem = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with SessionManager(timeout=10) as session_manager:

        while queue_manager.is_incomplete():
            url = await queue_manager.get_next_unvisited(visited)

            async with sem:
                html = await session_manager.fetch(url)
                if html is None:
                    queue_manager.task_done()
                    continue

                links = extractor.extract(url, html)
                same_domain_links = domain_filter.filter(links)
                printer.print(url, same_domain_links)
                await queue_manager.add_unvisited(same_domain_links, visited)

            queue_manager.task_done()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Error: URL parameter is required")
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))

# python3 main.py https://www.bbc.com