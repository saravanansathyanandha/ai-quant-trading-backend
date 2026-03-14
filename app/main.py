import asyncio
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.api.routes import router as api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Quant Trading Backend")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI Quant Trading Backend is running"}

@app.websocket("/ws/prices/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()
    logger.info(f"WebSocket connection established for {symbol}")
    try:
        price = 100.0
        while True:
            # Simulate live price updates
            price *= (1 + 0.0005)
            await websocket.send_text(json.dumps({
                "symbol": symbol,
                "price": round(price, 2),
                "timestamp": asyncio.get_event_loop().time()
            }))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for {symbol}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
