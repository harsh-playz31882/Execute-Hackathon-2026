from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models, schemas


# ---------
# Users
# ---------


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(
    db: Session,
    user_in: schemas.UserCreate,
    hashed_password: str,
) -> models.User:
    db_user = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=user_in.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------
# Energy Assets
# ---------


def create_asset(
    db: Session,
    owner_id: int,
    asset_in: schemas.AssetCreate,
) -> models.EnergyAsset:
    asset = models.EnergyAsset(
        owner_id=owner_id,
        asset_type=asset_in.asset_type,
        capacity_kw=asset_in.capacity_kw,
        location=asset_in.location,
        price_per_unit=asset_in.price_per_unit,
        description=asset_in.description,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def get_asset(db: Session, asset_id: int) -> Optional[models.EnergyAsset]:
    return db.query(models.EnergyAsset).filter(models.EnergyAsset.id == asset_id).first()


def list_assets(
    db: Session,
    asset_type: Optional[str] = None,
    location: Optional[str] = None,
) -> List[models.EnergyAsset]:
    query = db.query(models.EnergyAsset)
    filters = []
    if asset_type:
        filters.append(models.EnergyAsset.asset_type == asset_type)
    if location:
        filters.append(models.EnergyAsset.location == location)
    if filters:
        query = query.filter(and_(*filters))
    return query.all()


def list_assets_by_owner(
    db: Session,
    owner_id: int,
) -> List[models.EnergyAsset]:
    return (
        db.query(models.EnergyAsset)
        .filter(models.EnergyAsset.owner_id == owner_id)
        .all()
    )


def update_asset(
    db: Session,
    db_asset: models.EnergyAsset,
    asset_in: schemas.AssetUpdate,
) -> models.EnergyAsset:
    update_data = asset_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asset, field, value)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


# ---------
# Trade Interests
# ---------


def create_trade_interest(
    db: Session,
    user_id: int,
    interest_in: schemas.TradeInterestCreate,
) -> models.TradeInterest:
    interest = models.TradeInterest(
        asset_id=interest_in.asset_id,
        interested_user_id=user_id,
        message=interest_in.message,
    )
    db.add(interest)
    db.commit()
    db.refresh(interest)
    return interest


def get_trade_interest(
    db: Session,
    interest_id: int,
) -> Optional[models.TradeInterest]:
    return (
        db.query(models.TradeInterest)
        .filter(models.TradeInterest.id == interest_id)
        .first()
    )


def list_interests_by_user(
    db: Session,
    user_id: int,
) -> List[models.TradeInterest]:
    return (
        db.query(models.TradeInterest)
        .filter(models.TradeInterest.interested_user_id == user_id)
        .all()
    )


def list_interests_received_for_producer(
    db: Session,
    producer_id: int,
) -> List[models.TradeInterest]:
    return (
        db.query(models.TradeInterest)
        .join(models.EnergyAsset)
        .filter(models.EnergyAsset.owner_id == producer_id)
        .all()
    )


def update_trade_interest_status(
    db: Session,
    db_interest: models.TradeInterest,
    status: str,
) -> models.TradeInterest:
    db_interest.status = status
    db.add(db_interest)
    db.commit()
    db.refresh(db_interest)
    return db_interest


__all__ = [
    "get_user_by_id",
    "get_user_by_email",
    "create_user",
    "create_asset",
    "get_asset",
    "list_assets",
    "list_assets_by_owner",
    "update_asset",
    "create_trade_interest",
    "get_trade_interest",
    "list_interests_by_user",
    "list_interests_received_for_producer",
    "update_trade_interest_status",
]
