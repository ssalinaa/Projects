from typing import Dict

class RBACController:
    """
    Управлява достъпа до ресурси на базата на роли.
    Разделя административните от потребителските функции.
    """

    def __init__(self):
        # role_name -> list of permissions
        self._roles = {
            "ADMIN": ["create_vm", "delete_vm", "manage_billing", "view_all"],
            "DEVELOPER": ["create_vm", "restart_vm", "view_metrics"],
            "AUDITOR": ["view_all", "export_logs"]
        }
        self._user_roles: Dict[str, str] = {}

    def assign_role(self, username: str, role: str):
        if role in self._roles:
            self._user_roles[username] = role
            print(f"[RBAC] User {username} is now assigned to role {role}.")

    def has_permission(self, username: str, action: str) -> bool:
        """Проверява дали потребителят има право на конкретно действие."""
        role = self._user_roles.get(username)
        if not role: return False

        return action in self._roles[role]