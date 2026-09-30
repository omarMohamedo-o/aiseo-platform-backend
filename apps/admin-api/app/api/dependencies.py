"""Dependencies for FastAPI (AuthZ, DB, Services)."""

from __future__ import annotations

import uuid

from apps.admin_api.app.domain.admin_user import AdminRole, AdminUser
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Dummy token for MVP
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_admin(token: str = Depends(oauth2_scheme)) -> AdminUser:
    """Dependency to verify token and return the AdminUser.

    In MVP, we mock this by checking if the token is 'superadmin-token' or 'support-token'.
    """
    if token == "superadmin-token":
        return AdminUser(
            id=uuid.uuid4(),
            email="superadmin@geoplatform.io",
            role=AdminRole.SUPERADMIN,
        )
    elif token == "support-token":
        return AdminUser(
            id=uuid.uuid4(),
            email="support@geoplatform.io",
            role=AdminRole.SUPPORT,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid admin token",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def require_superadmin(admin: AdminUser = Depends(get_current_admin)) -> AdminUser:
    """Dependency that enforces SUPERADMIN role."""
    if not admin.can_manage_config():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires SUPERADMIN privileges",
        )
    return admin
