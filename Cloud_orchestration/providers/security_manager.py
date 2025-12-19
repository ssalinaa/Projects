import time
from enum import Enum
from typing import Set, Dict

class UserRole(Enum):
    """Дефинира нивата на достъп в облачната платформа."""
    ADMIN = "Admin"  # Пълни права
    OPERATOR = "Operator"  # Може да стартира/спира, но не и да трие
    VIEWER = "Viewer"  # Само четене на статус
    SECURITY = "Security"  # Само одит и логове

class SecurityManager:
    """
    Управлява сигурността и достъпа до ресурсите.
    Прилага принципа на 'Least Privilege' (Най-малки привилегии).
    """

    def __init__(self):
        self._user_roles: Dict[str, UserRole] = {}
        self._permissions: Dict[UserRole, Set[str]] = {
            UserRole.ADMIN: {"create", "start", "stop", "delete", "migrate", "view"},
            UserRole.OPERATOR: {"start", "stop", "view"},
            UserRole.VIEWER: {"view"},
            UserRole.SECURITY: {"view", "audit"}
        }
        self._audit_log = []

    def add_user(self, username: str, role: UserRole):
        """Регистрира нов потребител със специфична роля."""
        self._user_roles[username] = role
        self._log_security_event(f"User '{username}' assigned role {role.value}")

    def authorize(self, username: str, action: str) -> bool:
        """
        Проверява дали потребителят има право да извърши дадено действие.
        Това е сърцето на защитата на ресурсите.
        """
        user_role = self._user_roles.get(username)
        if not user_role:
            self._log_security_event(f"Unauthorized access attempt by unknown user: {username}", "WARNING")
            return False

        has_permission = action in self._permissions.get(user_role, set())

        status = "GRANTED" if has_permission else "DENIED"
        self._log_security_event(f"Access {status} for user '{username}' to perform '{action}'")

        return has_permission

    def _log_security_event(self, message: str, level: str = "INFO"):
        """Специфичен одит лог за събития по сигурността."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self._audit_log.append(f"[{timestamp}] [{level}] {message}")

    def get_audit_trail(self) -> str:
        """Връща пълната история на достъпа за целите на съответствието (compliance)."""
        return "\n".join(self._audit_log)