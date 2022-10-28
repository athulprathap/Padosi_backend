from pydantic import BaseModel, EmailStr
from  datetime import datetime
from typing import Optional
from pydantic.types import conint
from .user import UserOpt



# urgent_alert models
class urgent_alerts(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at = datetime

#The "createalert" class will automatically inherit the "Base" proprties and populate every field
class Createalert(urgent_alerts): 
    pass

