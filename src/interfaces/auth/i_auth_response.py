from typing import Protocol

class IAuthResponse(Protocol):
    """Interface for auth response"""
    
    @property
    def access_token(self) -> str:
        """Access token"""
        ...
    
    @property
    def expires_in(self) -> int:
        """Token expiration time"""
        ...
    
    @property
    def refresh_token(self) -> str:
        """Refresh token"""
        ...
    
    @property
    def scope(self) -> str:
        """Token scope"""
        ...
    
    @property
    def token_type(self) -> str:
        """Token type"""
        ...
