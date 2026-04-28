import requests
import hmac
import hashlib
import time
from src.utils.config import Config

class BinanceClient:
    def __init__(self):
        self.base = Config.BINANCE_API_BASE
        self.key = Config.BINANCE_API_KEY
        self.secret = Config.BINANCE_API_SECRET

    def _sign(self, params: dict) -> dict:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        signature = hmac.new(
            self.secret.encode(), query.encode(), hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def _headers(self):
        return {"X-MBX-APIKEY": self.key}

    def get_klines(self, symbol: str, interval: str, limit: int = 500):
        """Busca candles históricos (não requer autenticação)"""
        url = f"{self.base}/api/v3/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def get_balance(self):
        """Retorna saldos da conta (requer autenticação)"""
        url = f"{self.base}/api/v3/account"
        params = {"timestamp": int(time.time() * 1000), "recvWindow": 5000}
        params = self._sign(params)
        r = requests.get(url, params=params, headers=self._headers(), timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            b["asset"]: float(b["free"])
            for b in data["balances"]
            if float(b["free"]) > 0
        }

    def test_connection(self):
        """Valida a conexão e retorna True/False + mensagem"""
        try:
            balance = self.get_balance()
            usdt = balance.get("USDT", 0)
            return True, f"Conectado. Saldo USDT: {usdt:.2f}"
        except Exception as e:
            return False, str(e)