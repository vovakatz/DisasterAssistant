import os

from authlib.integrations.starlette_client import OAuth, OAuthError

from app.core.config import settings

# Configure OAuth
oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid email profile",
        "redirect_uri": os.environ.get("REDIRECT_URI", "http://localhost:8000/auth/callback"),
    },
)