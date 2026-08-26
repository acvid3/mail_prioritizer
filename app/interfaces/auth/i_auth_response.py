from typing import Protocol


class IAuthResponse(Protocol):
    @property
    def access_token(self) -> str:
        ...

    @property
    def expires_in(self) -> int:
        ...

    @property
    def refresh_token(self) -> str:
        ...

    @property
    def scope(self) -> str:
        ...

    @property
    def token_type(self) -> str:
        ...
