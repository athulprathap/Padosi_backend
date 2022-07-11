from fastapi import FastAPI
from utils.dbUtil import database

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="FastAPI (python)",
    description="FastAPI framework, high performance, <br>"
                "easy to learn, fast to code, ready for production",
    version="1.0",
    openapi_url="/openapi.json",
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
def hello_world():
    return {'message': 'Hello World'}
