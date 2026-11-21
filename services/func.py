import secrets

class Func:

    @staticmethod
    def create_session_string() -> str:
        return secrets.token_urlsafe(16)