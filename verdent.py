import logging
import random
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import ta
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError

SUCCESS_FILE = Path("success_trades.csv")

LOG_FILE = "verdent_logs.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class TradingAgent:
    def __init__(self, agent_id: str, initial_balance: float = 100.0):
        self.id = agent_id
        self.balance = float(initial_balance)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.strategy_params = {
            "rsi_period": 14,
            "ma_period": 14,
            "confidence_threshold": 0.60,
        }
        self.success_history: List[Dict[str, np.ndarray]] = self.load_global_success_history()
        self.failure_history: List[Dict[str, np.ndarray]] = []
        self.trades_executed = 0
        self.last_trade_amount = 0.0
        self.last_profit = 0.0
        self.last_return_pct = 0.0
        self.last_entry_price = 0.0
        self.last_exit_price = 0.0
        self.cumulative_profit = 0.0

    def compute_features(self, close_prices: pd.Series) -> np.ndarray:
        rsi_indicator = ta.momentum.RSIIndicator(close=close_prices, window=self.strategy_params["rsi_period"])
        sma_indicator = ta.trend.SMAIndicator(close=close_prices, window=self.strategy_params["ma_period"])

        rsi = float(rsi_indicator.rsi().iloc[-1])
        sma = float(sma_indicator.sma_indicator().iloc[-1])
        close = float(close_prices.iloc[-1])
        momentum = float(close - close_prices.iloc[-self.strategy_params["ma_period"]]) if len(close_prices) >= self.strategy_params["ma_period"] else 0.0

        features = np.array([rsi, sma, close, momentum], dtype=float)
        return features

    def load_global_success_history(self) -> List[Dict[str, np.ndarray]]:
        if not SUCCESS_FILE.exists():
            return []
        try:
            df = pd.read_csv(SUCCESS_FILE)
            if df.empty:
                return []
            return [
                {
                    "features": np.array([row["rsi"], row["sma"], row["close"], row["momentum"]], dtype=float),
                    "profit": float(row["profit"]),
                }
                for _, row in df.iterrows()
                if not pd.isna(row.get("rsi"))
            ]
        except Exception:
            return []

    def _build_training_data(self) -> Optional[Dict[str, np.ndarray]]:
        if not self.success_history:
            return None

        X = [entry["features"] for entry in self.success_history]
        y = [1] * len(X)

        if self.failure_history:
            X += [entry["features"] for entry in self.failure_history]
            y += [0] * len(self.failure_history)
        else:
            synthetic_negatives = [self._make_negative_sample(entry["features"]) for entry in self.success_history]
            X += synthetic_negatives
            y += [0] * len(synthetic_negatives)

        return {"X": np.vstack(X), "y": np.array(y, dtype=int)}

    def _describe_strategy(self, features: np.ndarray) -> str:
        rsi, sma, close, momentum = features
        if rsi < 30 and close > sma:
            return "Compra em suporte com RSI baixo e preço acima da média móvel"
        if rsi < 40 and close > sma:
            return "Compra agressiva com RSI moderado e preço acima da média móvel"
        if rsi > 70 and close < sma:
            return "Venda em sobrecompra com preço abaixo da média móvel"
        return "Estratégia de momentum baseada em RSI e SMA"

    def _make_negative_sample(self, features: np.ndarray) -> np.ndarray:
        rsi, sma, close, momentum = features
        negative_rsi = min(100.0, rsi + random.uniform(15, 30))
        negative_momentum = momentum - random.uniform(0.2, 0.8) * abs(momentum)
        return np.array([negative_rsi, sma, close, negative_momentum], dtype=float)

    def train_on_successes(self) -> None:
        data = self._build_training_data()
        if not data:
            return

        try:
            self.model.fit(data["X"], data["y"])
            logging.info(
                "Agente %s treinou com %d sucessos e %d falhas simuladas.",
                self.id,
                len(self.success_history),
                len(self.failure_history) if self.failure_history else len(self.success_history),
            )
        except ValueError as error:
            logging.warning("Agente %s não pôde treinar: %s", self.id, error)

    def should_trade(self, features: np.ndarray) -> bool:
        try:
            proba = self.model.predict_proba([features])[0]
            win_probability = proba[1]
            logging.debug("Agente %s probabilidade de vitória: %.2f", self.id, win_probability)
            return win_probability >= self.strategy_params["confidence_threshold"]
        except (NotFittedError, AttributeError, IndexError):
            rsi, sma, close, momentum = features
            return rsi < 40 and close > sma

    def make_trade(self, market_data: pd.DataFrame, index: int) -> float:
        if index < self.strategy_params["ma_period"] or index >= len(market_data) - 1:
            return 0.0

        window = market_data.iloc[index - self.strategy_params["ma_period"] + 1 : index + 1]
        features = self.compute_features(window["close"])
        self.trades_executed += 1

        if not self.should_trade(features):
            logging.info("Agente %s ignorou trade no índice %d.", self.id, index)
            return 0.0

        trade_amount = max(1.0, self.balance * 0.10)
        entry_price = float(market_data.iloc[index]["close"])
        exit_price = float(market_data.iloc[index + 1]["close"])
        return_pct = (exit_price - entry_price) / entry_price
        profit = trade_amount * return_pct
        self.last_trade_amount = trade_amount
        self.last_entry_price = entry_price
        self.last_exit_price = exit_price
        self.last_return_pct = return_pct
        self.last_profit = profit
        self.cumulative_profit += profit
        self.balance += profit

        if profit > 0:
            self.success_history.append({"features": features, "profit": profit})
            self.save_success_trade(market_data, index, features, trade_amount, profit, return_pct)
            self.train_on_successes()
            logging.info(
                "Agente %s trade vencedor: lucro=%.2f, saldo=%.2f, índice=%d, retorno=%.2f%%",
                self.id,
                profit,
                self.balance,
                index,
                return_pct * 100,
            )
        else:
            self.failure_history.append({"features": features, "profit": profit})
            logging.info(
                "Agente %s trade perdedor: perda=%.2f, saldo=%.2f, índice=%d, retorno=%.2f%%",
                self.id,
                profit,
                self.balance,
                index,
                return_pct * 100,
            )

        return profit

    def save_success_trade(
        self,
        market_data: pd.DataFrame,
        index: int,
        features: np.ndarray,
        trade_amount: float,
        profit: float,
        return_pct: float,
    ) -> None:
        timestamp = market_data.index[index]
        record = {
            "agent_id": self.id,
            "timestamp": str(timestamp),
            "rsi": float(features[0]),
            "sma": float(features[1]),
            "close": float(features[2]),
            "momentum": float(features[3]),
            "trade_amount": round(trade_amount, 4),
            "profit": round(profit, 4),
            "return_pct": round(return_pct * 100, 4),
            "balance_after": round(self.balance, 4),
            "strategy": self._describe_strategy(features),
        }
        if SUCCESS_FILE.exists():
            existing = pd.read_csv(SUCCESS_FILE)
            existing = pd.concat([existing, pd.DataFrame([record])], ignore_index=True)
        else:
            existing = pd.DataFrame([record])
        existing.to_csv(SUCCESS_FILE, index=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "balance": round(self.balance, 4),
            "trades_executed": self.trades_executed,
            "wins": len(self.success_history),
            "losses": len(self.failure_history),
            "last_trade_amount": round(self.last_trade_amount, 4),
            "last_profit": round(self.last_profit, 4),
            "last_return_pct": round(self.last_return_pct * 100, 4),
            "last_entry_price": round(self.last_entry_price, 6),
            "last_exit_price": round(self.last_exit_price, 6),
            "cumulative_profit": round(self.cumulative_profit, 4),
        }

    def check_deletion(self) -> bool:
        if self.balance < 30.0:
            logging.warning("Agente %s deletado: saldo crítico %.2f", self.id, self.balance)
            return True
        return False


