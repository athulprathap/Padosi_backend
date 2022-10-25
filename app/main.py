from fastapi import FastAPI

from app.pydantic_schemas.urgent_alerts import urgent_alerts
from .database import engine, Base
from .routes import user,post,auth,votes,otp,urgent_alerts



Base.metadata.create_all(bind=engine)

app = FastAPI()
 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)
app.include_router(otp.router)
app.include_router(urgent_alerts.router)




@app.get("/")
def root():
    return {"message": "Hello World"}