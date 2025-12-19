import time
from typing import List, Dict

class LogAggregator:
    """
    Централизирана система за събиране и анализ на логове.
    Позволява откриване на аномалии в реално време.
    """

    def __init__(self):
        self._central_store: List[dict] = []
        self._error_counters: Dict[str, int] = {}

    def ingest_log(self, source_id: str, message: str, level: str = "INFO"):
        """Приема лог запис от отдалечен ресурс."""
        entry = {
            "timestamp": time.time(),
            "source": source_id,
            "msg": message,
            "level": level
        }
        self._central_store.append(entry)

        if level == "ERROR":
            self._error_counters[source_id] = self._error_counters.get(source_id, 0) + 1
            if self._error_counters[source_id] > 5:
                print(f"[AGGREGATOR ALERT] Excessive errors detected in {source_id}!")

    def search(self, keyword: str):
        """Бързо филтриране на съобщения."""
        return [entry for entry in self._central_store if keyword in entry["msg"]]