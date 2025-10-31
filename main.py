import asyncio
from client import SessionManager


async def main():
    async with SessionManager(timeout=10) as session_manager:
        html = await session_manager.fetch('https://www.marca.com')

    print(html)

if __name__ == "__main__":
    asyncio.run(main())
