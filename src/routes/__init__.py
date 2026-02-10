from .oauth import router as oauth_router
from .emails import router as emails_router
from .classify import router as classify_router
from .home import router as home_router

__all__ = ["oauth_router", "emails_router", "classify_router", "home_router"]
