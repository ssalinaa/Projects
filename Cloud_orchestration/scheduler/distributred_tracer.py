import datetime
import random
from typing import Dict, List

class DistributedTracer:
    """
    Проследява жизнения цикъл на заявките през множество микроуслуги.
    Помага за откриване на 'тесни места' (bottlenecks).
    """
    def __init__(self):
        self._traces: Dict[str, List[str]] = {} # trace_id -> list of spans

    def start_trace(self) -> str:
        trace_id = f"tr-{random.getrandbits(32):08x}"
        self._traces[trace_id] = []
        return trace_id

    def add_span(self, trace_id: str, component_name: str, operation: str):
        """Добавя стъпка (span) към веригата на проследяване."""
        if trace_id in self._traces:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")
            self._traces[trace_id].append(f"[{timestamp}] {component_name}: {operation}")

    def get_trace_summary(self, trace_id: str):
        return " -> ".join(self._traces.get(trace_id, ["Trace not found"]))