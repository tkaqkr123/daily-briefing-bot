import pytest
from src.config import load_config


def test_load_config_parses_channel(tmp_path):
    cfg = tmp_path / "config.yml"
    cfg.write_text("""
schedule: "0 8 * * *"
slack:
  channel: "#briefing"
sources:
  weather:
    enabled: true
    city: "Busan"
  rss:
    enabled: false
    feeds: []
  github:
    enabled: false
    repos: []
""")
    config = load_config(str(cfg))
    assert config.slack.channel == "#briefing"
    assert config.sources.weather.city == "Busan"
    assert config.sources.rss.enabled is False


def test_load_config_raises_on_missing_slack(tmp_path):
    cfg = tmp_path / "config.yml"
    cfg.write_text("schedule: '0 8 * * *'\n")
    with pytest.raises(Exception):
        load_config(str(cfg))
