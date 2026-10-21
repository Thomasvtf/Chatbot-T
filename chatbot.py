"""Chatbot básico con API HTTP y una interfaz web mínima."""

import unicodedata
from typing import Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from iaGenerativa import generar_respuestas

app = FastAPI(title="Chatbot básico", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


def normalizar(texto: str) -> str:
    """Elimina tildes, convierte a minúsculas y quita espacios extra."""
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        caracter for caracter in texto if unicodedata.category(caracter) != "Mn"
    )

@app.get("/", response_class=HTMLResponse)
async def pagina(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    respuesta = await generar_respuestas(request.message)

    return ChatResponse(reply=respuesta)


