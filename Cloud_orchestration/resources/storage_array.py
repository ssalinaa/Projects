from datetime import time
from typing import Dict

class StorageArray:
    """
    Абстракция над физическите дискови масиви.
    Поддържа концепцията за 'Thin Provisioning' (разходване на място само при нужда).
    """

    def __init__(self, name: str, total_capacity_gb: float):
        self.name = name
        self.total_capacity = total_capacity_gb
        self.allocated_capacity = 0.0
        self._logical_volumes: Dict[str, dict] = {}

    def create_volume(self, volume_id: str, size_gb: float, thin: bool = True):
        """Създава виртуален диск за VM или Контейнер."""
        if self.allocated_capacity + size_gb > self.total_capacity:
            raise MemoryError(f"Storage Array {self.name} is out of space!")

        self._logical_volumes[volume_id] = {
            "size": size_gb,
            "is_thin": thin,
            "actual_usage": 0.0 if thin else size_gb,
            "created_at": time.time()
        }
        self.allocated_capacity += size_gb
        print(f"[STORAGE] Volume {volume_id} created ({size_gb}GB, Thin: {thin})")

    def delete_volume(self, volume_id: str):
        if volume_id in self._logical_volumes:
            self.allocated_capacity -= self._logical_volumes[volume_id]["size"]
            del self._logical_volumes[volume_id]
            print(f"[STORAGE] Volume {volume_id} destroyed.")

    def get_utilization(self) -> float:
        return (self.allocated_capacity / self.total_capacity) * 100