from fastapi import FastAPI
import os
import requests

app = FastAPI()

API_KEY = os.getenv("GEMINI_API_KEY")


def ask_ai(prompt):

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    r = requests.post(url, json=payload)

    return r.json()["candidates"][0]["content"]["parts"][0]["text"]


@app.get("/")
def home():
    return {"status": "AI agent running"}


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
