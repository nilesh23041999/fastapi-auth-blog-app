# File: schemas/user.py

from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str
    is_admin: bool = False  # Default to regular user