import os
from enum import Enum

class DiskFormat(Enum):
    """Стандартни формати за виртуални дискови имиджи."""
    RAW = ".raw"
    VMDK = ".vmdk"  # VMware формат
    QCOW2 = ".qcow2"  # QEMU/KVM формат
    VHD = ".vhd"  # Hyper-V формат

class VirtualDiskDrive:
    """
    Представлява виртуален дисков ресурс.
    Управлява жизнения цикъл на дисковото пространство и файловия формат.
    """

    def __init__(self, label: str, capacity_gb: int, disk_format: DiskFormat = DiskFormat.QCOW2):
        self._label = label
        self._capacity_gb = capacity_gb
        self._format = disk_format

        # Реално заето пространство във виртуалния диск (Thin Provisioning)
        self._used_space_gb = 0.0
        self._is_encrypted = False
        self._mount_point = None

    @property
    def disk_info(self) -> str:
        """Връща описание на диска (Read-only property)."""
        encryption_status = "Encrypted" if self._is_encrypted else "Plain"
        return f"Disk: {self._label} | Format: {self._format.value} | Size: {self._capacity_gb}GB ({encryption_status})"

    def mount(self, path: str):
        """Симулира монтиране на диска към файловата система на VM."""
        if self._used_space_gb > self._capacity_gb:
            raise IOError("Disk corruption detected: used space exceeds capacity.")
        self._mount_point = path
        print(f"Disk {self._label} mounted at {path}")

    def write_data(self, size_gb: float) -> bool:
        """
        Симулира запис на данни.
        Демонстрира концепцията 'Thin Provisioning' - дискът расте само при нужда.
        """
        if self._used_space_gb + size_gb <= self._capacity_gb:
            self._used_space_gb += size_gb
            return True
        print(f"Error: No space left on device {self._label}.")
        return False

    def resize(self, new_size_gb: int):
        """Позволява разширяване на виртуалния диск (Hot-resize)."""
        if new_size_gb < self._capacity_gb:
            raise ValueError("Disk shrinking poses a risk of data loss!")

        old_size = self._capacity_gb
        self._capacity_gb = new_size_gb
        print(f"Disk resized from {old_size}GB to {new_size_gb}GB.")

    def enable_encryption(self):
        """Активира софтуерно криптиране на данните върху диска."""
        self._is_encrypted = True
        print(f"Security: Disk {self._label} is now AES-256 encrypted.")

    def get_utilization_percentage(self) -> float:
        """Изчислява процента на заетото дисково пространство."""
        return (self._used_space_gb / self._capacity_gb) * 100