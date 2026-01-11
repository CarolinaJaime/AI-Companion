import asyncio
from typing import AsyncGenerator
from app.config import Settings
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.music import music, MUSIC_URLS

# Gemini
from google import genai
from google.genai import types

# Gemini client
client = genai.Client(api_key=Settings.GEMINI_API_KEY)
app = FastAPI(title="AI Companion API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# request models
class ChatRequest(BaseModel): # for /chat/stream
    session_id: str
    message: str
    system_prompt: str | None = None
    model: str = "gemini-2.5-flash"

class StudySessionStart(BaseModel):
    session_id: str
    music_preference: str = 'lofi'
    duration: int = 25
    volume: float = 0.5  # 0.0 to 1.0

class StudySessionEnd(BaseModel):
    session_id: str
    stop_music: bool = True

class MusicPlayRequest(BaseModel):
    preference: str = 'lofi'
    volume: float = 0.5

class VolumeRequest(BaseModel):
    volume: float  # 0.0 to 1.0

def sse(data: str) -> str:
    return f"data: {data}\n\n"

# gemini response
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
        gen_cfg = types.GenerateContentConfig(system_instruction=system_prompt) if system_prompt else None

    stream = client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=gen_cfg,
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

#client

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

# music endpoints

@app.get("/music/preferences")
async def get_music_preferences():
    """Get available music preferences"""
    preferences = [
        {
            "value": key,
            "label": info['title'],
            "url": info['url']
        }
        for key, info in MUSIC_URLS.items()
    ]
    return {"preferences": preferences}

@app.post("/music/play")
async def play_music(
    req: MusicPlayRequest,
    authorization: str | None = Header(default=None)
):
    """Play music on laptop speakers"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = music.play_music(req.preference, req.volume)
    return result

@app.post("/music/stop")
async def stop_music(authorization: str | None = Header(default=None)):
    """Stop music playback"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = music.stop()
    return result

@app.post("/music/pause")
async def pause_music(authorization: str | None = Header(default=None)):
    """Pause music playback"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = music.pause()
    return result

@app.post("/music/resume")
async def resume_music(authorization: str | None = Header(default=None)):
    """Resume music playback"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = music.resume()
    return result

@app.post("/music/volume")
async def set_volume(
    req: VolumeRequest,
    authorization: str | None = Header(default=None)
):
    """Set volume (0.0 to 1.0)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not 0.0 <= req.volume <= 1.0:
        raise HTTPException(status_code=400, detail="Volume must be between 0.0 and 1.0")
    
    result = music.set_volume(req.volume)
    return result

@app.get("/music/status")
async def get_music_status(authorization: str | None = Header(default=None)):
    """Get current music playback status"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    status = music.get_status()
    return status

@app.post("/study/start")
async def start_study_session(
    req: StudySessionStart,
    authorization: str | None = Header(default=None)
):
    """Start a study session with music on laptop speakers"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Start music
    music_result = music.play_music(req.music_preference, req.volume)
    
    # Store session
    study_sessions[req.session_id] = {
        'session_id': req.session_id,
        'music_preference': req.music_preference,
        'duration': req.duration,
        'volume': req.volume,
        'start_time': asyncio.get_event_loop().time(),
        'music_started': music_result.get('success', False)
    }
    
    return {
        'success': True,
        'session': study_sessions[req.session_id],
        'music_result': music_result
    }

@app.post("/study/end")
async def end_study_session(
    req: StudySessionEnd,
    authorization: str | None = Header(default=None)
):
    """End a study session and optionally stop music"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    music_result = None
    if req.stop_music:
        music_result = music.stop()
    
    # Update session
    if req.session_id in study_sessions:
        study_sessions[req.session_id]['end_time'] = asyncio.get_event_loop().time()
        study_sessions[req.session_id]['music_stopped'] = music_result.get('success', False) if music_result else False
    
    return {
        'success': True,
        'session_id': req.session_id,
        'music_result': music_result
    }