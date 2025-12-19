class AutoScaler:
    """
    Автоматично мащабира ресурсите нагоре или надолу (Scale-out/Scale-in).
    Оптимизира разходите, като изключва излишните мощности през нощта.
    """
    def __init__(self, min_instances: int, max_instances: int):
        self.min_i = min_instances
        self.max_i = max_instances
        self.current_instances = min_instances
        self._cooldown_period = 300 # 5 минути почивка между мащабиранията

    def evaluate_metrics(self, avg_cpu_load: float):
        """Взема решение за мащабиране на база средно натоварване."""
        if avg_cpu_load > 80.0 and self.current_instances < self.max_i:
            self.current_instances += 1
            print(f"[AUTOSCALE] Load high ({avg_cpu_load}%). Scaling UP to {self.current_instances} units.")
        elif avg_cpu_load < 20.0 and self.current_instances > self.min_i:
            self.current_instances -= 1
            print(f"[AUTOSCALE] Load low ({avg_cpu_load}%). Scaling DOWN to {self.current_instances} units.")

    def get_scaling_status(self):
        return {"active_units": self.current_instances, "limit": self.max_i}