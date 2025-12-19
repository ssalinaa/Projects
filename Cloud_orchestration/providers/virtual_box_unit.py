import time

from core.abstract_virtual_unit import AbstractVirtualUnit
from core.diagnostic_logger import LogLevel
from core.life_cycle_manager import ResourceState

class VirtualBoxUnit(AbstractVirtualUnit):
    """
    Имплементация на Type-2 хипервайзор (VirtualBox).
    Характерното тук е, че виртуализацията разчита на ресурси,
    предоставени от хост операционната система.
    """

    def __init__(self, name: str, specs: 'ResourceSpecification', gui_mode: str = "headless"):
        super().__init__(name, specs)

        # VirtualBox специфични атрибути
        self._gui_mode = gui_mode  # 'gui', 'seamless' или 'headless'
        self._guest_additions_version = "7.0.12"
        self._vbox_manage_path = "VBoxManage"

        # Периферни компоненти, типични за десктоп виртуализация
        self._shared_folders = []
        self._is_3d_acceleration_enabled = False
        self._video_memory_mb = 128

    def boot(self) -> bool:
        """
        Стартиране на VirtualBox инстанция.
        Прилага LSP, като имплементира процеса през 'VBoxManage startvm'.
        """
        self.log_event(f"Initializing VBox process in {self._gui_mode} mode...")
        self._update_state(ResourceState.INITIALIZING)

        # Проверка за специфичния овърхед на Type-2 виртуализацията
        self.log_event("Verifying Host OS resource availability (RAM/Swap)...")

        # Симулация на стартиране на виртуалната машина
        self.log_event(f"Executing: {self._vbox_manage_path} startvm {self.name}")
        time.sleep(0.4)

        self.log_event(f"Loading Guest Additions v{self._guest_additions_version}...")

        self._trigger_boot_sequence()
        return True

    def shutdown(self, force: bool = False) -> None:
        """Изпращане на команда за спиране към VirtualBox."""
        if force:
            self.log_event("Action: VBoxManage controlvm poweroff (Hard stop).", LogLevel.WARNING)
        else:
            self.log_event("Action: VBoxManage controlvm acpipowerbutton (Graceful).")
            time.sleep(0.2)

        self._update_state(ResourceState.STOPPED)

    def reboot(self) -> bool:
        """Стандартен рестарт чрез управление на процеса на хоста."""
        self.log_event("Restarting VBox instance...")
        self.shutdown()
        return self.boot()

    def add_shared_folder(self, host_path: str, guest_mount_name: str):
        """
        Специфична функция за Type-2 виртуализация: Споделени папки.
        Това е ключово за пренасяне на данни между хоста и госта.
        """
        config = {"host": host_path, "mount": guest_mount_name}
        self._shared_folders.append(config)
        self.log_event(f"Shared folder configured: {host_path} -> {guest_mount_name}")

    def toggle_3d_acceleration(self, status: bool):
        """Промяна на графичните настройки - типично за десктоп хипервайзори."""
        if self.current_state == ResourceState.RUNNING:
            raise RuntimeError("Графичните настройки не могат да се променят 'в движение'.")

        self._is_3d_acceleration_enabled = status
        self.log_event(f"3D Acceleration set to: {status}")

    def get_utilization(self) -> float:
        """
        Type-2 хипервайзорите имат най-висок овърхед, защото
        трафикът минава през хост операционната система.
        """
        base_load = self.specs.calculate_virtual_overhead()
        # Добавяме 12% овърхед заради Хост ОС контекстните превключвания
        return base_load + 0.12