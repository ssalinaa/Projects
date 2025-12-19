class StoragePolicyEnforcer:
    """
    Автоматизира жизнения цикъл на данните (ILM).
    Разпределя ресурсите според цената и производителността (Tiering).
    """

    def __init__(self):
        self._tiers = {
            "GOLD": {"media": "NVMe", "latency": "low"},
            "SILVER": {"media": "SSD", "latency": "medium"},
            "BRONZE": {"media": "HDD", "latency": "high"}
        }

    def assign_policy(self, volume_id: str, priority: str):
        """Прилага политика за съхранение към виртуален диск."""
        tier = self._tiers.get(priority, self._tiers["BRONZE"])
        print(f"[POLICY] Volume {volume_id} moved to {priority} tier ({tier['media']})")

    def rebalance_storage(self, iops_data: dict):
        """Анализира натоварването и предлага миграция към по-бърз слой."""
        for vol_id, iops in iops_data.items():
            if iops > 5000:
                self.assign_policy(vol_id, "GOLD")
            elif iops < 100:
                self.assign_policy(vol_id, "BRONZE")