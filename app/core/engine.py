import asyncio
import logging
from typing import Dict, List
from app.core.model import PricePredictor

logger = logging.getLogger(__name__)

class TradingEngine:
    def __init__(self):
        self.strategies: Dict[str, bool] = {}
        self.price_history: Dict[str, List[float]] = {}
        self.predictors: Dict[str, PricePredictor] = {}

    async def start_strategy(self, symbol: str):
        if symbol in self.strategies and self.strategies[symbol]:
            return {"status": "already_running", "symbol": symbol}
        
        self.strategies[symbol] = True
        self.price_history[symbol] = [100.0]  # Starting price
        self.predictors[symbol] = PricePredictor(symbol)
        
        asyncio.create_task(self._run_loop(symbol))
        return {"status": "started", "symbol": symbol}

    async def stop_strategy(self, symbol: str):
        if symbol in self.strategies:
            self.strategies[symbol] = False
            return {"status": "stopped", "symbol": symbol}
        return {"status": "not_found", "symbol": symbol}

    async def _run_loop(self, symbol: str):
        logger.info(f"Starting execution loop for {symbol}")
        while self.strategies.get(symbol):
            try:
                # Simulate getting live price
                current_price = self.price_history[symbol][-1] * (1 + 0.001)
                self.price_history[symbol].append(current_price)
                
                # Get AI prediction
                prediction = await self.predictors[symbol].predict(self.price_history[symbol][-20:])
                
                logger.info(f"[{symbol}] Price: {current_price:.2f}, AI Prediction: {prediction:.2f}")
                
                # Mock trade logic
                if prediction > current_price * 1.005:
                    logger.info(f"[{symbol}] SIGNAL: BUY")
                elif prediction < current_price * 0.995:
                    logger.info(f"[{symbol}] SIGNAL: SELL")
                
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Error in engine loop for {symbol}: {e}")
                await asyncio.sleep(10)
