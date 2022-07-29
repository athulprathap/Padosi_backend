from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..database import get_db, Base
from ..import schema, utils


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # image = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
def create(request: schema.CreateUser, db: Session(get_db)):
    hashed_password = utils.hash(request.password)
    request.password = hashed_password
    
    newUser = User(**request.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser