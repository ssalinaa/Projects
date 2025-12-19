class QuotaManager:
    """
    Управлява лимитите на ресурсите за отделните потребители (Tenants).
    Гарантира справедливо разпределение (Fair Share).
    """

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._limits = {
            "max_vms": 10,
            "max_cpu_cores": 40,
            "max_ram_gb": 128
        }
        self._current_usage = {"vms": 0, "cpu": 0, "ram": 0}

    def can_provision(self, cpu_requested: int, ram_requested: float) -> bool:
        """Проверява дали новата заявка влиза в лимитите."""
        if (self._current_usage["vms"] + 1 > self._limits["max_vms"] or
            self._current_usage["cpu"] + cpu_requested > self._limits["max_cpu_cores"] or
            self._current_usage["ram"] + ram_requested > self._limits["max_ram_gb"]):
            print(f"[QUOTA] Request DENIED for {self.tenant_id}. Limits exceeded.")
            return False
        return True

    def update_usage(self, vms_delta: int, cpu_delta: int, ram_delta: float):
        self._current_usage["vms"] += vms_delta
        self._current_usage["cpu"] += cpu_delta
        self._current_usage["ram"] += ram_delta