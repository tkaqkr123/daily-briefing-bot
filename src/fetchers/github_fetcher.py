import os
import httpx
from .base import BaseFetcher, FetchResult


class GithubFetcher(BaseFetcher):
    def __init__(self, repos: list[str]):
        self.repos = repos

    def fetch(self) -> FetchResult:
        try:
            token = os.environ.get("GITHUB_TOKEN", "")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            lines = []
            for repo in self.repos:
                resp = httpx.get(
                    f"https://api.github.com/repos/{repo}/issues",
                    headers=headers,
                    params={"state": "open", "per_page": 20},
                    timeout=10,
                )
                resp.raise_for_status()
                items = resp.json()
                prs = [i for i in items if "pull_request" in i]
                issues = [i for i in items if "pull_request" not in i]
                lines.append(f"{repo}: PR {len(prs)}개, 이슈 {len(issues)}개 열림")
            content = "\n".join(lines) if lines else "GitHub 정보 없음"
            return FetchResult(label="GitHub", content=content, success=True)
        except Exception as e:
            return FetchResult(label="GitHub", content="", success=False, error=str(e))
