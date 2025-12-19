import time

class LiveMigrator:
    """
    Управлява преместването на активни виртуални машини между хостове.
    Използва 'Pre-copy' алгоритъм за минимизиране на прекъсването.
    """

    def __init__(self, network_bandwidth_gbps: int = 10):
        self._bandwidth = network_bandwidth_gbps
        self._migration_jobs = []

    def migrate(self, unit: 'AbstractVirtualUnit', source_host: str, target_host: str) -> bool:
        """Извършва жива миграция на единицата."""
        print(f"[MIGRATOR] Starting Live Migration for {unit.name}...")
        print(f"[MIGRATOR] {source_host} ----> {target_host}")

        # 1. Итеративно копиране на RAM страниците
        ram_size = unit.specs._ram_mb
        transfer_time = ram_size / (self._bandwidth * 125)

        for i in range(1, 4):
            print(f"[MIGRATOR] Memory Sync Iteration {i}...")
            time.sleep(0.2)

        # 2. 'The Stun' - Спираме източника за милисекунди
        print(f"[MIGRATOR] Suspending source {unit.name} briefly...")

        # 3. Прехвърляне на регистрите на процесора
        print(f"[MIGRATOR] Resuming on {target_host}...")
        unit.assign_to_host(target_host)

        print(f"[SUCCESS] {unit.name} is now running on {target_host} with zero downtime.")
        return True