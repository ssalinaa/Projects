import random
from typing import Dict, List

class StepFunctionOrchestrator:
    """
    Оркестратор на работни процеси (Workflows).
    Управлява състоянието и преходите между отделните Serverless стъпки.
    """
    def __init__(self):
        self._workflows: Dict[str, List[str]] = {}
        self._active_executions: Dict[str, str] = {} # exec_id -> current_step

    def define_workflow(self, name: str, steps: List[str]):
        self._workflows[name] = steps
        print(f"[WORKFLOW] Defined sequence: {' -> '.join(steps)}")

    def execute(self, workflow_name: str):
        """Стартира изпълнението на веригата."""
        if workflow_name in self._workflows:
            exec_id = f"exec-{random.randint(1000, 9999)}"
            first_step = self._workflows[workflow_name][0]
            self._active_executions[exec_id] = first_step
            print(f"[ORCHESTRATOR] Started {workflow_name}. Current step: {first_step}")
            return exec_id

    def next_step(self, exec_id: str):
        """Преминава към следващата логическа стъпка."""
        print(f"[ORCHESTRATOR] Execution {exec_id} advancing...")