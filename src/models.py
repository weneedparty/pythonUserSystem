from __future__ import annotations
from datetime import datetime

from typing import Optional, Any
from pydantic import BaseModel

#
# general models
#

class User(BaseModel):
    id: Optional[int] = None
    email: str
    username: Optional[str] = None
    pictureid: Optional[str] = None

#
# models for restful api
#

class GeneralResponse(BaseModel):
    result: Optional[str] = None
    error: Optional[str] = None


class UserRegisterInput(BaseModel):
    email: str
    # deviceUUID: str

class UserRegisterOutput(GeneralResponse):
    result: Optional[str] = None


class UserRegisterConfirmInput(BaseModel):
    email: str
    random_string: str
    # deviceUUID: str

class JWTobject(BaseModel):
    jwt: str

class UserRegisterConfirmOutput(GeneralResponse):
    result: Optional[JWTobject] = None


class GetDataInput(BaseModel):
    jwt: str

class GetDataOutput(GeneralResponse):
    result: Optional[str] = None


class AuthJwtInput(BaseModel):
    jwt: str

class AuthJwtOutput(GeneralResponse):
    email: str

# class registerUserOutput(BaseModel):
#     user_id: Optional[int]
#     error: Optional[str]


# class LoginInput(BaseModel):
#     email: str
#     password: str


# class LoginOutput(BaseModel):
#     jwt: Optional[str]
#     error: Optional[str]

# class JWTBaseModel(BaseModel):
#     jwt: str


# class GetDataInput(JWTBaseModel):
#     data_type: int


# class GetDataOutput(BaseModel):
#     data: str
#     error: Optional[str]