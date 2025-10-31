from helper.extractor import LinksExtractor


def test_extract_links_basic():
    """Test extracting links from basic HTML."""
    html = '<html><body><a href="/page1">Link 1</a><a href="/page2">Link 2</a></body></html>'
    base_url = "https://example.com"

    extractor = LinksExtractor()
    links = extractor.extract(base_url, html)

    assert "https://example.com/page1" in links
    assert "https://example.com/page2" in links
    assert len(links) == 2


def test_extract_links_absolute_urls():
    """Test extracting absolute URLs."""
    html = '<html><body><a href="https://example.com/page1">Link</a></body></html>'
    base_url = "https://example.com"

    extractor = LinksExtractor()
    links = extractor.extract(base_url, html)

    assert "https://example.com/page1" in links


def test_extract_links_removes_fragments():
    """Test that URL fragments are removed."""
    html = '<html><body><a href="/page#section">Link</a></body></html>'
    base_url = "https://example.com"

    extractor = LinksExtractor()
    links = extractor.extract(base_url, html)

    assert "https://example.com/page" in links
    assert "https://example.com/page#section" not in links


def test_extract_links_ignores_tags_without_href():
    """Test that tags without href are ignored."""
    html = '<html><body><a>No href</a><a href="/page">With href</a></body></html>'
    base_url = "https://example.com"

    extractor = LinksExtractor()
    links = extractor.extract(base_url, html)

    assert len(links) == 1
    assert "https://example.com/page" in links


def test_extract_links_empty_html():
    """Test extracting links from empty HTML."""
    html = '<html><body></body></html>'
    base_url = "https://example.com"

    extractor = LinksExtractor()
    links = extractor.extract(base_url, html)

    assert len(links) == 0


def test_extract_links_duplicate_links():
    """Test that duplicate links are deduplicated."""
    html = '<html><body><a href="/page">Link 1</a><a href="/page">Link 2</a></body></html>'
    base_url = "https://example.com"

    extractor = LinksExtractor()
    links = extractor.extract(base_url, html)

    assert len(links) == 1
    assert "https://example.com/page" in links

