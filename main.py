from fastapi import FastAPI, Response, Request, status, Cookie, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import db
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import pandas as pd
import acoes
import pathlib
import pickle
from acoes import SMA, EMA, RSI, MF, ATR, CMA, MACD, ATR
from ai.tools.lstm_encoder_decoder_tools import prepare_data_for_prediction, BANKS
import json
#import tensorflow as tf
from sklearn import linear_model



class ItemLogin(BaseModel):
    email: str
    senha: str


class ItemSignup(BaseModel):
    email: str
    senha: str
    nome: str


class ItemSavePref(BaseModel):
    stock: str
    data: str


class ItemGetPref(BaseModel):
    stock: str


db_pool = db.connect()

app = FastAPI()

# Configuração do CORS para permitir qualquer origem
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


JWT_ALGORITHM = "HS256"
JWT_SECRET = "secrect=ke"


@app.post("/api/login")
async def login(item: ItemLogin):
    login = db.login(db_pool, item.email, item.senha)
    if "token" in login:
        payload = {"sub": item.email, "exp": datetime.utcnow() +
                   timedelta(minutes=30)}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        response = JSONResponse(
            content={"message": "Autenticado com sucesso", "token": token})
        expires = datetime.utcnow().replace(tzinfo=timezone.utc) + \
            timedelta(minutes=30)  # token expira em 30 minutos
        response.set_cookie(key="token", value=token,
                            expires=expires, httponly=True)
        response.set_cookie(key="userid", value=login["id"],
                            expires=expires, httponly=True)
        return response
    elif "erro" in login:
        return JSONResponse(content={"error": login["erro"]})
    else:
        return JSONResponse(content={"error": "Erro desconhecido"})


@app.get("/ai")
async def ai(token: str = Cookie(None)):
    try:
        jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return FileResponse("pages/ai.html")
    except:
        return FileResponse("pages/login.html")


@app.get("/login")
async def login_(token: str = Cookie(None)):
    try:
        jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return FileResponse("pages/ai.html")
    except:
        return FileResponse("pages/login.html")

# Rota para cadastro


@app.post("/api/signup")
async def signup(item: ItemSignup):
    login = db.signup(db_pool, item.nome, item.email, item.senha)
    if "token" in login:
        payload = {"sub": item.email, "exp": datetime.utcnow() +
                   timedelta(minutes=30)}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        response = JSONResponse(
            content={"message": "Autenticado com sucesso", "token": token})
        expires = datetime.utcnow().replace(tzinfo=timezone.utc) + \
            timedelta(minutes=30)  # token expira em 30 minutos
        response.set_cookie(key="token", value=token,
                            expires=expires, httponly=True)
        response.set_cookie(key="userid", value=login["id"],
                            expires=expires, httponly=True)
        return response
    elif "erro" in login:
        return JSONResponse(content={"error": login["erro"]})
    else:
        return JSONResponse(content={"error": "Erro desconhecido"})


@app.post("/api/savepref")
async def savepref(item: ItemSavePref, userid: str = Cookie(None)):
    savepref = db.savepref(db_pool, item.stock + ".SA", userid, item.data)
    return JSONResponse(content=savepref)


@app.get("/api/getpref/{stock}")
async def getpref(stock: str, userid: str = Cookie(None)):
    getpref = db.getpref(db_pool, stock + ".SA", userid)
    return JSONResponse(content=getpref)


@app.get("/api/user")
async def user(userid: str = Cookie(None)):
    user = db.user(db_pool, userid)
    return JSONResponse(content=user)


@app.get("/")
async def home():
    return FileResponse("pages/index.html")


@app.get("/about")
async def about():
    return FileResponse("pages/about.html")


@app.get("/contact")
async def contact():
    return FileResponse("pages/contact.html")


@app.get("/api/data/{ticker}")
async def read_item(ticker: str):
    return stock(ticker)


@app.post("/api/get_stock_data")
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


