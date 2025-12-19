from typing import List

class SpotInstanceMarket:
    """
    Управлява пазара за излишен капацитет.
    Цените се променят динамично според търсенето и предлагането.
    """

    def __init__(self, base_price: float):
        self._current_spot_price = base_price * 0.2 # Започваме от 20% от цената
        self._active_spot_vms: List[str] = []

    def update_market_price(self, supply_ratio: float):
        """Променя цената. Ако supply_ratio е ниско (малко ресурси), цената скача."""
        # supply_ratio: 0.0 (няма свободни) до 1.0 (всичко е свободно)
        self._current_spot_price += (1.0 - supply_ratio) * 0.1
        print(f"[MARKET] New Spot Price: ${self._current_spot_price:.4f}")

    def request_spot_instance(self, max_bid: float, vm_id: str) -> bool:
        """Потребителят казва колко е готов да плати. Ако цената е по-ниска, печели."""
        if max_bid >= self._current_spot_price:
            self._active_spot_vms.append(vm_id)
            print(f"[SPOT] VM {vm_id} started at ${self._current_spot_price:.4f}")
            return True
        return False

    def evict_expensive_vms(self):
        """Прекратява машини, чийто 'Bid' е станал по-нисък от пазарната цена."""
        # Симулация на изхвърляне от пазара при скок на цените
        print("[SPOT] Market pressure detected. Terminating low-bid instances...")