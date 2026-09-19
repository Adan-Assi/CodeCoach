# 🧠 CodeCoach – Engineering Notes

This file contains key design decisions and explanations.

---

## 📦 Why do we have requirements.txt and requirements-dev.txt?

### Decision
We split dependencies into production and development environments.

### Reasoning
- `requirements.txt` contains only runtime dependencies needed to run the FastAPI backend in production.
- `requirements-dev.txt` contains development tools like testing and debugging libraries (e.g., pytest, httpx).

### Dev answer
“I separated runtime and development dependencies to keep production environments minimal, faster to deploy, and more secure. Development tools like testing frameworks are isolated so they are not installed in production.”

---

## 🧪 Why use Pydantic models (AnalyzeRequest / AnalyzeResponse)?

### Decision
We define strict schemas for API input and output.

### Reasoning
- Ensures data validation before running logic
- Guarantees consistent API responses
- Improves type safety and documentation automatically via FastAPI

### Dev answer
“I used Pydantic models to enforce a strict contract between frontend and backend. It validates input automatically and ensures consistent structured output.”

---

## 🌐 Why FastAPI?

### Decision
FastAPI is used as backend framework.

### Reasoning
- Built-in request validation with Pydantic
- Automatic OpenAPI documentation (/docs)
- High performance and async support

### Dev answer
“I chose FastAPI because it provides automatic validation, built-in documentation, and is lightweight while still being production-ready.”

---

## 🤖 Why use an LLM (OpenAI) inside backend?

### Decision
Backend calls OpenAI API to analyze code.

### Reasoning
- Keeps frontend simple
- Centralizes AI logic in one place
- Allows better control over prompt + validation

### Dev answer
“I placed LLM logic in the backend to centralize control over prompts, validation, and error handling, instead of exposing API keys or logic to the frontend.”

---

## 🧱 Why separate ai_engine.py from main.py?

### Decision
AI logic is isolated from API routes.

### Reasoning
- Improves modularity
- Easier testing
- Keeps API layer clean

### Dev answer
“I separated AI logic from FastAPI routes to keep concerns isolated: API handling is in main.py, while AI processing is in ai_engine.py, making the code easier to maintain and test.”

---

## 🏛️ Key architectural idea

CodeCoach follows a simple structure:

Frontend → FastAPI → AI Engine → OpenAI → Structured Response → Frontend

---

## 🧪 How do we know our tests actually test something?

### Decision

We intentionally validate the test suite by breaking production behavior and observing test failures.

### Reasoning

- Tests are not just checked for “all passing”, but for **correct failure behavior**
- We deliberately simulate:
  - API errors (e.g., OpenAI failure → 503)
  - missing guardrails (e.g., token limits)
- When code behavior is changed, we verify that:
  - the **correct tests fail**
  - and unrelated tests remain stable

This ensures tests are meaningfully coupled to real behavior, not just superficial coverage.

A key insight is that this is a form of **manual mutation testing**:
we intentionally “mutate” (break) parts of the system and confirm the test suite detects it.

### Dev answer

“We verify our tests by intentionally breaking parts of the system, like error handling or model output validation, and ensuring the correct tests fail. This gives us confidence that the tests are meaningful and not just syntactic coverage, it's a lightweight form of mutation testing.”
