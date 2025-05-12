from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # for local dev
        "https://chatbot1-six-delta.vercel.app/",  # for production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": message}]}]}

    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code != 200:
            return {"reply": f"Failed to get response: {response.text}"}
        
        res = response.json()
        reply = res.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't parse the response.")
    except Exception as e:
        reply = f"Something went wrong: {e}"

    return {"reply": reply}
