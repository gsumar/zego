import aiohttp
import asyncio
from aiohttp import ClientSession

async def fetch(session: ClientSession, url: str) -> str | None:
    """Fetch the content of a URL asynchronously."""
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200 and response.content_type == "text/html":
                return await response.text()
    except Exception:
        pass
    return None

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'https://www.marca.com')

    print(html)

if __name__ == "__main__":
    asyncio.run(main())
