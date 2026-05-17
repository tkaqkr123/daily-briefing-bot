from pydantic import BaseModel
import yaml


class SlackConfig(BaseModel):
    channel: str


class WeatherConfig(BaseModel):
    enabled: bool = True
    city: str = "Seoul"


class RssFeed(BaseModel):
    url: str
    label: str
    count: int = 2


class RssConfig(BaseModel):
    enabled: bool = True
    feeds: list[RssFeed] = []


class GithubConfig(BaseModel):
    enabled: bool = True
    repos: list[str] = []


class SourcesConfig(BaseModel):
    weather: WeatherConfig = WeatherConfig()
    rss: RssConfig = RssConfig()
    github: GithubConfig = GithubConfig()


class AppConfig(BaseModel):
    schedule: str = "0 8 * * *"
    slack: SlackConfig
    sources: SourcesConfig = SourcesConfig()


def load_config(path: str = "config.yml") -> AppConfig:
    with open(path) as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)
