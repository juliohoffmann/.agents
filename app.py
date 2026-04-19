import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from binance_common.configuration import ConfigurationRestAPI
from binance_common.constants import SPOT_REST_API_PROD_URL
from binance_common.errors import Error
from binance_sdk_spot.spot import Spot
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from verdent import VerdentSimulator, LOG_FILE

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

load_dotenv()

CONFIG_FILE = Path("app_config.json")
SUCCESS_FILE = Path("success_trades.csv")
DEFAULT_SYMBOL = "EURUSDT"
DEFAULT_INTERVAL = "1d"
DEFAULT_BINANCE_API_BASE = "https://api.binance.com"

BINANCE_API_BASE = os.getenv("BINANCE_API_BASE", DEFAULT_BINANCE_API_BASE)

app = FastAPI(title="Verdent Trading Simulator")
app.mount("/static", StaticFiles(directory="frontend"), name="static")

LAST_SIMULATION: Dict[str, List[Dict[str, object]]] = {"agents": []}


class SimulatorConfig(BaseModel):
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    binance_api_base: Optional[str] = None
    symbol: str = DEFAULT_SYMBOL
    interval: str = DEFAULT_INTERVAL
    use_binance: bool = False
    live_trading_enabled: bool = False
    include_super_agent: bool = True
    num_agents: int = 5
    num_trades: int = 100


