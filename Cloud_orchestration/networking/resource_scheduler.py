class ResourceScheduler:
    """
    Автоматизиран диспечер на ресурси (DRS).
    Следи баланса на натоварване в клъстера и инициира миграции.
    """

    def __init__(self, provider: 'CloudProvider', migrator: 'LiveMigrator'):
        self._provider = provider
        self._migrator = migrator
        self._threshold_percent = 75.0  # Праг на натоварване за реакция

    def rebalance_cluster(self):
        """Анализира всички хостове и решава дали е нужна миграция."""
        hosts = self._provider._inventory._hosts

        overloaded_hosts = [h for h in hosts if h.get_cpu_usage() > self._threshold_percent]
        underloaded_hosts = [h for h in hosts if h.get_cpu_usage() < 30.0]

        if overloaded_hosts and underloaded_hosts:
            target_host = underloaded_hosts[0]
            for source_host in overloaded_hosts:
                # Вземаме най-лакомата машина от натоварения хост
                victim_vm = source_host.get_most_demanding_vm()
                print(f"[DRS] Cluster imbalance detected! Moving {victim_vm.name} to {target_host.name}")
                self._migrator.migrate(victim_vm, source_host.name, target_host.name)

    def set_automation_level(self, level: str):
        """Нива: Manual (само съвет), Partially (само при старт), Fully (автоматично)."""
        print(f"[DRS] Automation level set to: {level}")