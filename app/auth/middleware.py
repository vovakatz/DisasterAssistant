from fastapi import Request, status
from starlette.responses import RedirectResponse

from app.core.config import settings


# Admin route middleware
class AdminRouteMiddleware:
    """Middleware to protect admin routes."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # Create a request object to access session and URL
        request = Request(scope)
        path = request.url.path

        # Check if this is an admin route
        if path.startswith("/admin/"):
            # If user is not logged in, store current path and redirect to login
            if "user" not in request.session:
                request.session["next"] = str(request.url)
                return await self._redirect(scope, receive, send, "/login")

            # User is logged in, but we need to verify admin access
            try:
                user = request.session.get("user", {})
                email = user.get("email", "")

                # Check if user's email is directly in allowed list
                is_allowed = email in settings.ALLOWED_EMAILS

                # Check if user's domain is in allowed domains
                if not is_allowed and '@' in email:
                    domain = f"@{email.split('@')[1]}"
                    is_allowed = domain in settings.ALLOWED_DOMAINS

                if not is_allowed:
                    return await self._redirect(scope, receive, send, "/access-denied")
            except Exception:
                return await self._redirect(scope, receive, send, "/access-denied")

        # Continue processing the request
        return await self.app(scope, receive, send)

    async def _redirect(self, scope, receive, send, path):
        """Helper method to perform redirects from middleware"""
        response = RedirectResponse(path, status_code=status.HTTP_303_SEE_OTHER)
        await response(scope, receive, send)
        return