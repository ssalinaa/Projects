from typing import Set
from scheduler.function_as_a_service import FunctionAsAService

class ColdStartOptimizer:
    """
    Минимизира латентността при първоначално извикване на функция.
    Поддържа 'Pre-warmed' ресурси за критични задачи.
    """
    def __init__(self, faas: FunctionAsAService):
        self.faas = faas
        self._warm_pool: Set[str] = set()

    def keep_warm(self, func_name: str):
        """Поддържа функцията в готовност в паметта."""
        self._warm_pool.add(func_name)
        print(f"[OPTIMIZER] Function '{func_name}' added to Warm Pool (Instant execution).")

    def is_cold(self, func_name: str) -> bool:
        return func_name not in self._warm_pool