from fastapi import FastAPI
from database import init_db

app = FastAPI()
@app.on_event("startup")
def on_startup():
    init_db()
@app.get("/")
def root():
    return {"hello": "world"}