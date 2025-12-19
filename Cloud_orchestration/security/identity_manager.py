import hashlib
import secrets
from typing import Dict, Optional

class IdentityManager:
    """
    Управлява потребителските акаунти и автентикацията в облака.
    Поддържа сигурно съхранение на пароли чрез хеширане.
    """

    def __init__(self):
        self._users: Dict[str, dict] = {}  # username -> user_data
        self._active_sessions: Dict[str, str] = {}  # token -> username

    def create_user(self, username: str, password: str, email: str):
        salt = secrets.token_hex(8)
        hashed_pw = hashlib.sha256((password + salt).encode()).hexdigest()

        self._users[username] = {
            "password": hashed_pw,
            "salt": salt,
            "email": email,
            "status": "ACTIVE",
            "mfa_enabled": False
        }
        print(f"[IAM] User '{username}' created successfully.")

    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Проверява паролата и връща сесиен токен при успех."""
        user = self._users.get(username)
        if not user: return None

        check_hash = hashlib.sha256((password + user["salt"]).encode()).hexdigest()
        if check_hash == user["password"]:
            token = secrets.token_urlsafe(16)
            self._active_sessions[token] = username
            return token
        return None