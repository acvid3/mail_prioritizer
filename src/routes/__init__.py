from .oauth import router as oauth_router
from .emails import router as emails_router
from .classify import router as classify_router
from .main import router as main_router

__all__ = ["oauth_router", "emails_router", "classify_router", "main_router"]
