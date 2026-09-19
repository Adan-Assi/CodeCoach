import pytest
from fastapi.testclient import TestClient
from openai import OpenAIError

import main
from ai_engine import LLMBadOutputError, LLMUnavailableError


@pytest.fixture
def api():
    return TestClient(main.app)


def test_health(api):
    r = api.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_analyze_success_without_language(api, fake_llm):
    fake_llm()
    r = api.post("/analyze", json={"code": "print(1)"})
    assert r.status_code == 200
    assert set(r.json()) == {"explanation", "time_complexity", "space_complexity", "suggestions"}


@pytest.mark.parametrize(
    "exc, status",
    [(LLMUnavailableError(), 503), (LLMBadOutputError(), 502)],
)
def test_errors_map_to_http_status(api, monkeypatch, exc, status):
    def boom(**kwargs):
        raise exc

    monkeypatch.setattr(main, "run_analysis", boom)
    r = api.post("/analyze", json={"code": "print(1)"})
    assert r.status_code == status


def test_provider_error_details_never_reach_the_client(api, fake_llm):
    fake_llm(raises=OpenAIError("sk-secret-detail"))
    r = api.post("/analyze", json={"code": "print(1)"})
    assert r.status_code == 503
    assert "sk-secret-detail" not in r.text


@pytest.mark.parametrize(
    "payload",
    [
        {},                                          # missing code
        {"code": ""},                                # too short
        {"code": "x" * 8001},                        # too long
        {"code": "print(1)", "language": "x" * 31},  # language too long
    ],
)
def test_invalid_input_is_rejected_before_calling_the_llm(api, fake_llm, payload):
    calls = fake_llm()
    r = api.post("/analyze", json=payload)
    assert r.status_code == 422
    assert calls == []  # validation happens before any money is spent


def test_max_length_code_is_accepted(api, fake_llm):
    fake_llm()
    r = api.post("/analyze", json={"code": "x" * 8000})
    assert r.status_code == 200