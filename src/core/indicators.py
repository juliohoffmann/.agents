import ta
import pandas as pd

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Tendência
    df["ema_9"]  = ta.trend.EMAIndicator(df["close"], window=9).ema_indicator()
    df["ema_21"] = ta.trend.EMAIndicator(df["close"], window=21).ema_indicator()
    df["ema_50"] = ta.trend.EMAIndicator(df["close"], window=50).ema_indicator()

    # Momentum
    df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

    # Volatilidade
    bb = ta.volatility.BollingerBands(df["close"], window=20)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()
    df["bb_mid"]   = bb.bollinger_mavg()

    # Volume
    df["obv"] = ta.volume.OnBalanceVolumeIndicator(df["close"], df["volume"]).on_balance_volume()

    # MACD
    macd = ta.trend.MACD(df["close"])
    df["macd"]        = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    return df.dropna()
