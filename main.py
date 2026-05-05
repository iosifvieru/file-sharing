from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from controller import file_controller
from client import s3_client

def get_cors_origins() -> list[str]:
    origins = getenv("CORS_ORIGINS", "")
    return [origin.strip() for origin in origins.split(",") if origin.strip()]

@asynccontextmanager
async def lifespan(app: FastAPI):
    s3_client.create_bucket(s3_client.BUCKET_NAME)
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=file_controller.router)

@app.get("/health")
async def healthcheck():
    return {"status": "alive"}
