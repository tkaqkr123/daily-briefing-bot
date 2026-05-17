import os
import httpx
from .base import BaseFetcher, FetchResult


class WeatherFetcher(BaseFetcher):
    def __init__(self, city: str):
        self.city = city

    def fetch(self) -> FetchResult:
        try:
            api_key = os.environ["OPENWEATHER_API_KEY"]
            resp = httpx.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": self.city, "appid": api_key, "units": "metric", "lang": "kr"},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            desc = data["weather"][0]["description"]
            high = data["main"]["temp_max"]
            low = data["main"]["temp_min"]
            content = f"{self.city} {desc}, 최고 {int(high)}°C / 최저 {int(low)}°C"
            return FetchResult(label="날씨", content=content, success=True)
        except Exception as e:
            return FetchResult(label="날씨", content="", success=False, error=str(e))
