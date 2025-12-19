import math

class ResourceSpecification:
    """
    Управлява техническите спецификации на виртуалния ресурс.
    Този клас капсулира логиката по изчисление и валидация на хардуера.
    """

    def __init__(self, cpu_cores: int, ram_mb: int, storage_gb: int):
        # Проверка на минималните изисквания за виртуализация
        self.__min_cpu = 1
        self.__min_ram = 512
        self.__min_storage = 5

        # Задаване на параметрите чрез вътрешна валидация
        self._cpu_cores = self._validate_cpu(cpu_cores)
        self._ram_mb = self._validate_ram(ram_mb)
        self._storage_gb = self._validate_storage(storage_gb)

        # Архитектура (x86_64 е стандарт за повечето хипервайзори)
        self._architecture = "x86_64"
        self._overprovisioning_allowed = False

    def _validate_cpu(self, cores: int) -> int:
        """Гарантира, че броят ядра е положителен и е степен на двойката (добро правило)."""
        if cores < self.__min_cpu:
            raise ValueError(f"CPU cores cannot be less than {self.__min_cpu}.")
        return cores

    def _validate_ram(self, ram: int) -> int:
        """Проверява дали RAM паметта е достатъчна за виртуализация."""
        if ram < self.__min_ram:
            raise ValueError(f"RAM memory must be at least {self.__min_ram} MB.")
        return ram

    def _validate_storage(self, storage: int) -> int:
        """Валидира дисковото пространство."""
        if storage < self.__min_storage:
            raise ValueError(f"Disk space must be at least {self.__min_storage} GB.")
        return storage

    @property
    def total_ram_gb(self) -> float:
        """Превръща MB в GB за по-лесно четене."""
        return self._ram_mb / 1024.0

    def calculate_virtual_overhead(self) -> float:
        """
        Изчислява теоретичния овърхед на хипервайзора.
        """
        cpu_overhead = self._cpu_cores * 0.02  # 2% на ядро
        ram_overhead = self.total_ram_gb * 0.05  # 5% за управление на паметта
        return cpu_overhead + ram_overhead

    def enable_overprovisioning(self):
        """Позволява заделяне на повече ресурси, отколкото са налични физически."""
        self._overprovisioning_allowed = True
        print("ATTENTION: Overprovisioning is allowed. Performance degradation may occur.")

    def get_spec_summary(self) -> str:
        """Генерира техническо обобщение на хардуерния профил."""
        summary = (
            f"Hardware Profile ({self._architecture}):\n"
            f"- vCPUs: {self._cpu_cores}\n"
            f"- RAM: {self.total_ram_gb:.2f} GB\n"
            f"- Disk: {self._storage_gb} GB\n"
            f"- Overprovisioning: {'Enabled' if self._overprovisioning_allowed else 'Disabled'}"
        )
        return summary