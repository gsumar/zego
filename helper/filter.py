from abc import ABC, abstractmethod
from yarl import URL


class LinksFilter(ABC):
    """Interface for filtering links."""
    
    @abstractmethod
    def filter(self, links: set[str]) -> set[str]:
        """Filter links based on criteria."""
        pass


class LinksDomainFilter(LinksFilter):
    """Filters links to only include those matching a specific domain."""
    
    def __init__(self, domain: str):
        """
        Initialize the domain filter.
        
        Args:
            domain: The domain to filter by
        """
        self.domain = domain
    
    def filter(self, links: set[str]) -> set[str]:
        """Filter links to only include those matching the specified domain."""
        return {
            link for link in links
            if URL(link).host == self.domain
        }

