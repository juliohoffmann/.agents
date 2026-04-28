import random
import pandas as pd
from src.core.indicators import add_indicators
from src.utils.logger import get_logger

logger = get_logger("TradingAgent")

class TradingAgent:
    def __init__(self, agent_id: int, balance: float, params: dict = None):
        self.agent_id    = agent_id
        self.balance     = balance
        self.initial_bal = balance
        self.position    = None   # {"price": float, "qty": float}
        self.trades      = []
        self.params = params or {
            "rsi_buy":        random.randint(25, 40),
            "rsi_sell":       random.randint(60, 75),
            "ema_fast":       random.choice([9, 12]),
            "ema_slow":       random.choice([21, 26]),
            "risk_per_trade": round(random.uniform(0.01, 0.05), 3),
        }

    @property
    def win_rate(self):
        wins = sum(1 for t in self.trades if t["profit"] > 0)
        return wins / len(self.trades) if self.trades else 0

    @property
    def total_profit(self):
        return self.balance - self.initial_bal

    def decide(self, row: pd.Series) -> str:
        """Retorna 'buy', 'sell' ou 'hold'"""
        rsi = row.get("rsi", 50)
        ema_f = row.get("ema_9", 0)
        ema_s = row.get("ema_21", 0)

        if self.position is None:
            if rsi < self.params["rsi_buy"] and ema_f > ema_s:
                return "buy"
        else:
            if rsi > self.params["rsi_sell"] or ema_f < ema_s:
                return "sell"
        return "hold"

    def execute(self, action: str, price: float):
        if action == "buy" and self.position is None:
            risk_amount = self.balance * self.params["risk_per_trade"]
            qty = risk_amount / price
            self.position = {"price": price, "qty": qty}
            self.balance -= risk_amount
            logger.info(f"[Agent {self.agent_id}] BUY @ {price:.2f} | qty={qty:.6f}")

        elif action == "sell" and self.position:
            entry  = self.position["price"]
            qty    = self.position["qty"]
            profit = (price - entry) * qty
            self.balance += (entry * qty) + profit
            self.trades.append({
                "entry": entry, "exit": price,
                "profit": profit, "qty": qty
            })
            logger.info(
                f"[Agent {self.agent_id}] SELL @ {price:.2f} | "
                f"profit={profit:.4f} USDT | win_rate={self.win_rate:.2%}"
            )
            self.position = None

    def summary(self) -> dict:
        return {
            "agent_id":     self.agent_id,
            "balance":      round(self.balance, 4),
            "total_profit": round(self.total_profit, 4),
            "win_rate":     round(self.win_rate, 4),
            "total_trades": len(self.trades),
            "params":       self.params,
        }