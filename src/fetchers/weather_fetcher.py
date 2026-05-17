import httpx
from .base import BaseFetcher, FetchResult

WMO_CODES = {
    0: "맑음", 1: "대체로 맑음", 2: "구름 조금", 3: "흐림",
    45: "안개", 48: "안개",
    51: "이슬비", 53: "이슬비", 55: "이슬비",
    61: "비", 63: "비", 65: "강한 비",
    71: "눈", 73: "눈", 75: "강한 눈",
    80: "소나기", 81: "소나기", 82: "강한 소나기",
    95: "뇌우", 96: "뇌우(우박)", 99: "뇌우(우박)",
}


class WeatherFetcher(BaseFetcher):
    def __init__(self, city: str):
        self.city = city

    def _get_coords(self) -> tuple[float, float]:
        resp = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": self.city, "count": 1, "language": "ko", "format": "json"},
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            raise ValueError(f"도시를 찾을 수 없습니다: {self.city}")
        return results[0]["latitude"], results[0]["longitude"]

    def fetch(self) -> FetchResult:
        try:
            lat, lon = self._get_coords()
            resp = httpx.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "daily": "temperature_2m_max,temperature_2m_min,weathercode",
                    "timezone": "Asia/Seoul",
                    "forecast_days": 1,
                },
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()["daily"]
            code = data["weathercode"][0]
            high = data["temperature_2m_max"][0]
            low = data["temperature_2m_min"][0]
            desc = WMO_CODES.get(code, "날씨 정보 없음")
            content = f"{self.city} {desc}, 최고 {high:.0f}°C / 최저 {low:.0f}°C"
            return FetchResult(label="날씨", content=content, success=True)
        except Exception as e:
            return FetchResult(label="날씨", content="", success=False, error=str(e))