@app.get("/api/SMA")
def SMA_get(ticket, period=14, column='Close'):
    period = int(period)
    data = acoes.get_data(ticket)
    indicator_data = SMA(data, period=period, column=column)
    column_name = f"SMA_{period}_{column}"
    data[column_name] = indicator_data
    data.fillna(-9999, inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict


@app.get("/api/EMA")
def EMA_get(ticket, period=14, column='Close'):
    data = acoes.get_data(ticket)
    indicator_data = EMA(data, period=period, column=column)
    column_name = f"EMA_{period}_{column}"
    data[column_name] = indicator_data
    data.fillna(-9999, inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict


@app.get("/api/CMA")
def CMA_get(ticket, column='Close'):
    data = acoes.get_data(ticket)
    indicator_data = CMA(data, column=column)
    column_name = f"CMA_{column}"
    data[column_name] = indicator_data
    data.fillna(-9999, inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict


@app.get("/api/MACD")
def MACD_get(ticket, period_long=26, period_short=12, period_signal=9):
    data = acoes.get_data(ticket)
    indicator_data = MACD(data, period_long=26,
                          period_short=12, period_signal=9)
    column_name = f"MACD_{period_long}_{period_short}"
    column_name_signal_line = f"MACD_{period_signal}"
    data[column_name] = indicator_data[0]
    data[column_name_signal_line] = indicator_data[1]
    data.fillna(-9999, inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict


@app.get("/api/RSI")
def RSI_get(ticket, period=14, column='Close'):
    data = acoes.get_data(ticket)
    indicator_data = RSI(data, period=period, column=column)
    column_name = f"RSI_{column}_{period}"
    data[column_name] = indicator_data
    data.fillna(-9999, inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict


@app.get("/api/MF")
def MF_get(ticket, period=14, column='Close'):
    data = acoes.get_data(ticket)
    indicator_data = MF(data, period=period, column=column)
    column_name = f"MF_{column}_{period}"
    data[column_name] = indicator_data
    data.fillna(-9999, inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict


@app.get("/api/ATR")
def ATR_get(ticket, period=14):
    data = acoes.get_data(ticket)
    indicator_data = ATR(data, period=period)
    column_name = f"ATR__{period}"
    data[column_name] = indicator_data
    data.fillna(-9999, inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict


@app.get("/api/predict_lstm")
def predict_lstm(stock):
    if stock not in BANKS:
        raise HTTPException(422, "Model wasn't trained to use this stock!")
    window = 60

    data = acoes.get_data(stock, period="3mo", interval="1d")
    data = data["Close"]
    data = data.tail(window)

    parent_path = pathlib.Path(__file__).parents[1]
    min_max_scaler_path = "datasets\\01_raw\\min_max_scaler.pkl"
    min_max_scaler = pickle.load(open(min_max_scaler_path, "rb"))

    data_scaled = min_max_scaler.transform(data.to_numpy().reshape(-1, 1))
    transformed_data = prepare_data_for_prediction(
        data_scaled, 0, len(data_scaled), window)

    lstm_enco_deco = tf.keras.saving.load_model("lstm_encoder_decoder_model")
    predicted = lstm_enco_deco.predict(transformed_data)

    predicted = predicted[-1].reshape(1, -1)
    predicted = min_max_scaler.inverse_transform(predicted)[0]
    predicted = predicted.tolist()
    data.index = data.index.astype(str, copy=False)
    data_dict = data.to_dict()
    json_object = json.dumps(data_dict, indent=4)
    return {"data": json_object,
            "predictions": predicted}

@app.get("/api/predict_lr")
def predict_lr(stock):

    data = acoes.get_data(stock, start='1990-01-01', end=datetime.now().strftime('%Y-%m-%d'))
    datai = data
    features = ['Close', 'Open', 'CMA', 'EMA10', 'SMA10', 'EMA30', 'SMA30', 'EMA60', 'SMA60', 'RSI']
    
    data['CMA'] = acoes.CMA(data)
    data['EMA30'] = acoes.EMA(data, 30)
    data['SMA30'] = acoes.SMA(data, 30)
    data['EMA10'] = acoes.EMA(data, 10)
    data['SMA10'] = acoes.SMA(data, 10)
    data['EMA60'] = acoes.EMA(data, 60)
    data['SMA60'] = acoes.SMA(data, 60)
    data['RSI'] = acoes.RSI(data, 1)

    data['y1'] = data['Close'].shift(-1)
    data = data[features + ['y1']]

    data_to_train = data.iloc[0:-1]
    data_to_predict = data.iloc[-1:]

    data_to_train.dropna(inplace=True)

    X = data_to_train[features]
    y = data_to_train[['y1']]

    reg = linear_model.LinearRegression().fit(X, y)

    data_to_predict_X = data_to_predict[features]
    predict = reg.predict(data_to_predict_X).tolist()

    datai.index = datai.index.astype(str, copy = False)
    data_dict = datai.to_dict()
    json_object = json.dumps(data_dict, indent = 4)
    return {"data": json_object,
            "predictions": predict}

@app.get("/api/availableOptions")
def availabeOptions(model):
    if model == "lstm":
        return BANKS
    else:
        raise HTTPException(422, "Model doesn't exist")


app.mount("/static", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
