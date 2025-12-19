class SelfHealingCluster:
    """
    Имплементира концепцията за 'Reconciliation Loop'.
    Постоянно сравнява реалното състояние с дефинираното и коригира разликите.
    """
    def check_and_repair(self, desired_config: dict, actual_state: dict):
        for resource, status in actual_state.items():
            if status == "CRASHED" or status != desired_config[resource]:
                print(f"[SELF-HEALING] Deviation detected in {resource}. Re-provisioning...")
