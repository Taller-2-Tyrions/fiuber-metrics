from pydantic import BaseModel
from enum import Enum

class UserEvent(Enum):
    SIGNUP = "Signup"
    LOGIN = "Login"
    BLOCK = "Block"
    RESET = "Reset"

# class UserBase(BaseModel):
#     signup_federate: int
#     signup_user_pass: int