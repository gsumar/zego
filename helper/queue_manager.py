import asyncio
from typing import Optional


class QueueManager:
    """Manages an asyncio.Queue for URL processing."""

    def __init__(self):
        """Initialize the queue manager."""
        self.queue: asyncio.Queue = asyncio.Queue()
        self.lock: asyncio.Lock = asyncio.Lock()
    
    async def add(self, item: str) -> None:
        """
        Add an item to the queue.
        
        Args:
            item: The item to add to the queue
        """
        await self.queue.put(item)
    
    async def get_next(self) -> str:
        """
        Get the next item from the queue.
        
        Returns:
            The next item from the queue
        """
        return await self.queue.get()
    
    def task_done(self) -> None:
        """Mark a task as done."""
        self.queue.task_done()
    
    def is_incomplete(self) -> bool:
        """
        Check if there are incomplete tasks in the queue.
        
        Returns:
            True if queue is not empty, False otherwise
        """
        return not self.queue.empty()
    
    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        
        Returns:
            True if queue is empty, False otherwise
        """
        return self.queue.empty()
    
    async def join(self) -> None:
        """Wait until all tasks in the queue are processed."""
        await self.queue.join()

    async def add_unvisited(self, links: set[str], visited: set[str]) -> None:
        """
        Add unvisited links to the queue.

        Args:
            links: Set of links to potentially add
            visited: Set of already visited links
        """
        async with self.lock:
            for link in links:
                if link not in visited:
                    await self.add(link)

    async def get_next_unvisited(self, visited: set[str]) -> str:
        """
        Get the next unvisited URL from the queue.
        Skips already visited URLs and marks them as done.
        Waits for new items if queue is temporarily empty.

        Args:
            visited: Set of already visited URLs

        Returns:
            The next unvisited URL
        """
        while True:
            url = await self.get_next()
            async with self.lock:
                if url not in visited:
                    visited.add(url)
                    return url
            self.task_done()

