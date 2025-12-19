import time

from core.life_cycle_manager import ResourceState
from providers.base_container_unit import BaseContainerUnit

class PodmanContainerUnit(BaseContainerUnit):
    """
    Имплементация на Podman контейнер.
    Фокусира се върху daemonless архитектура и rootless сигурност.
    """

    def __init__(self, name: str, specs: 'ResourceSpecification', image_tag: str):
        super().__init__(name, specs, image_tag)

        # Podman специфични атрибути
        self._is_rootless = True  # По подразбиране работи без root права
        self._pod_id = None  # Идентификатор на Pod, ако е част от такъв
        self._infra_container = False

        # Симулация на локален сторидж (Podman често ползва различни пътища от Docker)
        self._storage_path = f"~/.local/share/containers/storage/overlay/{self._container_id}"

    def get_container_runtime(self) -> str:
        """Връща runtime средата, която Podman използва (обикновено crun)."""
        return "crun (low-latency C runtime)"

    def boot(self) -> bool:
        """
        Стартиране на Podman контейнер.
        Тук няма централен демон - процесът се стартира директно от потребителя.
        """
        self.log_event("Podman: Initializing container process (direct fork/exec)...")
        self._update_state(ResourceState.INITIALIZING)

        if self._is_rootless:
            self.log_event("Security: Running in ROOTLESS mode (User Namespace enabled).")
            # Симулация на UID/GID мапинг
            self.log_event("Mapping User ID 0 inside to UID 1000 outside.")

        # Прилагане на лимити
        self._apply_cgroup_limits()

        # Podman специфично: Регистрация в systemd (честа практика)
        self.log_event(f"Generating systemd unit file for {self.name}...")

        time.sleep(0.1)
        self._trigger_boot_sequence()
        return True

    def shutdown(self, force: bool = False) -> None:
        """Спиране на процеса."""
        if force:
            self.log_event("Podman: Sending SIGKILL to child process.")
        else:
            self.log_event("Podman: Graceful termination via SIGTERM.")

        self._update_state(ResourceState.STOPPED)

    def reboot(self) -> bool:
        """Рестарт на Podman контейнер."""
        self.log_event("Podman: Restarting process...")
        self.shutdown()
        return self.boot()

    def join_pod(self, pod_id: str):
        """
        Специфична функционалност за Podman: Групиране в Pod.
        Това позволява на контейнерите да споделят един и същ IP адрес (localhost).
        """
        self._pod_id = pod_id
        self.log_event(f"Network: Container joined Pod {pod_id}. Sharing Network Namespace.")

    def get_security_context(self) -> dict:
        """Връща информация за сигурността на контейнера."""
        return {
            "rootless": self._is_rootless,
            "runtime": self.get_container_runtime(),
            "pod_id": self._pod_id,
            "seccomp_profile": "default-enabled"
        }