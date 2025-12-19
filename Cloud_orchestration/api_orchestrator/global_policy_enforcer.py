class GlobalPolicyEnforcer:
    """
    Централизиран контрол на правилата в мулти-облачна среда.
    """
    def enforce_universal_rule(self, rule_name: str, scope: str):
        print(f"[POLICY-ENFORCER] Applying '{rule_name}' to all regions in {scope}.")