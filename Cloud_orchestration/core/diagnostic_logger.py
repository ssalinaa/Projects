import time
from enum import Enum

class LogLevel(Enum):
    """Нива на критичност на събитията."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class DiagnosticLogger:
    """
    Система за диагностика и запис на събития.
    Прилага принципа за единствена отговорност (SRP) - грижи се само за логовете.
    """

    def __init__(self, owner_name: str):
        self._owner_name = owner_name
        self._log_buffer = []
        self._is_verbose = True
        self._log_format = "[{timestamp}] [{owner}] [{level}] {message}"

    def _get_timestamp(self) -> str:
        """Помощен метод за генериране на точно време за лога."""
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        """
        Основен метод за записване на събитие.
        Капсулира процеса по форматиране и съхранение.
        """
        entry = self._log_format.format(
            timestamp=self._get_timestamp(),
            owner=self._owner_name.upper(),
            level=level.value,
            message=message
        )

        self._log_buffer.append(entry)

        if self._is_verbose:
            print(entry)

    def get_logs_by_level(self, level: LogLevel) -> list:
        """Филтрира логовете по ниво на критичност (полезно за диагностика)."""
        return [line for line in self._log_buffer if f"[{level.value}]" in line]

    def clear_logs(self):
        """Изчиства буфера с логове, за да освободи памет."""
        count = len(self._log_buffer)
        self._log_buffer.clear()
        self.log(f"Log buffer cleared. {count} entries removed.", LogLevel.INFO)

    def export_to_text(self) -> str:
        """Експортира всички събрани данни като единен текст."""
        return "\n".join(self._log_buffer)

    @property
    def error_count(self) -> int:
        """Връща броя на грешките, открити до момента."""
        return len(self.get_logs_by_level(LogLevel.ERROR)) + \
            len(self.get_logs_by_level(LogLevel.CRITICAL))