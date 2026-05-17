from unittest.mock import patch, MagicMock
from src.fetchers.weather_fetcher import WeatherFetcher


def test_weather_fetcher_returns_summary(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-key")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "weather": [{"description": "맑음"}],
        "main": {"temp_max": 23.4, "temp_min": 14.8},
    }
    mock_resp.raise_for_status.return_value = None
    with patch("httpx.get", return_value=mock_resp):
        result = WeatherFetcher(city="Seoul").fetch()
    assert result.success is True
    assert result.label == "날씨"
    assert "맑음" in result.content
    assert "23" in result.content
    assert "14" in result.content


def test_weather_fetcher_handles_error(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-key")
    with patch("httpx.get", side_effect=Exception("timeout")):
        result = WeatherFetcher(city="Seoul").fetch()
    assert result.success is False
