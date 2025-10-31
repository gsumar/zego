from aiohttp import ClientSession
from typing import Optional


class SessionManager:
    """Manages aiohttp ClientSession for making HTTP requests."""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize the SessionManager.
        
        Args:
            timeout: Default timeout for requests in seconds
        """
        self.timeout = timeout
        self.session: Optional[ClientSession] = None
    
    async def __aenter__(self):
        """Enter async context manager."""
        self.session = ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager and close session."""
        if self.session:
            await self.session.close()
    
    async def fetch(self, url: str) -> Optional[str]:
        """
        Fetch the content of a URL asynchronously.

        Args:
            url: The URL to fetch

        Returns:
            The HTML content as a string if successful, None otherwise
        """
        if not self.session:
            raise RuntimeError("SessionManager must be used as a context manager")

        try:
            async with self.session.get(url, timeout=self.timeout) as response:
                if response.status == 200 and response.content_type == "text/html":
                    return await response.text()
        except Exception:
            pass
        return None

