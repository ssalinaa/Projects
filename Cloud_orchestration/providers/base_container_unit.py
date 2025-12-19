from abc import ABC, abstractmethod
from core.abstract_virtual_unit import AbstractVirtualUnit

class BaseContainerUnit(AbstractVirtualUnit, ABC):
    """
    Абстрактна основа за контейнеризирани ресурси.
    Въвежда концепциите за споделено ядро (Shared Kernel) и изолация на ниво ОС.
    """

    def __init__(self, name: str, specs: 'ResourceSpecification', image_tag: str):
        super().__init__(name, specs)

        self._image_tag = image_tag
        self._container_id = self._generate_short_id()

        # Контейнерни специфики (Linux Namespaces)
        self._namespaces = {
            "mnt": True,  # Mount namespace
            "pid": True,  # Process ID isolation
            "net": True,  # Network stack isolation
            "uts": True  # Hostname isolation
        }

        # Специфики на ресурсите (Control Groups - cgroups)
        self._cpu_shares = specs._cpu_cores * 1024
        self._memory_limit_bytes = specs._ram_mb * 1024 * 1024

    def _generate_short_id(self) -> str:
        """Генерира кратък 12-символен идентификатор, типичен за среди като Docker."""
        import hashlib
        return hashlib.sha256(self.name.encode()).hexdigest()[:12]

    @abstractmethod
    def get_container_runtime(self) -> str:
        """Връща името на runtime средата (напр. runc, crun)."""
        pass

    def get_isolation_report(self) -> str:
        """Доклад за активните механизми за изолация."""
        active_ns = [ns for ns, active in self._namespaces.items() if active]
        return (f"Container: {self._container_id}\n"
                f"Active Namespaces: {', '.join(active_ns)}\n"
                f"CGroup Memory Limit: {self._memory_limit_bytes} bytes")

    def _apply_cgroup_limits(self):
        """
        Симулира записване на лимити в /sys/fs/cgroup.
        Това е начинът, по който контейнерите ограничават ресурсите си.
        """
        self.log_event(f"Applying CPU shares: {self._cpu_shares}")
        self.log_event(f"Setting memory.limit_in_bytes to {self._memory_limit_bytes}")

    def get_full_description(self) -> str:
        """Разширява описанието от Клас 4 със специфики за контейнера."""
        base_desc = super().get_full_description()
        return f"{base_desc}\nContainer ID: {self._container_id}\nImage: {self._image_tag}"

    def get_utilization(self) -> float:
        """
        Контейнерите имат пренебрежим овърхед (близо до 0),
        защото не емулират хардуер и не стартират нов кернел.
        """
        return 0.01