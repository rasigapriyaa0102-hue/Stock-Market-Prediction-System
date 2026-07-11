import pandas as pd

def add_indicators(df):
     # ensure numeric
    numeric_cols = ["Open","High","Low","Close","Volume"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()
    # SMA
    df["SMA20"] = df["Close"].rolling(window=20).mean()
    df["SMA50"] = df["Close"].rolling(window=50).mean()

    # EMA
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()

    # RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_DIFF"] = df["MACD"] - df["MACD_SIGNAL"]

    # Bollinger Bands
    sma20 = df["Close"].rolling(window=20).mean()
    std20 = df["Close"].rolling(window=20).std()

    df["BB_HIGH"] = sma20 + (2 * std20)
    df["BB_LOW"] = sma20 - (2 * std20)
    df["BB_MID"] = sma20

    # 🔵 Fibonacci Retracement
    high_price = df["High"].max()
    low_price = df["Low"].min()

    diff = high_price - low_price

    df["FIB_236"] = high_price - diff * 0.236
    df["FIB_382"] = high_price - diff * 0.382
    df["FIB_50"]  = high_price - diff * 0.5
    df["FIB_618"] = high_price - diff * 0.618
    df["FIB_786"] = high_price - diff * 0.786

    df = df.dropna()

    return df