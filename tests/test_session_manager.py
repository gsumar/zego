import pytest
from client.session_manager import SessionManager


@pytest.mark.asyncio
async def test_session_manager_context():
    """Test that SessionManager works as a context manager."""
    async with SessionManager(timeout=10) as manager:
        assert manager.session is not None


@pytest.mark.asyncio
async def test_session_manager_closes():
    """Test that SessionManager closes the session properly."""
    manager = SessionManager(timeout=10)
    async with manager:
        session = manager.session
        assert session is not None
    assert session.closed


@pytest.mark.asyncio
async def test_fetch_without_context_raises_error():
    """Test that fetch raises error when not used as context manager."""
    manager = SessionManager(timeout=10)
    with pytest.raises(RuntimeError, match="must be used as a context manager"):
        await manager.fetch("https://example.com")


@pytest.mark.asyncio
async def test_fetch_returns_html(mocker):
    """Test that fetch returns HTML content for valid response."""
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.content_type = "text/html"
    mock_response.text = mocker.AsyncMock(return_value="<html><body>Test</body></html>")
    mock_response.__aenter__ = mocker.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mocker.AsyncMock(return_value=None)

    async with SessionManager(timeout=10) as manager:
        manager.session.get = mocker.Mock(return_value=mock_response)
        result = await manager.fetch("https://example.com")

    assert result == "<html><body>Test</body></html>"


@pytest.mark.asyncio
async def test_fetch_returns_none_for_non_html(mocker):
    """Test that fetch returns None for non-HTML content."""
    mock_response = mocker.AsyncMock()
    mock_response.status = 200
    mock_response.content_type = "application/json"
    mock_response.__aenter__ = mocker.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mocker.AsyncMock(return_value=None)

    async with SessionManager(timeout=10) as manager:
        manager.session.get = mocker.Mock(return_value=mock_response)
        result = await manager.fetch("https://example.com")

    assert result is None


@pytest.mark.asyncio
async def test_fetch_returns_none_for_error_status(mocker):
    """Test that fetch returns None for non-200 status."""
    mock_response = mocker.AsyncMock()
    mock_response.status = 404
    mock_response.content_type = "text/html"
    mock_response.__aenter__ = mocker.AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = mocker.AsyncMock(return_value=None)

    async with SessionManager(timeout=10) as manager:
        manager.session.get = mocker.Mock(return_value=mock_response)
        result = await manager.fetch("https://example.com")

    assert result is None


@pytest.mark.asyncio
async def test_fetch_returns_none_on_exception(mocker):
    """Test that fetch returns None when an exception occurs."""
    async with SessionManager(timeout=10) as manager:
        manager.session.get = mocker.Mock(side_effect=Exception("Network error"))
        result = await manager.fetch("https://example.com")
    
    assert result is None

