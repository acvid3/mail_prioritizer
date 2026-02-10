from typing import Protocol

class IEmailService(Protocol):
    """Interface for email service"""
    
    def get_messages_list(self, headers: dict, max_results: int = 10) -> dict:
        """Get list of messages"""
        ...
    
    def get_message_content(self, message_id: str, headers: dict) -> str:
        """Get full content of a message"""
        ...
