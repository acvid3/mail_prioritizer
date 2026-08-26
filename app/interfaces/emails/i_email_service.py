from typing import Protocol


class IEmailService(Protocol):
    def get_messages_list(self, headers: dict, max_results: int = 10) -> dict:
        ...

    def get_message_content(self, message_id: str, headers: dict) -> str:
        ...
