from holowhoslive.config import Settings, get_settings
from holowhoslive.dependencies.database import engine
from holowhoslive.models import Base
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware

import holowhoslive.api as routers

app = FastAPI()

origins = [
    'http://localhost:8080',
    'https://holowhoslive.netlify.app',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

api_router = APIRouter(prefix='/api')
api_router.include_router(routers.user_router)
api_router.include_router(routers.channel_router)

app.include_router(api_router)


@app.get("/")
async def root(request: Request):
    return {
        'msg': "Holo Who's Live API",
        'docs': f'{request.url.scheme}://{request.url.hostname}:{request.url.port}/docs'
    }
