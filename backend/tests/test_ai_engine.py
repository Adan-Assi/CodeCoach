import json

import pytest
from openai import OpenAIError

from ai_engine import LLMBadOutputError, LLMUnavailableError, run_analysis
from models import AnalyzeResponse

VALID = {
    "explanation": "Prints 1.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "suggestions": [],
}


def test_valid_output_is_parsed(fake_llm):
    fake_llm(content=json.dumps(VALID))
    result = run_analysis(code="print(1)")
    assert isinstance(result, AnalyzeResponse)
    assert result.time_complexity == "O(1)"


def test_provider_error_becomes_unavailable(fake_llm):
    fake_llm(raises=OpenAIError("boom"))
    with pytest.raises(LLMUnavailableError):
        run_analysis(code="print(1)")


def test_truncated_output_is_rejected(fake_llm):
    fake_llm(finish_reason="length")
    with pytest.raises(LLMBadOutputError):
        run_analysis(code="print(1)")


def test_empty_content_is_rejected(fake_llm):
    fake_llm(content=None)
    with pytest.raises(LLMBadOutputError):
        run_analysis(code="print(1)")


@pytest.mark.parametrize(
    "content",
    [
        "not json at all",
        '{"explanation": "missing the other keys"}',
        json.dumps({**VALID, "suggestions": "should be a list"}),
        "[1, 2, 3]",
        "```json\n" + json.dumps(VALID) + "\n```",  # fenced JSON is treated as bad output, not guessed at
    ],
)
def test_malformed_output_is_rejected(fake_llm, content):
    fake_llm(content=content)
    with pytest.raises(LLMBadOutputError):
        run_analysis(code="print(1)")


def test_prompt_keeps_indentation_and_handles_missing_language(fake_llm):
    calls = fake_llm(content=json.dumps(VALID))
    code = "def f():\n    return 1"

    run_analysis(code=code)

    user_message = calls[0]["messages"][1]["content"]
    assert code in user_message               # indentation intact
    assert "Language: unspecified" in user_message
    assert "None" not in user_message


def test_output_length_is_capped(fake_llm):
    calls = fake_llm(content=json.dumps(VALID))
    run_analysis(code="print(1)")
    assert "max_completion_tokens" in calls[0]  # a cost guardrail shouldn't silently disappear