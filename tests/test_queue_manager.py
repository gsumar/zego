import pytest
import asyncio
from helper.queue_manager import QueueManager


@pytest.mark.asyncio
async def test_queue_manager_initialization():
    """Test that QueueManager initializes correctly."""
    queue_manager = QueueManager()
    assert queue_manager.queue is not None
    assert queue_manager.lock is not None
    assert queue_manager.is_empty()


@pytest.mark.asyncio
async def test_add_item():
    """Test adding an item to the queue."""
    queue_manager = QueueManager()
    await queue_manager.add("https://example.com")
    
    assert not queue_manager.is_empty()
    assert queue_manager.is_incomplete()


@pytest.mark.asyncio
async def test_get_next():
    """Test getting the next item from the queue."""
    queue_manager = QueueManager()
    url = "https://example.com"
    await queue_manager.add(url)
    
    result = await queue_manager.get_next()
    assert result == url


@pytest.mark.asyncio
async def test_task_done():
    """Test marking a task as done."""
    queue_manager = QueueManager()
    await queue_manager.add("https://example.com")
    
    url = await queue_manager.get_next()
    queue_manager.task_done()
    
    # After task_done, join should complete immediately
    await asyncio.wait_for(queue_manager.join(), timeout=0.1)


@pytest.mark.asyncio
async def test_is_empty():
    """Test is_empty method."""
    queue_manager = QueueManager()
    assert queue_manager.is_empty()
    
    await queue_manager.add("https://example.com")
    assert not queue_manager.is_empty()
    
    await queue_manager.get_next()
    assert queue_manager.is_empty()


@pytest.mark.asyncio
async def test_is_incomplete():
    """Test is_incomplete method."""
    queue_manager = QueueManager()
    assert not queue_manager.is_incomplete()
    
    await queue_manager.add("https://example.com")
    assert queue_manager.is_incomplete()


@pytest.mark.asyncio
async def test_join_waits_for_completion():
    """Test that join waits for all tasks to complete."""
    queue_manager = QueueManager()
    await queue_manager.add("https://example.com")
    
    # Get the item but don't mark it as done yet
    url = await queue_manager.get_next()
    
    # join should timeout because task is not done
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(queue_manager.join(), timeout=0.1)
    
    # Now mark it as done
    queue_manager.task_done()
    
    # join should complete immediately
    await asyncio.wait_for(queue_manager.join(), timeout=0.1)


@pytest.mark.asyncio
async def test_add_unvisited_filters_visited():
    """Test that add_unvisited only adds unvisited links."""
    queue_manager = QueueManager()
    visited = {"https://example.com/page1", "https://example.com/page2"}
    links = {"https://example.com/page1", "https://example.com/page3", "https://example.com/page4"}
    
    await queue_manager.add_unvisited(links, visited)
    
    # Should only add page3 and page4 (not page1 which is visited)
    url1 = await queue_manager.get_next()
    url2 = await queue_manager.get_next()
    
    added_urls = {url1, url2}
    assert "https://example.com/page3" in added_urls
    assert "https://example.com/page4" in added_urls
    assert "https://example.com/page1" not in added_urls


@pytest.mark.asyncio
async def test_add_unvisited_empty_links():
    """Test add_unvisited with empty links set."""
    queue_manager = QueueManager()
    visited = set()
    links = set()
    
    await queue_manager.add_unvisited(links, visited)
    
    assert queue_manager.is_empty()


@pytest.mark.asyncio
async def test_add_unvisited_all_visited():
    """Test add_unvisited when all links are already visited."""
    queue_manager = QueueManager()
    visited = {"https://example.com/page1", "https://example.com/page2"}
    links = {"https://example.com/page1", "https://example.com/page2"}
    
    await queue_manager.add_unvisited(links, visited)
    
    assert queue_manager.is_empty()


@pytest.mark.asyncio
async def test_get_next_unvisited_skips_visited():
    """Test that get_next_unvisited skips already visited URLs."""
    queue_manager = QueueManager()
    visited = {"https://example.com/page1"}
    
    await queue_manager.add("https://example.com/page1")
    await queue_manager.add("https://example.com/page2")
    
    # Should skip page1 and return page2
    url = await queue_manager.get_next_unvisited(visited)
    
    assert url == "https://example.com/page2"
    assert "https://example.com/page2" in visited


