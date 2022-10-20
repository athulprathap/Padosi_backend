from app.notify.schema import UserDevicePayload, MessagePayload
from . import notify


async def register_device(user_device: UserDevicePayload):
    return await notify.save(user_device)


async def send_message(message: MessagePayload):
    return await notify.send(message)