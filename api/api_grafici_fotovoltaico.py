from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os
import asyncio
import redis.asyncio as redis
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


REDIS_URL = os.environ.get("REDIS_URL")


class ConnectionManager:
    def __init__(self):
        self.connection: WebSocket | None = None

    async def connect(self, websocket: WebSocket):
        logger.info("connect........................")
        await websocket.accept()
        self.connection = websocket


    def disconnect(self):
        self.connection = None

    async def send_message(self, message: str):
        logger.info("sending_triggered........................")
        if self.connection:
            logger.info("message........................")
            await self.connection.send_text(message)

manager = ConnectionManager()


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.redis_listener_task = asyncio.create_task(redis_listener())

async def redis_listener():
    redis_client = redis.from_url(REDIS_URL)
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('weather')

    async for message in pubsub.listen():
        if message['type'] == 'message':
            await manager.send_message(message['data'].decode('utf-8'))



@app.middleware('http')
async def dataToDB_handler(request: Request, call_next):
    if request.url.path == "/":
        app.mount("/static", StaticFiles(directory="static"), name="static")
        request.scope["templates"] = Jinja2Templates(directory="templates")

    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
async def get_layout(request: Request):
    templates = request.scope.get("templates")
    return templates.TemplateResponse(request=request, name="layout.html")


@app.get("/update")
async def update():
    pass

@app.post("/graph")
def graph_data(request: Request):
    pass

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep the connection open
    except WebSocketDisconnect:
        manager.disconnect()
