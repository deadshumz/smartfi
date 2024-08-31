from pydantic import BaseModel, EmailStr, ConfigDict


class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
