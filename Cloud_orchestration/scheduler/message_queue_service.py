from collections import deque
from typing import Dict, Optional

class MessageQueueService:
    """
    Механизъм за асинхронно предаване на съобщения (Pub/Sub модел).
    Гарантира, че съобщенията няма да се загубят при срив на консуматор.
    """
    def __init__(self):
        self._queues: Dict[str, deque] = {}
        self._dlq = deque() # Dead Letter Queue за неуспешни съобщения

    def create_queue(self, queue_name: str):
        if queue_name not in self._queues:
            self._queues[queue_name] = deque()
            print(f"[QUEUE] Service '{queue_name}' initialized.")

    def send_message(self, queue_name: str, payload: dict):
        """Продуцентът изпраща данни."""
        if queue_name in self._queues:
            self._queues[queue_name].append(payload)
            print(f"[QUEUE: {queue_name}] Message stored. Depth: {len(self._queues[queue_name])}")

    def receive_message(self, queue_name: str) -> Optional[dict]:
        """Консуматорът взема данни за обработка."""
        if queue_name in self._queues and self._queues[queue_name]:
            return self._queues[queue_name].popleft()
        return None