import csv, os
from src.agents.trading_agent import TradingAgent
from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger("SuperAgent")
TRADES_FILE = "src/data/success_trades.csv"

class SuperAgent(TradingAgent):
    def __init__(self, balance: float):
        super().__init__(agent_id=999, balance=balance)
        self._load_winning_params()

    def _load_winning_params(self):
        """Lê success_trades.csv e ajusta params pela média dos vencedores"""
        if not os.path.exists(TRADES_FILE):
            logger.warning("Nenhum histórico de trades vencedores encontrado.")
            return

        rsi_buys, rsi_sells, risks = [], [], []
        with open(TRADES_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if float(row.get("profit", 0)) > 0:
                        rsi_buys.append(float(row["rsi_buy"]))
                        rsi_sells.append(float(row["rsi_sell"]))
                        risks.append(float(row["risk_per_trade"]))
                except (KeyError, ValueError):
                    continue

        if rsi_buys:
            self.params["rsi_buy"]        = round(sum(rsi_buys) / len(rsi_buys))
            self.params["rsi_sell"]       = round(sum(rsi_sells) / len(rsi_sells))
            self.params["risk_per_trade"] = round(sum(risks) / len(risks), 3)
            logger.info(f"SuperAgent calibrado: {self.params}")

    def save_winning_trade(self, trade: dict):
        """Salva trade vencedor para aprendizado futuro"""
        if trade["profit"] <= 0:
            return
        row = {**trade, **self.params}
        file_exists = os.path.exists(TRADES_FILE)
        with open(TRADES_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)