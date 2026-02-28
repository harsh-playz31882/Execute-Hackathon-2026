from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...core.security import get_current_active_user
from ...db import crud, models, schemas
from ...db.database import get_db
from ...services.permissions import ensure_asset_owner, require_role


router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.AssetOut],
)
def list_energy_assets(
    asset_type: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    assets = crud.list_assets(db, asset_type=asset_type, location=location)
    return assets


@router.get(
    "/{asset_id}",
    response_model=schemas.AssetOut,
)
def get_energy_asset(
    asset_id: int,
    db: Session = Depends(get_db),
):
    asset = crud.get_asset(db, asset_id=asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    return asset


@router.post(
    "/",
    response_model=schemas.AssetOut,
    status_code=status.HTTP_201_CREATED,
)
def create_energy_asset(
    asset_in: schemas.AssetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    require_role(current_user, "producer")
    asset = crud.create_asset(db, owner_id=current_user.id, asset_in=asset_in)
    return asset


@router.put(
    "/{asset_id}",
    response_model=schemas.AssetOut,
)
def update_energy_asset(
    asset_id: int,
    asset_in: schemas.AssetUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    ensure_asset_owner(current_user, db_asset)
    updated = crud.update_asset(db, db_asset=db_asset, asset_in=asset_in)
    return updated


@router.get(
    "/owner/me",
    response_model=List[schemas.AssetOut],
)
def list_my_assets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    require_role(current_user, "producer")
    assets = crud.list_assets_by_owner(db, owner_id=current_user.id)
    return assets


__all__ = ["router"]

