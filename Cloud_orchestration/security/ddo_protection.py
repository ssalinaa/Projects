from typing import Dict

class DDoSProtection:
    """
    Защитава облачната инфраструктура от обемни атаки.
    Имплементира механизми за автоматично смекчаване (Mitigation).
    """
    def __init__(self, rps_threshold: int = 1000):
        self._threshold = rps_threshold
        self._traffic_stats: Dict[str, int] = {} # IP -> requests_per_second

    def process_packet(self, source_ip: str) -> bool:
        """Следи интензитета на трафика от всеки източник."""
        current_rps = self._traffic_stats.get(source_ip, 0) + 1
        self._traffic_stats[source_ip] = current_rps

        if current_rps > self._threshold:
            print(f"[DDoS SHIELD] Mitigation active for {source_ip} (RPS: {current_rps})")
            return False
        return True

    def reset_counters(self):
        """Извиква се всяка секунда за нулиране на статистиките."""
        self._traffic_stats.clear()