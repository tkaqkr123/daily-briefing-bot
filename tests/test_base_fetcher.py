from src.fetchers.base import FetchResult, BaseFetcher


def test_fetch_result_success():
    r = FetchResult(label="날씨", content="맑음", success=True)
    assert r.success is True
    assert r.error == ""


def test_fetch_result_failure():
    r = FetchResult(label="뉴스", content="", success=False, error="timeout")
    assert r.success is False
    assert r.error == "timeout"


def test_base_fetcher_is_abstract():
    import inspect
    assert inspect.isabstract(BaseFetcher)
