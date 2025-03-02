from typing import Dict, Any

from fastapi import APIRouter

from app.auth import oauth
from app.auth.dependencies import verify_admin_access
from app.core.config import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.responses import RedirectResponse
from fastapi import Request, status, Depends
from authlib.integrations.starlette_client import OAuthError

auth_router = APIRouter()

@auth_router.get("/login")
async def login(request: Request):
    """Initiate Google OAuth login flow."""
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@auth_router.get("/auth/callback")
async def auth_callback(request: Request):
    """Handle OAuth callback and validate user."""
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")

        if not user_info:
            # If userinfo is not in token, get it from ID token
            id_info = id_token.verify_oauth2_token(
                token["id_token"], requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            user_info = id_info

        # Store user info in session
        request.session["user"] = {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
        }

        # Redirect to the page the user was trying to access, or home
        return RedirectResponse(
            url=request.session.get("next", "/"),
            status_code=status.HTTP_303_SEE_OTHER
        )
    except OAuthError as e:
        return {"error": str(e)}


@auth_router.get("/logout")
async def logout(request: Request):
    """Clear session and log out."""
    # request.session.pop("user", None)
    request.session.clear()
    return RedirectResponse(url="/")


# Access denied page
@auth_router.get("/access-denied")
async def access_denied():
    """Show access denied message."""
    return {"error": "Access Denied", "message": "You don't have permission to access this resource"}


# Example of a protected admin route using dependency
@auth_router.get("/admin/dashboard")
async def admin_dashboard(user: Dict[str, Any] = Depends(verify_admin_access)):
    """
    Admin dashboard endpoint.

    This route is double-protected:
    1. By the middleware checking all /admin/* routes
    2. By the verify_admin_access dependency
    """
    return {
        "message": "Welcome to the admin dashboard!",
        "user": user,
    }
