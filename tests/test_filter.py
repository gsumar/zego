from helper.filter import LinksDomainFilter


def test_filter_by_domain_same_domain():
    """Test filtering links from the same domain."""
    links = {
        "https://example.com/page1",
        "https://example.com/page2",
        "https://other.com/page3"
    }

    domain_filter = LinksDomainFilter("example.com")
    result = domain_filter.filter(links)

    assert "https://example.com/page1" in result
    assert "https://example.com/page2" in result
    assert "https://other.com/page3" not in result
    assert len(result) == 2


def test_filter_by_domain_no_matches():
    """Test filtering when no links match the domain."""
    links = {
        "https://other1.com/page1",
        "https://other2.com/page2"
    }

    domain_filter = LinksDomainFilter("example.com")
    result = domain_filter.filter(links)

    assert len(result) == 0


def test_filter_by_domain_all_match():
    """Test filtering when all links match the domain."""
    links = {
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    }

    domain_filter = LinksDomainFilter("example.com")
    result = domain_filter.filter(links)

    assert len(result) == 3


def test_filter_by_domain_empty_set():
    """Test filtering an empty set of links."""
    links = set()

    domain_filter = LinksDomainFilter("example.com")
    result = domain_filter.filter(links)

    assert len(result) == 0


def test_filter_by_domain_with_subdomain():
    """Test that subdomains are treated as different domains."""
    links = {
        "https://example.com/page1",
        "https://sub.example.com/page2"
    }

    domain_filter = LinksDomainFilter("example.com")
    result = domain_filter.filter(links)

    assert "https://example.com/page1" in result
    assert "https://sub.example.com/page2" not in result
    assert len(result) == 1

