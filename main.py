from fastapi import FastAPI
import os
import requests

app = FastAPI()

API_KEY = os.getenv("GEMINI_API_KEY")


def ask_ai(prompt):
    model = "gemini-2.5-flash"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        r = requests.post(url, json=payload, timeout=20)
        data = r.json()

        if "error" in data:
            return {"error": data["error"]}

        # safer extraction
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return {"error": str(e)}

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
    prompt = YOUR_PROMPT_HERE
    return ask_ai(prompt)
    
    prompt = """
You are an AUTONOMOUS BUSINESS OPERATIONS ENGINE.

You manage:
- Tutoring business (clients, schools, parents)
- Cologne resale business (buyers, sourcing, margins)
- Cello gig business (weddings, venues, events)

RULES:
- You MUST output VALID JSON ONLY.
- No explanations.
- No markdown.
- No extra text.

JSON FORMAT:

{
  "top_opportunities": [
    {
      "rank": 1,
      "business": "tutoring | cologne | cello",
      "opportunity": "",
      "why_it_matters": "",
      "expected_income": "",
      "difficulty": 1-10
    }
  ],
  "today_plan": [
    {
      "time": "",
      "task": "",
      "business": ""
    }
  ],
  "leads": [
    {
      "type": "school | venue | buyer | platform",
      "name": "",
      "action": ""
    }
  ],
  "money_focus": ""
}

Be aggressive about prioritizing income.
Only include actionable items that can be executed in real life.
"""

    return {"result": ask_ai(prompt)}
