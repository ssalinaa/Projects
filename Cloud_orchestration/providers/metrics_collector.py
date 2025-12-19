import time
import random
from typing import List, Dict

from core.life_cycle_manager import ResourceState

class MetricsCollector:
    """
    Система за събиране и анализ на телеметрични данни от виртуалните ресурси.
    Позволява вземането на решения за мащабиране (Scaling) въз основа на данни.
    """

    def __init__(self, provider: 'CloudProvider'):
        self._provider = provider
        # Структура: {uuid: [{"timestamp": t, "cpu": c, "ram": r}, ...]}
        self._history: Dict[str, List[Dict]] = {}
        self._collection_interval = 5  # секунди (симулирано)

    def collect_now(self):
        """Обхожда всички активни ресурси и записва текущото им натоварване."""
        inventory = self._provider._inventory._resources
        timestamp = time.time()

        for uuid, unit in inventory.items():
            if unit.current_state == ResourceState.RUNNING:
                # Симулираме реално натоварване с малко шум (random)
                current_metrics = {
                    "timestamp": timestamp,
                    "cpu_load": unit.get_utilization() * 100 + random.uniform(-2, 5),
                    "ram_usage_mb": unit.specs._ram_mb * random.uniform(0.1, 0.8),
                    "network_io_mbps": random.uniform(0, 100)
                }

                if uuid not in self._history:
                    self._history[uuid] = []

                self._history[uuid].append(current_metrics)

                # Пазим само последните 100 измервания, за да не препълним паметта
                if len(self._history[uuid]) > 100:
                    self._history[uuid].pop(0)

    def get_average_load(self, uuid: str, window: int = 5) -> float:
        """Изчислява средното натоварване на CPU за последните N измервания."""
        data = self._history.get(uuid, [])
        if not data:
            return 0.0

        last_n = data[-window:]
        avg_cpu = sum(d["cpu_load"] for d in last_n) / len(last_n)
        return round(avg_cpu, 2)

    def detect_anomalies(self, uuid: str) -> bool:
        """Засича дали ресурсът е претоварен (напр. над 90% CPU)."""
        avg = self.get_average_load(uuid)
        if avg > 90.0:
            print(f"[ALARM] Resource {uuid} is under heavy load: {avg}%")
            return True
        return False

    def get_resource_report(self, uuid: str) -> str:
        """Генерира текстов отчет за производителността на конкретна машина."""
        if uuid not in self._history:
            return "No data collected yet."

        last_val = self._history[uuid][-1]
        return (f"--- Metrics for {uuid} ---\n"
                f"CPU Load: {last_val['cpu_load']:.2f}%\n"
                f"RAM Usage: {last_val['ram_usage_mb']:.0f} MB\n"
                f"Net I/O: {last_val['network_io_mbps']:.1f} Mbps")