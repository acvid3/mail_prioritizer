from typing import Protocol


class IAuthRequest(Protocol):
    @property
    def code(self) -> str:
        ...

    @property
    def client_id(self) -> str:
        ...

    @property
    def client_secret(self) -> str:
        ...

    @property
    def redirect_uri(self) -> str:
        ...
