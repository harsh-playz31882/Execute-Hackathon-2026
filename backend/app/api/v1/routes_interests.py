from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.security import get_current_active_user
from ...db import crud, models, schemas
from ...db.database import get_db
from ...services.permissions import require_role


router = APIRouter()


@router.post(
    "/",
    response_model=schemas.TradeInterestOut,
    status_code=status.HTTP_201_CREATED,
)
def create_interest(
    interest_in: schemas.TradeInterestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    # Any authenticated user except the asset owner can express interest
    asset = crud.get_asset(db, asset_id=interest_in.asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    if asset.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot express interest in your own asset",
        )

    interest = crud.create_trade_interest(
        db,
        user_id=current_user.id,
        interest_in=interest_in,
    )
    return interest


@router.get(
    "/mine",
    response_model=List[schemas.TradeInterestOut],
)
def list_my_interests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    interests = crud.list_interests_by_user(db, user_id=current_user.id)
    return interests


@router.get(
    "/received",
    response_model=List[schemas.TradeInterestOut],
)
def list_received_interests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    # Only producers receive interests on their assets
    require_role(current_user, "producer")
    interests = crud.list_interests_received_for_producer(
        db,
        producer_id=current_user.id,
    )
    return interests


@router.patch(
    "/{interest_id}",
    response_model=schemas.TradeInterestOut,
)
def update_interest_status(
    interest_id: int,
    update_in: schemas.TradeInterestUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    interest = crud.get_trade_interest(db, interest_id=interest_id)
    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found",
        )

    # Only the producer who owns the asset can change status
    asset = crud.get_asset(db, asset_id=interest.asset_id)
    if not asset or asset.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to modify this interest",
        )

    if update_in.status not in {"pending", "accepted", "rejected"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status value",
        )

    updated = crud.update_trade_interest_status(
        db,
        db_interest=interest,
        status=update_in.status,
    )
    return updated


__all__ = ["router"]
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
