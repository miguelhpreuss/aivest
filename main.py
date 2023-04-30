from fastapi import FastAPI, Response, Request, status, Cookie
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import db
from ai import stock
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel


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

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