class SuperTradingAgent(TradingAgent):
    def __init__(self, agent_id: str, initial_balance: float = 100.0):
        super().__init__(agent_id, initial_balance)
        self.latest_strategy = "Inicial padrão"
        self.evolution_steps = 0

    def evolve_strategy(self) -> None:
        if not self.success_history:
            return

        features = np.vstack([entry["features"] for entry in self.success_history])
        avg_rsi, avg_sma, avg_close, avg_momentum = features.mean(axis=0)
        old_params = self.strategy_params.copy()

        if avg_rsi < 35:
            self.strategy_params["confidence_threshold"] = max(0.50, self.strategy_params["confidence_threshold"] - 0.05)
        elif avg_rsi > 55:
            self.strategy_params["confidence_threshold"] = min(0.80, self.strategy_params["confidence_threshold"] + 0.05)

        if avg_momentum > 0:
            self.strategy_params["rsi_period"] = max(10, self.strategy_params["rsi_period"] - 1)
        else:
            self.strategy_params["rsi_period"] = min(30, self.strategy_params["rsi_period"] + 1)

        if avg_close > avg_sma:
            self.strategy_params["ma_period"] = max(10, self.strategy_params["ma_period"] - 1)
        else:
            self.strategy_params["ma_period"] = min(50, self.strategy_params["ma_period"] + 1)

        self.evolution_steps += 1
        self.latest_strategy = (
            f"Evolução {self.evolution_steps}: RSI {self.strategy_params['rsi_period']}, "
            f"MA {self.strategy_params['ma_period']}, "
            f"confiança {self.strategy_params['confidence_threshold']:.2f}"
        )
        logging.info(
            "SuperAgente %s evoluiu de %s para %s com média RSI %.2f e momentum %.4f",
            self.id,
            old_params,
            self.strategy_params,
            avg_rsi,
            avg_momentum,
        )

    def train_on_successes(self) -> None:
        super().train_on_successes()
        self.evolve_strategy()

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "super"
        data["latest_strategy"] = self.latest_strategy
        return data


