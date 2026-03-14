from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.engine import TradingEngine

router = APIRouter()
engine = TradingEngine()

class StrategyRequest(BaseModel):
    symbol: str

@router.post("/start")
async def start_strategy(request: StrategyRequest):
    return await engine.start_strategy(request.symbol)

@router.post("/stop")
async def stop_strategy(request: StrategyRequest):
    result = await engine.stop_strategy(request.symbol)
    if result["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Strategy not found")
    return result

@router.get("/status")
async def get_status():
    return {"active_strategies": [s for s, active in engine.strategies.items() if active]}
