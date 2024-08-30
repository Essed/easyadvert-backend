from pydantic import BaseModel, EmailStr
from typing import Optional


class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    subject_type_id: int

class UserCreate(TunedModel):
    name: str 
    email: str
    password_hash: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None
    subject_type_id: Optional[int] = None
    password_hash: Optional[str] = None

class AnnouncementBase(BaseModel):
    owner_id: int
    type_id: int
    platform_id: int
    format_id: int
    title: str
    description: Optional[str] = None
    link: Optional[str] = None
    image_url: Optional[str] = None

class AnnouncementCreate(TunedModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    type_id: int
    platform_id: int
    format_id: int
    price: float
    url_photo: str

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    url_photo: str
    price: float

class DeviceBase(BaseModel):
    account_id: int
    name: str
    last_ip: Optional[str] = None
    user_agent: Optional[str] = None

class DeviceCreate(TunedModel):
    name: str
    account_id: int
    last_ip: Optional[str] = None
    user_agent: Optional[str] = None

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    last_ip: Optional[str] = None
    user_agent: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


