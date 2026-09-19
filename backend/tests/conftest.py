"""
backend/tests/conftest.py

This file defines shared pytest fixtures used across multiple tests (reusable components.)

It provides a controlled testing environment by replacing external dependencies
(such as the OpenAI API) with fake implementations.

Main purpose:
- Avoid real API calls during tests (faster, free, and reliable)
- Provide predictable outputs for consistent test results
- Allow inspection of what was sent to external services

Key components:
- A dummy OPENAI_API_KEY to prevent runtime errors during import
- A VALID_JSON sample response that mimics a real LLM output
- A fake_llm fixture that uses monkeypatch to replace the real OpenAI client
  inside ai_engine with a fake version
  
The fake client follows the same structure as the real OpenAI SDK (duck typing),
so the application behaves as if it is calling the real API, but actually uses
predefined responses instead.

Notes: 
- Monkeypatch is a pytest testing tool that allows us to replace attributes
  or functions with our own versions for testing purposes.

- Fixtures defined here are automatically discovered by pytest and injected into any test
  function that requests them by name (e.g. fake_llm), so they do NOT need to be imported
  in test files.
  Any file named test_*.py or inside the tests/ directory is automatically  treated as
  a test module by pytest.
"""

import json
import os

os.environ["OPENAI_API_KEY"] = "test-key"

from types import SimpleNamespace # used to create simple objects with attributes for mocking

import pytest

# a valid JSON string (as defined in AnalyzeResponse model), that
# the fake LLM will return when called.
VALID_JSON = json.dumps(
    {
        "explanation": "Prints 1.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "suggestions": ["Add a docstring."],
    }
)


@pytest.fixture
def fake_llm(monkeypatch):
    """Replace the OpenAI client inside ai_engine. Returns a list of the kwargs each call received."""
    import ai_engine

    def install(content=VALID_JSON, finish_reason="stop", raises=None):
        calls = []

        def create(**kwargs):
            calls.append(kwargs)
            if raises is not None:
                raise raises
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        finish_reason=finish_reason,
                        message=SimpleNamespace(content=content),
                    )
                ]
            )

        # create a fake client that mimics the structure of the real OpenAI client,
        # but uses our create function instead of making real API calls.
        fake_client = SimpleNamespace(
            chat=SimpleNamespace(completions=SimpleNamespace(create=create))
        )

        # we replace the OpenAI client in ai_engine with our fake_client.
        monkeypatch.setattr(ai_engine, "client", fake_client)
        return calls

    return install # return the install function so tests can call it to set up the fake LLM