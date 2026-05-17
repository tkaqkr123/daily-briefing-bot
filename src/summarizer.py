from dataclasses import dataclass, field
from datetime import date
from .fetchers.base import FetchResult

SECTION_EMOJI = {
    "날씨": "🌤",
    "뉴스": "📰",
    "GitHub": "🐙",
}


@dataclass
class SummaryResult:
    text: str
    success: bool
    error: str = field(default="")


class AISummarizer:
    def summarize(self, results: list[FetchResult]) -> SummaryResult:
        successful = [r for r in results if r.success and r.content]
        if not successful:
            return SummaryResult(text="", success=False, error="수집된 데이터 없음")

        today = date.today().strftime("%Y-%m-%d")
        lines = [f"📅 *{today} 일일 브리핑*\n"]

        for r in successful:
            emoji = SECTION_EMOJI.get(r.label, "•")
            lines.append(f"{emoji} *{r.label}*")
            for item in r.content.strip().split("\n"):
                lines.append(f"  • {item}")
            lines.append("")

        return SummaryResult(text="\n".join(lines).strip(), success=True)
