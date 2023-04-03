from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import db

from pydantic import BaseModel


class Item(BaseModel):
    email: str
    senha: str

db_pool = db.connect()

#db.signup(db_pool, "mii", "a@a.com", "admin123")

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


@app.post("/api/login")
async def login(item: Item):
    login = db.login(db_pool, item.email, item.senha)
    if "token" in login:
        return {"message": "Autenticado com sucesso", "token": login["token"]}
    elif "erro" in login:
        return {"error": login["erro"]}
    else:
        return {"error": "Erro desconhecido"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)