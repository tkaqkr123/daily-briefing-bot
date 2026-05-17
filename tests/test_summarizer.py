from unittest.mock import patch, MagicMock
from src.summarizer import AISummarizer
from src.fetchers.base import FetchResult


def test_summarizer_returns_text(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    mock_response = MagicMock()
    mock_response.text = "오늘 날씨가 맑습니다!"
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with patch("google.generativeai.configure"), \
         patch("google.generativeai.GenerativeModel", return_value=mock_model):
        summarizer = AISummarizer()
        results = [FetchResult(label="날씨", content="맑음 23도", success=True)]
        summary = summarizer.summarize(results)

    assert summary.success is True
    assert summary.text == "오늘 날씨가 맑습니다!"


def test_summarizer_skips_failed_results(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    mock_response = MagicMock()
    mock_response.text = "브리핑"
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with patch("google.generativeai.configure"), \
         patch("google.generativeai.GenerativeModel", return_value=mock_model):
        summarizer = AISummarizer()
        results = [
            FetchResult(label="날씨", content="맑음", success=True),
            FetchResult(label="뉴스", content="", success=False, error="timeout"),
        ]
        summarizer.summarize(results)

    call_args = mock_model.generate_content.call_args[0][0]
    assert "날씨" in call_args
    assert "뉴스" not in call_args


def test_summarizer_fails_when_all_sources_failed(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    with patch("google.generativeai.configure"), \
         patch("google.generativeai.GenerativeModel"):
        summarizer = AISummarizer()
        summary = summarizer.summarize([
            FetchResult(label="날씨", content="", success=False, error="err")
        ])
    assert summary.success is False
