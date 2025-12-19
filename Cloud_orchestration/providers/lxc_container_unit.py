import time

from core.diagnostic_logger import LogLevel
from core.life_cycle_manager import ResourceState
from providers.base_container_unit import BaseContainerUnit

class LXCContainerUnit(BaseContainerUnit):
    """
    Имплементация на LXC (Linux Containers).
    Представлява 'Системен контейнер', който имитира пълна ОС,
    но използва споделеното ядро на хоста.
    """

    def __init__(self, name: str, specs: 'ResourceSpecification', os_template: str):
        super().__init__(name, specs, image_tag=os_template)

        # LXC специфични атрибути
        self._config_path = f"/var/lib/lxc/{self.name}/config"
        self._is_autostart = False
        self._backend_storage = "dir"  # Може да бъде zfs, lvm, btrfs

        # Симулация на системните услуги вътре в LXC
        self._internal_services = ["systemd", "syslogd", "sshd", "network-manager"]

    def get_container_runtime(self) -> str:
        """Връща LXC библиотеката като runtime."""
        return "lxc-runtime (liblxc)"

    def boot(self) -> bool:
        """
        Стартиране на LXC контейнер.
        Тук се симулира стартирането на init процеса (PID 1).
        """
        self.log_event(f"LXC: Loading configuration from {self._config_path}...")
        self._update_state(ResourceState.INITIALIZING)

        # Прилагане на хардуерна изолация
        self.log_event("LXC: Setting up AppArmor/SELinux profiles for isolation.")
        self._apply_cgroup_limits()

        # Симулация на стартиране на системните процеси
        for service in self._internal_services:
            self.log_event(f"LXC Init: Starting internal service: {service}...")
            time.sleep(0.05)

        self._trigger_boot_sequence()
        self.log_event(f"LXC: System container '{self.name}' is fully operational.")
        return True

    def shutdown(self, force: bool = False) -> None:
        """Спиране на контейнера."""
        if force:
            self.log_event("LXC: Immediate poweroff (lxc-stop -kill).", LogLevel.WARNING)
        else:
            self.log_event("LXC: Sending SIGPWR to init process for clean shutdown.")
            time.sleep(0.2)

        self._update_state(ResourceState.STOPPED)

    def reboot(self) -> bool:
        """Рестартиране на системния контейнер."""
        self.log_event("LXC: Performing warm reboot...")
        self.shutdown()
        return self.boot()

    def set_autostart(self, enabled: bool):
        """Конфигурира дали контейнерът да стартира автоматично с хоста."""
        self._is_autostart = enabled
        self.log_event(f"Config: Autostart set to {enabled}")

    def get_container_stats(self) -> dict:
        """Връща справка за консумацията на системния контейнер."""
        return {
            "name": self.name,
            "runtime": self.get_container_runtime(),
            "services_running": len(self._internal_services),
            "storage_backend": self._backend_storage,
            "memory_usage_mb": self.specs._ram_mb * 0.4  # Симулация на заетост
        }