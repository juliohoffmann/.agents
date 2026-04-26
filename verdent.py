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


# Biblioteca de Estratégias carregada do arquivo
STRATEGY_LIBRARY = {
    1: {"name": "RSI sobrevendido + reversão", "type": "reversal", "signal": "buy"},
    2: {"name": "RSI sobrecomprado + pullback", "type": "reversal", "signal": "sell"},
    3: {"name": "Golden Cross (MA)", "type": "trend", "signal": "buy"},
    4: {"name": "Death Cross (MA)", "type": "trend", "signal": "sell"},
    5: {"name": "Suporte e resistência", "type": "range", "signal": "both"},
    6: {"name": "Breakout de canal", "type": "breakout", "signal": "buy"},
    7: {"name": "Breakdown de canal", "type": "breakout", "signal": "sell"},
    8: {"name": "Bollinger Bands squeeze", "type": "volatility", "signal": "buy"},
    9: {"name": "Bollinger Bands reversão", "type": "reversal", "signal": "both"},
    10: {"name": "MACD crossover", "type": "trend", "signal": "buy"},
    11: {"name": "MACD divergência", "type": "divergence", "signal": "both"},
    12: {"name": "ADX tendência forte", "type": "trend", "signal": "both"},
    13: {"name": "ADX tendência fraca", "type": "range", "signal": "none"},
    14: {"name": "Momentum de volume", "type": "volume", "signal": "buy"},
    15: {"name": "Volume divergente", "type": "divergence", "signal": "sell"},
    16: {"name": "Estocástico sobrevendido", "type": "reversal", "signal": "buy"},
    17: {"name": "Estocástico sobrecomprado", "type": "reversal", "signal": "sell"},
    18: {"name": "Candle engolfo bullish", "type": "candle", "signal": "buy"},
    19: {"name": "Candle engolfo bearish", "type": "candle", "signal": "sell"},
    20: {"name": "Martelo e martelo invertido", "type": "candle", "signal": "buy"},
    21: {"name": "Estrela cadente", "type": "candle", "signal": "sell"},
    22: {"name": "Fibonacci retração", "type": "fibonacci", "signal": "buy"},
    23: {"name": "Fibonacci extensão", "type": "fibonacci", "signal": "both"},
    24: {"name": "Pivôs diários", "type": "pivot", "signal": "both"},
    25: {"name": "Canal de regressão linear", "type": "trend", "signal": "buy"},
    26: {"name": "Price action inside bar", "type": "breakout", "signal": "both"},
    27: {"name": "Price action pin bar", "type": "candle", "signal": "both"},
    28: {"name": "Volume Profile high node", "type": "volume", "signal": "sell"},
    29: {"name": "Volume Profile low node", "type": "volume", "signal": "buy"},
    30: {"name": "Sentimento de mercado", "type": "sentiment", "signal": "both"},
    31: {"name": "Pullback à média móvel", "type": "trend", "signal": "buy"},
    32: {"name": "Retest de rompimento", "type": "reversal", "signal": "buy"},
    33: {"name": "Trade de gap", "type": "gap", "signal": "both"},
    34: {"name": "Trade de notícia", "type": "news", "signal": "both"},
    35: {"name": "Multi-timeframe confirmação", "type": "multi", "signal": "both"},
    36: {"name": "Hedge parcial", "type": "hedge", "signal": "both"},
    37: {"name": "Scalping range", "type": "scalping", "signal": "both"},
    38: {"name": "Swing trade em canal", "type": "swing", "signal": "both"},
    39: {"name": "Trend following com EMA 21/55", "type": "trend", "signal": "buy"},
    40: {"name": "Trend following com EMA 8/21", "type": "trend", "signal": "buy"},
    41: {"name": "Padrão de triângulo", "type": "pattern", "signal": "buy"},
    42: {"name": "Padrão de bandeira", "type": "pattern", "signal": "buy"},
    43: {"name": "Padrão de flâmula", "type": "pattern", "signal": "buy"},
    44: {"name": "Padrão cabeça e ombros invertido", "type": "pattern", "signal": "buy"},
    45: {"name": "Padrão cabeça e ombros", "type": "pattern", "signal": "sell"},
    46: {"name": "Trade com paridade correlacionada", "type": "correlation", "signal": "both"},
    47: {"name": "Trade de volatilidade baixa", "type": "volatility", "signal": "none"},
    48: {"name": "Trade de volatilidade alta", "type": "volatility", "signal": "both"},
    49: {"name": "Supertrend buy", "type": "trend", "signal": "buy"},
    50: {"name": "Supertrend sell", "type": "trend", "signal": "sell"},
    51: {"name": "Cluster de candles de indecisão", "type": "range", "signal": "none"},
    52: {"name": "Volume on Balance (OBV)", "type": "volume", "signal": "both"},
    53: {"name": "On Balance Volume divergência", "type": "divergence", "signal": "both"},
    54: {"name": "CCI compra", "type": "reversal", "signal": "buy"},
    55: {"name": "CCI venda", "type": "reversal", "signal": "sell"},
    56: {"name": "Linha de tendência dinâmica", "type": "trend", "signal": "both"},
    57: {"name": "Keltner Channel breakout", "type": "breakout", "signal": "buy"},
    58: {"name": "Keltner Channel fade", "type": "reversal", "signal": "sell"},
    59: {"name": "Ichimoku buy setup", "type": "trend", "signal": "buy"},
    60: {"name": "Ichimoku sell setup", "type": "trend", "signal": "sell"},
    61: {"name": "Três corvos negros", "type": "candle", "signal": "sell"},
    62: {"name": "Três soldados brancos", "type": "candle", "signal": "buy"},
    63: {"name": "SAR parabólico", "type": "trend", "signal": "both"},
    64: {"name": "Trade de média arqueada", "type": "trend", "signal": "both"},
    65: {"name": "Trade de confluência", "type": "confluence", "signal": "both"},
    66: {"name": "Estratégia de telhado e chão", "type": "range", "signal": "both"},
    67: {"name": "Estratégia de reversão de 50%", "type": "reversal", "signal": "both"},
    68: {"name": "Estratégia de escala de posição", "type": "position", "signal": "both"},
    69: {"name": "Trade de breakout falso", "type": "breakout", "signal": "sell"},
    70: {"name": "Transferência de risco parcial", "type": "risk", "signal": "both"},
    71: {"name": "Estratégia de tapering", "type": "risk", "signal": "sell"},
    72: {"name": "Estratégia de capitalização", "type": "risk", "signal": "buy"},
    73: {"name": "Tendência com MACD e RSI", "type": "trend", "signal": "buy"},
    74: {"name": "Convergência média móvel", "type": "trend", "signal": "buy"},
    75: {"name": "Reversão ao VWAP", "type": "reversal", "signal": "buy"},
    76: {"name": "Rompimento diário", "type": "breakout", "signal": "buy"},
    77: {"name": "Rompimento semanal", "type": "breakout", "signal": "buy"},
    78: {"name": "Faixa com RSI", "type": "range", "signal": "buy"},
    79: {"name": "Tendência com canal de Donchian", "type": "trend", "signal": "buy"},
    80: {"name": "Reversão com Bandas de Donchian", "type": "reversal", "signal": "sell"},
    81: {"name": "Fibonacci cluster", "type": "fibonacci", "signal": "both"},
    82: {"name": "Múltiplos indicadores", "type": "confluence", "signal": "both"},
    83: {"name": "Hedge inverso", "type": "hedge", "signal": "both"},
    84: {"name": "Stop mental", "type": "risk", "signal": "both"},
    85: {"name": "Posição única", "type": "risk", "signal": "both"},
    86: {"name": "Gestão de perdas", "type": "risk", "signal": "both"},
    87: {"name": "Relação risco/retorno", "type": "risk", "signal": "both"},
    88: {"name": "Correlação cruzada", "type": "correlation", "signal": "both"},
    89: {"name": "Volatilidade implícita", "type": "volatility", "signal": "none"},
}

