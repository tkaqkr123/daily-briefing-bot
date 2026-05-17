import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .config import AppConfig
from .fetchers.base import BaseFetcher, FetchResult
from .fetchers.rss_fetcher import RssFetcher
from .fetchers.weather_fetcher import WeatherFetcher
from .fetchers.github_fetcher import GithubFetcher
from .summarizer import AISummarizer
from .publisher import SlackPublisher

logger = logging.getLogger(__name__)


def build_fetchers(config: AppConfig) -> list[BaseFetcher]:
    fetchers: list[BaseFetcher] = []
    if config.sources.weather.enabled:
        fetchers.append(WeatherFetcher(city=config.sources.weather.city))
    if config.sources.rss.enabled and config.sources.rss.feeds:
        feeds = [{"url": f.url, "label": f.label} for f in config.sources.rss.feeds]
        fetchers.append(RssFetcher(feeds=feeds))
    if config.sources.github.enabled and config.sources.github.repos:
        fetchers.append(GithubFetcher(repos=config.sources.github.repos))
    return fetchers


def run_pipeline(config: AppConfig) -> bool:
    fetchers = build_fetchers(config)
    results: list[FetchResult] = []

    with ThreadPoolExecutor(max_workers=max(len(fetchers), 1)) as executor:
        futures = {executor.submit(f.fetch): f for f in fetchers}
        for future in as_completed(futures):
            result = future.result()
            if not result.success:
                logger.warning(f"Fetcher failed [{result.label}]: {result.error}")
            results.append(result)

    summarizer = AISummarizer()
    summary = summarizer.summarize(results)

    if summary.success:
        text = summary.text
    else:
        logger.warning(f"AI summarization failed: {summary.error}. Using raw fallback.")
        lines = [f"[{r.label}] {r.content}" for r in results if r.success]
        text = "\n".join(lines) if lines else "오늘 브리핑 데이터를 가져오지 못했습니다."

    publisher = SlackPublisher(channel=config.slack.channel)
    pub_result = publisher.publish(text)
    return pub_result.success
