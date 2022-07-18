from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


class UserUpdate(BaseModel):
    fullname: str