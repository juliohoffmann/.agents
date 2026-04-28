import pandas as pd
import numpy as np
from src.core.binance_client import BinanceClient
from src.utils.config import Config

class DataFetcher:
    def __init__(self):
        self.client = BinanceClient()

    def fetch(self, symbol=None, interval=None, limit=500) -> pd.DataFrame:
        symbol   = symbol   or Config.BINANCE_SYMBOL
        interval = interval or Config.BINANCE_INTERVAL

        if Config.USE_BINANCE:
            return self._from_binance(symbol, interval, limit)
        return self._simulated(limit)

    def _from_binance(self, symbol, interval, limit) -> pd.DataFrame:
        raw = self.client.get_klines(symbol, interval, limit)
        df = pd.DataFrame(raw, columns=[
            "open_time","open","high","low","close","volume",
            "close_time","quote_volume","trades",
            "taker_buy_base","taker_buy_quote","ignore"
        ])
        for col in ["open","high","low","close","volume"]:
            df[col] = df[col].astype(float)
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        return df[["open_time","open","high","low","close","volume"]]

    def _simulated(self, limit) -> pd.DataFrame:
        """Gera candles sintéticos para testes sem API"""
        np.random.seed(42)
        close = np.cumsum(np.random.randn(limit) * 10) + 30000
        df = pd.DataFrame({
            "open_time": pd.date_range("2024-01-01", periods=limit, freq="1h"),
            "open":   close - np.random.rand(limit) * 5,
            "high":   close + np.random.rand(limit) * 10,
            "low":    close - np.random.rand(limit) * 10,
            "close":  close,
            "volume": np.random.rand(limit) * 100 + 10,
        })
        return df