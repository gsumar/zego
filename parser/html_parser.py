from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag


def extract_links(base_url: str, html: str) -> set[str]:
    """Extract and normalize all same-domain links from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    found_links = set()
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        href = urldefrag(href)[0]  # Remove URL fragment (#...)
        full_url = urljoin(base_url, href)
        found_links.add(full_url)
    return found_links

