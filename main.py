from fastapi import FastAPI
from controllers import file_controllers

app = FastAPI()

app.include_router(router=file_controllers.router)

@app.get("/health")
async def healthcheck():
    return {"status": "alive"}
