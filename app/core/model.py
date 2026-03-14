import random
import asyncio

class PricePredictor:
    """
    Mock AI model for price prediction.
    In a real-world scenario, this would load a pre-trained model (e.g., LSTM, XGBoost).
    """
    def __init__(self, symbol: str):
        self.symbol = symbol

    async def predict(self, historical_data):
        # Simulate model inference delay
        await asyncio.sleep(0.1)
        # Mock prediction: current price + small random noise
        last_price = historical_data[-1] if historical_data else 100.0
        prediction = last_price * (1 + random.uniform(-0.02, 0.02))
        return prediction
