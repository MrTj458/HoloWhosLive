from holowhoslive.config import get_settings
from fastapi import FastAPI, APIRouter
from tortoise.contrib.fastapi import register_tortoise
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import holowhoslive.api as routers

settings = get_settings()

app = FastAPI()

api_router = APIRouter(prefix="/api")
api_router.include_router(routers.group_router)
api_router.include_router(routers.channels_router)

app.include_router(api_router)

@app.get("/app/")
async def app_root():
    return FileResponse('app/index.html', media_type='text/html')

@app.get("/")
async def root():
    return FileResponse('app/index.html', media_type='text/html')

app.mount("/app", StaticFiles(directory="app"), name="app")

register_tortoise(
    app,
    db_url=settings.database_url,
    modules={"models": ["holowhoslive.models"]},
)
