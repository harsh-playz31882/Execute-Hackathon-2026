from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # e.g. "producer", "consumer", "investor"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    assets = relationship(
        "EnergyAsset",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    trade_interests = relationship(
        "TradeInterest",
        back_populates="interested_user",
        cascade="all, delete-orphan",
    )


class EnergyAsset(Base):
    __tablename__ = "energy_assets"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    asset_type = Column(String, nullable=False)  # solar, biogas, wind
    capacity_kw = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="active", nullable=False)  # active / inactive
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="assets")
    interests = relationship(
        "TradeInterest",
        back_populates="asset",
        cascade="all, delete-orphan",
    )


class TradeInterest(Base):
    __tablename__ = "trade_interests"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("energy_assets.id"), nullable=False, index=True)
    interested_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    message = Column(Text, nullable=True)
    status = Column(
        String,
        default="pending",  # pending / accepted / rejected
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    asset = relationship("EnergyAsset", back_populates="interests")
    interested_user = relationship("User", back_populates="trade_interests")


__all__ = [
    "User",
    "EnergyAsset",
    "TradeInterest",
]

