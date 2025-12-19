class PolicyEngine:
    """
    Автоматично прилага правила (Guardrails) върху заявките за ресурси.
    Предотвратява несъобразено използване на инфраструктурата.
  """

    def __init__(self):
        self._global_policies = []

    def add_policy(self, name: str, condition_fn):
        self._global_policies.append({"name": name, "check": condition_fn})

    def validate_request(self, request_context: dict) -> bool:
        """Проверява заявката срещу всички активни политики."""
        for policy in self._global_policies:
            if not policy["check"](request_context):
                print(f"[POLICY DENIED] Request failed policy: {policy['name']}")
                return False
        return True

# Пример за политика: Максимум 4 CPU за стандартни потребители
def max_cpu_policy(ctx):
    return ctx.get("requested_cpu", 0) <= 4 or ctx.get("role") == "ADMIN"