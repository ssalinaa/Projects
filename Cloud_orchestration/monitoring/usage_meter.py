import time

class UsageMeter:
    """
    Отчита потреблението на ресурси за единица време.
    Трансформира техническите данни в бизнес метрики.
    """

    def __init__(self, unit_id: str):
        self.unit_id = unit_id
        self._start_time = time.time()
        self._total_cpu_hours = 0.0
        self._total_gb_hours = 0.0
        self._last_update = self._start_time

    def update_consumption(self, current_cpu_cores: int, current_ram_gb: float):
        """Метод, извикван периодично за натрупване на потреблението."""
        now = time.time()
        duration_hours = (now - self._last_update) / 3600

        self._total_cpu_hours += current_cpu_cores * duration_hours
        self._total_gb_hours += current_ram_gb * duration_hours
        self._last_update = now

    def get_accumulated_usage(self) -> dict:
        return {
            "unit_id": self.unit_id,
            "cpu_hours": round(self._total_cpu_hours, 4),
            "ram_gb_hours": round(self._total_gb_hours, 4),
            "uptime_seconds": int(time.time() - self._start_time)
        }