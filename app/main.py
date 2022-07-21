from fastapi import FastAPI
from pydantic import BaseModel
import models
from  database import engine, Base
from  routes import post, user, auth
from config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
