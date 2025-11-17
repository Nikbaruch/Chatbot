from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from openai import OpenAI
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SITE_PASSWORD = os.getenv("SITE_PASSWORD")  # récupéré depuis Vercel


# 🔐 Route de vérification du mot de passe
@app.post("/auth")
async def auth(request: Request):
    data = await request.json()
    if data.get("password") == SITE_PASSWORD:
        return {"success": True}
    return {"success": False}


# 🔐 Le frontend est servi SEULEMENT si autorisé
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
