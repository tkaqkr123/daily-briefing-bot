import os
import time
import logging
from dataclasses import dataclass, field
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


@dataclass
class PublishResult:
    success: bool
    error: str = field(default="")


class SlackPublisher:
    def __init__(self, channel: str):
        self.channel = channel
        self.client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    def publish(self, text: str) -> PublishResult:
        for attempt in range(2):
            try:
                self.client.chat_postMessage(channel=self.channel, text=text)
                return PublishResult(success=True)
            except SlackApiError as e:
                logger.error(f"Slack publish attempt {attempt + 1} failed: {e}")
                if attempt == 0:
                    time.sleep(2)
        return PublishResult(success=False, error="전송 실패 (2회 시도)")
