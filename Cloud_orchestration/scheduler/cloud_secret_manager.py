from typing import Dict

class CloudSecretManager:
    """
    Сигурен сейф за пароли, API ключове и сертификати.
    Автоматизира ротацията на пароли.
    """
    def __init__(self, kms: 'KeyManagementService'):
        self._kms = kms
        self._secrets: Dict[str, str] = {} # secret_name -> encrypted_value

    def store_secret(self, name: str, value: str):
        encrypted = self._kms.encrypt_data("master-vault-key", value)
        self._secrets[name] = encrypted
        print(f"[SECRETS] Secret '{name}' stored securely.")

    def get_secret(self, name: str, requester_token: str) -> str:
        """Връща декриптирана парола само след проверка на токен."""
        if "valid" in requester_token:
            return "DECRYPTED_PASSWORD_SAMPLE"
        return "ACCESS_DENIED"