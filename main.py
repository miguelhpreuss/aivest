from fastapi import FastAPI, Response, Request, status, Cookie, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import db
from ai import stock
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import pandas as pd
import acoes
from acoes import SMA, EMA, RSI, MF, ATR, CMA, MACD, ATR
import json

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
    #data.to_sql("data", ALCHEMY_POSTGRES_ENGINE.connect(), if_exists='replace')
    data.index = data.index.astype(str)
    data = data.to_dict()
    return data

@app.get("/api/SMA")
def SMA_get(ticket, period=14, column='Close'):
    period=int(period)
    #connection = ALCHEMY_POSTGRES_ENGINE.connect()
    #try:
    #    data = pd.read_sql("data", connection, index_col="Date")
    #except Exception as exc:
    #    raise HTTPException(status_code=422, detail="No stock was selected to be able to calculate indicator =")
    data = acoes.get_data(ticket+ ".SA")
    ########################################
    indicator_data = SMA(data, period=period, column=column)
    column_name = f"SMA_{period}_{column}"
    data[column_name] = indicator_data
    data.to_sql("data", connection, if_exists="replace", index=False)
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict

@app.get("/api/EMA")
def EMA_get(ticket, period=14, column='Close'):
    #connection = ALCHEMY_POSTGRES_ENGINE.connect()
    #try:
    #    data = pd.read_sql("data", connection, index_col='Date')
    #except Exception as exc:
    #    raise HTTPException(status_code=422, detail="No stock was selected to be able to calculate indicator =")
    data = acoes.get_data(ticket + ".SA")
    ###
    indicator_data = EMA(data, period=period, column=column)
    column_name = f"EMA_{period}_{column}"
    data[column_name] = indicator_data
    #data.to_sql("data", connection, if_exists="replace", index=False)
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict
    
@app.get("/api/CMA")
def CMA_get(ticket, column='Close'):
    #connection = ALCHEMY_POSTGRES_ENGINE.connect()
    #try:
    #    data = pd.read_sql("data", connection, index_col="Date")
    #except Exception as exc:
    #    raise HTTPException(status_code=422, detail="No stock was selected to be able to calculate indicator =")
    data = acoes.get_data(ticket + ".SA")
    ####
    indicator_data = CMA(data, column=column)
    column_name = f"CMA_{column}"
    data[column_name] = indicator_data
    #data.to_sql("data", connection, if_exists="replace", index=False)
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict

@app.get("/api/MACD")
def MACD_get(ticket,period_long=26, period_short=12, period_signal=9):
    #connection = ALCHEMY_POSTGRES_ENGINE.connect()
    #try:
    #    data = pd.read_sql("data", connection, index_col="Date")
    #except Exception as exc:
    #    raise HTTPException(status_code=422, detail="No stock was selected to be able to calculate indicator =")
    data = acoes.get_data(ticket + ".SA")
    ###
    indicator_data = MACD(data, period_long=26, period_short=12, period_signal=9)
    column_name = f"MACD_{period_long}_{period_short}"
    column_name_signal_line =f"MACD_{period_signal}"
    data[column_name] = indicator_data[0]
    data[column_name_signal_line] = indicator_data[1]
    #data.to_sql("data", connection, if_exists="replace", index=False)
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict

@app.get("/api/RSI")
def RSI_get(ticket, period=14, column='Close'):
    #connection = ALCHEMY_POSTGRES_ENGINE.connect()
    #try:
    #    data = pd.read_sql("data", connection, index_col="Date")
    #except Exception as exc:
    #    raise HTTPException(status_code=422, detail="No stock was selected to be able to calculate indicator =")
    data = acoes.get_data(ticket + ".SA")
    ####
    indicator_data = RSI(data, period=period, column=column)
    column_name = f"RSI_{column}_{period}"
    data[column_name] = indicator_data
    #data.to_sql("data", connection, if_exists="replace", index=False)
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict

@app.get("/api/MF")
def MF_get(ticket, period=14, column='Close'):
    #connection = ALCHEMY_POSTGRES_ENGINE.connect()
    #try:
    #    data = pd.read_sql("data", connection, index_col="Date")
    #except Exception as exc:
    #    raise HTTPException(status_code=422, detail="No stock was selected to be able to calculate indicator =")
    data = acoes.get_data(ticket + ".SA")
    ###
    indicator_data = MF(data, period=period, column=column)
    column_name = f"MF_{column}_{period}"
    data[column_name] = indicator_data
    #data.to_sql("data", connection, if_exists="replace", index=False)
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict

@app.get("/api/ATR")
def ATR_get(ticket, period=14):
    #connection = ALCHEMY_POSTGRES_ENGINE.connect()
    #try:
    #    data = pd.read_sql("data", connection, index_col="Date")
    #except Exception as exc:
    #    raise HTTPException(status_code=422, detail="No stock was selected to be able to calculate indicator =")
    data = acoes.get_data(ticket + ".SA")
    ###
    indicator_data = ATR(data, period=period)
    column_name = f"ATR__{period}"
    data[column_name] = indicator_data
    #data.to_sql("data", connection, if_exists="replace", index=False)
    data.fillna(-9999,inplace=True)
    data.index = data.index.astype(str)
    data_dict = data.to_dict()
    final_dict = {}
    final_dict['data'] = data_dict
    final_dict['indicator_name'] = column_name
    return final_dict

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
