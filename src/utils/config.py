import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BINANCE_API_KEY     = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET  = os.getenv("BINANCE_API_SECRET", "")
    USE_BINANCE         = os.getenv("USE_BINANCE", "false").lower() == "true"
    BINANCE_SYMBOL      = os.getenv("BINANCE_SYMBOL", "BTCUSDT")
    BINANCE_INTERVAL    = os.getenv("BINANCE_INTERVAL", "1h")
    BINANCE_API_BASE    = os.getenv("BINANCE_API_BASE", "https://api.binance.com")
    NUM_AGENTS          = int(os.getenv("NUM_AGENTS", 5))
    NUM_TRADES          = int(os.getenv("NUM_TRADES", 100))
    INITIAL_BALANCE     = float(os.getenv("INITIAL_BALANCE", 1000))
    ENABLE_SUPER_AGENT  = os.getenv("ENABLE_SUPER_AGENT", "true").lower() == "true"
    MIN_WIN_RATE        = float(os.getenv("MIN_WIN_RATE_TO_LEARN", 0.55))
    LOG_FILE            = os.getenv("LOG_FILE", "verdent_logs.txt")

    @classmethod
    def validate(cls):
        if cls.USE_BINANCE:
            if not cls.BINANCE_API_KEY or not cls.BINANCE_API_SECRET:
                raise ValueError("USE_BINANCE=true mas API Key/Secret não configurados no .env")
        return True