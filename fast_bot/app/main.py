from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.messages.router import messages_router

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), 'static')


app.include_router(messages_router)
