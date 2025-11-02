from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag


class Extractor(ABC):
    """Interface for extracting links from content."""

    @abstractmethod
    def extract(self, base_url: str, content: str) -> set[str]:
        """Extract links from content."""
        pass


class LinksExtractor(Extractor):
    """Extracts and normalizes all links from HTML content."""

    def extract(self, base_url: str, content: str) -> set[str]:
        """Extract and normalize all links from HTML."""
        soup = BeautifulSoup(content, "html.parser")
        found_links = set()
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            href = urldefrag(href)[0]  # Remove URL fragment (#...)
            full_url = urljoin(base_url, href)
            found_links.add(full_url)
        return found_links

