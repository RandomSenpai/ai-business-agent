from fastapi import FastAPI
import os
import requests

app = FastAPI()

API_KEY = os.getenv("GEMINI_API_KEY")


def ask_ai(prompt):

    model = "gemini-2.5-flash"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    r = requests.post(url + f"?key={API_KEY}", json=payload)
    data = r.json()

    if "error" in data:
        return {
            "error": "Gemini API failed",
            "details": data["error"]
        }

    if "candidates" in data:
        return data["candidates"][0]["content"]["parts"][0]["text"]

    return {"error": "Unexpected response", "raw": data}


@app.get("/")
def home():
    return {"status": "AI agent running"}

@app.get("/models")
def list_models():

    url = "https://generativelanguage.googleapis.com/v1beta/models?key=" + API_KEY

    r = requests.get(url)

    return r.json()

@app.get("/plan")
def plan():

prompt = """
You are an AUTONOMOUS BUSINESS AGENT.

You run 3 income streams:
1. Tutoring business
2. Cologne resale business
3. Cello gig business

YOUR JOB:
- find actionable opportunities (not general advice)
- rank the TOP 5 opportunities ONLY
- give specific next actions I can do TODAY
- NO questions back to user
- NO explanations
- NO essays

OUTPUT FORMAT:

1. TOP OPPORTUNITIES (ranked)
- each must be specific and actionable

2. TODAY ACTION PLAN (hour-by-hour)

3. LEADS TO PURSUE (real-world targets like schools, platforms, venues)

4. MONEY PRIORITY FOCUS (what makes most money fastest)

Be strict, concise, and operational.
"""

    return {"result": ask_ai(prompt)}
