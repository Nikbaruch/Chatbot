from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from openai import OpenAI
import os

app = FastAPI()

# CORS pour permettre au front de communiquer
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Servir index.html à la racine
@app.get("/")
def serve_front():
    return FileResponse("index.html")


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message", "")

    if not user_message:
        return JSONResponse({"error": "No message provided"}, status_code=400)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": user_message}],
            max_completion_tokens=4096,
            temperature=0.9,
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
