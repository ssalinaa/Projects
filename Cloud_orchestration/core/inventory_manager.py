from typing import Dict, List, Optional

class InventoryManager:
    """
    Управлява инвентара от всички виртуални ресурси в облачната среда.
    Осигурява методи за търсене, филтриране и мониторинг на ресурсите.
    """

    def __init__(self):
        # Речник за бързо търсене по UUID (O(1) сложност)
        self._resources: Dict[str, 'AbstractVirtualUnit'] = {}
        # Списък за хронологичен ред
        self._audit_log: List[str] = []
        self._max_capacity = 1000  # Лимит на инвентара за този мениджър

    def register_unit(self, unit: 'AbstractVirtualUnit'):
        """Добавя нова виртуална единица към системата."""
        if len(self._resources) >= self._max_capacity:
            raise OverflowError("The inventory is full. Cannot be added more resources.")

        if unit.unique_id in self._resources:
            return  # Вече е регистриран

        self._resources[unit.unique_id] = unit
        self._audit_log.append(f"REGISTER: Unit {unit.name} ({unit.unique_id}) added to inventory.")

    def unregister_unit(self, uuid: str):
        """Премахва единица от инвентара (напр. след терминиране)."""
        if uuid in self._resources:
            unit = self._resources.pop(uuid)
            self._audit_log.append(f"UNREGISTER: Unit {unit.name} removed.")
        else:
            print(f"Warning: Unit with UUID {uuid} not found.")

    def find_by_name(self, name: str) -> List['AbstractVirtualUnit']:
        """Търси ресурси по име (може да има дубликати в имената)."""
        return [u for u in self._resources.values() if u.name == name]

    def get_unit_by_id(self, uuid: str) -> Optional['AbstractVirtualUnit']:
        """Връща конкретна единица по нейния уникален идентификатор."""
        return self._resources.get(uuid)

    def get_total_resource_usage(self) -> dict:
        """
        Агрегира консумацията на всички ресурси в инвентара.
        """
        total_cpu = 0
        total_ram = 0

        for unit in self._resources.values():
            total_cpu += unit.specs._cpu_cores
            total_ram += unit.specs._ram_mb

        return {
            "active_units": len(self._resources),
            "allocated_cpu": total_cpu,
            "allocated_ram_mb": total_ram,
            "audit_entries": len(self._audit_log)
        }

    def generate_inventory_report(self) -> str:
        """Генерира детайлен текстов отчет за състоянието на целия облак."""
        report = [f"--- CLOUD INVENTORY REPORT ---"]
        for uuid, unit in self._resources.items():
            report.append(f"ID: {uuid} | Name: {unit.name} | State: {unit.current_state.value}")
        return "\n".join(report)