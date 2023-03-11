from typing import Union
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    email: str
    full_name: str
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
