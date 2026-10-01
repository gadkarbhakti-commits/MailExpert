import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from fastapi.templating import Jinja2Templates

# Load environment variables
load_dotenv()
templates = Jinja2Templates(directory="templates")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not found")

# Configure Groq
client = Groq(api_key=api_key)

# FastAPI app
app = FastAPI(title="ReplyAI")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class EmailRequest(BaseModel):
    email: str
    tone: str
    length: str


# Frontend route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

async def stream_reply(prompt):
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


@app.post("/generate")
def generate_reply(request: EmailRequest):

    prompt = f"""
You are an expert professional email assistant.

Generate a high-quality email reply.

Original Email:
{request.email}

Tone:
{request.tone}

Length:
{request.length}

Instructions:
- Understand the context of the original email.
- Write a natural, human-like reply.
- Keep the requested tone.
- Keep the requested length.
- Include a greeting.
- Include a professional closing.
- Do not repeat the original email.
- Do not invent facts.
- Respond directly to the sender's request.
- Return only the email reply without explanations.
"""

    try:
        return StreamingResponse(
            stream_reply(prompt),
            media_type="text/plain"
        )

    except Exception as e:
        print("Groq Error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )