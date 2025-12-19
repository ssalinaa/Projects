class ComplianceDataSovereignty:
    """
    Гарантира, че данните остават в рамките на определени географски или политически зони.
    Следи за съответствие с GDPR, CCPA и други регулации.
    """
    def __init__(self):
        self._geo_fences = {"EU_USERS": ["GERMANY", "IRELAND", "FRANCE"]}

    def check_migration_allowed(self, user_origin: str, target_location: str) -> bool:
        if user_origin == "EU_USERS" and target_location not in self._geo_fences["EU_USERS"]:
            print(f"[BLOCK] Compliance violation: EU data cannot move to {target_location}")
            return False
        return True