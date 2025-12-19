import time
import uuid
from core.life_cycle_manager import ResourceState

class FailoverManager:
    """
    Управлява автоматичното възстановяване на виртуални ресурси.
    Гарантира непрекъсваемост на услугите (Business Continuity).
    """

    def __init__(self, cloud_provider: 'CloudProvider'):
        self._provider = cloud_provider
        self._restart_attempts: dict = {}  # UUID -> брой опити
        self._max_retries = 3
        self._recovery_log = []

    def check_health(self):
        """
        Проверява състоянието на всички ресурси в инвентара.
        Ако открие грешка, стартира процедура по възстановяване.
        """
        inventory = self._provider._inventory._resources

        for uuid, unit in inventory.items():
            if unit.current_state == ResourceState.ERROR:
                self._handle_failure(unit)
            elif unit.current_state == ResourceState.STOPPED:
                # В някои облаци STOPPED може да е нормално, тук симулираме проверка
                self._recovery_log.append(f"Notice: Unit {unit.name} is offline but stable.")

    def _handle_failure(self, unit: 'AbstractVirtualUnit'):
        """Вътрешна логика за рестартиране или миграция."""
        uuid = unit.unique_id
        count = self._restart_attempts.get(uuid, 0)

        if count < self._max_retries:
            self._restart_attempts[uuid] = count + 1
            print(f"[RECOVERY] Attempting to restart {unit.name} (Try {count + 1}/{self._max_retries})...")

            try:
                unit.reboot()
                if unit.current_state == ResourceState.RUNNING:
                    print(f"[RECOVERY] Unit {unit.name} recovered successfully.")
                    del self._restart_attempts[uuid]
            except Exception as e:
                print(f"[RECOVERY] Restart failed: {str(e)}")
        else:
            self._initiate_migration(unit)

    def _initiate_migration(self, unit: 'AbstractVirtualUnit'):
        """
        Ако рестартът не помага, мигрираме ресурса (Fencing & Migration).
        Това е критична стъпка при хардуерен дефект на хост възела.
        """
        print(f"[CRITICAL] Unit {unit.name} failed multiple times. Initiating Failover Migration...")
        new_host = f"host-{self._provider._region}-backup-node"

        unit.assign_to_host(new_host)
        unit.boot()

        self._recovery_log.append(f"FAILOVER: {unit.name} migrated to {new_host}")
        if uuid in self._restart_attempts:
            del self._restart_attempts[uuid]

    def get_recovery_report(self) -> str:
        """Връща списък с всички успешни и неуспешни възстановявания."""
        return "\n".join(self._recovery_log) if self._recovery_log else "No failover events recorded."