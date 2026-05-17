from unittest.mock import patch, MagicMock
from src.fetchers.weather_fetcher import WeatherFetcher


def test_weather_fetcher_returns_summary():
    mock_forecast = MagicMock()
    mock_forecast.json.return_value = {
        "daily": {
            "weathercode": [0],
            "temperature_2m_max": [23.4],
            "temperature_2m_min": [14.4],
        }
    }
    mock_forecast.raise_for_status.return_value = None

    with patch.object(WeatherFetcher, "_get_coords", return_value=(37.5665, 126.9780)), \
         patch("httpx.get", return_value=mock_forecast):
        result = WeatherFetcher(city="Seoul").fetch()

    assert result.success is True
    assert result.label == "날씨"
    assert "맑음" in result.content
    assert "23" in result.content
    assert "14" in result.content


def test_weather_fetcher_handles_error():
    with patch.object(WeatherFetcher, "_get_coords", side_effect=Exception("city not found")):
        result = WeatherFetcher(city="UnknownCity").fetch()
    assert result.success is False
