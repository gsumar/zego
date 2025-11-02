from aiohttp import ClientSession, TCPConnector
from typing import Optional


class SessionManager:
    """Manages aiohttp ClientSession for making HTTP requests with connection pooling."""

    def __init__(self, timeout: int = 10, max_connections: int = 100):
        """
        Initialize the SessionManager with connection pooling.

        Args:
            timeout: Default timeout for requests in seconds
            max_connections: Maximum number of concurrent connections
        """
        self.timeout = timeout
        self.max_connections = max_connections
        self.session: Optional[ClientSession] = None

    async def __aenter__(self):
        """Enter async context manager with connection pooling."""
        # TCPConnector with connection pooling
        connector = TCPConnector(
            limit=self.max_connections,  # Max total connections
            limit_per_host=30,  # Max connections per host
            ttl_dns_cache=300,  # DNS cache for 5 minutes
            force_close=False,  # Reuse connections
            enable_cleanup_closed=True  # Clean up closed connections
        )
        self.session = ClientSession(connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager and close session."""
        if self.session:
            await self.session.close()

    async def fetch(self, url: str) -> Optional[str]:
        """
        Fetch the content of a URL asynchronously with early content-type checking.

        Args:
            url: The URL to fetch

        Returns:
            The HTML content as a string if successful, None otherwise
        """
        if not self.session:
            raise RuntimeError("SessionManager must be used as a context manager")

        try:
            async with self.session.get(url, timeout=self.timeout) as response:
                # Early status check
                if response.status != 200:
                    return None

                # Early content-type check (before downloading)
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' not in content_type:
                    return None

                # Download the full response with efficient encoding
                content = await response.text(encoding='utf-8', errors='ignore')

                return content
        except Exception:
            pass
        return None

