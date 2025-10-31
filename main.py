import asyncio
from client import SessionManager


async def main(url: str):
    async with SessionManager(timeout=10) as session_manager:
        html = await session_manager.fetch(url)

    print(html)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Error: URL parameter is required")
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))

# python3 main.py https://www.bbc.com