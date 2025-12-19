from typing import Dict, Set

class MultiTenancyIsolation:
    """
    Осигурява строга изолация между различните клиенти (Tenants).
    Управлява достъпа до споделени ресурси като мрежи и сторидж.
    """

    def __init__(self):
        # tenant_id -> list of resources
        self._tenancy_map: Dict[str, Set[str]] = {}

    def register_resource(self, tenant_id: str, resource_id: str):
        """Прикрепя ресурс към конкретен клиент."""
        if tenant_id not in self._tenancy_map:
            self._tenancy_map[tenant_id] = set()
        self._tenancy_map[tenant_id].add(resource_id)

    def verify_access(self, tenant_id: str, resource_id: str) -> bool:
        """Проверява дали клиентът има право да достъпи дадения ресурс."""
        allowed = resource_id in self._tenancy_map.get(tenant_id, set())
        if not allowed:
            print(f"[SECURITY ALERT] Tenant {tenant_id} attempted illegal access to {resource_id}!")
        return allowed