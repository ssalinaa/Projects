import random
import itertools

from enum import Enum
from typing import List
from core.life_cycle_manager import ResourceState

class BalancerAlgorithm(Enum):
    ROUND_ROBIN = "Round Robin"
    LEAST_CONNECTIONS = "Least Connections"
    IP_HASH = "IP Hash"

class LoadBalancer:
    """
    Разпределя мрежовия трафик между група от виртуални единици.
    Осигурява отказноустойчивост и оптимизира използването на ресурсите.
    """

    def __init__(self, name: str, algorithm: BalancerAlgorithm = BalancerAlgorithm.ROUND_ROBIN):
        self._name = name
        self._algorithm = algorithm
        self._backend_pool: List['AbstractVirtualUnit'] = []
        # Използваме итератор за Round Robin логиката
        self._pool_cycle = None
        self._vip = f"10.0.0.{random.randint(100, 254)}"  # Virtual IP

    def add_to_pool(self, unit: 'AbstractVirtualUnit'):
        """Добавя нова машина към пула на балансиращия сървър."""
        if unit not in self._backend_pool:
            self._backend_pool.append(unit)
            self._refresh_cycle()
            print(f"[LB: {self._name}] Unit {unit.name} added to backend pool.")

    def remove_from_pool(self, unit_id: str):
        """Премахва машина от пула (например при планирана профилактика)."""
        self._backend_pool = [u for u in self._backend_pool if u.unique_id != unit_id]
        self._refresh_cycle()

    def _refresh_cycle(self):
        """Обновява итератора при промяна в пула."""
        if self._backend_pool:
            self._pool_cycle = itertools.cycle(self._backend_pool)
        else:
            self._pool_cycle = None

    def get_next_target(self) -> 'AbstractVirtualUnit':
        """
        Избира следващата здрава машина, към която да насочи трафика.
        Демонстрира автоматично прескачане на повредени ресурси.
        """
        if not self._pool_cycle:
            raise RuntimeError("No backends available in the pool.")

        # Опитваме се да намерим здрава машина (Healthy check)
        attempts = len(self._backend_pool)
        for _ in range(attempts):
            target = next(self._pool_cycle)
            if target.current_state == ResourceState.RUNNING:
                return target

        raise RuntimeError("All backend units are currently offline or in error state.")

    def route_request(self, client_ip: str):
        """Симулира насочване на потребителска заявка."""
        try:
            target = self.get_next_target()
            print(f"[LB: {self._name}] Routing request from {client_ip} -> {target.name} ({target.unique_id})")
        except Exception as e:
            print(f"[LB: {self._name}] CRITICAL: Request failed. {str(e)}")

    def get_status(self) -> dict:
        """Връща информация за състоянието на балансьора."""
        return {
            "lb_name": self._name,
            "vip": self._vip,
            "algorithm": self._algorithm.value,
            "active_backends": len([u for u in self._backend_pool if u.current_state == ResourceState.RUNNING]),
            "total_backends": len(self._backend_pool)
        }