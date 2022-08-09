from holowhoslive.config import get_settings
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import holowhoslive.api as routers

settings = get_settings()

app = FastAPI()

origins = [
    "https://www.holowhos.live",
]
if settings.dev:
    origins.append("http://localhost:8080")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(routers.group_router)
api_router.include_router(routers.channels_router)

app.include_router(api_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse('static/index.html')


register_tortoise(
    app,
    db_url=settings.database_url,
    modules={"models": ["holowhoslive.models"]},
)
