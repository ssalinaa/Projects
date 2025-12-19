import time
import uuid

from core.abstract_virtual_unit import AbstractVirtualUnit
from core.diagnostic_logger import LogLevel
from core.life_cycle_manager import ResourceState

class KVMHypervisorUnit(AbstractVirtualUnit):
    """
    Имплементация на KVM (Kernel-based Virtual Machine).
    Фокусира се върху интеграцията с Linux ядрото и Libvirt библиотеката.
    """

    def __init__(self, name: str, specs: 'ResourceSpecification', bridge_interface: str):
        super().__init__(name, specs)

        # KVM специфични параметри
        self._bridge = bridge_interface
        self._virt_type = "kvm"
        self._domain_xml_path = f"/etc/libvirt/qemu/{self.name}.xml"

        # Симулация на QEMU емулатор (KVM използва QEMU за периферна емулация)
        self._emulator_path = "/usr/bin/qemu-system-x86_64"
        self._machine_type = "pc-q35-6.2"

    def boot(self) -> bool:
        """
        Стартиране на KVM домейн.
        Прилага LSP, като запазва същата сигнатура, но променя вътрешната логика.
        """
        self.log_event(f"Parsing Libvirt XML configuration from {self._domain_xml_path}")
        self._update_state(ResourceState.INITIALIZING)

        # KVM специфика: Проверка за хардуерна поддръжка (VT-x / AMD-V)
        self.log_event("Checking CPU extensions: vmx/svm support detected.")

        # Симулация на стартиране на QEMU процес
        self.log_event(f"Executing: {self._emulator_path} -name {self.name} -machine {self._machine_type}")
        time.sleep(0.3)

        # Заделяне на памет чрез HugePages (оптимизация във виртуализацията)
        self.log_event("Allocating memory using HugePages for performance optimization.")

        self._trigger_boot_sequence()
        return True

    def shutdown(self, force: bool = False) -> None:
        """Изпращане на сигнал за спиране към KVM процеса."""
        if force:
            self.log_event("Sending SIGKILL to QEMU process (Destroying domain).", LogLevel.WARNING)
        else:
            self.log_event("Sending ACPI_SHUTDOWN via virsh...")
            time.sleep(0.1)

        self._update_state(ResourceState.STOPPED)

    def reboot(self) -> bool:
        """Рестартиране чрез virsh reboot."""
        self.log_event("Soft reboot initiated via libvirt daemon.")
        self.shutdown()
        return self.boot()

    def create_snapshot(self, snapshot_name: str):
        """
        Специфична функционалност за KVM: Създаване на снимка на състоянието.
        Демонстрира Open/Closed Principle - добавяме функционалност без да променяме ядрото.
        """
        timestamp = time.strftime("%Y%m%d-%H%M")
        self.log_event(f"Creating qcow2 external snapshot: {snapshot_name}_{timestamp}")
        self.log_event("Snapshot created and metadata synchronized.")

    def get_utilization(self) -> float:
        """
        KVM е известен с много ниския си овърхед, тъй като е част от ядрото.
        """
        base_load = self.specs.calculate_virtual_overhead()
        return base_load + 0.04  # Само 4% овърхед за KVM/QEMU