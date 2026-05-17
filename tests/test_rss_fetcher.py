from unittest.mock import patch, MagicMock
from src.fetchers.rss_fetcher import RssFetcher

FEEDS = [{"url": "http://example.com/rss", "label": "TestFeed"}]

def test_rss_fetcher_returns_headlines():
    mock_feed = MagicMock()
    mock_feed.entries = [
        MagicMock(title="Article One"),
        MagicMock(title="Article Two"),
    ]
    with patch("feedparser.parse", return_value=mock_feed):
        result = RssFetcher(feeds=FEEDS).fetch()
    assert result.success is True
    assert result.label == "뉴스"
    assert "Article One" in result.content
    assert "Article Two" in result.content

def test_rss_fetcher_limits_to_3_per_feed():
    mock_feed = MagicMock()
    mock_feed.entries = [MagicMock(title=f"Article {i}") for i in range(10)]
    with patch("feedparser.parse", return_value=mock_feed):
        result = RssFetcher(feeds=FEEDS).fetch()
    assert result.content.count("Article") == 3

def test_rss_fetcher_handles_error():
    with patch("feedparser.parse", side_effect=Exception("network error")):
        result = RssFetcher(feeds=FEEDS).fetch()
    assert result.success is False
    assert result.error != ""