class AgentManager:
    def __init__(self, num_agents: int = 5, include_super_agent: bool = False):
        self.agents: List[TradingAgent] = []
        if include_super_agent and num_agents > 0:
            self.agents.append(SuperTradingAgent(str(uuid.uuid4())))
            self.agents.extend([TradingAgent(str(uuid.uuid4())) for _ in range(num_agents - 1)])
        else:
            self.agents = [TradingAgent(str(uuid.uuid4())) for _ in range(num_agents)]

    def active_agents(self) -> List[TradingAgent]:
        return list(self.agents)

    def remove_agent(self, agent: TradingAgent) -> None:
        if agent in self.agents:
            self.agents.remove(agent)

    def summary(self) -> None:
        for agent in self.agents:
            logging.info(
                "Resumo Agente %s - Saldo: %.2f, Trades: %d, Sucessos: %d, Falhas: %d",
                agent.id,
                agent.balance,
                agent.trades_executed,
                len(agent.success_history),
                len(agent.failure_history),
            )


class VerdentSimulator:
    def __init__(self, num_agents: int = 5, market_data: Optional[pd.DataFrame] = None, include_super_agent: bool = False):
        self.manager = AgentManager(num_agents, include_super_agent=include_super_agent)
        self.market_data = market_data if market_data is not None else self.load_historical_data()

    @staticmethod
    def load_historical_data(days: int = 300) -> pd.DataFrame:
        np.random.seed(42)
        prices = [1.1000]
        for _ in range(1, days):
            drift = np.random.normal(loc=0.0001, scale=0.003)
            prices.append(max(0.90, prices[-1] * (1 + drift)))
        return pd.DataFrame({"close": prices}, index=pd.date_range("2023-01-01", periods=days))

    def run_simulation(self, num_trades: int = 100) -> List[Dict[str, Any]]:
        summaries: List[Dict[str, Any]] = []
        logging.info("Iniciando simulação Verdent com %d agentes", len(self.manager.agents))

        for trade_round in range(num_trades):
            if not self.manager.agents:
                logging.warning("Nenhum agente restante. Simulação interrompida na rodada %d.", trade_round)
                break

            market_index = random.randint(20, len(self.market_data) - 2)
            for agent in self.manager.active_agents():
                agent.make_trade(self.market_data, market_index)
                if agent.check_deletion():
                    self.manager.remove_agent(agent)

            logging.info(
                "Rodada %d concluída - agentes restantes: %d",
                trade_round + 1,
                len(self.manager.agents),
            )

        self.manager.summary()
        for agent in self.manager.active_agents():
            summaries.append(agent.to_dict())

        logging.info("Simulação concluída.")
        print(f"Simulação finalizada. Veja o arquivo {LOG_FILE} para os logs detalhados.")
        return summaries


if __name__ == "__main__":
    simulator = VerdentSimulator(num_agents=10)
    simulator.run_simulation(num_trades=100)
