import base64
import os
import time
from typing import Dict

class KeyManagementService:
    """
    Управлява жизнения цикъл на криптиращите ключове (КМS).
    Поддържа Master Keys и генериране на Data Encryption Keys (DEKs).
    """

    def __init__(self):
        self._master_keys: Dict[str, bytes] = {}
        self._key_audit_log = []

    def create_master_key(self, key_id: str):
        """Генерира нов главен ключ (AES-256 симулация)."""
        self._master_keys[key_id] = os.urandom(32)
        self._log_event(f"Master Key {key_id} created.")

    def encrypt_data(self, key_id: str, plaintext: str) -> str:
        """Симулира криптиране на данни с главен ключ."""
        if key_id not in self._master_keys:
            raise ValueError("Key not found")

        # Опростена симулация на криптиране чрез XOR и Base64
        key = self._master_keys[key_id]
        encoded = base64.b64encode(plaintext.encode()).decode()
        self._log_event(f"Data encrypted with key {key_id}")
        return f"ENC:{key_id}:{encoded[::-1]}"  # Обърнат стринг като симулация на шифър

    def _log_event(self, msg: str):
        self._key_audit_log.append(f"[{time.ctime()}] {msg}")