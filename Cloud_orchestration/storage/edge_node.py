from typing import Dict

class EdgeNode:
    """
    Представлява отдалечена изчислителна точка с ниска латентност.
    Управлява локални ресурси и синхронизира само важните данни с центъра.
    """
    def __init__(self, location: str, capacity_gb: int):
        self.location = location
        self.capacity = capacity_gb
        self._local_cache: Dict[str, bytes] = {}
        self._is_online = True

    def process_locally(self, data_packet: str):
        """Изпълнява бърза обработка на място."""
        if self._is_online:
            print(f"[EDGE: {self.location}] Processing packet locally to save latency.")
            return f"Processed at Edge: {data_packet[:10]}..."
        return None

    def sync_to_cloud(self, data: str):
        """Изпраща обобщена информация към централния облак (Batching)."""
        print(f"[EDGE: {self.location}] Syncing summary to Central DC...")