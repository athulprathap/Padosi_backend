from fastapi import FastAPI
from app.api.routes import user,post,auth,votes,comments,events,search,admin,profiles,imagesupload,notifications,urgentalerts
from app.api.database import engine, Base,database
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://admin.padosii.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
@app.on_event("startup")  # datbase connection
async def startup():
    await database.connect()


@app.on_event("shutdown")  # database disconnect
async def shutdown():
    await database.disconnect()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)
app.include_router(comments.router)
# app.include_router(otp.router)
app.include_router(notifications.router)
app.include_router(events.router)
app.include_router(search.router)
app.include_router(admin.router)
app.include_router(profiles.router)
app.include_router(imagesupload.router)
app.include_router(urgentalerts.router)

@app.get("/")
def root():
    return {"message": "Hello World"}