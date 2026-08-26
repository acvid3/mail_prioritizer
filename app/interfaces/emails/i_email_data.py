from typing import Protocol


class IEmailData(Protocol):
    @property
    def id(self) -> str:
        ...

    @property
    def thread_id(self) -> str:
        ...

    @property
    def subject(self) -> str:
        ...

    @property
    def from_email(self) -> str:
        ...

    @property
    def date(self) -> str:
        ...

    @property
    def snippet(self) -> str:
        ...

    @property
    def content(self) -> str:
        ...

    def to_dict(self) -> dict:
        ...
