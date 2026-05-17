import feedparser
from .base import BaseFetcher, FetchResult


class RssFetcher(BaseFetcher):
    def __init__(self, feeds: list[dict]):
        self.feeds = feeds

    def fetch(self) -> FetchResult:
        try:
            headlines = []
            for feed_cfg in self.feeds:
                feed = feedparser.parse(feed_cfg["url"])
                for entry in feed.entries[:3]:
                    headlines.append(f"[{feed_cfg['label']}] {entry.title}")
            content = "\n".join(headlines) if headlines else "뉴스 없음"
            return FetchResult(label="뉴스", content=content, success=True)
        except Exception as e:
            return FetchResult(label="뉴스", content="", success=False, error=str(e))
