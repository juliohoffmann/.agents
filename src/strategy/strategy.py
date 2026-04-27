# Biblioteca de Estratégias de Trading
# Baseado no documento Binance_Padrao.pdf

from typing import Dict, List, Any
from enum import Enum


class StrategyType(Enum):
    REVERSAL = "reversal"
    TREND = "trend"
    RANGE = "range"
    BREAKOUT = "breakout"


class Signal(Enum):
    BUY = "buy"
    SELL = "sell"
    BOTH = "both"


# Biblioteca de Estratégias
STRATEGY_LIBRARY: Dict[int, Dict[str, Any]] = {
    1: {"name": "RSI sobrevendido + reversão", "type": StrategyType.REVERSAL.value, "signal": Signal.BUY.value},
    2: {"name": "RSI sobrecomprado + pullback", "type": StrategyType.REVERSAL.value, "signal": Signal.SELL.value},
    3: {"name": "Golden Cross (MA)", "type": StrategyType.TREND.value, "signal": Signal.BUY.value},
    4: {"name": "Death Cross (MA)", "type": StrategyType.TREND.value, "signal": Signal.SELL.value},
    5: {"name": "Suporte e resistência", "type": StrategyType.RANGE.value, "signal": Signal.BOTH.value},
    6: {"name": "Quebra de resistência", "type": StrategyType.BREAKOUT.value, "signal": Signal.BUY.value},
    7: {"name": "Quebra de suporte", "type": StrategyType.BREAKOUT.value, "signal": Signal.SELL.value},
}


# Configurações de banca (baseado na tabela principal)
BANK_CONFIGS: List[Dict[str, Any]] = [
    {
        "bank": "DE 90 A 150 USDT",
        "strategy": "Millionaire Strategy",
        "long1stOrderSize": 9,
        "short1stOrderSize": 3,
        "leverage": 20,
        "stopLoss": 180,
        "doubleFirstLong": True,
        "doubleFirstShort": True,
        "quantidadeMoedas": 1
    },
    {
        "bank": "300 USDT",
        "strategy": "Millionaire Strategy",
        "long1stOrderSize": 9,
        "short1stOrderSize": 3,
        "leverage": 20,
        "stopLoss": 180,
        "doubleFirstLong": True,
        "doubleFirstShort": True,
        "quantidadeMoedas": 2
    },
    {
        "bank": "500 USDT",
        "strategy": "Millionaire Strategy",
        "long1stOrderSize": 9,
        "short1stOrderSize": 3,
        "leverage": 20,
        "stopLoss": 180,
        "doubleFirstLong": True,
        "doubleFirstShort": True,
        "quantidadeMoedas": 3
    },
    {
        "bank": "1.000 USDT",
        "strategy": "Millionaire Strategy",
        "long1stOrderSize": 9,
        "short1stOrderSize": 3,
        "leverage": 20,
        "stopLoss": 180,
        "doubleFirstLong": True,
        "doubleFirstShort": True,
        "quantidadeMoedas": 6
    },
    {
        "bank": "2.000 USDT",
        "strategy": "Millionaire Strategy",
        "long1stOrderSize": 9,
        "short1stOrderSize": 3,
        "leverage": 20,
        "stopLoss": 180,
        "doubleFirstLong": True,
        "doubleFirstShort": True,
        "quantidadeMoedas": 8
    },
]


def get_strategy_by_id(strategy_id: int) -> Dict[str, Any]:
    """Retorna configuração de estratégia por ID"""
    return STRATEGY_LIBRARY.get(strategy_id, {})


def get_bank_config(bank_value: float) -> Dict[str, Any]:
    """Retorna configuração de banca mais adequada para o valor"""
    for config in BANK_CONFIGS:
        if "A" in config["bank"]:
            # Para valores entre 90 e 150
            if 90 <= bank_value <= 150:
                return config
        else:
            # Para valores específicos
            bank_num = float(config["bank"].replace(".", "").replace(" ", ""))
            if abs(bank_num - bank_value) < bank_num * 0.2:  # 20% de tolerância
                return config
    
    # Default: menor configuração
    return BANK_CONFIGS[0]


def calculate_position_size(bank_config: Dict[str, Any], is_long: bool = True) -> float:
    """Calcula tamanho da posição baseado na configuração"""
    if is_long:
        return bank_config.get("long1stOrderSize", 9)
    return bank_config.get("short1stOrderSize", 3)


def should_double_position(bank_config: Dict[str, Any], is_long: bool = True) -> bool:
    """Verifica se deve dobrar a posição"""
    if is_long:
        return bank_config.get("doubleFirstLong", True)
    return bank_config.get("doubleFirstShort", True)