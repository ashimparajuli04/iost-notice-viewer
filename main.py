from fastapi import FastAPI
from database import init_db
from routers import routers


app = FastAPI()
@app.on_event("startup")
def on_startup():
    init_db()

for routes in routers:
    app.include_router(routes.router)
