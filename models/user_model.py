from pydantic import BaseModel
from enum import Enum
from typing import Any

class status_choice(str, Enum):
    Success = "Success"
    Error = "Error"

class dataResponse(BaseModel):
    Status : status_choice
    Message : Any

class createUserModel(BaseModel):
    username : str
    password : str
    email : str

class loginUserModel(BaseModel):
    identity : str
    password : str

