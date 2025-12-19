from core.virtual_unit_factory import VirtualUnitFactory
from providers.auto_scaler import AutoScaler
from providers.backup_manager import BackupManager
from providers.cloud_provider import CloudProvider
from providers.cloud_rest_api import CloudRestAPI
from providers.failover_manager import FailoverManager
from providers.infrastructure_as_code import InfrastructureAsCode
from providers.metrics_collector import MetricsCollector
from providers.notification_service import NotificationService, AlertLevel
from providers.security_manager import SecurityManager

class CloudOrchestrator:
    """
    Върховният контролер на виртуалната инфраструктура.
    Обединява всички подсистеми в единна, функционираща платформа.
    """

    def __init__(self, name: str):
        self.name = name

        # Инстанциране на основните подсистеми (Композиция)
        self.provider = CloudProvider("Global-Cloud", "eu-central-1")
        self.factory = VirtualUnitFactory()
        self.security = SecurityManager()
        self.metrics = MetricsCollector(self.provider)
        self.backup = BackupManager(self.provider)
        self.notifier = NotificationService()

        # Инстанциране на интелигентните двигатели
        self.iac = InfrastructureAsCode(self.factory, self.provider)
        self.autoscaler = AutoScaler(self.metrics, self.iac)
        self.failover = FailoverManager(self.provider)

        # Интерфейс
        self.api = CloudRestAPI(self.provider, self.security)

        print(f"--- {self.name} ORCHESTRATOR ONLINE ---")

    def run_system_cycle(self):
        """
        Симулира един работен цикъл на облака:
        Мониторинг -> Автоскалиране -> Failover -> Известия.
        """
        print(f"\n[SYSTEM CYCLE] Running health and metrics scan...")

        # 1. Събиране на данни
        self.metrics.collect_now()

        # 2. Проверка за повреди и самолекуване
        self.failover.check_health()

        # 3. Автоматично мащабиране въз основа на натоварването
        # (Използваме примерен празен шаблон за демонстрация)
        self.autoscaler.evaluate_and_scale('{"resources": []}')

        # 4. Проверка на критични аларми
        for uuid in self.provider._inventory._resources:
            if self.metrics.detect_anomalies(uuid):
                self.notifier.notify(
                    AlertLevel.CRITICAL,
                    f"Resource {uuid} is overheating!",
                    source="Monitor"
                )

    def get_platform_health_report(self):
        """Обобщен доклад за състоянието на целия облак."""
        provider_stats = self.provider.get_provider_status()
        backup_stats = self.backup.get_storage_usage()

        return (f"=== {self.name} HEALTH REPORT ===\n"
                f"{provider_stats}\n"
                f"Total Backup Storage: {backup_stats:.2f} GB\n"
                f"Security Events: {len(self.security._audit_log)}\n"
                f"Status: OPERATIONAL")