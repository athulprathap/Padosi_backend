from fastapi import FastAPI
from pydantic import BaseModel

from app.routes import votes
from .models import user, post
from .database import engine, Base
from .routes import user,post,auth
from .config import settings



Base.metadata.create_all(bind=engine)

app = FastAPI()
 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Hello World"}