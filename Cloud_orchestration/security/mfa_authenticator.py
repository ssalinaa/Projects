import random
import secrets
from typing import Dict

class MFAAuthenticator:
    """
    Добавя втори слой на сигурност чрез еднократни кодове.
    """

    def __init__(self):
        self._user_secrets: Dict[str, str] = {}  # username -> secret_seed

    def setup_mfa(self, username: str):
        """Генерира таен ключ за потребителя."""
        secret = secrets.token_hex(16)
        self._user_secrets[username] = secret
        print(f"[MFA] Setup for {username}. Secret key: {secret} (Scan this QR!)")

    def verify_code(self, username: str, code: str) -> bool:
        """Проверява подадения код (симулация на TOTP)."""
        if username not in self._user_secrets: return True  # Ако не е настроен MFA

        # За симулацията приемаме '123456' като валиден тестов код
        is_valid = (code == "123456")
        print(f"[MFA] Verification for {username}: {'SUCCESS' if is_valid else 'FAILED'}")
        return is_valid