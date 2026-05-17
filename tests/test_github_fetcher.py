from unittest.mock import patch, MagicMock
from src.fetchers.github_fetcher import GithubFetcher


def test_github_fetcher_counts_prs_and_issues(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_test")
    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"title": "PR 1", "pull_request": {}},
        {"title": "Issue 1"},
        {"title": "Issue 2"},
    ]
    mock_resp.raise_for_status.return_value = None
    with patch("httpx.get", return_value=mock_resp):
        result = GithubFetcher(repos=["owner/repo"]).fetch()
    assert result.success is True
    assert result.label == "GitHub"
    assert "PR 1개" in result.content
    assert "이슈 2개" in result.content


def test_github_fetcher_handles_error(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_test")
    with patch("httpx.get", side_effect=Exception("403 forbidden")):
        result = GithubFetcher(repos=["owner/repo"]).fetch()
    assert result.success is False
