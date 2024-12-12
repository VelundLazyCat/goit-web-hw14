from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=2, max_length=20)
    email: str = Field(min_length=10, max_length=50)
    telephon_number: str = Field(min_length=7, max_length=12)
    birthday: date = Field()
    description: str = Field(max_length=250)


class ContactResponse(BaseModel):
    contact_id: int
    first_name: str
    last_name: str
    email: str
    telephon_number: str
    birthday: date
    description: str

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
