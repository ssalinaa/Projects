from _ast import List
from enum import Enum

class RAIDLevel(Enum):
    RAID0 = 0  # Striping (Скорост, без защита)
    RAID1 = 1  # Mirroring (Защита чрез дублиране)
    RAID5 = 5  # Parity (Баланс между капацитет и защита)
    RAID10 = 10  # Mirror + Stripe

class RAIDController:
    """
    Управлява група от дискове за постигане на надеждност и производителност.
    Имплементира логика за възстановяване на данни при отказ.
    """

    def __init__(self, level: RAIDLevel):
        self.level = level
        self._member_disks: List[str] = []
        self._is_degraded = False

    def assemble_group(self, disk_ids: List[str]):
        """Сглобява RAID група от списък с налични дискове."""
        min_disks = {RAIDLevel.RAID0: 2, RAIDLevel.RAID1: 2, RAIDLevel.RAID5: 3, RAIDLevel.RAID10: 4}

        if len(disk_ids) < min_disks[self.level]:
            raise ValueError(f"{self.level.name} requires at least {min_disks[self.level]} disks.")

        self._member_disks = disk_ids
        print(f"[RAID] {self.level.name} array operational with {len(disk_ids)} disks.")

    def calculate_usable_space(self, disk_size_gb: float) -> float:
        """Изчислява реално достъпното място според RAID нивото."""
        n = len(self._member_disks)
        if self.level == RAIDLevel.RAID0:
            return n * disk_size_gb
        elif self.level == RAIDLevel.RAID1:
            return disk_size_gb
        elif self.level == RAIDLevel.RAID5:
            return (n - 1) * disk_size_gb
        elif self.level == RAIDLevel.RAID10:
            return (n / 2) * disk_size_gb
        return 0.0

    def handle_disk_failure(self, failed_disk_id: str):
        """Симулира реакция при повреда на компонент."""
        if failed_disk_id in self._member_disks:
            if self.level == RAIDLevel.RAID0:
                print("[RAID] CRITICAL: RAID0 failure. ALL DATA LOST.")
            else:
                self._is_degraded = True
                print(f"[RAID] WARNING: Disk {failed_disk_id} failed. Array in DEGRADED mode.")