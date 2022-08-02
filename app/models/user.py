from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..database import  Base , get_db
from typing import Dict
from ..pydantic_schemas.user import CreateUser


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # image = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

def create_user(user: CreateUser, db: Session,):
    newUser = User(username=user.username, email=user.email, password=user.password)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser


def singleUser(db: Session, id: int=0):
    
    single_user = db.query(User).filter(User.id == id).first()
    
    return single_user


def update_user(db: Session, id: int=0, values: Dict={}):
    
    updated = db.query(User).filter(User.id == id)
    updated.update(values)
    db.commit()
    
    return updated