# Lista de moedas suportadas
SUPPORTED_COINS = [
    "ADA/USDT", "TRX/USDT", "ARB/USDT", "XRP/USDT", "APT/USDT", "FIL/USDT", 
    "SUSHI/USDT", "ATOM/USDT", "NOT/USDT", "1000PEPE/USDT", "CFX/USDT", 
    "1INCH/USDT", "MASK/USDT", "SNX/USDT", "THETA/USDT", "OP/USDT", 
    "COMP/USDT", "SUI/USDT", "CHZ/USDT", "1000SHIB/USDT", "DOGE/USDT", 
    "NEAR/USDT", "SAND/USDT", "APE/USDT", "SOL/USDT", "CRV/USDT", 
    "DOT/USDT", "UNI/USDT", "BNB/USDT", "LTC/USDT", "BCH/USDT", 
    "LINK/USDT", "ETC/USDT", "ETH/USDT", "AAVE/USDT", "AVAX/USDT"
]


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
        # Estratégia atual do agente
        self.current_strategy_id = random.randint(1, 89)
        self.current_strategy = STRATEGY_LIBRARY[self.current_strategy_id]
        self.strategy_history: List[Dict[str, Any]] = []

    def select_strategy_by_market(self, features: np.ndarray) -> Dict[str, Any]:
        """Seleciona a melhor estratégia com base nas condições do mercado."""
        rsi, sma, close, momentum = features
        
        # Seleciona estratégia baseada nos indicadores
        if rsi < 30:
            # RSI sobrevendido - estratégia de reversão
            return STRATEGY_LIBRARY[1]
        elif rsi > 70:
            # RSI sobrecomprado - estratégia de venda
            return STRATEGY_LIBRARY[2]
        elif close > sma and momentum > 0:
            # Tendência de alta - estratégia de tendência
            if rsi < 50:
                return STRATEGY_LIBRARY[3]  # Golden Cross
            return STRATEGY_LIBRARY[39]  # EMA 21/55
        elif close < sma and momentum < 0:
            # Tendência de baixa - estratégia de venda
            if rsi > 50:
                return STRATEGY_LIBRARY[4]  # Death Cross
            return STRATEGY_LIBRARY[50]  # Supertrend sell
        
        # Condições neutras - usa estratégia atual ou seleciona aleatória
        return self.current_strategy

    def get_strategy_name(self) -> str:
        """Retorna o nome da estratégia atual."""
        return self.current_strategy["name"]

    def get_strategy_type(self) -> str:
        """Retorna o tipo da estratégia atual."""
        return self.current_strategy["type"]

    def get_strategy_signal(self) -> str:
        """Retorna o sinal da estratégia atual."""
        return self.current_strategy["signal"]

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
        """Descreve a estratégia atual baseada nos indicadores e na biblioteca."""
        # Atualiza a estratégia baseada nas condições do mercado
        self.current_strategy = self.select_strategy_by_market(features)
        return f"{self.current_strategy['name']} ({self.current_strategy['type']})"

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
        """Decide se deve fazer um trade baseado na estratégia atual e nos indicadores."""
        # Atualiza a estratégia baseada nas condições do mercado
        self.current_strategy = self.select_strategy_by_market(features)
        signal = self.current_strategy["signal"]
        
        # Se a estratégia indica "none", não faz trade
        if signal == "none":
            return False
        
        rsi, sma, close, momentum = features
        
        # Se não há histórico de treinamento, usa lógica baseada na estratégia
        if not self.success_history and not self.failure_history:
            # Permite trade se a estratégia indica buy/sell e condições são favoráveis
            if signal == "buy":
                return rsi < 60 and close > sma * 0.99  # Preço próximo ou acima da média
            elif signal == "sell":
                return rsi > 40 and close < sma * 1.01  # Preço próximo ou abaixo da média
            return rsi < 55 and close > sma * 0.99  # Condição padrão
            
        try:
            proba = self.model.predict_proba([features])[0]
            win_probability = proba[1]
            logging.debug("Agente %s probabilidade de vitória: %.2f", self.id, win_probability)
            return win_probability >= self.strategy_params["confidence_threshold"]
        except (NotFittedError, AttributeError, IndexError):
            # Fallback: usa lógica baseada na estratégia
            if signal == "buy":
                return rsi < 60 and close > sma * 0.99
            elif signal == "sell":
                return rsi > 40 and close < sma * 1.01
            return rsi < 55 and close > sma * 0.99

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
            "current_strategy": self.current_strategy["name"],
            "strategy_type": self.current_strategy["type"],
            "strategy_signal": self.current_strategy["signal"],
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
        """Evolui a estratégia do agente com base nos resultados."""
        if not self.success_history:
            return

        features = np.vstack([entry["features"] for entry in self.success_history])
        avg_rsi, avg_sma, avg_close, avg_momentum = features.mean(axis=0)
        old_params = self.strategy_params.copy()
        old_strategy = self.current_strategy["name"]

        # Ajusta parâmetros baseados nos resultados
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

        # Seleciona nova estratégia da biblioteca baseada nos resultados
        self._select_best_strategy(avg_rsi, avg_momentum, avg_close, avg_sma)

        self.evolution_steps += 1
        self.latest_strategy = (
            f"Evolução {self.evolution_steps}: {self.current_strategy['name']} | "
            f"RSI {self.strategy_params['rsi_period']}, "
            f"MA {self.strategy_params['ma_period']}, "
            f"confiança {self.strategy_params['confidence_threshold']:.2f}"
        )
        logging.info(
            "SuperAgente %s evoluiu de '%s' para '%s' com média RSI %.2f e momentum %.4f",
            self.id,
            old_strategy,
            self.current_strategy["name"],
            avg_rsi,
            avg_momentum,
        )

    def _select_best_strategy(self, avg_rsi: float, avg_momentum: float, avg_close: float, avg_sma: float) -> None:
        """Seleciona a melhor estratégia da biblioteca baseada nos indicadores."""
        
        # Condições de mercado determinam a melhor estratégia
        if avg_rsi < 30:
            # Mercado sobrevendido - usa estratégia de reversão
            self.current_strategy_id = 1
            self.current_strategy = STRATEGY_LIBRARY[1]
        elif avg_rsi > 70:
            # Mercado sobrecomprado - usa estratégia de venda
            self.current_strategy_id = 2
            self.current_strategy = STRATEGY_LIBRARY[2]
        elif avg_momentum > 0 and avg_close > avg_sma:
            # Tendência de alta clara
            if avg_rsi < 50:
                self.current_strategy_id = 3  # Golden Cross
                self.current_strategy = STRATEGY_LIBRARY[3]
            else:
                self.current_strategy_id = 39  # EMA 21/55
                self.current_strategy = STRATEGY_LIBRARY[39]
        elif avg_momentum < 0 and avg_close < avg_sma:
            # Tendência de baixa clara
            if avg_rsi > 50:
                self.current_strategy_id = 4  # Death Cross
                self.current_strategy = STRATEGY_LIBRARY[4]
            else:
                self.current_strategy_id = 50  # Supertrend sell
                self.current_strategy = STRATEGY_LIBRARY[50]
        elif abs(avg_momentum) < 0.001:
            # Mercado lateral - usa estratégia de range
            self.current_strategy_id = 5  # Suporte e resistência
            self.current_strategy = STRATEGY_LIBRARY[5]
        else:
            # Usa estratégia de confluência
            self.current_strategy_id = 65
            self.current_strategy = STRATEGY_LIBRARY[65]

    def train_on_successes(self) -> None:
        super().train_on_successes()
        self.evolve_strategy()

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "super"
        data["latest_strategy"] = self.latest_strategy
        data["evolution_steps"] = self.evolution_steps
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
