from abc import ABC, abstractmethod
from enum import Enum
import time

class ResourceState(Enum):
    """Дефинира всички възможни състояния на един виртуален ресурс."""
    CREATED = "Created"
    INITIALIZING = "Initializing"
    RUNNING = "Running"
    PAUSED = "Paused"
    STOPPED = "Stopped"
    TERMINATED = "Terminated"
    ERROR = "Error"

class LifecycleManager(ABC):
    """
    Абстрактен клас, който дефинира протокола за управление на жизнения цикъл.
    """

    def __init__(self):
        self._current_state = ResourceState.CREATED
        self._last_state_change = time.time()
        self._state_history = []

    @property
    def current_state(self) -> ResourceState:
        """Връща текущото състояние на ресурса."""
        return self._current_state

    def _update_state(self, new_state: ResourceState):
        """
        Вътрешен метод за смяна на състоянието с водене на история.
        Това гарантира капсулация на логиката по превключване.
        """
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        transition_msg = f"{timestamp}: Transition from {self._current_state.value} to {new_state.value}"

        self._state_history.append(transition_msg)
        self._current_state = new_state
        self._last_state_change = time.time()
        print(transition_msg)

    @abstractmethod
    def boot(self) -> bool:
        """Метод за първоначално стартиране и зареждане на операционна система/имидж."""
        pass

    @abstractmethod
    def shutdown(self, force: bool = False) -> None:
        """
        Метод за безопасно или принудително спиране.
        :param force: Ако е True, спира ресурса незабавно (hard power off).
        """
        pass

    @abstractmethod
    def reboot(self) -> bool:
        """Рестартиране на ресурса."""
        pass

    def get_uptime_seconds(self) -> float:
        """Изчислява колко време е минало от последната промяна на състоянието."""
        if self._current_state == ResourceState.RUNNING:
            return time.time() - self._last_state_change
        return 0.0

    def get_state_report(self) -> str:
        """Генерира текстов доклад за историята на състоянията."""
        header = f"--- State History Report ---"
        body = "\n".join(self._state_history)
        return f"{header}\n{body}\nTotal Transitions: {len(self._state_history)}"