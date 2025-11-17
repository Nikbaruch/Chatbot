from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# Permet au front-end de communiquer avec le back-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu peux mettre ton domaine Vercel plus tard
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚡ Instancie OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {
        "role": "system",
        "content": """You are an immersive storyteller specialized in writing long, mature-themed narratives. 
You can write about tension, power dynamics, emotions, and relationships between characters, but avoid 
graphic sexual descriptions or extreme explicitness.

Guidelines:
- Write in a detailed, dramatic, and engaging style.
- Use vivid imagery and sensory descriptions (sound, smell, atmosphere).
- Focus on characters’ emotions, tension, and internal conflict.
- Make the story long, with multiple paragraphs, and keep continuity.
- When the user gives input, integrate it naturally into the story's next scene.
"""
    }
]

MAX_TOKENS = 32768

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    if not user_input:
        return {"error": "No message provided"}

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        max_completion_tokens=MAX_TOKENS,
        temperature=0.9
    )

    bot_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_reply})
    return {"reply": bot_reply}

