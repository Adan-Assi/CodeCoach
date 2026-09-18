# 💬 CodeCoach — AI Code Mentor

## 🧠 Overview

CodeCoach is a lightweight AI-powered backend system that helps developers **understand what their code does**, not just whether it runs.

You paste a code snippet, and the system returns:

- 🧾 A plain-English explanation
- ⚡ Time complexity (Big-O)
- 🧠 Space complexity (Big-O)
- 💡 Suggestions for improvement

At its core, CodeCoach is an **API-first backend built with FastAPI**, designed to later plug into an AI model (LLM) and a frontend UI.

---

## 🏗️ Current State of the Project

Right now, CodeCoach is a **fully working backend API skeleton**:

✔ REST API running locally  
✔ Input validation using structured models  
✔ Auto-generated API documentation (`/docs`)  
✔ Request/response contracts enforced  
✔ Ready to plug in AI logic (next step)

---

## 🧰 Tech Stack

### Backend
- Python 🐍
- FastAPI ⚡ (web framework)
- Pydantic 📦 (data validation & schemas)
- Uvicorn (ASGI server)

### Planned / Next
- OpenAI API / LLM integration 🤖
- Frontend (Vite + React or Streamlit)
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
  "explanation": "Placeholder explanation.",
  "time_complexity": "O(?)",
  "space_complexity": "O(?)",
  "suggestions": ["Placeholder suggestion."]
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
cd CodeCoach/backend
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
pip install fastapi "uvicorn[standard]" pydantic
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

### 6. Open the API docs

```
http://127.0.0.1:8000/docs
```

---

## 🔮 Next Steps (Roadmap)

### 🚀 Step 1: Replace placeholder logic

* Connect `/analyze` to an LLM (OpenAI or similar)
* Send `req.code` to model
* Return real explanation + complexity

---

### 🌐 Step 2: Build frontend

* Simple UI (paste code → see results)
* Options:

  * React (Vite)
  * or Streamlit (faster MVP)

---

### ⚙️ Step 3: Improve API design

* Add error handling
* Add logging
* Add rate limiting (optional)

---

### ☁️ Step 4: Deploy

* Backend → Render / Railway
* Frontend → Vercel / Streamlit Cloud

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