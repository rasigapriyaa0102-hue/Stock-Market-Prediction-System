import pandas as pd
import numpy as np
import os
import joblib

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

from indicators import add_indicators

DATA_PATH = "data"
SEQ_LENGTH = 60
PRED_DAYS = 30   # 🔥 30 days output

X_all = []
y_all = []

scalers = {}

for file in os.listdir(DATA_PATH):

    stock = file.replace(".csv","")
    df = pd.read_csv(os.path.join(DATA_PATH, file))

    for col in ["Open","High","Low","Close","Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()
    df = add_indicators(df)

    df["Sentiment"] = 0

    features = df[[
        "Close","Volume",
        "SMA20","SMA50",
        "EMA20","EMA50",
        "RSI",
        "MACD","MACD_SIGNAL","MACD_DIFF",
        "BB_HIGH","BB_LOW","BB_MID",
        "FIB_236","FIB_382","FIB_50","FIB_618","FIB_786",
        "Sentiment"
    ]]

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(features)
    scalers[stock] = scaler

    for i in range(SEQ_LENGTH, len(scaled) - PRED_DAYS):
        X_all.append(scaled[i-SEQ_LENGTH:i])
        y_all.append(scaled[i:i+PRED_DAYS, 0])  # 30 days target

X_all = np.array(X_all)
y_all = np.array(y_all)

# 🔥 MODEL
model = Sequential()
model.add(LSTM(128, input_shape=(SEQ_LENGTH, X_all.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(64))
model.add(Dense(PRED_DAYS))  # 30 outputs

model.compile(optimizer="adam", loss="mse")

model.fit(X_all, y_all, epochs=30, batch_size=32)

os.makedirs("models", exist_ok=True)

model.save("models/model.h5")
joblib.dump(scalers, "models/scalers.pkl")

print("✅ 30-day model trained")