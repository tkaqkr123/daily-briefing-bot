import os
from dataclasses import dataclass, field
from google import genai
from google.genai import types
from .fetchers.base import FetchResult

SYSTEM_PROMPT = """당신은 친근하고 유익한 일일 브리핑 어시스턴트입니다.
주어진 정보를 바탕으로 1-2문단의 자연스러운 하루 브리핑을 한국어로 작성해주세요.
톤은 친근하고 간결하게."""


@dataclass
class SummaryResult:
    text: str
    success: bool
    error: str = field(default="")


class AISummarizer:
    def __init__(self):
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    def summarize(self, results: list[FetchResult]) -> SummaryResult:
        successful = [r for r in results if r.success and r.content]
        if not successful:
            return SummaryResult(text="", success=False, error="수집된 데이터 없음")

        context = "\n\n".join(f"[{r.label}]\n{r.content}" for r in successful)
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=context,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                ),
            )
            return SummaryResult(text=response.text, success=True)
        except Exception as e:
            return SummaryResult(text="", success=False, error=str(e))
