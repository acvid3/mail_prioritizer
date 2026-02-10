from typing import Protocol

class IEmailData(Protocol):
    """Interface for email data"""
    
    @property
    def id(self) -> str:
        """Email ID"""
        ...
    
    @property
    def thread_id(self) -> str:
        """Thread ID"""
        ...
    
    @property
    def subject(self) -> str:
        """Email subject"""
        ...
    
    @property
    def from_email(self) -> str:
        """Sender email"""
        ...
    
    @property
    def date(self) -> str:
        """Email date"""
        ...
    
    @property
    def snippet(self) -> str:
        """Email snippet"""
        ...
    
    @property
    def content(self) -> str:
        """Email content"""
        ...
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        ...
