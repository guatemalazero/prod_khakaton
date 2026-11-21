from typing import Protocol

class FuncServiceInterface(Protocol):
    @staticmethod
    def create_session_string() -> str: ...