# 💬 CodeCoach — AI Code Mentor

## 🧠 Overview
CodeCoach helps developers understand and improve their code using AI.
Paste your snippet, and get:
- An explanation of what it does
- Estimated time & space complexity
- Suggestions for improvement

## 🛠️ Tech Stack
- Python + FastAPI
- OpenAI GPT API
- Streamlit (frontend)
- Deployed on Render & Streamlit Cloud

## 🚀 How to Run Locally
1. Clone this repo
2. Create `.env` file with your OpenAI API key
3. Run backend:
   ```bash
   uvicorn backend.main:app --reload