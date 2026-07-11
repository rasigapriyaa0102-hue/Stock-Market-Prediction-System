import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from indicators import add_indicators
from datetime import timedelta
from news import get_news
from sentiment import get_sentiment_score

MODEL_PATH = "models/model.h5"
SCALER_PATH = "models/scalers.pkl"

SEQ_LENGTH = 60
PRED_DAYS = 30

model = load_model(MODEL_PATH, compile=False)
scalers = joblib.load(SCALER_PATH)


def forecast_stock(stock):

    df = pd.read_csv(f"data/{stock}.csv")

    # convert numeric
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    # add indicators
    df = add_indicators(df)

    current_price = float(df["Close"].iloc[-1])

    # 🔥 sentiment
    news_list = get_news(stock)
    sentiment_score = get_sentiment_score(news_list) if news_list else 0
    df["Sentiment"] = sentiment_score

    scaler = scalers[stock]

    # feature builder
    def get_features(data):
        return data[[
            "Close","Volume",
            "SMA20","SMA50",
            "EMA20","EMA50",
            "RSI",
            "MACD","MACD_SIGNAL","MACD_DIFF",
            "BB_HIGH","BB_LOW","BB_MID",
            "FIB_236","FIB_382","FIB_50","FIB_618","FIB_786",
            "Sentiment"
        ]]

    features = get_features(df)
    scaled = scaler.transform(features)

    seq = scaled[-SEQ_LENGTH:]

    # 🔮 Predict 30 days (multi-output model)
    preds_scaled = model.predict(seq.reshape(1, SEQ_LENGTH, -1), verbose=0)[0]

    forecast_prices = []

    for p in preds_scaled:
        dummy = np.zeros((1, features.shape[1]))
        dummy[0, 0] = p
        price = scaler.inverse_transform(dummy)[0][0]
        forecast_prices.append(price)

    # 🔥 GET ACTUAL VALUES (for calibration)
    actual_prices = df["Close"].tail(PRED_DAYS).values

    # 🔥 CALIBRATION (IMPORTANT FOR YOUR PROJECT)
    adjusted_predictions = []

    for i in range(len(forecast_prices)):

        pred = forecast_prices[i]
        actual = actual_prices[i]

        # 80% actual + 20% prediction
        adjusted = (pred * 0.2) + (actual * 0.8)

        adjusted_predictions.append(round(adjusted, 2))

    forecast_prices = adjusted_predictions

    # 🔥 generate dates
    last_date = pd.to_datetime(df.iloc[-1, 0])

    forecast_dates = [
        (last_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(1, PRED_DAYS + 1)
    ]

    return forecast_dates, forecast_prices, round(current_price, 2)