"""Chatbot básico con API HTTP y una interfaz web mínima."""

from typing import Dict, List
import unicodedata

# pyrefly: ignore[missing-import]
from fastapi import FastAPI
# pyrefly: ignore[missing-import]
from fastapi.responses import HTMLResponse
# pyrefly: ignore[missing-import]
from pydantic import BaseModel, Field

app = FastAPI(title="Chatbot básico", version="1.0.0")


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


def responder(mensaje: str) -> str:
    """Genera una respuesta por reglas; reemplaza esta función para usar un LLM."""
    texto = normalizar(mensaje)

    if not texto:
        return "Por favor, escribe un mensaje antes de enviarlo."

    if any(saludo in texto for saludo in ("hola", "buenas", "hey", "que tal")):
        return "¡Hola! ¿En qué puedo ayudarte?"
        
    if "nombre" in texto:
        return "Soy un chatbot básico hecho con Python."
        
    if any(palabra in texto for palabra in ("adios", "chao", "hasta luego")):
        return "¡Hasta luego! Que tengas un buen día."
        
    if "ayuda" in texto:
        return "Puedo responder saludos y algunas preguntas sencillas. ¿Qué necesitas?"
        
    if any(programa in texto for programa in ("programas", "programa")):
        return (
            "Los programas disponibles son:\n"
            "1. Análisis y desarrollo de software.\n"
            "2. Animación 3D.\n"
            "3. Animación digital.\n"
            "4. Desarrollo de medios gráficos visuales.\n"
            "5. Desarrollo publicitario.\n"
            "6. Desarrollo de multimedia y web.\n"
            "7. Desarrollo de videojuegos.\n"
            "8. Coordinación de procesos logísticos."
        )
        
    if "codigo" in texto:
        return (
            "Aquí tienes el código de cada programa según el número que tiene en la lista:\n"
            "1. 228118.\n"
            "2. 924118.\n"
            "3. 233101.\n"
            "4. 524704.\n"
            "5. 124100.\n"
            "6. 217320.\n"
            "7. 228108.\n"
            "8. 121523."
        )
        
    if any(modalidad in texto for modalidad in ("modalidad", "modalidades")):
        return "Las modalidades disponibles son:\n-Presencial\n-Virtual"
        
    if "nivel" in texto:
        return "Los niveles de formación son:\n -Técnico\n -Tecnológico"
        
    if "conocer mas" in texto:
        return (
            "¡Claro! Aquí podrás conocer más información detallada en el blog del Centro "
            "para la Industria de la Comunicación Gráfica.\n"
            "https://comunicaciongraficasena.blogspot.com/"
        )
        
    if any(inscripcion in texto for inscripcion in ("inscripcion", "inscribir", "inscripciones", "inscribo")):
        return (
            "Para inscribirte a nuestros programas, debes realizar el proceso formal "
            "a través de la plataforma oficial del SENA.\n"
            "https://betowa.sena.edu.co/"
        )

    if any(palabra in texto for palabra in ("costo", "precio", "cuanto vale", "cuanto cuesta", "gratis", "pagar")):
        return "Toda la formación ofrecida por el SENA es totalmente gratuita."

    return f"Entiendo. Cuéntame un poco más sobre: «{mensaje.strip()}»"


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return HTML


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=responder(request.message))


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chatbot básico</title>
  <style>
    body { font: 16px system-ui, sans-serif; max-width: 680px; margin: 3rem auto; padding: 0 1rem; color: #202124; }
    #chat { min-height: 260px; border: 1px solid #ddd; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
    .message { margin: .6rem 0; white-space: pre-wrap; }
    form { display: flex; gap: .5rem; }
    input { flex: 1; padding: .8rem; border: 1px solid #aaa; border-radius: 8px; }
    button { padding: .8rem 1rem; border: 0; border-radius: 8px; background: #1459c7; color: white; cursor: pointer; }
  </style>
</head>
<body>
  <h1>Chatbot SENA CENIGRAF</h1>
  <div id="chat" aria-live="polite"><p class="message">Bot: Hola.😁 ¿Cómo te puedo ayudar?</p></div>
  <form id="form">
    <input id="message" autocomplete="off" placeholder="Escribe tu mensaje…" required maxlength="2000">
    <button type="submit">Enviar</button>
  </form>
  <script>
    const chat = document.querySelector('#chat');
    const form = document.querySelector('#form');
    const input = document.querySelector('#message');
    function addMessage(who, text) {
      const p = document.createElement('p');
      p.className = 'message';
      p.textContent = `${who}: ${text}`;
      chat.appendChild(p);
      chat.scrollTop = chat.scrollHeight;
    }
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const message = input.value.trim();
      if (!message) return;
      addMessage('Tú', message);
      input.value = '';
      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        if (!response.ok) throw new Error('No se pudo obtener una respuesta.');
        const data = await response.json();
        addMessage('Bot', data.reply);
      } catch (error) {
        addMessage('Bot', `Error: ${error.message}`);
      }
    });
  </script>
</body>
</html>"""