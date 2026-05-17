from unittest.mock import patch, MagicMock
from src.fetchers.rss_fetcher import RssFetcher

FEEDS = [{"url": "http://example.com/rss", "label": "TestFeed"}]


def _make_entry(title, link=""):
    e = MagicMock()
    e.title = title
    e.link = link
    return e


def test_rss_fetcher_returns_headlines_with_links():
    mock_feed = MagicMock()
    mock_feed.entries = [
        _make_entry("Article One", "https://example.com/1"),
        _make_entry("Article Two", "https://example.com/2"),
    ]
    with patch("feedparser.parse", return_value=mock_feed):
        result = RssFetcher(feeds=FEEDS).fetch()
    assert result.success is True
    assert result.label == "뉴스"
    assert "Article One" in result.content
    assert "https://example.com/1" in result.content


def test_rss_fetcher_returns_headline_without_link():
    mock_feed = MagicMock()
    mock_feed.entries = [_make_entry("Article No Link", "")]
    with patch("feedparser.parse", return_value=mock_feed):
        result = RssFetcher(feeds=FEEDS).fetch()
    assert result.success is True
    assert "Article No Link" in result.content


def test_rss_fetcher_limits_to_3_per_feed():
    mock_feed = MagicMock()
    mock_feed.entries = [_make_entry(f"Article {i}", f"https://example.com/{i}") for i in range(10)]
    with patch("feedparser.parse", return_value=mock_feed):
        result = RssFetcher(feeds=FEEDS).fetch()
    assert result.content.count("Article") == 3


def test_rss_fetcher_handles_error():
    with patch("feedparser.parse", side_effect=Exception("network error")):
        result = RssFetcher(feeds=FEEDS).fetch()
    assert result.success is False
    assert result.error != ""
