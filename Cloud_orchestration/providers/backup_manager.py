import hashlib
import time
from datetime import datetime
from typing import Dict, List

class BackupManager:
    """
    Управлява жизнения цикъл на архивните копия (Backups).
    Осигурява интегритет на данните и възможност за възстановяване (DR).
    """

    def __init__(self, cloud_provider: 'CloudProvider', storage_tier: str = "S3_STANDARD"):
        self._provider = cloud_provider
        self._storage_tier = storage_tier
        # Речник за съхранение: {unit_uuid: [backup_metadata, ...]}
        self._backup_repository: Dict[str, List[Dict]] = {}
        self._retention_days = 30

    def create_backup(self, unit_id: str, backup_type: str = "INCREMENTAL"):
        """
        Създава копие на състоянието на виртуалната единица.
        Демонстрира интеграция със Snapshot функционалностите на хипервайзорите.
        """
        unit = self._provider._inventory.get_unit_by_id(unit_id)
        if not unit:
            print(f"[BACKUP ERROR] Unit {unit_id} not found.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_action(f"Starting {backup_type} backup for {unit.name}...")

        # Симулираме извличане на делта промените (Deltas)
        backup_size = unit.specs._disk_gb * (0.05 if backup_type == "INCREMENTAL" else 1.0)

        backup_entry = {
            "backup_id": f"bak-{int(time.time())}",
            "timestamp": timestamp,
            "type": backup_type,
            "size_gb": round(backup_size, 2),
            "status": "COMPLETED",
            "checksum": hashlib.md5(f"{unit_id}-{timestamp}".encode()).hexdigest()
        }

        if unit_id not in self._backup_repository:
            self._backup_repository[unit_id] = []

        self._backup_repository[unit_id].append(backup_entry)
        print(f"[BACKUP] Success: {backup_entry['backup_id']} saved to {self._storage_tier}.")

    def restore_unit(self, backup_id: str, target_unit_id: str):
        """Възстановява състоянието на машина от конкретен архив."""
        for unit_id, backups in self._backup_repository.items():
            for b in backups:
                if b["backup_id"] == backup_id:
                    print(f"[RESTORE] Reverting {target_unit_id} to state from {b['timestamp']}...")
                    time.sleep(0.5)
                    print("[RESTORE] Data integrity verified. Resource is back online.")
                    return True

        print("[RESTORE ERROR] Backup ID not found.")
        return False

    def log_action(self, message: str):
        print(f"[BACKUP-SVC] {message}")

    def get_storage_usage(self) -> float:
        """Изчислява общия обем на архивите в GB."""
        return sum(b["size_gb"] for backups in self._backup_repository.values() for b in backups)