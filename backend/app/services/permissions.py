from fastapi import HTTPException, status

from ..db import models


def require_role(user: models.User, *allowed_roles: str) -> None:
    """
    Ensure the user has one of the allowed roles.
    """
    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


def ensure_asset_owner(user: models.User, asset: models.EnergyAsset) -> None:
    """
    Ensure the current user is the owner of the given asset.
    """
    if asset.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this asset",
        )


__all__ = ["require_role", "ensure_asset_owner"]
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
