# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from .simplify import run_instruction
from .diagram import extract_steps, create_diagram_svg
from .texttspeech import text_to_audio_base64

app = FastAPI()


class TransformRequest(BaseModel):
    text: str
    mode: str = "simplify"    # "simplify", "summarize", "explain10", "example", "steps"
    level: str = "6th grade"  


class TTSRequest(BaseModel):
    text: str
    lang: str = "en"


class DiagramRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "LearnEasy backend is running"}


# TEXT TRANSFORMATION (simplification, summarization, etc.)
@app.post("/transform")
def transform(request: TransformRequest):
    output = run_instruction(
        text=request.text,
        mode=request.mode,
        level=request.level,
    )
    return {"result": output}


# DIAGRAM GENERATION (flowchart SVG)
@app.post("/diagram")
def diagram(request: DiagramRequest):
    steps = extract_steps(request.text)
    if not steps:
        return {"svg": "", "steps": []}
    svg = create_diagram_svg(steps)
    return {"svg": svg, "steps": steps}


# TEXT-TO-SPEECH
@app.post("/tts")
def tts(request: TTSRequest):
    audio_b64 = text_to_audio_base64(request.text, lang=request.lang)
    return {"audio_base64": audio_b64}
