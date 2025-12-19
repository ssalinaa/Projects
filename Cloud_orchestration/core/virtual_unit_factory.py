import datetime

from core.diagnostic_logger import DiagnosticLogger
from core.network_interface_card import NetworkInterfaceCard
from core.resource_specification import ResourceSpecification
from core.virtual_disk_drive import VirtualDiskDrive

class VirtualUnitFactory:
    """
    Фабрика за създаване на виртуални единици.
    Прилага шаблона 'Factory Method', за да капсулира сглобяването на
    всички компоненти (Hardware, Storage, Network, Logging).
    """

    def __init__(self, datacenter_region: str):
        self._region = datacenter_region
        self._created_count = 0
        self._creation_log = []

    def build_compute_unit(self,
                           unit_type: str,
                           name: str,
                           cpu: int,
                           ram: int,
                           disk_gb: int,
                           image: 'VirtualMachineImage') -> 'AbstractVirtualUnit':
        """
        Основен метод за производство на ресурси.
        Този метод координира работата на всички предходни 8 класа.
        """
        print(f"[FACTORY] Building new {unit_type} in region: {self._region}...")

        # 1. Създаване на хардуерни спецификации
        specs = ResourceSpecification(cpu, ram, disk_gb)

        # 2. Валидация на ресурсите спрямо системния имидж
        if not image.validate_specs(ram, disk_gb):
            raise ValueError(f"Incompatible hardware for image: {image.full_name}")

        # 3. Подготовка на периферията
        vnic = NetworkInterfaceCard(interface_id=f"eth0-{name}")
        vdisk = VirtualDiskDrive(label=f"root-disk-{name}", capacity_gb=disk_gb)
        logger = DiagnosticLogger(owner_name=name)

        # 4. Сглобяване
        self._created_count += 1
        self._creation_log.append(f"{datetime.now()}: Created {name} ({unit_type})")

        # Тук връщаме 'сглобения' обект
        print(f"[FACTORY] Successfully assembled unit: {name}")
        return None  # Връщаме None за момента, докато не дефинираме конкретните VM/Container класове

    def get_factory_stats(self) -> str:
        """Връща статистика за работата на фабриката."""
        return (f"Factory Region: {self._region}\n"
                f"Total Units Produced: {self._created_count}\n"
                f"Uptime: Running")

    def _internal_quality_check(self, unit: 'AbstractVirtualUnit') -> bool:
        """Симулира вътрешен контрол на качеството след сглобяване."""
        # Проверка дали всички компоненти са инициализирани правилно
        return unit.specs is not None and unit.unique_id is not None