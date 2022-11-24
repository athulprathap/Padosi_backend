from fastapi import APIRouter

from ..schema import UserDevice, UserDevicePayload, Response, MessagePayload
from .. import utils

router = APIRouter(tags = ['notifications'])


@router.post("/v1/register", response_model=UserDevice, status_code=201)
async def register(payload: UserDevicePayload):
    return await utils.register_device(payload)


@router.post("/v1/message", response_model=Response, status_code=201)
async def send_message(payload: MessagePayload):
    return await utils.send_message(payload)
