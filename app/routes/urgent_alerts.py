from fastapi import FastAPI, Response, requests, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from .. import oauth2
from .. import model,schema
from sqlalchemy import func
from ..database import get_db
from ..modules.users.userRepository import register_new, singleUser, updateUser
from ..pydantic_schemas.user import CreateUser, UserOpt,  User, UserUpdate
import os


router = APIRouter( tags = ['urgent_alerts'])

@router.get("/urgent-alerts")
async def get_all_urgent_alerts():
    pass

@router.post("/urgent-alerts")
async def create_new_urgent_alerts():
    pass

@router.get("/urgent-alerts/count")
async def get_number_of_urgent_alerts():
    pass

@router.get("/urgent-alerts/{id}")
async def find_urgent_alert_by_id():
    pass

@router.put("/urgent-alerts/{id}")
async def update_urgent_alert():
    pass

@router.delete("/urgent-alerts/{id}")
async def delete_urgent_alerts():
    pass

@router.get("/urgent-alerts/{id}/respond")
async def respond_to_urgent_alerts():
    pass