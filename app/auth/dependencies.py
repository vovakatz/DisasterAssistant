from typing import Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings


# Authentication dependency
async def get_current_user(request: Request) -> Dict[str, Any]:
    """Get current user from session."""
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Admin access check dependency
async def verify_admin_access(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Verify user has admin access based on email/domain."""
    email = user.get("email", "")

    # Check if user's email is directly in allowed list
    if email in settings.ALLOWED_EMAILS:
        return user

    # Check if user's domain is in allowed domains
    domain = f"@{email.split('@')[1]}" if '@' in email else ""
    if domain and domain in settings.ALLOWED_DOMAINS:
        return user

    # Not authorized
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to access this resource",
    )