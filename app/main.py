from fastapi import FastAPI
from app.api.routes import user,post,auth,votes,otp,comments,events
from app.api.database import engine, Base,database



Base.metadata.create_all(bind=engine)

app = FastAPI()
 
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
app.include_router(otp.router)
# app.include_router(notifications.router)
app.include_router(events.router)



@app.get("/")
def root():
    return {"message": "Hello World"}