from holowhoslive.config import get_settings
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

import holowhoslive.api as routers

settings = get_settings()

origins = [
    "https://www.holowhos.live",
]
if settings.dev:
    origins.append("http://localhost:8080")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(routers.yt_channel_router)
api_router.include_router(routers.group_router)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"msg": "Holo Who's Live API", "dev": settings.dev}
