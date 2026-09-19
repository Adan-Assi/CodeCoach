# 💬 CodeCoach – AI Code Mentor

## 🧠 Overview

CodeCoach is a lightweight AI-powered backend system that helps developers **understand what their code does**, not just whether it runs.

You paste a code snippet, and the system returns:

- 🧾 A plain-English explanation
- ⚡ Time complexity (Big-O)
- 🧠 Space complexity (Big-O)
- 💡 Suggestions for improvement

At its core, CodeCoach is an **API-first backend built with FastAPI**, designed to later plug into an AI model (LLM) and a frontend UI.

---

## 🧰 Tech Stack

### Backend
- Python
- FastAPI (web framework)
- Pydantic (data validation & schemas)
- OpenAI
- pytest
- Uvicorn (ASGI server)

### Planned / Next
- Frontend (React + TypeScript (Vite))
- Deployment (Render / Railway / similar)

---

## 🚀 What's Built So Far

### 1. API Server

A running backend that exposes HTTP endpoints:

* `GET /health` → checks if server is alive
* `POST /analyze` → receives code and returns analysis (currently placeholder)

---

### 2. Typed Request System (Input Validation)

The backend expects structured input like:

```json
{
  "code": "print(1)",
  "language": "python"
}
```

This is validated automatically before the function runs.

---

### 3. Structured Response System

The backend guarantees responses like:

```json
{
  "explanation": "Counts how many pairs in the list sum to the target...",
  "time_complexity": "O(n²) — nested loop over the input",
  "space_complexity": "O(1) — only a counter is stored",
  "suggestions": ["Use a set or dict to reduce this to O(n)."]
}
```

So the frontend can rely on a consistent format.

---

### 4. Auto Documentation

FastAPI automatically generates interactive docs:

```
http://127.0.0.1:8000/docs
```

Which makes it possible to:

* Test endpoints live
* Send JSON requests
* See schemas automatically

---

## 🧪 How to Run Locally

### 1. Clone the project

```bash
git clone https://github.com/Adan-Assi/CodeCoach.git
cd CodeCoach
```


### 2. Create virtual environment

```bash
python -m venv .venv
```


### 3. Activate environment

**Windows (PowerShell):**

```bash
.venv\Scripts\Activate
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Set environment variables

Create a .env file in `backend/`:
```bash
OPENAI_API_KEY=your_api_key_here
```
(You can copy from .env.example)


### 6. Run the server

```bash
uvicorn main:app --reload
```
<em>The server requires OPENAI_API_KEY to be set. Without a valid key, /analyze returns 503.</em>


### 7. Open the API docs

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Running Tests

Install development dependencies (from `backend/`):
```bash
pip install -r requirements-dev.txt
````

Run the test suite (from `backend/`):

```bash
python -m pytest
```

> Note: Tests use a mocked LLM, so no real API key or external calls are required.

---

## 🔮 Roadmap

### ✅ Step 1: AI layer (implemented, verified with mocks)

- OpenAI integrated in `ai_engine.py`; the model is asked for JSON and the reply is validated with Pydantic
- Failure handling:
  - provider error or unavailable → `503`
  - unusable model output (malformed, wrong shape, truncated) → `502`
- Guardrails: output token cap, request timeout, limited retries
- Code is wrapped in delimiters and the model is told to treat it as data, not instructions (a mitigation, not a guarantee; not yet tested against a live model)

**Status:** implemented; verified with mocks; not yet verified against the live API.  
**Remaining:** run real snippets against the live API and tune the prompt based on the results.


### ✅ Step 2: Testing

- pytest suite covering:
  - valid outputs
  - malformed JSON and wrong response shapes
  - provider failures and truncated or empty responses
  - input validation, including that invalid input never reaches the LLM
- LLM replaced by a fake client via monkeypatching, so tests are deterministic and need no API key
- Manually verified that tests fail when key behaviors are removed (for example, the output token cap or the error status codes)

**Later:** coverage reporting; an opt-in live-API check.


### 🚧 Step 3: API hardening (next)

- Rate limiting per client (SlowAPI)
- CORS allowed origins read from configuration instead of code


### 🌐 Step 4: Frontend (planned)

React + TypeScript (Vite), with:
- code input box
- loading and error states
- results view: explanation, time complexity, space complexity, suggestions


### ☁️ Step 5: Deployment (planned)

- Backend: Render or Railway
- Frontend: Vercel
- Environment variable management on the host
- Production logging
- Health check: `/health` already exists


### 💭 Ideas (not planned)

- Model fallback if the primary model fails
- Caching for repeated requests
- Request logging middleware

---

## 📌 Status

- ✅ **Working:** FastAPI backend, LLM integration (verified with mocks), 21 automated tests
- 🚧 **Next:** rate limiting and CORS configuration
- ❌ **Not yet:** frontend, deployment, verification against the live OpenAI API

---

## 📁 Project Structure

```text
CodeCoach/
├── README.md
└── backend/
    ├── main.py                # FastAPI app, routes, mapping of errors to HTTP status codes
    ├── models.py              # Pydantic request/response schemas
    ├── ai_engine.py           # The only module that talks to the LLM provider
    ├── tests/                 # pytest suite (LLM mocked)
    ├── pytest.ini             # pytest configuration (run tests from backend/)
    ├── requirements.txt       # runtime dependencies
    ├── requirements-dev.txt   # runtime + test dependencies
    └── .env.example           # template for local configuration
```

---

## ⚙️ Configuration

Set these in `backend/.env` (copy from `.env.example`). The `.env` file is git-ignored and must never be committed.

| Variable | Required | Default | Purpose |
|:--|:--|:--|:--|
| `OPENAI_API_KEY` | Yes | none | API key. The server refuses to start without it. |
| `OPENAI_MODEL` | No | `gpt-4o` | Model used for analysis. |

The test suite sets its own dummy key and never calls the real API.

---

## 🚦 API Behavior

`POST /analyze` accepts `code` (1–8,000 characters) and an optional `language` (up to 30 characters).

The mapping of standard HTTP status codes to API outcomes is as follows:

| Status | Meaning |
|:--|:--|
| `200` | Analysis returned |
| `422` | Invalid input: missing or empty code, code over 8,000 characters, or language too long |
| `502` | The provider responded, but the output was unusable (malformed, wrong shape, or truncated) |
| `503` | Provider error or unavailable (network problem, rejected key, rate limit, or timeout) |

Error responses use generic messages. Provider error details are logged on the server and never returned to the client.

---

## ⚠️ Limitations

- Explanations and complexity estimates are generated by an LLM and can be wrong. Treat them as a starting point, not a verdict.
- Every request costs API credit. Input length and output tokens are capped to limit this.
- Submitted code is sent to a third-party provider (OpenAI).
- There is no authentication or rate limiting yet.
- The LLM integration has not yet been verified against the live API.

---

## 💡 Philosophy Behind CodeCoach

This project is not just about building an API.

It’s about learning:

> How real-world systems are structured:
>
> * Input → validation → processing → response

And gradually evolving from:

> “it works on my machine”
> to
> “it’s a real deployable system”

---

## 🧭 Final Note

This is the foundation phase.

Everything built so far is the **scaffolding** for the real product:
an AI-powered code understanding assistant.

Next step: **make it intelligent.**