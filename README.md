# Zego Web Crawler

A fast, asynchronous web crawler built with Python and aiohttp.

## Features

- **Asynchronous crawling** with 50 concurrent workers
- **Connection pooling** for efficient HTTP requests
- **Regex-based link extraction** (3-5x faster than BeautifulSoup)
- **Domain filtering** to stay within the target website
- **Memory optimized** with early content-type checking

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py <url>
```

Example:
```bash
python main.py https://example.com
```

## Architecture

- **SessionManager**: HTTP client with connection pooling and early rejection
- **QueueManager**: Async queue with visited URL tracking
- **LinksExtractor**: Fast regex-based link extraction
- **LinksDomainFilter**: Filters links to stay within target domain
- **LinksPrinter**: Outputs discovered URLs

## Performance Optimizations

1. **Connection Pooling**: Reuses TCP connections (100 max, 30 per host)
2. **DNS Caching**: 5-minute TTL to reduce DNS lookups
3. **Early Content-Type Check**: Rejects non-HTML before downloading
4. **Compiled Regex**: Pre-compiled patterns for fast link extraction

## Testing

```bash
pytest tests/ -v
```

All 35 tests cover core functionality including concurrency, queue management, and HTTP handling.

