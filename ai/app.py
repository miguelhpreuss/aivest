from fastapi import FastAPI, HTTPException
import pandas as pd
import json
import uvicorn
from database import ALCHEMY_POSTGRES_ENGINE
import acoes
from acoes import SMA, EMA, RSI, MF, ATR, CMA, MACD, ATR
from tools.lstm_encoder_decoder_tools import prepare_data_for_prediction, BANKS
import pathlib
import pickle
import tensorflow as tf
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"message": "welcome to smart invest system"}

@app.post("/get_stock_data")
def get_stock_data(stock, period="1mo", interval="1d",
                start=None, end=None, prepost=False, actions=True,
                auto_adjust=True, back_adjust=False, repair=False, keepna=False,
                proxy=None, rounding=False, timeout=10,
                debug=True, raise_errors=False):
    
    data = acoes.get_data(stock, period=period, interval=interval,
                start=start, end=end, prepost=prepost, actions=actions,
                auto_adjust=auto_adjust, back_adjust=back_adjust, repair=repair, keepna=keepna,
                proxy=proxy, rounding=rounding, timeout=timeout,
                debug=debug, raise_errors=raise_errors)

    data.index = data.index.astype(str)
    data = data.to_dict()
    return data


@app.post("/SMA")
def SMA_post(stock, stock_period="1mo", interval="1d", period=14, column='Close'):
    period=int(period)
    data = acoes.get_data(stock, period=stock_period, interval=interval)

    data.index = data.index.astype(str)
    data = data.to_dict()
    indicator_data = SMA(data, period=stock_period, interval=interval, column=column)
    column_name = f"SMA_{period}_{column}"
    data[column_name] = indicator_data
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict

@app.post("/EMA")
def EMA_post(stock, stock_period="1mo", interval="1d", period=14, column='Close'):
    period=int(period)
    data = acoes.get_data(stock, period=stock_period, interval=interval)

    indicator_data = EMA(data, period=period, column=column)
    column_name = f"EMA_{period}_{column}"
    data[column_name] = indicator_data
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    json_object = json.dumps(data_dict, indent = 4)
    return {"data": json_object,
            "indicator_name": column_name}
    
@app.post("/CMA")
def CMA_post(stock, stock_period="1mo", interval="1d",column='Close'):
    data = acoes.get_data(stock, period=stock_period, interval=interval)

    indicator_data = CMA(data, column=column)
    column_name = f"CMA_{column}"
    data[column_name] = indicator_data
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    json_object = json.dumps(data_dict, indent = 4)
    return {"data": json_object,
            "indicator_name": column_name}

@app.post("/MACD")
def MACD_post(stock, stock_period="1mo", interval="1d", period_long=26, period_short=12, period_signal=9):
    period_long = int(period_long)
    period_short = int(period_short)
    period_signal = int(period_signal)

    data = acoes.get_data(stock, period=stock_period, interval=interval)


    indicator_data = MACD(data, period_long=26, period_short=12, period_signal=9)
    column_name = f"MACD_{period_long}_{period_short}"
    column_name_signal_line =f"MACD_{period_signal}"
    data[column_name] = indicator_data[0]
    data[column_name_signal_line] = indicator_data[1]
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    json_object = json.dumps(data_dict, indent = 4)
    return {"data": json_object,
            "indicator_name": [column_name, column_name_signal_line],
            }

@app.post("/RSI")
def RSI_post(stock, stock_period="1mo", interval="1d", period=14, column='Close'):
    period = int(period)
    data = acoes.get_data(stock, period=stock_period, interval=interval)

    indicator_data = RSI(data, period=period, column=column)
    column_name = f"RSI_{column}_{period}"
    data[column_name] = indicator_data
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    json_object = json.dumps(data_dict, indent = 4)
    return {"data": json_object,
            "indicator_name": column_name}

@app.post("/MF")
def MF_post(stock, stock_period="1mo", interval="1d", period=14, column='Close'):
    period = int(period)
    data = acoes.get_data(stock, period=stock_period, interval=interval)

    indicator_data = MF(data, period=period, column=column)
    column_name = f"MF_{column}_{period}"
    data[column_name] = indicator_data
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    json_object = json.dumps(data_dict, indent = 4)
    return {"data": json_object,
            "indicator_name": column_name}

@app.post("/ATR")
def ATR_post(stock, stock_period="1mo", interval="1d",period=14):
    period = int(period)
    data = acoes.get_data(stock, period=stock_period, interval=interval)

    indicator_data = ATR(data, period=period)
    column_name = f"ATR__{period}"
    data[column_name] = indicator_data
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    json_object = json.dumps(data_dict, indent = 4)
    return {"data": json_object,
            "indicator_name": column_name}

@app.post("/Predict_5_days")
def predict_five_days(stock):
    if stock not in BANKS:
        raise HTTPException(422, "Model wasn't trained to use this stock!")
    window = 60

    data = acoes.get_data(stock, period="3mo", interval="1d")
    data = data["Close"]
    data = data.tail(window)

    parent_path = pathlib.Path(__file__).parents[1]
    min_max_scaler_path = pathlib.Path(parent_path, "datasets", "01_raw", "min_max_scaler.pkl")
    min_max_scaler = pickle.load(open(min_max_scaler_path, "rb"))

    data_scaled =  min_max_scaler.transform(data.to_numpy().reshape(-1,1))
    transformed_data = prepare_data_for_prediction(data_scaled, 0, len(data_scaled), window)

    lstm_model_path = pathlib.Path(parent_path, "lstm_encoder_decoder_model")
    lstm_enco_deco = tf.keras.models.load_model(lstm_model_path)
    predicted = lstm_enco_deco.predict(transformed_data)

    predicted = predicted[-1].reshape(1, -1)
    predicted = min_max_scaler.inverse_transform(predicted)[0]
    predicted = predicted.tolist()
    data.index = data.index.astype(str, copy = False)
    data_dict = data.to_dict()
    json_object = json.dumps(data_dict, indent = 4)
    return {"data": json_object,
            "predictions": predicted}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, log_level="info", reload=True)