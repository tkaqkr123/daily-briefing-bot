from unittest.mock import patch, MagicMock
from slack_sdk.errors import SlackApiError
from src.publisher import SlackPublisher


def test_publisher_sends_message(monkeypatch):
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test")
    mock_client = MagicMock()
    with patch("src.publisher.WebClient", return_value=mock_client):
        result = SlackPublisher(channel="#test").publish("Good morning!")
    assert result.success is True
    mock_client.chat_postMessage.assert_called_once_with(
        channel="#test", text="Good morning!"
    )


def test_publisher_retries_once_on_failure(monkeypatch):
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test")
    mock_client = MagicMock()
    mock_client.chat_postMessage.side_effect = SlackApiError(
        "error", {"error": "rate_limited"}
    )
    with patch("src.publisher.WebClient", return_value=mock_client), \
         patch("src.publisher.time.sleep"):
        result = SlackPublisher(channel="#test").publish("Hello")
    assert result.success is False
    assert mock_client.chat_postMessage.call_count == 2
