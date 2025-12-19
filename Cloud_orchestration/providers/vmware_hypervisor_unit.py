import time

from core.abstract_virtual_unit import AbstractVirtualUnit
from core.diagnostic_logger import LogLevel
from core.life_cycle_manager import ResourceState

class VMWareHypervisorUnit(AbstractVirtualUnit):
    """
    Конкретна имплементация на виртуална машина за VMWare среда.
    Този клас симулира Type 1 хипервайзор архитектура.
    """

    def __init__(self, name: str, specs: 'ResourceSpecification', esxi_host_ip: str):
        super().__init__(name, specs)

        self._esxi_host = esxi_host_ip
        self._vm_tools_version = "12.1.5"
        self._is_vm_tools_running = False

        # Специфични VMWare настройки (Advanced Configuration)
        self._vmx_config_path = f"/vmfs/volumes/datastore1/{name}/{name}.vmx"
        self._hardware_version = 19  # VMWare Hardware compatibility level

    def boot(self) -> bool:
        """
        Имплементация на зареждането (Клас 2).
        При пълната виртуализация имаме симулация на BIOS/UEFI.
        """
        self.log_event(f"Connecting to ESXi host at {self._esxi_host}...")
        self._update_state(ResourceState.INITIALIZING)

        # Симулация на VMWare Boot Sequence
        self.log_event(f"Loading VMX configuration from {self._vmx_config_path}")
        time.sleep(0.5)  # Симулираме време за заделяне на хардуерни ресурси

        self.log_event("Starting Virtual BIOS...")
        self.log_event("Performing Power-On Self-Test (POST)...")

        self._trigger_boot_sequence()
        self._is_vm_tools_running = True
        return True

    def shutdown(self, force: bool = False) -> None:
        """Безопасно изключване чрез комуникация с VM Tools."""
        if force:
            self.log_event("Hard Power-Off triggered (Immediate).", LogLevel.WARNING)
        else:
            self.log_event("Sending ACPI shutdown signal to Guest OS...")
            self._is_vm_tools_running = False
            time.sleep(0.2)

        self._update_state(ResourceState.STOPPED)

    def reboot(self) -> bool:
        """Рестартиране на виртуалната машина."""
        self.log_event("Initiating Guest Reboot...")
        self.shutdown()
        return self.boot()

    def vmotion_migrate(self, target_host_ip: str):
        """
        Специфична VMWare функционалност за 'жива' миграция (vMotion).
        Демонстрира как разширяваме базовия клас със специфични за домейна методи.
        """
        if self.current_state != ResourceState.RUNNING:
            raise RuntimeError("vMotion е възможен само за работещи машини.")

        self.log_event(f"Starting vMotion migration from {self._esxi_host} to {target_host_ip}")
        # Симулация на копиране на RAM паметта по мрежата
        self._esxi_host = target_host_ip
        self.log_event("Migration successful. VM is now running on the new host.")

    def get_utilization(self) -> float:
        """
        Изчислява натоварването, включително овърхеда на VMWare.
        Пълната виртуализация има по-висок овърхед от контейнерите.
        """
        base_load = self.specs.calculate_virtual_overhead()
        return base_load + 0.08  # Добавяме 8% фиксиран овърхед за ESXi Hypervisor