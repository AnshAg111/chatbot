from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import openai
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            response = get_chatbot_response(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        pass
    

@app.get("/index", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def get_chatbot_response(message: str):
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
