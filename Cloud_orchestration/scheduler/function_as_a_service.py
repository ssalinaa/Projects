import time
from typing import Dict

class FunctionAsAService:
    """
    Симулира Serverless платформа (като AWS Lambda).
    Управлява жизнения цикъл на краткотрайни (ephemeral) функции.
    """

    def __init__(self, name: str):
        self.name = name
        self._functions: Dict[str, callable] = {}
        self._execution_stats: Dict[str, int] = {}  # func_name -> count

    def deploy_function(self, func_name: str, code_logic: callable):
        """Качва код в облака, готов за изпълнение."""
        self._functions[func_name] = code_logic
        self._execution_stats[func_name] = 0
        print(f"[FaaS] Function '{func_name}' deployed to {self.name}.")

    def invoke(self, func_name: str, *args, **kwargs):
        """Извиква функцията при събитие."""
        if func_name not in self._functions:
            raise NameError(f"Function {func_name} not found.")

        start_time = time.time()
        print(f"[FaaS] Warming up environment for {func_name}...")

        result = self._functions[func_name](*args, **kwargs)

        duration = time.time() - start_time
        self._execution_stats[func_name] += 1
        print(f"[FaaS] {func_name} executed in {duration:.4f}s. Result: {result}")
        return result