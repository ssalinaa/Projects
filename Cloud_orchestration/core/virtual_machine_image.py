from enum import Enum
from datetime import datetime

class OSType(Enum):
    """Видове поддържани операционни системи."""
    LINUX = "Linux"
    WINDOWS = "Windows"
    UNIX = "Unix"
    OTHER = "Other"

class VirtualMachineImage:
    """
    Представлява системен имидж (шаблон) за създаване на виртуални единици.
    Отговаря за версиите и минималните системни изисквания.
    """

    def __init__(self, os_name: str, version: str, os_type: OSType):
        self._os_name = os_name
        self._version = version
        self._os_type = os_type

        # Минимални изисквания, за да може този имидж да зареди
        self._min_ram_required = 1024  # MB
        self._min_disk_required = 10  # GB

        # Метаданни за имиджа
        self._is_read_only = True
        self._checksum = self._generate_checksum()
        self._created_at = datetime.now()

    def _generate_checksum(self) -> str:
        """Симулира генериране на SHA-256 хеш за проверка на интегритета."""
        import hashlib
        raw_data = f"{self._os_name}-{self._version}-{self._os_type.value}"
        return hashlib.sha256(raw_data.encode()).hexdigest()

    @property
    def full_name(self) -> str:
        """Връща пълното име на имиджа (напр. 'Ubuntu 22.04 LTS')."""
        return f"{self._os_name} {self._version}"

    def validate_specs(self, available_ram: int, available_disk: int) -> bool:
        """
        Проверява дали хардуерът е достатъчен за този софтуерен имидж.
        Това е ключова валидация преди стартиране (Provisioning logic).
        """
        if available_ram < self._min_ram_required:
            print(f"Error: {self.full_name} requires at least {self._min_ram_required}MB RAM.")
            return False

        if available_disk < self._min_disk_required:
            print(f"Error: {self.full_name} requires at least {self._min_disk_required}GB Disk.")
            return False

        return True

    def get_boot_command(self) -> str:
        """Връща специфичната команда за зареждане според типа ОС."""
        if self._os_type == OSType.LINUX:
            return "/boot/vmlinuz-linux root=UUID=..."
        elif self._os_type == OSType.WINDOWS:
            return "bootmgr.exe"
        return "generic_boot_loader"

    def update_version(self, new_version: str):
        """Позволява обновяване на версията на шаблона."""
        self.log_action(f"Updating image from {self._version} to {new_version}")
        self._version = new_version
        self._checksum = self._generate_checksum()

    def log_action(self, message: str):
        """Вътрешен метод за запис на промени по имиджа."""
        print(f"[IMAGE_REGISTRY] {datetime.now()}: {message}")