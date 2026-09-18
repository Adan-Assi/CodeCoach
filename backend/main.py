"""
backend/main.py

This file defines the backend API using FastAPI.

What this file does:
- Creates the FastAPI application instance (the server)
- Defines API endpoints (routes) like /health and /analyze
- Defines request/response "schemas" using Pydantic for validation
- Connects frontend requests (HTTP) to Python functions

API Design Summary:
“I need a way to check if backend is alive” → /health

“I need a way to send code and get analysis back” → /analyze

Goal:
Provide a clean API that the frontend (Vite app) can call.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import AnalyzeRequest, AnalyzeResponse
from ai_engine import run_analysis

# FastAPI application instance
app = FastAPI(title="CodeCoach API")

# CORS configuration to allow requests from the Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- API endpoints (routes) -----
# The HTTP routes exposed by the backend.
# Each endpoint is a function that runs when a specific URL is called.

# Method: GET
# URL: /health
# Purpose: Simple health check endpoint to verify that the backend is running.
@app.get("/health")
def health():
    return {"status": "ok"} # If the server is running and can respond, return ok.

# Method: POST
# URL: /analyze
# Purpose: Accepts a code snippet and returns an analysis of it.
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    """
    Notice that:
     Input(req) is validated against AnalyzeRequest, and
     Output is validated against AnalyzeResponse.
    """

    result = run_analysis(req.language, req.code)
    return AnalyzeResponse(**result)