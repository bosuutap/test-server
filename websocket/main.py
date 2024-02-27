from fastapi import FastAPI, Request, WebSocket
from lite_test import lite

app = FastAPI()

@app.get("/")
async def home():
    return "Lite Test Server"
    
@app.websocket("/lite")
async def connection(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        result = lite(data)
        await ws.send_text(result)