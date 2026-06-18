from fastapi import FastAPI
import os
import requests

app = FastAPI()

API_KEY = os.getenv("GEMINI_API_KEY")


def ask_ai(prompt):

    model = "gemini-1.5-flash-001"

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
You are my AI business assistant.

I run:
- tutoring
- cologne resale
- cello gigs

Do:
1. find opportunities
2. rank them
3. suggest schedule changes
4. draft outreach messages

Return structured plan.
"""

    return {"result": ask_ai(prompt)}
