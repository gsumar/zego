from abc import ABC, abstractmethod


class Printer(ABC):
    """Interface for printing output."""
    
    @abstractmethod
    def print(self, *args, **kwargs) -> None:
        """Print output."""
        pass


class LinksPrinter(Printer):
    """Prints links in a formatted tree structure."""
    
    def print(self, url: str, links: set[str]) -> None:
        """
        Print links in a formatted tree structure.
        
        Args:
            url: The base URL
            links: Set of links to print
        """
        print(f"\n🌐 {url}")
        for link in sorted(links):
            print(f" └─ {link}")

