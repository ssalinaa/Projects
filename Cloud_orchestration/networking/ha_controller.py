from typing import Dict
from core.life_cycle_manager import ResourceState
from providers.notification_service import AlertLevel

class HAController:
    """
    Контролер за висока наличност.
    Следи за състоянието на физическите хостове и рестартира ресурси при авария.
    """

    def __init__(self, provider: 'CloudProvider', notifier: 'NotificationService'):
        self._provider = provider
        self._notifier = notifier
        self._monitored_hosts: Dict[str, bool] = {}  # host_id -> is_alive

    def monitor_heartbeat(self, host_id: str, is_responding: bool):
        """Регистрира сигнал от физически хост."""
        self._monitored_hosts[host_id] = is_responding

        if not is_responding:
            self._handle_host_failure(host_id)

    def _handle_host_failure(self, failed_host_id: str):
        """Процедура по спасяване на виртуалните машини."""
        self._notifier.notify(AlertLevel.CRITICAL, f"Host {failed_host_id} has FAILED!", "HA-Manager")

        # 1. Идентифицираме кои машини са били на този хост
        failed_vms = self._provider._inventory.get_vms_on_host(failed_host_id)

        # 2. Намираме нови хостове с капацитет
        for vm in failed_vms:
            new_host = self._provider._inventory.find_spare_capacity(vm.specs)
            if new_host:
                print(f"[HA] Restarting {vm.name} on {new_host.name}...")
                vm.current_state = ResourceState.BOOTING
                vm.assign_to_host(new_host.name)
            else:
                print(f"[HA ERROR] No capacity to restart {vm.name}!")