def env_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_config() -> SimulatorConfig:
    config = SimulatorConfig()
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            config = SimulatorConfig(**data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Arquivo de configuração inválido.")

    config.api_key = config.api_key or os.getenv("BINANCE_API_KEY")
    config.api_secret = config.api_secret or os.getenv("BINANCE_API_SECRET")
    config.binance_api_base = config.binance_api_base or os.getenv("BINANCE_API_BASE", BINANCE_API_BASE)
    config.symbol = config.symbol or os.getenv("BINANCE_SYMBOL", DEFAULT_SYMBOL)
    config.interval = config.interval or os.getenv("BINANCE_INTERVAL", DEFAULT_INTERVAL)
    config.use_binance = config.use_binance or env_bool(os.getenv("USE_BINANCE"), False)
    config.live_trading_enabled = config.live_trading_enabled or env_bool(os.getenv("LIVE_TRADING_ENABLED"), False)
    config.include_super_agent = config.include_super_agent or env_bool(os.getenv("INCLUDE_SUPER_AGENT"), True)

    try:
        config.num_agents = int(os.getenv("NUM_AGENTS", str(config.num_agents)))
    except ValueError:
        config.num_agents = 5
    try:
        config.num_trades = int(os.getenv("NUM_TRADES", str(config.num_trades)))
    except ValueError:
        config.num_trades = 100

    return config


def save_config(config: SimulatorConfig) -> SimulatorConfig:
    CONFIG_FILE.write_text(json.dumps(config.model_dump(), indent=2), encoding="utf-8")
    return config


def create_binance_client(config: SimulatorConfig) -> Spot:
    base_path = config.binance_api_base or os.getenv("BINANCE_API_BASE", SPOT_REST_API_PROD_URL)
    configuration = ConfigurationRestAPI(
        api_key=config.api_key,
        api_secret=config.api_secret,
        base_path=base_path,
    )
    return Spot(config_rest_api=configuration)


def fetch_binance_data(config: SimulatorConfig) -> pd.DataFrame:
    if not config.api_key or not config.api_secret:
        raise HTTPException(status_code=400, detail="API Key e Secret são necessários para usar dados da Binance.")

    client = create_binance_client(config)
    try:
        response = client.rest_api.klines(
            symbol=config.symbol,
            interval=config.interval,
            limit=max(config.num_trades + 50, 200),
        )
        raw_klines = response.data()
        if not raw_klines:
            raise ValueError("Nenhum dado retornado pela Binance.")

        close_prices = [float(item[4]) for item in raw_klines]
        timestamps = [pd.to_datetime(item[0], unit="ms") for item in raw_klines]
        return pd.DataFrame({"close": close_prices}, index=timestamps)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados Binance: {exc}")


def get_market_data(config: SimulatorConfig) -> pd.DataFrame:
    if config.use_binance:
        return fetch_binance_data(config)
    return VerdentSimulator.load_historical_data()


def load_success_trades(limit: int = 50) -> List[Dict[str, Any]]:
    if not SUCCESS_FILE.exists():
        return []
    df = pd.read_csv(SUCCESS_FILE)
    if df.empty:
        return []
    df = df.sort_values("timestamp", ascending=False)
    return df.head(limit).to_dict("records")


def get_success_strategy_summary() -> Dict[str, Any]:
    if not SUCCESS_FILE.exists():
        return {
            "total_successes": 0,
            "average_profit": 0.0,
            "top_strategy": None,
            "unique_strategies": 0,
        }
    df = pd.read_csv(SUCCESS_FILE)
    if df.empty:
        return {
            "total_successes": 0,
            "average_profit": 0.0,
            "top_strategy": None,
            "unique_strategies": 0,
        }
    most_common_strategy = df["strategy"].mode().iloc[0] if "strategy" in df.columns else None
    return {
        "total_successes": int(len(df)),
        "average_profit": round(float(df["profit"].mean()), 4),
        "top_strategy": most_common_strategy,
        "unique_strategies": int(df["strategy"].nunique()) if "strategy" in df.columns else 0,
    }


def get_binance_account_info(config: SimulatorConfig) -> Dict[str, object]:
    if not config.api_key or not config.api_secret:
        raise HTTPException(status_code=400, detail="API Key e Secret são necessários para acessar a Binance.")

    client = create_binance_client(config)
    try:
        response = client.rest_api.get_account(
            omit_zero_balances=False,
            recv_window=5000,
        )
        account = response.data()
    except Error as exc:
        raise HTTPException(status_code=400, detail=f"Erro Binance: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro Binance inesperado: {exc}")

    balances = []
    total_usdt = 0.0

    for item in account.get("balances", []):
        free = float(item.get("free", 0))
        locked = float(item.get("locked", 0))
        amount = free + locked
        if amount <= 0:
            continue

        asset = item.get("asset")
        asset_value_usdt = None
        if asset == "USDT":
            asset_value_usdt = amount
        else:
            for quote_symbol in ["USDT", "BUSD", "BTC", "ETH"]:
                symbol = f"{asset}{quote_symbol}"
                try:
                    ticker = client.rest_api.ticker_price(symbol=symbol).data()
                    price = float(ticker.get("price", 0))
                    if quote_symbol in {"USDT", "BUSD"}:
                        asset_value_usdt = amount * price
                    elif quote_symbol == "BTC":
                        btc_price = float(client.rest_api.ticker_price(symbol="BTCUSDT").data().get("price", 0))
                        asset_value_usdt = amount * price * btc_price
                    elif quote_symbol == "ETH":
                        eth_price = float(client.rest_api.ticker_price(symbol="ETHUSDT").data().get("price", 0))
                        asset_value_usdt = amount * price * eth_price
                    break
                except HTTPException:
                    continue

        balances.append(
            {
                "asset": asset,
                "free": free,
                "locked": locked,
                "amount": amount,
                "value_usdt": round(asset_value_usdt, 4) if asset_value_usdt is not None else None,
            }
        )
        if asset_value_usdt is not None:
            total_usdt += asset_value_usdt

    return {
        "account_type": account.get("accountType", "UNKNOWN"),
        "makerCommission": account.get("makerCommission"),
        "takerCommission": account.get("takerCommission"),
        "canTrade": account.get("canTrade"),
        "balances": balances,
        "total_usdt": round(total_usdt, 4),
    }


@app.get("/")
def root() -> FileResponse:
    return FileResponse(Path("frontend") / "index.html")


@app.get("/api/config")
def get_config() -> Dict[str, object]:
    config = load_config()
    return config.dict()


@app.post("/api/config")
def post_config(config: SimulatorConfig) -> Dict[str, object]:
    saved = save_config(config)
    return {"success": True, "config": saved.dict()}


@app.get("/api/binance/test")
def test_binance() -> Dict[str, object]:
    config = load_config()
    if not config.use_binance:
        return {"success": False, "detail": "Ative a opção 'Usar dados da Binance' para testar a conexão."}
    if not config.api_key or not config.api_secret:
        return {"success": False, "detail": "API Key e Secret são necessários para conectar à Binance."}

    logging.info("Binance test: use_binance=%s, api_key_set=%s, api_secret_set=%s",
                 config.use_binance,
                 bool(config.api_key),
                 bool(config.api_secret))

    try:
        account_info = get_binance_account_info(config)
        return {"success": True, "data": account_info}
    except HTTPException as exc:
        logging.error("Binance test failed: %s", exc.detail)
        raise
    except Error as exc:
        logging.error("Binance test failed: %s", exc)
        return {
            "success": False,
            "detail": f"Erro Binance: {exc}",
            "error_type": type(exc).__name__,
            "error_raw": str(exc),
        }
    except Exception as exc:
        logging.error("Binance test unexpected error: %s", exc)
        return {"success": False, "detail": f"Erro ao validar a conta Binance: {exc}"}


@app.get("/api/binance/test/")
def test_binance_slash() -> Dict[str, object]:
    return test_binance()


@app.get("/api/debug-config")
def debug_config() -> Dict[str, object]:
    config = load_config()
    return {
        "use_binance": config.use_binance,
        "api_key_set": bool(config.api_key),
        "api_secret_set": bool(config.api_secret),
        "binance_api_base": config.binance_api_base,
        "symbol": config.symbol,
        "interval": config.interval,
        "live_trading_enabled": config.live_trading_enabled,
        "include_super_agent": config.include_super_agent,
        "num_agents": config.num_agents,
        "num_trades": config.num_trades,
    }


@app.post("/api/simulate")
def simulate() -> Dict[str, object]:
    config = load_config()
    market_data = get_market_data(config)
    simulator = VerdentSimulator(
        num_agents=config.num_agents,
        market_data=market_data,
        include_super_agent=config.include_super_agent,
    )
    agents = simulator.run_simulation(num_trades=config.num_trades)
    LAST_SIMULATION["agents"] = agents
    return {
        "success": True,
        "agents": agents,
        "log_file": str(LOG_FILE),
        "market_source": "Binance" if config.use_binance else "Simulada",
        "symbol": config.symbol,
        "interval": config.interval,
        "live_trading_enabled": config.live_trading_enabled,
        "include_super_agent": config.include_super_agent,
        "note": "O modo real está disponível como opção futura. Atualmente, os agentes apenas simulam com dados históricos reais ou simulados.",
    }


@app.get("/api/agents")
def get_agents() -> Dict[str, object]:
    return {"agents": LAST_SIMULATION.get("agents", [])}


@app.get("/api/success-trades")
def success_trades(limit: int = 50) -> Dict[str, object]:
    trades = load_success_trades(limit)
    return {"success": True, "trades": trades}


@app.get("/api/success-strategy")
def success_strategy() -> Dict[str, object]:
    summary = get_success_strategy_summary()
    return {"success": True, "summary": summary}


@app.get("/api/logs")
def get_logs(lines: int = 80) -> Dict[str, object]:
    if not Path(LOG_FILE).exists():
        return {"lines": []}
    with open(LOG_FILE, "rb") as file:
        raw = file.read()
    text = raw.decode("utf-8", errors="replace")
    content = text.splitlines()
    return {"lines": [line.strip() for line in content[-lines:]]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000)