@pytest.mark.asyncio
async def test_get_next_unvisited_adds_to_visited():
    """Test that get_next_unvisited adds URL to visited set."""
    queue_manager = QueueManager()
    visited = set()
    
    await queue_manager.add("https://example.com/page1")
    
    url = await queue_manager.get_next_unvisited(visited)
    
    assert url == "https://example.com/page1"
    assert "https://example.com/page1" in visited


@pytest.mark.asyncio
async def test_get_next_unvisited_marks_visited_as_done():
    """Test that get_next_unvisited marks skipped URLs as done."""
    queue_manager = QueueManager()
    visited = {"https://example.com/page1"}
    
    await queue_manager.add("https://example.com/page1")
    await queue_manager.add("https://example.com/page2")
    
    # Get page2 (page1 should be marked as done automatically)
    url = await queue_manager.get_next_unvisited(visited)
    queue_manager.task_done()  # Mark page2 as done
    
    # join should complete because both are marked as done
    await asyncio.wait_for(queue_manager.join(), timeout=0.1)


@pytest.mark.asyncio
async def test_concurrent_add_unvisited_with_visited_set():
    """Test that concurrent add_unvisited calls respect the visited set."""
    queue_manager = QueueManager()
    visited = {"https://example.com/page1"}  # page1 already visited
    links1 = {"https://example.com/page1", "https://example.com/page2"}
    links2 = {"https://example.com/page2", "https://example.com/page3"}

    # Add concurrently
    await asyncio.gather(
        queue_manager.add_unvisited(links1, visited),
        queue_manager.add_unvisited(links2, visited)
    )

    # Collect all URLs from queue
    urls = []
    while not queue_manager.is_empty():
        urls.append(await queue_manager.get_next())

    # page1 should not be in queue (was visited)
    # page2 might appear twice (both calls added it since it wasn't in visited initially)
    # page3 should be in queue once
    assert "https://example.com/page1" not in urls
    assert "https://example.com/page2" in urls
    assert "https://example.com/page3" in urls


@pytest.mark.asyncio
async def test_concurrent_get_next_unvisited_no_duplicates():
    """Test that concurrent get_next_unvisited calls don't return duplicates."""
    queue_manager = QueueManager()
    visited = set()
    
    # Add multiple URLs
    for i in range(10):
        await queue_manager.add(f"https://example.com/page{i}")
    
    # Get URLs concurrently
    tasks = [queue_manager.get_next_unvisited(visited) for _ in range(10)]
    urls = await asyncio.gather(*tasks)
    
    # All URLs should be unique
    assert len(urls) == len(set(urls))
    assert len(visited) == 10


@pytest.mark.asyncio
async def test_multiple_items_fifo_order():
    """Test that items are retrieved in FIFO order."""
    queue_manager = QueueManager()
    urls = ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]
    
    for url in urls:
        await queue_manager.add(url)
    
    retrieved = []
    for _ in range(3):
        retrieved.append(await queue_manager.get_next())
    
    assert retrieved == urls


@pytest.mark.asyncio
async def test_complex_workflow():
    """Test a complex workflow simulating real usage."""
    queue_manager = QueueManager()
    visited = set()

    # Start with initial URL
    await queue_manager.add("https://example.com")

    # Process first URL
    url1 = await queue_manager.get_next_unvisited(visited)
    assert url1 == "https://example.com"

    # Discover new links
    discovered_links = {"https://example.com/page1", "https://example.com/page2"}
    await queue_manager.add_unvisited(discovered_links, visited)
    queue_manager.task_done()

    # Process second URL
    url2 = await queue_manager.get_next_unvisited(visited)
    assert url2 in discovered_links

    # Discover more links (only new ones to avoid duplicates in queue)
    more_links = {"https://example.com/page3"}
    await queue_manager.add_unvisited(more_links, visited)
    queue_manager.task_done()

    # Process remaining URLs
    url3 = await queue_manager.get_next_unvisited(visited)
    queue_manager.task_done()

    url4 = await queue_manager.get_next_unvisited(visited)
    queue_manager.task_done()

    # All URLs should be unique
    all_urls = {url1, url2, url3, url4}
    assert len(all_urls) == 4
    assert "https://example.com" in all_urls
    assert "https://example.com/page1" in all_urls
    assert "https://example.com/page2" in all_urls
    assert "https://example.com/page3" in all_urls

    # Join should complete
    await asyncio.wait_for(queue_manager.join(), timeout=0.1)

