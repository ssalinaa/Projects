import time
from core.diagnostic_logger import LogLevel
from core.life_cycle_manager import ResourceState
from providers.base_container_unit import BaseContainerUnit

class DockerContainerUnit(BaseContainerUnit):
    """
    Имплементация на Docker контейнер.
    Фокусира се върху управлението на слоести файлови системи и Docker Runtime.
    """

    def __init__(self, name: str, specs: 'ResourceSpecification', image_tag: str, ports: dict):
        super().__init__(name, specs, image_tag)

        # Docker специфични атрибути
        self._port_mapping = ports
        self._storage_driver = "overlay2"
        self._is_privileged = False
        self._restart_policy = "always"

        # Симулация на слоевете на имиджа (Image Layers)
        self._image_layers = [
            "Layer 1: OS Base (Alpine)",
            "Layer 2: Runtime (Python 3.9)",
            "Layer 3: Application Code"
        ]

    def get_container_runtime(self) -> str:
        """Връща стандартния за Docker runtime."""
        return "containerd (via runc)"

    def boot(self) -> bool:
        """
        Стартиране на Docker контейнер.
        За разлика от VM, тук няма BIOS или зареждане на ядро.
        """
        self.log_event(f"Docker Engine: Pulling missing layers for {self._image_tag}...")
        self._update_state(ResourceState.INITIALIZING)

        # Симулация на OverlayFS монтиране
        for layer in self._image_layers:
            self.log_event(f"Mounting {layer} as Read-Only.")
        self.log_event("Creating Writable Layer (Container Layer).")

        # Прилагане на ресурси чрез cgroups
        self._apply_cgroup_limits()

        # Настройка на мрежата (Port Forwarding)
        for container_port, host_port in self._port_mapping.items():
            self.log_event(f"NAT: Mapping {self._host_node}:{host_port} -> {container_port}")

        time.sleep(0.1)  # Docker стартира почти мигновено
        self._trigger_boot_sequence()
        self.log_event(f"Docker container {self.name} is now UP and RUNNING.")
        return True

    def shutdown(self, force: bool = False) -> None:
        """Спиране на контейнера чрез изпращане на сигнали."""
        if force:
            self.log_event("Docker Engine: Sending SIGKILL (immediate stop).", LogLevel.WARNING)
        else:
            self.log_event("Docker Engine: Sending SIGTERM to PID 1...")
            # Docker изчаква 10 секунди по подразбиране преди SIGKILL
            time.sleep(0.1)

        self._update_state(ResourceState.STOPPED)

    def reboot(self) -> bool:
        """Docker рестарт - просто убива и стартира нов процес."""
        self.log_event(f"Docker Restart Policy: {self._restart_policy}")
        self.shutdown()
        return self.boot()

    def set_privileged_mode(self, status: bool):
        """
        Контролира дали контейнерът има директен достъп до хардуера на хоста.
        Важно за сигурността във виртуализацията.
        """
        self._is_privileged = status
        self.log_event(f"Security: Privileged mode set to {status}")

    def get_container_inspect(self) -> dict:
        """Симулира командата 'docker inspect'."""
        return {
            "Id": self._container_id,
            "Image": self._image_tag,
            "State": self.current_state.value,
            "Ports": self._port_mapping,
            "StorageDriver": self._storage_driver
        }