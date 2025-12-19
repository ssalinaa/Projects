import time
from enum import Enum

class ScalingPolicy(Enum):
    CONSERVATIVE = "Conservative"  # Изчаква по-дълго преди промяна
    AGGRESSIVE = "Aggressive"  # Мащабира веднага при пик
    COST_OPTIMIZED = "Cost"  # Фокус върху изключване на излишни ресурси

class AutoScaler:
    """
    Автономен агент, който регулира броя на виртуалните единици.
    Свързва MetricsCollector с InfrastructureAsCode.
    """

    def __init__(self, metrics: 'MetricsCollector', iac_engine: 'InfrastructureAsCode'):
        self._metrics = metrics
        self._iac = iac_engine
        self._policy = ScalingPolicy.CONSERVATIVE

        # Прагове за реакция
        self._upper_threshold = 80.0  # 80% CPU -> Scale Up
        self._lower_threshold = 20.0  # 20% CPU -> Scale Down
        self._cool_down_period = 60  # Секунди между две мащабирания
        self._last_action_time = 0

    def evaluate_and_scale(self, stack_config_json: str):
        """
        Анализира състоянието на целия стек и взема решение за промяна.
        Това е затворен цикъл на управление (Feedback Loop).
        """

        current_time = time.time()
        if current_time - self._last_action_time < self._cool_down_period:
            return  # Изчакваме "cool-down" периода

        # Вземаме средното натоварване на всички машини в стека
        resources = self._iac._deployed_stack
        if not resources:
            return

        total_load = sum(self._metrics.get_average_load(uuid) for uuid in resources)
        avg_system_load = total_load / len(resources)

        print(f"[AUTOSCALER] System Load: {avg_system_load:.1f}% | Policy: {self._policy.value}")

        if avg_system_load > self._upper_threshold:
            self._scale_up(stack_config_json)
            self._last_action_time = current_time
        elif avg_system_load < self._lower_threshold and len(resources) > 1:
            self._scale_down()
            self._last_action_time = current_time

    def _scale_up(self, config_json: str):
        """Добавя нови копия на ресурсите (Horizontal Scaling)."""
        print("[AUTOSCALER] High load detected! Provisioning additional resource...")
        # Симулираме добавяне на един нов ресурс към стека през IaC
        self._iac.apply_template(config_json)

    def _scale_down(self):
        """Премахва излишните ресурси за пестене на пари."""
        print("[AUTOSCALER] Low load detected. Decommissioning idle resource...")
        if self._iac._deployed_stack:
            uuid_to_remove = self._iac._deployed_stack.pop()
            self._iac._provider.decommission_unit(uuid_to_remove)

    def set_policy(self, new_policy: ScalingPolicy):
        """Промяна на поведението на автоскалирането."""
        self._policy = new_policy
        if new_policy == ScalingPolicy.AGGRESSIVE:
            self._upper_threshold = 60.0
            self._cool_down_period = 10