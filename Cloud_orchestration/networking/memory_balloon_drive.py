class MemoryBalloonDriver:
    """
    Механизъм за гъвкаво управление на паметта (Memory Reclaim).
    Позволява на хипервайзора да 'краде' памет от по-малко активни машини.
    """

    def __init__(self, unit_id: str):
        self.unit_id = unit_id
        self._current_balloon_size_mb = 0

    def inflate(self, amount_mb: int):
        """'Надува' балона, принуждавайки Guest ОС да освободи кеш памет."""
        self._current_balloon_size_mb += amount_mb
        print(f"[BALLOON: {self.unit_id}] Inflated by {amount_mb}MB. Total reclaimed: {self._current_balloon_size_mb}MB")

    def deflate(self, amount_mb: int):
        """'Свива' балона, връщайки памет на виртуалната машина."""
        self._current_balloon_size_mb = max(0, self._current_balloon_size_mb - amount_mb)
        print(f"[BALLOON: {self.unit_id}] Deflated. VM can now use more memory.")

    def get_driver_status(self):
        return {"reclaimed_mb": self._current_balloon_size_mb}