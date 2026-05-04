from os import getenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from controller import file_controller
from client import s3_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    s3_client.create_bucket(s3_client.BUCKET_NAME)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=file_controller.router)

@app.get("/health")
async def healthcheck():
    return {"status": "alive"}
