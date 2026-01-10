import os
import asyncio
from typing import AsyncGenerator

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Gemini
from google import genai
from google.genai import types

load_dotenv()
app = FastAPI(title="AI Companion API")

class ChatRequest(BaseModel):
    session_id: str
    message: str
    system_prompt: str | None = None
    model: str = "gemini-2.5-flash"

# Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def sse(data: str) -> str:
    return f"data: {data}\n\n"

# femini response
async def gemini_stream_text(
    model: str,
    contents: list[str],
    system_prompt: str | None = None, 
    ) -> AsyncGenerator[str, None]:
    """
    Streams partial text using google-genai SDK.
    Docs: client.models.generate_content_stream(...)
    """
    gen_cfg = None
    if system_prompt:
        gen_cfg = types.GenerateContentConfig(system_instruction=system_prompt)

    stream = client.models.generate_content_stream(
        model=model,
        contents=contents,
        generation_config=gen_cfg,
    )
    # Iterate SDK stream and yield text fragments
    for chunk in stream:
        if getattr(chunk, "text", None):
            yield chunk.text


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
def echo(data: dict):
    return {"received": data}

@app.get("/sse-test")
async def sse_test():
    async def events():
        for i in range(5):
            yield f"data: tick {i}\n\n"
            await asyncio.sleep(0.3)
        yield "data: [DONE]\n\n"
    return StreamingResponse(events(), media_type="text/event-stream")

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest, authorization: str | None = Header(default=None)):
    # TODO: replace with JWT verification
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    async def event_generator():
        contents = [req.message]   # add conversation history or RAG later
        async for frag in gemini_stream_text(req.model, contents, req.system_prompt):
            yield sse(frag)
            await asyncio.sleep(0)  # cooperative yield
        yield sse("[DONE]")
    return StreamingResponse(event_generator(), media_type="text/event-stream")
