from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# ---------
# Auth / User
# ---------


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str  # "producer", "consumer", "investor"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ---------
# Energy Assets
# ---------


class AssetBase(BaseModel):
    asset_type: str
    capacity_kw: float
    location: str
    price_per_unit: float
    description: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    asset_type: Optional[str] = None
    capacity_kw: Optional[float] = None
    location: Optional[str] = None
    price_per_unit: Optional[float] = None
    description: Optional[str] = None
    status: Optional[str] = None


class AssetOut(AssetBase):
    id: int
    owner_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------
# Trade Interests
# ---------


class TradeInterestBase(BaseModel):
    asset_id: int
    message: Optional[str] = None


class TradeInterestCreate(TradeInterestBase):
    pass


class TradeInterestUpdate(BaseModel):
    status: str  # "pending", "accepted", "rejected"


class TradeInterestOut(BaseModel):
    id: int
    asset_id: int
    interested_user_id: int
    message: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


__all__ = [
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserOut",
    "Token",
    "TokenData",
    "AssetBase",
    "AssetCreate",
    "AssetUpdate",
    "AssetOut",
    "TradeInterestBase",
    "TradeInterestCreate",
    "TradeInterestUpdate",
    "TradeInterestOut",
]

