from pydantic import BaseModel

class UserList(BaseModel):
    email: str
    fullname: str


class UserCreate(UserList):
    password: str
