import datetime
import hashlib

class AuditLogger:
    """
    Осигурява отчетност (Accountability).
    Записва всяка промяна в конфигурацията на облака.
    """

    def __init__(self):
        self._log_storage = []

    def log_action(self, user_id: str, action: str, resource_id: str, status: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "actor": user_id,
            "operation": action,
            "target": resource_id,
            "result": status,
            "event_hash": "" 
        }
        # Симулация на генериране на защитен хеш
        entry["event_hash"] = hashlib.sha256(str(entry).encode()).hexdigest()
        self._log_storage.append(entry)
        print(f"[AUDIT] {user_id} performed {action} on {resource_id} -> {status}")

    def get_logs_for_resource(self, resource_id: str):
        return [log for log in self._log_storage if log["target"] == resource_id]