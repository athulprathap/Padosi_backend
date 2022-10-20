from fastapi import APIRouter

from app.notify.schema import UserDevice, UserDevicePayload, Response, MessagePayload
from .. import nutils

router = APIRouter()


@router.post("/v1/register", response_model=UserDevice, status_code=201)
async def register(payload: UserDevicePayload):
    return await nutils.register_device(payload)


@router.post("/v1/message", response_model=Response, status_code=201)
async def send_message(payload: MessagePayload):
    return await nutils.send_message(payload)
