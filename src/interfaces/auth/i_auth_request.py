from typing import Protocol

class IAuthRequest(Protocol):
    """Interface for auth request"""
    
    @property
    def code(self) -> str:
        """Authorization code"""
        ...
    
    @property
    def client_id(self) -> str:
        """Client ID"""
        ...
    
    @property
    def client_secret(self) -> str:
        """Client secret"""
        ...
    
    @property
    def redirect_uri(self) -> str:
        """Redirect URI"""
        ...
