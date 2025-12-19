from typing import List, Dict
from scheduler.function_as_a_service import FunctionAsAService

class EventTriggerManager:
    """
    Свързва външни събития с конкретни Serverless функции.
    Имплементира модела 'Event-Driven Architecture'.
    """
    def __init__(self, faas_provider: FunctionAsAService):
        self.faas = faas_provider
        # event_type -> list of (function_name)
        self._bindings: Dict[str, List[str]] = {}

    def bind_event(self, event_type: str, func_name: str):
        if event_type not in self._bindings:
            self._bindings[event_type] = []
        self._bindings[event_type].append(func_name)
        print(f"[TRIGGER] Linked {event_type} to function {func_name}.")

    def emit_event(self, event_type: str, event_data: dict):
        """Симулира настъпване на събитие (напр. качване на снимка)."""
        print(f"[EVENT] Detected event: {event_type}")
        if event_type in self._bindings:
            for func in self._bindings[event_type]:
                self.faas.invoke(func, event_data)