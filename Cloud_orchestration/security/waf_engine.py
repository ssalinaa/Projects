class WAFEngine:
    """
    Филтрира входящия уеб трафик за специфични заплахи.
    Работи на приложно ниво (Layer 7).
    """
    def __init__(self):
        self._malicious_patterns = [
            "SELECT * FROM", "DROP TABLE", "<script>", "OR 1=1"
        ]
        self._blocked_requests_count = 0

    def inspect_request(self, payload: str, source_ip: str) -> bool:
        """Сканира тялото на заявката за опасни сигнатури."""
        for pattern in self._malicious_patterns:
            if pattern.lower() in payload.lower():
                self._blocked_requests_count += 1
                print(f"[WAF ALERT] Blocked request from {source_ip} due to pattern: {pattern}")
                return False # Заявката е блокирана
        return True # Заявката е чиста