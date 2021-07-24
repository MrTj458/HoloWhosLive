from holowhoslive.dependencies.database import engine
from holowhoslive.models import Base
import holowhoslive.routers as routers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()


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

app.include_router(routers.user_router)
app.include_router(routers.youtube_router)


@app.get("/api")
async def root():
    return {"message": "Holo Who's Live API"}
