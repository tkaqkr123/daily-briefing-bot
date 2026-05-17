from src.summarizer import AISummarizer
from src.fetchers.base import FetchResult


def test_summarizer_returns_formatted_text():
    summarizer = AISummarizer()
    results = [
        FetchResult(label="날씨", content="서울 맑음, 최고 23°C / 최저 14°C", success=True),
        FetchResult(label="뉴스", content="[Hacker News] Article One\n[TechCrunch] Article Two", success=True),
    ]
    summary = summarizer.summarize(results)
    assert summary.success is True
    assert "일일 브리핑" in summary.text
    assert "날씨" in summary.text
    assert "맑음" in summary.text
    assert "뉴스" in summary.text


def test_summarizer_skips_failed_results():
    summarizer = AISummarizer()
    results = [
        FetchResult(label="날씨", content="맑음", success=True),
        FetchResult(label="뉴스", content="", success=False, error="timeout"),
    ]
    summary = summarizer.summarize(results)
    assert summary.success is True
    assert "뉴스" not in summary.text


def test_summarizer_fails_when_all_sources_failed():
    summarizer = AISummarizer()
    summary = summarizer.summarize([
        FetchResult(label="날씨", content="", success=False, error="err")
    ])
    assert summary.success is False
