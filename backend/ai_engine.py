import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_analysis(language: str, code: str) -> Dict[str, Any]:
    prompt = f"""
    You are CodeCoach, an AI coding mentor.

    Analyze this {language} code:

    {code}

    Return STRICT JSON:
    {{
      "explanation": "...",
      "time_complexity": "...",
      "space_complexity": "...",
      "suggestions": ["..."]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful coding mentor."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    import json
    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except:
        return { 
            "explanation": content,
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
            "suggestions": []
        }