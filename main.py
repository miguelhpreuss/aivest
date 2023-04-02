from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import db

db_pool = db.connect()

db.signup(db_pool, "mhp", "kkk@as.com", "askoask")

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)