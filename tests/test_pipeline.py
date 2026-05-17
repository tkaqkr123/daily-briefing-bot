from unittest.mock import patch, MagicMock
from src.pipeline import run_pipeline, build_fetchers
from src.config import AppConfig, SlackConfig, SourcesConfig, WeatherConfig, RssConfig, GithubConfig
from src.summarizer import SummaryResult
from src.publisher import PublishResult


def _config(weather=False, rss=False, github=False):
    return AppConfig(
        slack=SlackConfig(channel="#test"),
        sources=SourcesConfig(
            weather=WeatherConfig(enabled=weather, city="Seoul"),
            rss=RssConfig(enabled=rss, feeds=[]),
            github=GithubConfig(enabled=github, repos=[]),
        ),
    )


def test_run_pipeline_success():
    config = _config()
    with patch("src.pipeline.AISummarizer") as MockS, \
         patch("src.pipeline.SlackPublisher") as MockP:
        MockS.return_value.summarize.return_value = SummaryResult(text="브리핑", success=True)
        MockP.return_value.publish.return_value = PublishResult(success=True)
        assert run_pipeline(config) is True


def test_run_pipeline_fallback_on_ai_failure():
    config = _config()
    with patch("src.pipeline.AISummarizer") as MockS, \
         patch("src.pipeline.SlackPublisher") as MockP:
        MockS.return_value.summarize.return_value = SummaryResult(
            text="", success=False, error="API error"
        )
        MockP.return_value.publish.return_value = PublishResult(success=True)
        assert run_pipeline(config) is True
        sent_text = MockP.return_value.publish.call_args[0][0]
        assert "브리핑 데이터를 가져오지 못했습니다" in sent_text


def test_build_fetchers_only_enabled():
    config = _config(weather=True, rss=False, github=False)
    from src.fetchers.weather_fetcher import WeatherFetcher
    import os
    os.environ["OPENWEATHER_API_KEY"] = "test"
    fetchers = build_fetchers(config)
    assert len(fetchers) == 1
    assert isinstance(fetchers[0], WeatherFetcher)
