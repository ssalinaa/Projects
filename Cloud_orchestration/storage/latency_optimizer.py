from typing import Dict

class LatencyOptimizer:
    """
    Интелигентен рутер, който минимизира закъснението за крайния потребител.
    Използва географски данни и текущо натоварване на мрежата.
    """

    def __init__(self):
        self._node_latencies: Dict[str, float] = {}  # node_id -> latency_ms

    def register_node(self, node_id: str, latency: float):
        self._node_latencies[node_id] = latency

    def get_best_node(self) -> str:
        """Връща възела с най-ниско закъснение."""
        if not self._node_latencies:
            return "Central_DC"

        best_node = min(self._node_latencies, key=self._node_latencies.get)
        print(f"[OPTIMIZER] Closest node for user: {best_node} ({self._node_latencies[best_node]}ms)")
        return best_node