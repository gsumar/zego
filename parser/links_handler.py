from yarl import URL


def filter_by_domain(links: set[str], domain: str) -> set[str]:
    """Filter links to only include those matching the specified domain."""
    return {
        link for link in links
        if URL(link).host == domain
    }

