from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import file_controller
from dotenv import load_dotenv

def get_cors_origins() -> list[str]:
    origins = getenv("CORS_ORIGINS", "")
    return [origin.strip() for origin in origins.split(",") if origin.strip()]

load_dotenv()
app = FastAPI()

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
