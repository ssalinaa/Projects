from typing import Dict, List, Set

class VLANManager:
    """
    Управлява виртуалните локални мрежи (VLANs).
    Прилага 802.1Q тагване за сегментация на трафика.
    """

    def __init__(self):
        # Структура: {vlan_id: set(interface_ids)}
        self._vlan_map: Dict[int, Set[str]] = {}
        self._reserved_vlans = {1, 4094}  # Стандартни резервирани VLAN-и

    def create_vlan(self, vlan_id: int, description: str):
        """Създава нов сегмент (Broadcast Domain)."""
        if not (1 <= vlan_id <= 4094):
            raise ValueError("VLAN ID must be between 1 and 4094.")

        if vlan_id not in self._vlan_map:
            self._vlan_map[vlan_id] = set()
            print(f"[VLAN] Created VLAN {vlan_id}: {description}")

    def assign_interface_to_vlan(self, vlan_id: int, interface_id: str):
        """
        Причислява vNIC към конкретен VLAN (Access Port).
        Това гарантира, че интерфейсът може да говори само в своя сегмент.
        """
        if vlan_id not in self._vlan_map:
            self.create_vlan(vlan_id, "Auto-generated segment")

        self._vlan_map[vlan_id].add(interface_id)
        print(f"[VLAN {vlan_id}] Interface {interface_id} tagged and assigned.")

    def is_communication_allowed(self, vlan_src: int, vlan_dest: int) -> bool:
        """
        Проверява дали два интерфейса могат да си говорят на L2.
        Без рутер (L3), комуникацията между различни VLAN-и е невъзможна.
        """
        return vlan_src == vlan_dest

    def get_vlan_inventory(self):
        """Връща справка за разпределението на мрежовите сегменти."""
        return {vid: list(interfaces) for vid, interfaces in self._vlan_map.items()}