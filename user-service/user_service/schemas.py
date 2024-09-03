from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    password_confirmation: str
    

class UserUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    password: str = None
    password_confirmation: str = None


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
