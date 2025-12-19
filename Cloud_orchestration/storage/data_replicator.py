import time
from collections import deque

class DataReplicator:
    """
    Осигурява консистентност на данните в географски разпределени клъстери.
    Управлява конфликти при едновременен запис.
    """
    def __init__(self):
        self._replication_queue = deque()
        self._conflict_resolution_policy = "Last-Write-Wins"

    def replicate(self, data_payload: dict, target_region: str):
        """Изпраща пакет данни за синхронизация към отдалечен регион."""
        timestamp = time.time()
        replicated_data = {**data_payload, "rep_ts": timestamp}
        self._replication_queue.append((target_region, replicated_data))
        print(f"[REPLICATOR] Data queued for {target_region}. Queue size: {len(self._replication_queue)}")

    def process_queue(self):
        """Симулира фоновия процес на пренос на данни."""
        while self._replication_queue:
            target, data = self._replication_queue.popleft()
            print(f"[REPLICATOR] Successfully synced data to {target}.")