from holowhoslive.config import Settings, get_settings
from holowhoslive.dependencies.database import engine
from holowhoslive.models import Base
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

from holowhoslive.api import channel_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user_router)
app.include_router(channel_router)


@app.get("/")
async def root(request: Request):
    return {
        'msg': "Holo Who's Live API",
        'docs': f'{request.url.scheme}://{request.url.hostname}:{request.url.port}/docs'
    }
