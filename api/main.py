from fastapi import FastAPI
from api.utils.dbUtil import database, engine, metadata
from api.users import router as user_router
from api.auth import router as auth_router
from api.otps import router as otp_router
from api.posts import router as post_router

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="FastAPI (python)",
    description="FastAPI framework, high performance, <br>"
                "easy to learn, fast to code, ready for production",
    version="1.0",
    openapi_url="/openapi.json",
)

@app.on_event("startup")  # datbase connection
async def startup():
    await database.connect()


@app.on_event("shutdown")  # database disconnect
async def shutdown():
    await database.disconnect()

app.include_router(auth_router.router, tags=["Auth"]) # router.post("/auth/register", ...)
app.include_router(user_router.router, tags=["Users"]) # router.post("/user/register", ...)
app.include_router(otp_router.router, tags=["OTPs"]) # router.post("/user/login", ...)
app.include_router(post_router.router, tags=["Posts"]) # router.post("/post/newpost", ...)




#@app.get('/')
#def hello_world():
#   return {'message': 'Hello World'}
