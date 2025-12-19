from typing import List, Optional
from core.inventory_manager import InventoryManager

class CloudProvider:
    """
    Представлява облачен доставчик или локален център за данни.
    Управлява ресурсите на високо ниво и следи за глобалните лимити.
    """

    def __init__(self, provider_name: str, region: str):
        self._provider_name = provider_name
        self._region = region
        self._inventory = InventoryManager()

        # Глобални квоти за този регион
        self._quotas = {
            "max_vcpus": 128,
            "max_ram_gb": 512,
            "max_storage_tb": 10
        }
        self._current_usage = {"cpu": 0, "ram": 0, "storage": 0}

    def can_provision(self, specs: 'ResourceSpecification') -> bool:
        """Проверява дали доставчикът има свободен капацитет (Admission Control)."""
        within_cpu = (self._current_usage["cpu"] + specs._cpu_cores) <= self._quotas["max_vcpus"]
        within_ram = (self._current_usage["ram"] + specs.total_ram_gb) <= self._quotas["max_ram_gb"]

        if not (within_cpu and within_ram):
            print(f"[!] Quota exceeded for region {self._region}. Provisioning denied.")
            return False
        return True

    def deploy_unit(self, unit: 'AbstractVirtualUnit'):
        """Регистрира и 'разполага' единицата в облака."""
        if self.can_provision(unit.specs):
            self._inventory.register_unit(unit)
            self._current_usage["cpu"] += unit.specs._cpu_cores
            self._current_usage["ram"] += unit.specs.total_ram_gb
            unit.assign_to_host(f"host-{self._region}-node-{len(self._inventory._resources)}")
            print(f"[*] {unit.name} deployed successfully in {self._provider_name} ({self._region}).")
        else:
            raise RuntimeError("Insufficient cloud resources.")

    def get_provider_status(self) -> str:
        """Генерира справка за натоварването на облачния регион."""
        stats = self._inventory.get_total_resource_usage()
        cpu_p = (self._current_usage["cpu"] / self._quotas["max_vcpus"]) * 100
        ram_p = (self._current_usage["ram"] / self._quotas["max_ram_gb"]) * 100

        return (f"Provider: {self._provider_name} | Region: {self._region}\n"
                f"Active Units: {stats['active_units']}\n"
                f"Resource Load: CPU {cpu_p:.1f}%, RAM {ram_p:.1f}%")

    def decommission_unit(self, uuid: str):
        """Премахва единица и освобождава квотите."""
        unit = self._inventory.get_unit_by_id(uuid)
        if unit:
            self._current_usage["cpu"] -= unit.specs._cpu_cores
            self._current_usage["ram"] -= unit.specs.total_ram_gb
            self._inventory.unregister_unit(uuid)
            print(f"[-] Unit {uuid} decommissioned. Resources released.")