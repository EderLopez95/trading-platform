import asyncio
from app.infrastructure.data_provider.mt5_provider import MT5Provider
from fastapi import APIRouter, WebSocket
from app.worker.bot_controller import BotController
from app.infrastructure.config.config_loader import ConfigLoader
from app.infrastructure.ws.ws_manager import ws_manager
from app.domain.models.config_model import AppConfigModel

router = APIRouter(prefix="/api")
bot_controller = BotController()
config_loader = ConfigLoader()

@router.get("/")
def root():
    return {
        "service": "Trading Bot API",
        "status": bot_controller.status(),
        "docs": "/docs"
    }

@router.post("/start")
def start_bot():
    return {"status": bot_controller.start()}

@router.post("/stop")
def stop_bot():
    return {"status": bot_controller.stop()}

@router.get("/status")
def bot_status():
    return {"status": bot_controller.status()}

@router.get("/config")
def get_config():
    return config_loader.load()

@router.post("/config")
def update_config(config: AppConfigModel):
    config_loader.save(config)
    return {
        "success": True,
        "message": "Config updated"
    }

@router.get("/symbols/search")
def search_symbols(query: str = ""):
    provider = MT5Provider()
    return provider.search_symbols(query)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    ws_manager.set_loop(asyncio.get_running_loop())
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        ws_manager.disconnect(websocket)
