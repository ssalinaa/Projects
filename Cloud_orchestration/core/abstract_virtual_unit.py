from abc import ABC
import time

from core.base_identity import BaseIdentity
from core.life_cycle_manager import LifecycleManager, ResourceState

class AbstractVirtualUnit(BaseIdentity, LifecycleManager, ABC):
    """
    Основен агрегатор за виртуални ресурси.
    Обединява идентичност, жизнен цикъл и хардуерни спецификации.
    Следва принципа за отвореност/затвореност (Open/Closed Principle).
    """

    def __init__(self, name: str, specs: 'ResourceSpecification'):
        # Инициализираме идентичността
        BaseIdentity.__init__(self, name)
        # Инициализираме жизнения цикъл
        LifecycleManager.__init__(self)

        self._specs = specs

        # Общи метаданни за виртуализацията
        self._host_node = None  # Физическият сървър, на който "живее" единицата
        self._tags = {}  # Етикети за организиране (напр. {"env": "prod"})
        self._uptime_start = None

    @property
    def specs(self) -> 'ResourceSpecification':
        """Връща хардуерния профил на единицата."""
        return self._specs

    def assign_to_host(self, host_name: str):
        """
        Метод за разпределяне към физически възел.
        Във виртуализацията това се нарича 'Placement'.
        """
        if self.current_state != ResourceState.CREATED:
            raise RuntimeError("Cannot change the host of a resource that has already started.")
        self._host_node = host_name
        self.log_event(f"Residing on physical node: {host_name}")

    def add_tag(self, key: str, value: str):
        """Добавя метаданни за по-лесно управление на облака."""
        self._tags[key] = value

    def get_full_description(self) -> str:
        """
        Демонстрира как събираме данни от различни компоненти.
        """
        status_info = f"Status: {self.current_state.value}"
        hw_info = self._specs.get_spec_summary()
        return f"Virtual Unit: {self.name}\nUUID: {self.unique_id}\n{status_info}\n{hw_info}"

    def log_event(self, message: str):
        """Помощен метод за записване на събития в историята на обекта."""
        timestamp = time.strftime('%H:%M:%S')
        print(f"LOG [{self.name}] @ {timestamp}: {message}")

    def _trigger_boot_sequence(self):
        """Вътрешен метод за отчитане на времето при стартиране."""
        self._uptime_start = time.time()
        self._update_state(ResourceState.RUNNING)