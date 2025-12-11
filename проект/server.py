from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# для работы с браузером
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.post("http://127.0.0.1:8000/api/chat")
def chat(msg: Message):
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjY1MDk0YTRlLThiNjktNDgwZi1hZGFiLTU0M2VmNThlNDZjNiIsImV4cCI6NDkxODk3NTIwOH0.ZYQJqsjOIQ2aiesA9QDhBF7h7AZJhAuKOxZ_UtxoIt4SaQZjvNYdr67NViyVIpJjQNSlQSXnSZ7bEB54ojY-5g"
    }

    data = {
        "model": "deepseek-ai/DeepSeek-R1-0528",
        "messages": [
            {"role": "system",
             "content": "You are the SkillWeaver AI learning platform."},
            {"role": "user", "content": msg.message}
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    json = response.json()

    text = json["choices"][0]["message"]["content"]

    # убираем think-блок
    if "</think>" in text:
        text = text.split("</think>", 1)[1].strip()

    return {"reply": text}
